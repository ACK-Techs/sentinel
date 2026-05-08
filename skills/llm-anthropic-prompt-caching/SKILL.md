---
name: llm-anthropic-prompt-caching
description: "Anthropic prompt caching ile tekrar eden system prompt veya uzun doküman bölümlerini cache'leyerek input token maliyetini azaltmak ve yanıt süresini kısaltmak gerektiğinde kullan."
---

## Purpose
Prompt caching, sabit kalan uzun içerikleri (system prompt, döküman, örnek veriler) yeniden göndermeden cache'den okutur. Cache hit = %90 maliyet indirimi + ~2x hızlanma.

## Cache-control ekleme
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Uzun bir sistem promptu... (örneğin 5000 token)",
            "cache_control": {"type": "ephemeral"}  # bu noktaya kadar cache
        }
    ],
    messages=[{"role": "user", "content": "Soru?"}]
)
```

## Cache noktaları (breakpoints)
- `cache_control: {type: "ephemeral"}` ile işaretlenen son bloğa kadar cache'lenir.
- En fazla **4** cache noktası tanımlanabilir.
- Cache TTL: 5 dakika (her hit yeniler).

## Nerede kullanılır?
```python
# 1. System prompt (her istekte aynı):
system = [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]

# 2. Uzun doküman + soru:
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": long_document, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": "Bu belgeye göre X nedir?"}
        ]
    }
]
```

## Cache kullanım izleme
```python
print(response.usage.cache_creation_input_tokens)  # ilk istek: yazdı
print(response.usage.cache_read_input_tokens)       # sonraki istekler: okudu
```

## Common mistakes
- Her istekte farklılaşan içeriği cache breakpoint'inin üstüne koymak — cache miss'e neden olur.
- Minimum token eşiğini (1024 token) aşmayan içeriği cache'lemeye çalışmak.
- Tool use sonuçlarını cache breakpoint'inden sonraya koymayı unutmak.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-sdk-python`
- `skills/llm-anthropic-token-counting`
