---
name: llm-anthropic-vision
description: "Anthropic vision API'si ile görüntü analizi yapmak; base64 veya URL formatında image content block oluşturmak ve çoklu görüntülü mesajlar yazmak gerektiğinde kullan."
---

## Purpose
Claude görüntüleri okur, analiz eder, karşılaştırır ve açıklar. Grafik, screenshot, diyagram veya fotoğraf içeren kullanım senaryoları için content block formatı kritiktir.

## URL ile görüntü gönderme
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/chart.png"
                    }
                },
                {"type": "text", "text": "Bu grafikte ne görüyorsun?"}
            ]
        }
    ]
)
```

## Base64 ile görüntü gönderme
```python
import base64

with open("screenshot.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

content = [
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",  # image/jpeg, image/gif, image/webp
            "data": image_data
        }
    },
    {"type": "text", "text": "Bu ekran görüntüsünde hata var mı?"}
]
```

## Çoklu görüntü
```python
content = [
    {"type": "image", "source": {"type": "url", "url": url1}},
    {"type": "image", "source": {"type": "url", "url": url2}},
    {"type": "text", "text": "Bu iki grafik arasındaki fark nedir?"}
]
```

## Sınırlar
- Maksimum görüntü boyutu: 5MB (base64 öncesi)
- Her mesajda maksimum 20 görüntü
- Desteklenen: PNG, JPEG, GIF, WebP

## Common mistakes
- `media_type` ile gerçek dosya formatının uyuşmaması.
- Büyük PNG dosyasını base64 ile göndermek yerine Files API veya URL kullanmak.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-file-api`
- `skills/llm-openai-vision`
