---
name: llm-openai-function-calling
description: "OpenAI Chat Completions API'de tools parametresiyle fonksiyon tanımlamak, model tarafından dönen tool_calls bloğunu işlemek ve çok turlu araç döngüsü kurmak gerektiğinde kullan."
---

## Purpose
Function calling (tools), modelin yapılandırılmış parametre çıkararak dış fonksiyon çağırmasını sağlar. Anthropic tool use ile kavramsal olarak aynı; sözdizimi farklı.

## Araç tanımlama
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_prometheus_metric",
            "description": "Prometheus'tan anlık metrik değeri sorgular.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "PromQL ifadesi"},
                    "time": {"type": "string", "description": "ISO 8601 timestamp (opsiyonel)"}
                },
                "required": ["query"]
            }
        }
    }
]
```

## Araç çağrısı döngüsü
```python
messages = [{"role": "user", "content": "CPU kullanımı kaç?"}]

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        tools=tools,
        tool_choice="auto",
        messages=messages
    )
    
    choice = response.choices[0]
    messages.append(choice.message)  # assistant mesajını ekle
    
    if choice.finish_reason == "stop":
        break
    
    if choice.finish_reason == "tool_calls":
        for tc in choice.message.tool_calls:
            args = json.loads(tc.function.arguments)
            result = call_tool(tc.function.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": str(result)
            })
```

## tool_choice seçenekleri
- `"auto"`: model kendi karar verir
- `"none"`: araç kullanma
- `{"type": "function", "function": {"name": "get_prometheus_metric"}}`: zorla çağır

## Paralel araç çağrısı
Model birden fazla `tool_calls` içeren yanıt verebilir; her biri için ayrı `tool` mesajı döndür.

## Common mistakes
- `finish_reason: "tool_calls"` kontrolü atlayıp döngüyü erken sonlandırmak.
- `tool_call_id` eşleştirmesini atlamak — OpenAI her sonucu kendi ID'siyle ilişkilendirir.
- `arguments` alanını `json.loads()` ile parse etmeyi unutmak; ham string gelir.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-anthropic-tool-use`
- `skills/llm-prompt-tool-descriptions`
