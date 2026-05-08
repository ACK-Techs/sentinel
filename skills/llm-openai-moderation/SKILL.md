---
name: llm-openai-moderation
description: "OpenAI Moderation API ile kullanıcı girdisini veya model çıktısını zararlı içerik kategorilerine karşı taramak, politika uygulama kapısı kurmak ve moderasyon sonuçlarını yorumlamak gerektiğinde kullan."
---

## Purpose
Moderation API, içeriğin zararlı olup olmadığını ücretsiz sınıflandırır. Kullanıcı girdilerini LLM'e göndermeden önce veya model çıktılarını kullanıcıya iletmeden önce filtre kapısı olarak kullanılır.

## Temel kullanım
```python
response = client.moderations.create(
    input="Kullanıcı mesajı burada",
    model="omni-moderation-latest"
)

result = response.results[0]
if result.flagged:
    print("İçerik zararlı olarak işaretlendi!")
    for category, flagged in result.categories.__dict__.items():
        if flagged:
            print(f"  Kategori: {category}")
```

## Kategoriler
```
hate, hate/threatening
harassment, harassment/threatening
self-harm, self-harm/intent, self-harm/instructions
sexual, sexual/minors
violence, violence/graphic
illicit, illicit/violent
```

## Skor eşiği ile karar
```python
result = response.results[0]
# scores: her kategori için 0-1 olasılık
for category, score in result.category_scores.__dict__.items():
    if score > 0.7:  # özel eşik
        print(f"Yüksek risk: {category} ({score:.3f})")
```

## Üretim kalıbı
```python
def safe_complete(user_message: str) -> str:
    mod = client.moderations.create(input=user_message)
    if mod.results[0].flagged:
        return "Bu istek politikamıza aykırı içerik içeriyor."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message.content
```

## Common mistakes
- Yalnızca `flagged` boolean'ına bakıp kategori bazlı farklı yanıt üretmemek — tüm ihlaller aynı şekilde ele alınmaz.
- Moderation API'nin her dili ve kültürü eşit hassasiyette ele almadığını bilmemek.
- Çıktı moderasyonunu unutmak — model zararlı içerik üretebilir, sadece giriş denetimi yetmez.

## References
- `skills/llm-openai-chat-completion`
- `skills/agentic-sec-jailbreak-resistance`
- `skills/llm-prompt-injection-defense`
