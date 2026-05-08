---
name: llm-openai-compatible-server
description: "vLLM, LiteLLM, Ollama gibi OpenAI-compatible API server'larını Sentinel veya OpenAI SDK ile entegre etmek; base_url ve model adını ayarlayarak yerli veya özel modellere bağlanmak gerektiğinde kullan."
---

## Purpose
OpenAI-compatible endpoint, mevcut OpenAI SDK kodunu değiştirmeden farklı backend'lere yönlendirmeye olanak verir. Yerel modeller, açık kaynak alternatifler ve maliyet optimizasyonu için kullanılır.

## OpenAI SDK ile bağlantı
```python
from openai import OpenAI

# Ollama:
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # zorunlu ama değeri önemli değil
)

# vLLM:
client = OpenAI(
    base_url="http://vllm-server:8000/v1",
    api_key="token-abc123"
)

# LiteLLM proxy:
client = OpenAI(
    base_url="http://litellm:4000",
    api_key=os.environ["LITELLM_API_KEY"]
)

# Model adı backend'e özel:
response = client.chat.completions.create(
    model="llama3.2:3b",   # Ollama model adı
    messages=[...]
)
```

## Sentinel profili olarak yapılandırma
```yaml
# sentinel.yaml
llm:
  provider: openai-compatible
  base_url: http://localhost:11434/v1
  model: llama3.2:3b
  api_key: ollama
```

## LiteLLM ile çoklu backend yönlendirme
```yaml
# litellm config.yaml
model_list:
  - model_name: fast
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434
  - model_name: smart
    litellm_params:
      model: anthropic/claude-sonnet-4-6
      api_key: os.environ/ANTHROPIC_API_KEY
```

## Uyumluluk sınırları
OpenAI-compat endpoint'ler chat completions'ı destekler; Responses API, Assistants API ve Embeddings modele göre farklılık gösterir.

## Common mistakes
- `base_url`'de trailing `/v1` ekini unutmak — 404 hatası.
- `model` adını OpenAI model adıyla değil backend'e özel adla girmek gerektiğini gözden kaçırmak.

## References
- `skills/llm-local-ollama-openai-compat`
- `skills/llm-local-vllm-setup`
- `skills/llm-openai-chat-completion`
