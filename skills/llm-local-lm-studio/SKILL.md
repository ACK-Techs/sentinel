---
name: llm-local-lm-studio
description: "LM Studio GUI ile yerel model yükleme, OpenAI-uyumlu sunucuyu başlatma ve Sentinel CLI'yi bu endpoint'e bağlama adımlarında kullan"
---

## Purpose
LM Studio, macOS/Windows/Linux'ta GUI üzerinden GGUF modellerini indirip çalıştırmayı ve localhost OpenAI-compatible server açmayı sağlar. Bu skill, modeli seçip sunucuyu başlatmaktan Sentinel profiline eklemeye kadar tüm adımları kapsar.

## Workflow

### 1. Sunucuyu Başlat
LM Studio → "Local Server" sekmesi → "Start Server"
Varsayılan: `http://localhost:1234/v1`

### 2. Endpoint Doğrulaması
```bash
curl http://localhost:1234/v1/models | jq '.data[].id'
# Çıktı: ["lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF"]
```

### 3. Sentinel Profiline Bağla
`sentinel.yaml` içinde:
```yaml
profiles:
  local-lmstudio:
    provider: openai-compatible
    base_url: http://localhost:1234/v1
    api_key: lm-studio         # herhangi bir string kabul edilir
    model: meta-llama-3-8b-instruct
    timeout_seconds: 120
    max_tokens: 2048
```

### 4. Test
```bash
sentinel --profile local-lmstudio chat "Merhaba, çalışıyor musun?"
sentinel doctor --profile local-lmstudio
```

### 5. Context Limit Ayarı
LM Studio → model kartı → "Context Length" → üretimde kullandığınız pencereyi girin (ör. 8192). Model GUI'de açıkken bu değeri değiştirirseniz sunucuyu yeniden başlatın.

## Common mistakes
- `api_key` boş bırakmak: LM Studio herhangi bir string bekler, boş bırakıldığında 401 döner.
- Context limitini model kartından değil Sentinel config'den ayarlamaya çalışmak — bu değer model tarafında belirlenir.
- Sunucu açıkken modeli değiştirmek: endpoint aynı kalır ama token davranışı farklılaşır, profile notu tutun.
- Ekip ortamında LAN'da güvensiz açık bırakmak: `--server-port` ile birlikte firewall kuralı zorunlu.

## References
- `skills/agentic-cli-config-validation`
- `skills/llm-local-air-gap-deploy`
