---
name: llm-anthropic-file-api
description: "Anthropic Files API ile PDF veya diğer dokümanları bir kez yükleyip birden fazla istekte dosya ID'siyle referans etmek, büyük dokümanları token maliyeti olmadan yönetmek gerektiğinde kullan."
---

## Purpose
Files API, aynı dosyayı her istekte tekrar göndermek yerine bir kez yükleyip ID ile referans etmeyi sağlar. PDF analizi ve çok turlu doküman işlemede maliyet açısından avantajlı.

## Dosya yükleme
```python
with open("report.pdf", "rb") as f:
    file_response = client.files.upload(
        file=("report.pdf", f, "application/pdf")
    )
file_id = file_response.id  # file_...
```

## Dosyayı mesajda kullanma
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file_id
                    }
                },
                {"type": "text", "text": "Bu raporun özetini çıkar."}
            ]
        }
    ]
)
```

## Dosya yönetimi
```python
# Tüm dosyaları listele:
files = client.files.list()
for f in files.data:
    print(f.id, f.filename, f.size)

# Dosya silme:
client.files.delete(file_id)
```

## Desteklenen formatlar
- PDF (her sayfa görüntü olarak işlenir)
- Düz metin dosyaları

## Common mistakes
- Dosyayı her istekte tekrar yüklemek — Files API'nin amacı bundan kaçınmak.
- Silinmiş file_id ile istek göndermek — 404 hatası.
- Dosya içeriğinin değiştiğinde ID'nin değişmeyeceğini ve eski içeriğin kullanılacağını unutmak.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-vision`
- `skills/llm-anthropic-prompt-caching`
