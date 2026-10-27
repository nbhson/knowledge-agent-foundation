# MODEL.md — Model Local Đang Dùng

> Danh mục model Ollama trên máy cá nhân (Mac M4 24GB). Cập nhật bằng `ollama list`.

## Model đang cài đặt

| Model | ID | Size | Vai trò |
|-------|----|------|---------|
| `qwen2.5-coder:14b` | f4031aab637d... | 9.0 GB | **Chính** — code chat, refactor, viết hàm phức tạp |
| `deepseek-r1:14b` | c333b7232bdb... | 9.0 GB | Reasoning — phân tích kiến trúc, debug khó |
| `qwen2.5vl:7b` | 5ced39dfa4ba... | 6.0 GB | Vision — đọc screenshot UI, phân tích ảnh |
| `gemma3:12b` | f4031aab637d... | 8.1 GB | Chat tổng quát, viết docs |
| `nomic-embed-text:latest` | 0a109f422b47... | 274 MB | **Embedding** — RAG, semantic search (768 dims) |
| `gpt-oss:20b-cloud` | 875e8e3a629a... | — (cloud) | Fallback cloud khi task quá nặng cho local |

## Gợi ý sử dụng

- **Coding chính:** `qwen2.5-coder:14b` — cân bằng tốc độ/chất lượng tốt nhất cho 24GB RAM
- **RAG pipeline:** dùng `nomic-embed-text` làm embedding — rẻ, nhanh, chuẩn
- **Nhờ vision:** `qwen2.5vl:7b` khi cần agent "nhìn" ảnh UI

Chi tiết setup: xem [local-ai-setup-for-mac.md](./local-ai-setup-for-mac.md) và [local-ai-setup-for-window.md](./local-ai-setup-for-window.md).
