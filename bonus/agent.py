import os
import uuid
from datetime import datetime, timezone
from typing import List

from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from feast import FeatureStore

class HybridMemoryAgent:
    def __init__(self, qdrant_path: str = ":memory:", feast_repo_path: str = "app/feast_repo"):
        self.embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        
        # Initialize Vector Store (Episodic Memory)
        self.qdrant = QdrantClient(qdrant_path)
        self.collection = "user_memory"
        
        # Check if collection exists, if not create it
        existing = {c.name for c in self.qdrant.get_collections().collections}
        if self.collection not in existing:
            self.qdrant.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            
        # Initialize Feature Store (Stable Profile)
        self.feast_store = FeatureStore(repo_path=feast_repo_path)
        
    def remember(self, text: str, user_id: str = "u_001") -> None:
        """Add a new piece of episodic memory for this user."""
        vector = next(self.embedder.embed([text])).tolist()
        point_id = str(uuid.uuid4())
        
        self.qdrant.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "user_id": user_id,
                        "text": text,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
            ]
        )

    def recall(self, query: str, user_id: str = "u_001", top_k: int = 3) -> str:
        """Retrieve top-K memories + user profile features → return assembled context."""
        
        # 1. Fetch Episodic Memory (Vector Search)
        query_vector = next(self.embedder.embed([query])).tolist()
        
        hits = self.qdrant.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=top_k,
        ).points
        
        # Filter by user_id
        memories = [hit.payload["text"] for hit in hits if hit.payload.get("user_id") == user_id]
        
        # 2. Fetch Stable Profile & Activity (Feature Store)
        try:
            features = self.feast_store.get_online_features(
                features=[
                    "user_profile_features:topic_affinity",
                    "query_velocity_features:queries_last_hour",
                ],
                entity_rows=[{"user_id": user_id}],
            ).to_dict()
            
            topic_affinity = features["topic_affinity"][0] if features.get("topic_affinity") else "unknown"
            queries_last_hour = features["queries_last_hour"][0] if features.get("queries_last_hour") else 0
        except Exception as e:
            # Fallback if Feast is not fully initialized for the user
            topic_affinity = "unknown"
            queries_last_hour = 0
            
        # 3. Assemble Context
        context = (
            f"--- SYSTEM CONTEXT ---\n"
            f"User ID: {user_id}\n"
            f"User's preferred topic: {topic_affinity}\n"
            f"User's activity level: {queries_last_hour} queries in the last hour\n"
            f"\n--- EPISODIC MEMORY (Related to query) ---\n"
        )
        
        if memories:
            for i, mem in enumerate(memories, 1):
                context += f"{i}. {mem}\n"
        else:
            context += "No relevant memories found.\n"
            
        context += f"\n--- USER QUERY ---\n{query}\n"
        
        return context
