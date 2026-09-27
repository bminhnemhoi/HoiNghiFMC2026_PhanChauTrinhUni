# Máy chủ Ollama riêng của đề tài: mô hình lưu ở D:\ollama\models, cổng 11435.
# Không đổi Ollama mặc định của máy (cổng 11434, mô hình ở ổ C) — các dự án khác không bị ảnh hưởng.
# Người dùng đồng ý 27/9/2026 ("đồng ý chuyển Ollama sang D"); docs/DECISIONS.md.
# Chạy lại sau mỗi lần khởi động máy:  powershell -ExecutionPolicy Bypass -File scripts\ollama_d.ps1
$exe = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
$env:OLLAMA_MODELS = "D:\ollama\models"
$env:OLLAMA_HOST = "127.0.0.1:11435"
$env:OLLAMA_KEEP_ALIVE = "30m"
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:11435/api/version" -TimeoutSec 3 | Out-Null
    Write-Output "Project Ollama server already running (port 11435)."
} catch {
    Start-Process -FilePath $exe -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 5
    Write-Output "Started project Ollama server (port 11435, models in D:\ollama\models)."
}
