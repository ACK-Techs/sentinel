---
name: llm-local-ollama-setup
description: "Ollama'yı kurmak, model çekmek, GPU/CPU yapılandırmasını doğrulamak ve REST API endpoint'ini açmak gerektiğinde kullan. Yerel LLM çalıştırmanın en hızlı yolu."
---

## Purpose
Ollama, tek komutla yerel LLM çalıştırmayı sağlar. Docker veya Python ortamı gerektirmeden kurulur; OpenAI-compatible API ile Sentinel'e entegre edilir.

## Kurulum
```bash
# Linux/macOS:
curl -fsSL https://ollama.com/install.sh | sh

# Docker:
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# GPU (NVIDIA):
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 ollama/ollama
```

## Model çekme ve çalıştırma
```bash
ollama pull llama3.2:3b
ollama pull llama3.2:8b
ollama pull mistral:7b
ollama pull nomic-embed-text  # embedding modeli

ollama list          # indirilen modeller
ollama run llama3.2  # interaktif
```

## REST API
```bash
# Doğrulama:
curl http://localhost:11434/api/tags

# Chat tamamlama:
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"Merhaba"}]}'

# Streaming olmadan:
curl -X POST http://localhost:11434/api/generate \
  -d '{"model":"llama3.2","prompt":"PromQL nedir?","stream":false}'
```

## Servis yönetimi
```bash
ollama serve &    # arka planda başlat
sudo systemctl enable ollama  # systemd ile otomatik başlatma
```

## GPU sağlık kontrolü
```bash
nvidia-smi
# Ollama GPU kullanıyor mu:
ollama run llama3.2 "test" &
nvidia-smi | grep -i ollama
```

## Common mistakes
- `ollama pull` yerine `ollama run` ile büyük model çekmeye başlamak — run da pull yapar ama interaktif modda sıkışır.
- GPU driver kurulmadan GPU flag'i vermek — sessizce CPU'ya düşer.
- Varsayılan 11434 portunu firewall'da açık tutmak — dış ağdan erişime izin verir.

## References
- `skills/llm-local-ollama-modelfile`
- `skills/llm-local-ollama-openai-compat`
- `skills/llm-local-gpu-memory`
