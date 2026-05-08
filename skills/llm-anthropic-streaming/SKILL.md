---
name: llm-anthropic-streaming
description: "Anthropic Messages API'de streaming SSE (Server-Sent Events) yanıtlarını alıp delta event'lerini işlemek, metin birleştirmek ve kullanım sayacını hesaplamak gerektiğinde kullan."
---

## Purpose
Streaming, ilk token'ın kullanıcıya gösterilme süresini düşürür. Event akışını doğru ayrıştırmak hem Python SDK hem de raw HTTP için bilinmesi gerekir.

## Python SDK ile streaming
```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Kısa bir hikaye yaz."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Tamamlama sonrası kullanım:
final_message = stream.get_final_message()
print(f"\nInput: {final_message.usage.input_tokens} tokens")
```

## Raw SSE event formatı
```
event: message_start
data: {"type":"message_start","message":{"id":"msg_...","type":"message","role":"assistant","content":[],"model":"claude-sonnet-4-6","stop_reason":null,"usage":{"input_tokens":25,"output_tokens":1}}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Bir"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" zamanlar"}}

event: message_stop
data: {"type":"message_stop"}
```

## Event türleri
| Event | Açıklama |
|---|---|
| `message_start` | Mesaj başladı, input token sayısı var |
| `content_block_start` | Yeni içerik bloğu (text veya tool_use) |
| `content_block_delta` | Delta metin veya JSON parçası |
| `content_block_stop` | Blok bitti |
| `message_delta` | stop_reason güncellendi, output token |
| `message_stop` | Mesaj tamamen bitti |

## Tool use ile streaming
Tool use block'ları `input_json_delta` event'leriyle parça parça gelir; tüm JSON birikmeden `json.loads()` çalıştırma.

## Common mistakes
- `message_delta` event'indeki output_tokens'ı okumayı atlamak — `message_start`'ta yalnızca input_tokens var.
- `data: [DONE]` beklemek — Anthropic bu formatı kullanmaz.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-tool-use`
- `skills/llm-openai-streaming-sse`
