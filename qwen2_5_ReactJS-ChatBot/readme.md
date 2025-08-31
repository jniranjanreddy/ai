```
Windows
Invoke-WebRequest -Uri "http://127.0.0.1:8000/chat" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"message": "Hello, Qwen!"}'


Linux
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"message": "Hello, Qwen!"}'
```