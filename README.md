# Lab 05 - C401 A2: VinFast Service Copilot

Agent hỗ trợ chẩn đoán xe điện VinFast theo pipeline:

`Symptom -> Candidate DTC -> Diagnostic reasoning -> Next actions`

Hệ thống dùng LangGraph + LangChain tools, dữ liệu lịch sử sửa chữa và diagnostic lưu trong SQLite.

## Mục tiêu

- Nhận mô tả triệu chứng từ kỹ thuật viên.
- Trích xuất context xe (`model`, `model_year`, `firmware`, `symptom`).
- Truy vấn dữ liệu lịch sử sửa chữa để sinh candidate DTC.
- Truy vấn diagnostic để gợi ý nguyên nhân và bước kiểm tra/sửa chữa.
- Vẫn đưa candidate khi metadata thiếu/sai (graceful fallback), đồng thời cảnh báo độ chắc chắn.

## Cấu trúc chính

```text
lab05_c401_a2/
├── src/
│   ├── agent.py                    # Main agent (CLI), graph START->agent->END
│   ├── streamlit_app.py            # Giao diện Streamlit
│   ├── system_prompt.txt           # Prompt điều phối output
│   ├── tools_mapping.py            # Khai báo tool list + dispatch map
│   ├── tools/
│   │   ├── validate_input.py
│   │   ├── get_repair_history.py   # Query SQLite repair_history
│   │   ├── get_diagnostic.py       # Query SQLite diagnostic_manual
│   │   ├── compute_confidence.py
│   │   └── retrieve_manual.py
│   ├── ingestion/
│   │   └── load_to_sqlite.py       # Nạp JSON -> SQLite
│   └── data/
│       ├── structure_database.db
│       ├── repair_history.json
│       ├── diagnostic_manual.json
│       └── service_manual.json
├── group/
├── individual/
└── README.md
```

## Luồng xử lý agent hiện tại

1. Nhận context chat (tối đa 6 cặp gần nhất + user hiện tại).
2. Gọi `llm_with_tools`.
3. Nếu model trả `tool_calls` native -> chạy tool theo vòng lặp.
4. Nếu không có native call -> thử parse JSON tool call trong text.
5. Nếu vẫn không có tool call -> chạy deterministic pipeline:
   - LLM structured extraction (JSON schema)
   - regex fallback nếu parse lỗi
   - `validate_input`
   - `get_repair_history` (lọc strict -> nới lỏng)
   - `get_diagnostic`
   - `compute_confidence`
   - `retrieve_manual` (khi đủ metadata và đạt điều kiện)
   - LLM synthesis output theo format chuẩn.

## Cấu hình môi trường

Tạo `src/.env`:

```env
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=qwen2.5-coder:7b

QDRANT_BASE_URL=...
QDRANT_API_KEY=...
```

## Chạy bằng CLI

```bash
cd src
python agent.py
```

## Chạy giao diện Streamlit

```bash
cd src
pip install streamlit
streamlit run streamlit_app.py
```

Mở: `http://localhost:8501`

## Nạp lại dữ liệu vào SQLite (nếu cần)

```bash
cd src
python ingestion/load_to_sqlite.py
```

## Ghi chú

- `dtc` sẽ ưu tiên top candidate nếu có dữ liệu, không phụ thuộc tuyệt đối vào `decision`.
- Khi thiếu metadata, agent vẫn trả candidate tham khảo nhưng có cảnh báo.
- Nếu muốn đẩy repo và gặp divergent branches:
  - `git pull --rebase origin main`
  - resolve conflict (nếu có), rồi `git push origin main`.
