---
name: llm-local-air-gap-deploy
description: "İnternet erişimi olmayan (air-gap) ortama GGUF model transferi, Ollama veya llama.cpp kurulumu ve Sentinel bağlantısı gerektiğinde kullan"
---

## Purpose
Air-gap ortamlar; model indirmeyi, pip kurulumunu ve Docker pull'u engeller. Bu skill, gerekli binary ve model dosyalarını çevrimdışı makineye taşıma, çalıştırma ve Sentinel'e bağlama adımlarını kapsar.

## Workflow

### 1. Kaynak Makinede Paketle
```bash
# Ollama binary + model
ollama pull llama3.2:3b
# Model dosyası: ~/.ollama/models/ altında
tar czf ollama-bundle.tar.gz \
  $(which ollama) \
  ~/.ollama/models/blobs/ \
  ~/.ollama/models/manifests/

# veya GGUF doğrudan
wget https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf
```

### 2. Güvenli Transfer
```bash
# USB veya iç ağ üzerinden
scp ollama-bundle.tar.gz user@air-gap-host:/opt/llm/
rsync -avz --checksum model.gguf user@air-gap-host:/opt/llm/
```

### 3. Air-Gap Makinede Kur
```bash
tar xzf ollama-bundle.tar.gz -C /usr/local/
chmod +x /usr/local/bin/ollama

# Model registry kopyala
mkdir -p ~/.ollama
cp -r ./models ~/.ollama/

# Servisi başlat (offline)
OLLAMA_HOST=0.0.0.0:11434 ollama serve &
```

### 4. Sentinel Konfigürasyonu
```yaml
profiles:
  air-gap:
    provider: openai-compatible
    base_url: http://localhost:11434/v1
    api_key: ollama
    model: llama3.2:3b
    allow_internet: false
```

### 5. Bütünlük Doğrulaması
```bash
sha256sum model.gguf > model.gguf.sha256
# Hedef makinede:
sha256sum -c model.gguf.sha256
```

## Common mistakes
- Sadece binary'i taşıyıp model manifest dosyalarını unutmak — Ollama modeli başlatamaz.
- Transfer sırasında checksum doğrulaması yapmamak — bozuk model sessiz hallüsinasyon üretir.
- Sentinel'de `allow_internet: false` koymadan ortam değişkenlerinin dışa leak etmesine izin vermek.
- llama.cpp build için C++ toolchain gerektirdiğini unutmak — air-gap'te pre-built binary zorunlu.

## References
- `skills/llm-local-lm-studio`
- `skills/llm-local-gemma`
- `skills/agentic-sec-env-var-handling`
