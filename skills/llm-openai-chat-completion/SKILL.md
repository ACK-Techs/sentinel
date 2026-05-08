---
name: llm-openai-chat-completion
description: "OpenAI Chat Completions API ile istek göndermek, yanıt yapısını anlamak ve temel parametreleri (model, temperature, max_tokens) yapılandırmak gerektiğinde kullan. OpenAI-compatible server'lar için de geçerlidir."
---

## Purpose
OpenAI Chat Completions, sektörün de-facto LLM API standardıdır. Ollama, vLLM, LiteLLM gibi araçlar da aynı endpoint'i kullanır.

## Temel istek (Python)
```python
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Sen yardımcı bir asistansın."},
        {"role": "user", "content": "Python nedir?"}
    ],
    max_tokens=512,
    temperature=0.7
)

print(response.choices[0].message.content)
print(f"Kullanılan tokenlar: {response.usage.total_tokens}")
```

## Yanıt yapısı
```json
{
  "id": "chatcmpl-...",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "..."},
      "finish_reason": "stop"
    }
  ],
  "usage": {"prompt_tokens": 20, "completion_tokens": 80, "total_tokens": 100}
}
```

## finish_reason değerleri
- `stop`: doğal bitiş
- `length`: `max_tokens` sınırı
- `tool_calls`: araç çağrısı bekleniyor
- `content_filter`: içerik filtresi tetiklendi

## Temel parametreler

| Parametre | Etki |
|---|---|
| `temperature` | 0=deterministik, 1=yaratıcı, 2=kaotik |
| `top_p` | nucleus sampling (temperature ile beraber değil) |
| `n` | kaç seçenek üretilsin |
| `presence_penalty` | yeni konu teşviki (0-2) |
| `frequency_penalty` | tekrar ceza (0-2) |

## Common mistakes
- `temperature` ve `top_p`'yi aynı anda kullanmak — yalnızca birini ayarla.
- `n > 1` ile birden fazla seçenek isteyip yalnızca `choices[0]`'ı işlemek.
- `finish_reason: "length"` durumunu kontrol etmemek — yanıt kesilmiş olabilir.

## References
- `skills/llm-openai-function-calling`
- `skills/llm-openai-streaming-sse`
- `skills/llm-openai-compatible-server`
