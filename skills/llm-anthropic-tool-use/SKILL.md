---
name: llm-anthropic-tool-use
description: "Anthropic Messages API'de tool tanımlamak, model tarafından dönen tool_use block'u işlemek, tool_result göndermek ve çok adımlı araç döngüsü kurmak gerektiğinde kullan."
---

## Purpose
Tool use (function calling), modelin dış fonksiyon çağırmasını sağlar. Doğru döngü implementasyonu olmadan model askıda kalır.

## Araç tanımlama
```python
tools = [
    {
        "name": "get_weather",
        "description": "Belirtilen şehrin güncel hava durumunu döndürür.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Şehir adı"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
]
```

## Araç çağrısı döngüsü
```python
messages = [{"role": "user", "content": "İstanbul'da hava nasıl?"}]

while True:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    if response.stop_reason == "end_turn":
        break  # model bitti

    if response.stop_reason == "tool_use":
        # Araç çağrısını işle
        tool_calls = [b for b in response.content if b.type == "tool_use"]
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tc in tool_calls:
            result = call_tool(tc.name, tc.input)  # gerçek fonksiyon çağrısı
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": str(result)
            })
        messages.append({"role": "user", "content": tool_results})
```

## Paralel araç çağrısı
Model birden fazla araç aynı turda çağırabilir; tüm sonuçlar tek `user` mesajında döndürülür.

## Common mistakes
- `tool_use` stop_reason'ı kontrol etmeden döngüden çıkmak — model bekliyor.
- `tool_use_id` eşleştirmesini atlamak; her sonuç kendi `tool_use_id`'sine bağlanmalı.
- Araç sonucunu string yerine dict olarak göndermek — `content` string veya content block listesi olmalı.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-sdk-python`
- `skills/llm-prompt-tool-descriptions`
