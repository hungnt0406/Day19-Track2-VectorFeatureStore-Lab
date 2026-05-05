import os
import sys
from pathlib import Path

# Add the repo root to sys.path so we can run from anywhere
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bonus.agent import HybridMemoryAgent

def main():
    print("Initializing Hybrid Memory Agent...")
    # Initialize agent pointing to the feast_repo
    feast_repo_path = str(ROOT / "app" / "feast_repo")
    agent = HybridMemoryAgent(feast_repo_path=feast_repo_path)
    
    # Seed some episodic memory
    print("Seeding episodic memory...")
    agent.remember("I recently read an article about Kubernetes scaling infrastructure.")
    agent.remember("Cloud security is becoming my main focus this quarter.")
    agent.remember("I am trying to learn more about semantic search and vector databases.")
    
    # 5 Demo Queries
    print("")
    print("="*50)
    print("DEMO QUERIES")
    print("="*50)
    
    queries = [
        "What have I read about Kubernetes?",                               # 1. Simple lookup
        "Recommend what to read next",                                      # 2. Profile-needed
        "What am I focused on lately?",                                     # 3. Fresh-activity
        "Documents about scaling infrastructure?",                          # 4. Paraphrase
        "Give me a cloud security summary"                                  # 5. Mixed
    ]
    
    for i, q in enumerate(queries, 1):
        print("")
        print(f">>> QUERY {i}: {q}")
        context = agent.recall(query=q)
        print(context)

if __name__ == "__main__":
    main()
