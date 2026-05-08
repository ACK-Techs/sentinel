---
name: llm-anthropic-extended-thinking
description: "Anthropic extended thinking (derin akıl yürütme) modunu etkinleştirmek, düşünme bütçesi ayarlamak ve thinking block içeren yanıtları işlemek gerektiğinde kullan."
---

## Purpose
Extended thinking, Claude'un karmaşık çok adımlı problemlerde görünür iç düşünme süreci yürütmesini sağlar. `thinking` content block'ları yanıtta görünür.

## Etkinleştirme
```python
response = client.messages.create(
    model="claude-opus-4-7",  # thinking yalnızca belirli modellerde
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # düşünmeye ayrılan maksimum token
    },
    messages=[{"role": "user", "content": "Bu matematik problemini çöz: ..."}]
)
```

## Yanıt işleme
```python
for block in response.content:
    if block.type == "thinking":
        print("Düşünce süreci:")
        print(block.thinking)
    elif block.type == "text":
        print("Yanıt:")
        print(block.text)
```

## budget_tokens seçimi
- Basit problem: 2000–5000
- Orta karmaşıklık: 5000–10000
- Derin analiz: 10000–32000 (model limitine bak)
- Bütçe tükenirse model düşünmeyi keser, yanıtlamaya devam eder

## Streaming ile kullanım
Thinking block'ları da stream edilir; `thinking_delta` event türüne dikkat et.

## Ne zaman kullanılır?
- Çok adımlı matematik/mantık problemleri
- Karmaşık kod hata ayıklama
- Uzun belge analizi ve çıkarım
- Belirsiz veya çelişkili gereksinimlerin değerlendirilmesi

## Common mistakes
- Basit sorularda yüksek budget_tokens vermek — gereksiz maliyet ve gecikme.
- thinking block içindeki düşünce akışını son kullanıcıya göstermek; iç süreç olarak ele alınmalı.
- `claude-haiku` gibi thinking desteklemeyen modelde parametreyi kullanmak.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-model-selection`
- `skills/llm-anthropic-streaming`
