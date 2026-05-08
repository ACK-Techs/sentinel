---
name: llm-openai-responses-api
description: "OpenAI Responses API (yeni nesil API) ile oturum yönetimi, built-in araçlar (web_search, code_interpreter, file_search) ve çok turlu etkileşim kurmak gerektiğinde kullan."
---

## Purpose
Responses API, Chat Completions'ın yerini alacak şekilde tasarlanmıştır. Built-in araçlar, oturum ID ile durum yönetimi ve tam event akışı sunar.

## Temel kullanım
```python
response = client.responses.create(
    model="gpt-4o",
    input="Python ile HTTP istek nasıl yapılır?",
    instructions="Sen yardımcı bir yazılım asistanısın."
)
print(response.output_text)
```

## Oturum sürekliliği
```python
# İlk istek:
response = client.responses.create(
    model="gpt-4o",
    input="Kubernetes nedir?"
)
session_id = response.id

# Aynı oturuma devam:
follow_up = client.responses.create(
    model="gpt-4o",
    previous_response_id=session_id,
    input="HPA ile nasıl ölçeklenir?"
)
```

## Built-in araçlar
```python
# Web arama:
response = client.responses.create(
    model="gpt-4o",
    input="Bugünkü haberler neler?",
    tools=[{"type": "web_search_preview"}]
)

# Kod yorumlayıcı:
response = client.responses.create(
    model="gpt-4o",
    input="Bu CSV dosyasını analiz et.",
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}]
)
```

## Chat Completions ile fark

| | Chat Completions | Responses API |
|---|---|---|
| Oturum yönetimi | Manuel | `previous_response_id` |
| Built-in araçlar | Yok | web_search, code_interpreter |
| Durum | Stateless | ID ile saklı |

## Common mistakes
- `previous_response_id` ile eskiden kalma mesajları tekrar göndermek — API kendisi yönetiyor.
- Responses API'yi tüm OpenAI-compatible server'ların desteklediğini varsaymak — özeldir.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-openai-function-calling`
