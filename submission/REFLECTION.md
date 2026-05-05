# Reflection — Lab 19

**Tên:** Hung Cucu
**Cohort:** A20
**Path đã chạy:** lite

---

## Câu hỏi (≤ 200 chữ)

> Trên golden set 50 queries, mode nào thắng ở loại query nào (`exact` /
> `paraphrase` / `mixed`), và tại sao? Khi nào bạn **không** dùng hybrid
> (i.e. khi nào pure BM25 hoặc pure vector là lựa chọn đúng)?

- `exact`: BM25 và Hybrid có kết quả tương đương (rất cao). BM25 mạnh do có thể khớp chính xác verbatim từng từ khóa.
- `mixed`: Hybrid chiến thắng tuyệt đối nhờ việc kết hợp được cả tín hiệu từ khóa chính xác (BM25) và ý tưởng ngữ nghĩa (Vector), phù hợp với hành vi tìm kiếm thực tế của user.
- `paraphrase`: Vector và Hybrid chiếm ưu thế do khả năng truy xuất ngữ nghĩa khi không có từ khóa verbatim (mặc dù model `bge-small` tiếng Anh bị giảm điểm trên tập tiếng Việt).

**Khi không dùng hybrid:**
- **Pure BM25:** Khi tìm kiếm mã lỗi (error codes), ID, tên riêng, từ viết tắt mà việc khớp ngữ nghĩa sẽ gây nhiễu, hoặc khi hệ thống bị giới hạn khắt khe về compute/latency.
- **Pure Vector:** Khi các truy vấn hoàn toàn mang tính concept/paraphrase mà việc khớp từ khóa chính xác không có ý nghĩa hoặc gây sai lệch, ví dụ query đa ngôn ngữ (cross-lingual).

---

## Điều ngạc nhiên nhất khi làm lab này

Sự kết hợp giữa Vector Store (episodic memory) và Feature Store (stable profile) tạo ra một pipeline RAG cực kỳ cá nhân hóa và mạnh mẽ. Việc cấu hình TTL khác nhau trong Feast cho thấy rõ sự tinh tế trong việc thiết kế data streaming.

---

## Bonus challenge

- [x] Đã làm bonus (xem `bonus/`)
- [ ] Pair work với: _Không có_
