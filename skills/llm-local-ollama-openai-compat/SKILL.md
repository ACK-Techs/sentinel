---
name: llm-local-ollama-openai-compat
description: "Ollama'nın OpenAI-compatible endpoint'ini (/v1/chat/completions) Sentinel, Python OpenAI SDK veya LangChain ile entegre etmek; yerel modeli üretim kodu değiştirmeden kullanmak gerektiğinde kullan."
---

## Purpose
Ollama `/v1` prefix'iyle OpenAI API'sini tam taklit eder. Anthropic → yerel model veya OpenAI → yerel model geçişinde minimum kod değişikliği sağlar.

## Python OpenAI SDK ile
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # boş string de çalışır
)

response = client.chat.completions.create(
    model="llama3.2:8b",
    messages=[
        {"role": "system", "content": "Sen bir Kubernetes uzmanısın."},
        {"role": "user", "content": "HPA nedir?"}
    ]
)
print(response.choices[0].message.content)
```

## Streaming
```python
with client.chat.completions.create(
    model="llama3.2:8b",
    messages=[...],
    stream=True
) as stream:
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
```

## Embedding
```python
embedding = client.embeddings.create(
    model="nomic-embed-text",
    input=["PromQL nedir?"]
)
vector = embedding.data[0].embedding
```

## Sentinel entegrasyonu
```yaml
# sentinel.yaml veya .env
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.2:8b
LLM_API_KEY=ollama
```

## LangChain ile
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="llama3.2"
)
```

## Common mistakes
- Ollama'nın tool use desteğinin modele bağlı olduğunu bilmemek — llama3.2 destekler, bazı modeller desteklemez.
- `localhost` yerine container'dan container erişiminde `host.docker.internal` kullanmayı unutmak.
- Embedding modelini chat endpoint'ine sormak — ayrı `nomic-embed-text` gibi model gerekir.

## References
- `skills/llm-local-ollama-setup`
- `skills/llm-openai-compatible-server`
- `skills/llm-local-ollama-modelfile`
