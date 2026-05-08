---
name: llm-anthropic-messages-api
description: "Anthropic Messages API'ye HTTP veya SDK üzerinden istek gönderirken, istek/yanıt JSON yapısını, content block formatını ve gerekli/opsiyonel alanları anlamak gerektiğinde kullan."
---

## Purpose
Anthropic API'nin temel istek-yanıt yapısı. SDK kullanımı altında bu HTTP şeması vardır; hata ayıklarken veya raw request oluştururken doğrudan gereklidir.

## İstek yapısı
```json
POST https://api.anthropic.com/v1/messages

{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "Sen yardımcı bir asistansın.",
  "messages": [
    {"role": "user", "content": "Merhaba"},
    {"role": "assistant", "content": "Merhaba! Nasıl yardımcı olabilirim?"},
    {"role": "user", "content": "Python öğrenmek istiyorum."}
  ]
}
```

Zorunlu header'lar:
```
x-api-key: <API_KEY>
anthropic-version: 2023-06-01
content-type: application/json
```

## Yanıt yapısı
```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {"type": "text", "text": "Python öğrenmek için..."}
  ],
  "model": "claude-sonnet-4-6",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 25,
    "output_tokens": 150
  }
}
```

## Content block türleri
- `text`: metin yanıtı
- `tool_use`: araç çağrısı (tool_use block)
- `image`: base64 veya URL görüntü (input içinde)

## stop_reason değerleri
- `end_turn`: model doğal bitirdi
- `max_tokens`: token limiti aşıldı
- `stop_sequence`: durdurma dizisi tetiklendi
- `tool_use`: araç çağrısı bekleniyor

## Common mistakes
- `messages` dizisinde user/assistant sırasını bozuk verme — API 400 döner.
- `max_tokens` belirtmemek; zorunludur.
- `system` mesajını `messages` dizisine koymak yerine ayrı alan olarak göndermek.

## References
- `skills/llm-anthropic-sdk-python`
- `skills/llm-anthropic-tool-use`
- `skills/llm-anthropic-streaming`
