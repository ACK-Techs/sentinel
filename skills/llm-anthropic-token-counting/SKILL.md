---
name: llm-anthropic-token-counting
description: "Anthropic token sayma API'si ile istek göndermeden önce token sayısını ölçmek, maliyet tahmini yapmak ve context window dolmadan önce içeriği budamak gerektiğinde kullan."
---

## Purpose
API isteği göndermeden önce token sayısını bilmek: bütçe kontrolü, context window yönetimi ve kullanıcıya maliyet göstermek için kullanılır.

## Token sayma API'si
```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    system="Sen yardımcı bir asistansın.",
    messages=[
        {"role": "user", "content": "Python ile HTTP istek nasıl yapılır?"}
    ]
)
print(count.input_tokens)  # örn. 45
```

## Araç içeren sayma
```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    tools=tools,  # tool tanımları da sayılır
    messages=messages
)
```

## Konuşma geçmişi yönetimi
```python
MAX_CONTEXT = 100_000  # modele göre ayarla

def trim_history(messages, system, model="claude-sonnet-4-6"):
    while True:
        count = client.messages.count_tokens(
            model=model, system=system, messages=messages
        )
        if count.input_tokens < MAX_CONTEXT * 0.8:
            break
        # En eski user/assistant çiftini çıkar:
        messages = messages[2:]
    return messages
```

## Maliyet tahmini
```python
PRICES = {
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},  # USD/MTok
    "claude-haiku-4-5-20251001": {"input": 0.25, "output": 1.25}
}

def estimate_cost(model, input_tokens, expected_output=200):
    p = PRICES[model]
    cost = (input_tokens / 1_000_000 * p["input"]) + \
           (expected_output / 1_000_000 * p["output"])
    return cost
```

## Common mistakes
- Token sayarken sistem promptunu atlamak — sayım yanlış çıkar.
- Context window'un tam dolana kadar beklemek yerine %80 eşiğinde budamak.
- Tool tanımlarının token maliyetini hesaba katmamak; her tool ~100–300 token.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-prompt-caching`
- `skills/llm-anthropic-model-selection`
