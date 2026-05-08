---
name: llm-openai-vision
description: "OpenAI vision API'si ile görüntü içeren mesajlar oluşturmak, URL veya base64 image_url content formatını kullanmak ve çoklu görüntü analizi yapmak gerektiğinde kullan."
---

## Purpose
GPT-4o ve benzeri modeller görüntü girişini `image_url` content türü üzerinden alır. Grafana dashboard ekran görüntüsü analizi, hata ekranı teşhisi gibi senaryolar için kullanılır.

## URL ile görüntü
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/grafana-dashboard.png"}
                },
                {"type": "text", "text": "Bu dashboard'da anormal bir durum var mı?"}
            ]
        }
    ],
    max_tokens=512
)
```

## Base64 görüntü
```python
import base64

with open("screenshot.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

content = [
    {
        "type": "image_url",
        "image_url": {"url": f"data:image/png;base64,{b64}"}
    },
    {"type": "text", "text": "Bu hata mesajını açıkla."}
]
```

## Detail parametresi
```python
"image_url": {
    "url": "...",
    "detail": "high"   # "low" | "high" | "auto" (varsayılan)
}
```
- `low`: 85 token sabit; küçük görüntüler ve hız için
- `high`: görüntü tile'lara bölünür, ~1700 token; detaylı analiz için

## Çoklu görüntü karşılaştırma
```python
content = [
    {"type": "image_url", "image_url": {"url": before_url}},
    {"type": "image_url", "image_url": {"url": after_url}},
    {"type": "text", "text": "Bu iki grafiğin farkı nedir?"}
]
```

## Common mistakes
- `detail: "high"` ile büyük görüntüler göndermek; token maliyeti 10x artabilir.
- `data:image/jpeg` yerine `data:image/png` MIME türü yazmak — format uyuşmazlığı.
- Gizli bilgi içeren ekran görüntülerini OpenAI'ye göndermek.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-anthropic-vision`
