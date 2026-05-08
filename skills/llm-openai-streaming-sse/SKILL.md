---
name: llm-openai-streaming-sse
description: "OpenAI Chat Completions API'de stream=True ile SSE delta event'lerini almak, metin chunk'larını birleştirmek ve tool_call delta'larını JSON'a dönüştürmek gerektiğinde kullan."
---

## Purpose
OpenAI streaming formatı Anthropic'ten farklıdır; delta yapısı ve `[DONE]` sonlandırıcı özgüdür. Her iki API ile çalışıyorsan farkları bilmek şarttır.

## Python SDK ile streaming
```python
with client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Kısa hikaye yaz."}],
    stream=True
) as stream:
    full_text = ""
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
            full_text += delta.content
        if chunk.choices[0].finish_reason:
            break
```

## Raw SSE formatı
```
data: {"id":"chatcmpl-...","choices":[{"delta":{"role":"assistant"},"finish_reason":null,"index":0}]}
data: {"id":"chatcmpl-...","choices":[{"delta":{"content":"Bir"},"finish_reason":null,"index":0}]}
data: {"id":"chatcmpl-...","choices":[{"delta":{"content":" zamanlar"},"finish_reason":null,"index":0}]}
data: {"id":"chatcmpl-...","choices":[{"delta":{},"finish_reason":"stop","index":0}]}
data: [DONE]
```

## Streaming tool call delta birleştirme
Tool call argument'ları parça parça gelir:
```python
tool_call_accumulator = {}

for chunk in stream:
    for tc_delta in chunk.choices[0].delta.tool_calls or []:
        idx = tc_delta.index
        if idx not in tool_call_accumulator:
            tool_call_accumulator[idx] = {"id": tc_delta.id, "name": tc_delta.function.name, "arguments": ""}
        tool_call_accumulator[idx]["arguments"] += tc_delta.function.arguments or ""

# Sonunda:
for tc in tool_call_accumulator.values():
    args = json.loads(tc["arguments"])
```

## Async streaming
```python
async with client.chat.completions.create(..., stream=True) as stream:
    async for chunk in stream:
        ...
```

## Common mistakes
- `data: [DONE]` gelince `json.loads()` çağırmak — parse hatası verir; önce kontrol et.
- `delta.content` None olduğunda string birleştirme yapmak — ilk chunk'ta rol gelir, içerik gelmez.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-anthropic-streaming`
