---
name: llm-local-gemma
description: "Google Gemma 2/3 model ailesini Ollama ile çalıştırma, instruction formatını doğrulama ve Sentinel profiline bağlama gerektiğinde kullan"
---

## Purpose
Gemma modelleri, özel instruction formatı (`<start_of_turn>user\n...<end_of_turn>`) gerektirir. Ollama bu formatı otomatik uygular; doğrudan API kullanırken manuel olarak eklemek gerekir. Bu skill her iki senaryoyu da kapsar.

## Workflow

### 1. Modeli İndir
```bash
ollama pull gemma3:4b          # 4B parametre, Q4 quantize
ollama pull gemma3:12b         # daha güçlü
ollama pull gemma2:2b          # çok hafif, hızlı prototip
```

### 2. Ollama ile Çalıştır
```bash
ollama run gemma3:4b "Türkçe özetle: $(cat belge.txt)"
```

### 3. Doğrudan API (instruction format zorunlu)
```python
import requests

prompt = """<start_of_turn>user
Aşağıdaki JSON şemasını Python dataclass'a çevir:
{"name": "string", "age": "integer"}
<end_of_turn>
<start_of_turn>model
"""

resp = requests.post("http://localhost:11434/api/generate", json={
    "model": "gemma3:4b",
    "prompt": prompt,
    "stream": False,
    "options": {"temperature": 0.2, "num_ctx": 8192}
})
print(resp.json()["response"])
```

### 4. Sentinel sentinel.yaml
```yaml
profiles:
  gemma-local:
    provider: openai-compatible
    base_url: http://localhost:11434/v1
    api_key: ollama
    model: gemma3:4b
    system_prompt_support: true   # Gemma3 sistem promptu destekler
```

### 5. Vision (Gemma3 multimodal)
```bash
ollama pull gemma3:4b   # vision destekli build otomatik gelir
# Görüntü gönderimi için skills/llm-local-multi-modal bakın
```

## Common mistakes
- Gemma2'ye sistem promptu göndermek — Gemma2, sistem promptunu user turu olarak işler; Gemma3 gerçek sistem desteği sunar.
- `<end_of_turn>` token'ını unutmak — model yanıt üretmeden bekler.
- 8k context için model çekerken Ollama'nın varsayılan 2048 limitinde kalmak — `num_ctx` açıkça set edin.
- Gemma3'ün lisans koşullarının ticari kullanımda Google tarafından ayrıca onay gerektirdiğini unutmak.

## References
- `skills/llm-local-lm-studio`
- `skills/llm-local-multi-modal`
