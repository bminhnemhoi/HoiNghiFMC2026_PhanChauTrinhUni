---
name: kaggle-vllm-runner
description: Chạy mô hình mở bằng vLLM trên Kaggle 2×T4 qua Kaggle CLI (render → push → status → output), chia shard mỗi GPU một tiến trình, chạy tiếp khi đứt, đo tốc độ, lượng tử hóa (T0.4, T1.4, T5.0–T5.4).
---
# Chạy vLLM trên Kaggle

## Chuẩn bị (một lần)
- Người dùng (HG0.3): tài khoản Kaggle đã xác minh số điện thoại (bật GPU + Internet), API token (`KAGGLE_API_TOKEN` hoặc `~/.kaggle/kaggle.json`), `KAGGLE_USERNAME` trong `.env`; đồng ý điều khoản Llama 3.1 và Vistral trên Hugging Face; tạo Kaggle Secret `HF_TOKEN`. CLI `kaggle` nằm trong `.venv/bin/`.
- Secret chỉ gắn được qua giao diện và theo từng notebook, nên **chỉ một kernel cố định cần token**: `vnsoc-weights` (T4.9 đẩy lần đầu → HG5.0 người dùng gắn secret → T5.0 tải mô hình gated, lượng tử nếu cần, lưu làm output). Mọi job chạy sau gắn output đó qua `kernel_sources` (đường dẫn `/kaggle/input/vnsoc-weights/...`) nên không cần secret. Thí điểm (T1.4) chỉ dùng mô hình không gated: Qwen3-8B-AWQ trên cả 2 GPU.
- Dataset riêng tư `<user>/vnsoc-requests`: `kaggle datasets init -p data/kaggle_requests` rồi `kaggle datasets create -p data/kaggle_requests` (mặc định riêng tư — không bao giờ thêm cờ công khai `-u/--public`), các lần sau `kaggle datasets version -p data/kaggle_requests -m "<ghi chú>"`.

## Một job
1. Viết yêu cầu JSONL: `{"request_id", "model_key", "messages":[{"role":"user","content":...}], "sampling":{"temperature":0,"max_tokens":128}}` (lấy mẫu tín hiệu: `n:5, temperature:0.7, top_p:0.95`). `request_id = <question_id>|<condition>|<model_key>|<sample>`.
2. Spec job (JSON): `{"shards":[{"model_key":"qwen3_8b","model":"<hf_id hoặc /kaggle/input/...>","quantization":"awq","max_model_len":8192,"chat_template_kwargs":{"enable_thinking":false},"requests":"/kaggle/input/vnsoc-requests/<file>.jsonl","out":"/kaggle/working/<job>_qwen.jsonl"}, {… GPU 1 …}], "pip":["vllm==<phiên bản đã chạy được ở T0.4>"]}`.
3. `$PY -m vnsoc.run.kaggle_jobs render --job-id <id> --spec <spec.json>` → `kaggle/jobs/<id>/run.py` + `kernel-metadata.json` (riêng tư, GPU, Internet, `machine_shape: NvidiaTeslaT4`).
4. `$PY -m vnsoc.run.kaggle_jobs push --job-id <id>`; theo dõi `status` (mỗi 10–15 phút, không dồn dập); xong → `fetch` về `data/runs/kaggle/<id>/`.
5. Chuyển sang `RunRecord` (`src/vnsoc/run/collect.py`, T5.x viết): khớp `request_id`, gắn `prompt_hash`, `model_version` (commit HF), `backend: vllm`; kiểm schema.
6. Đứt giữa chừng (12 giờ/phiên): job mới với `resume_from` trỏ tới đầu ra cũ (gắn kernel cũ vào `kernel_sources`).

## Lưu ý kỹ thuật
- T4 = compute 7.5: không bf16 → `dtype: half` (gemma2/gemma3/glm4 bị vLLM từ chối ở fp16 → `float32` hoặc không chạy trên T4); AWQ/GPTQ chạy được; FlashAttention cần SM80+ nên vLLM tự dùng backend khác. Bản vLLM mới có thể kéo torch dựng cho CUDA mới hơn driver của Kaggle: T0.4 ghi driver (`nvidia-smi`), thử `vllm` kèm `--extra-index-url https://download.pytorch.org/whl/cu129` hoặc phiên bản cũ hơn cho tới khi chạy được, ghi phiên bản vào `configs/models.yaml`; vẫn hỏng → DR10 (HF transformers, batch nhỏ).
- Lượng tử: dùng checkpoint AWQ/GPTQ có sẵn (kiểm nguồn, giấy phép) hoặc tự tạo bằng llm-compressor (AutoAWQ đã ngừng phát triển). bitsandbytes 4-bit tại chỗ: từ vLLM 0.28 cần thêm gói `vllm-bnb-plugin` (và `bitsandbytes>=0.48.1`).
- 8B fp16 (~16 GB) không vừa một T4: dùng bản 4-bit (AWQ/GPTQ có sẵn trên HF, kiểm nguồn) hoặc tự lượng tử (T5.0), hoặc `tensor_parallel_size: 2` với `gpus: "0,1"` (ngoại lệ một tiến trình cho cả 2 GPU).
- Qwen3: luôn `chat_template_kwargs={"enable_thinking": false}`. Sailor2: `max_model_len` 4096, không chạy A4. A4 (Qwen3, Llama): shard riêng với `max_model_len: 32768` (KV cache khoảng 4–5 GB cho 32k token với bản 4-bit — vừa một T4, batch nhỏ).
- A4: sắp yêu cầu theo văn bản, đặt văn bản trước câu hỏi để tận dụng prefix caching.
- Đo tốc độ thật ở T0.4/T5.1 (token/giây vào/ra từ file `.stats.json`) và cập nhật ước tính giờ GPU; tổng dự án 50–80 giờ (tuần 7–9 theo lịch file 02). Ghi giờ mỗi job vào docs/LOG.md.
- T5.4 (lượng tử hóa): một mô hình chạy fp16 (2 GPU) trên 500 câu so với bản 4-bit; báo cáo khác biệt nhãn.
