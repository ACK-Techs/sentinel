---
name: llm-anthropic-batch-api
description: "Anthropic Message Batches API ile yüzlerce veya binlerce bağımsız isteği toplu göndermek, batch durumunu izlemek ve tamamlanan sonuçları almak gerektiğinde kullan."
---

## Purpose
Batch API, eş zamanlı çalışma gerektirmeyen (offline işleme, dataset annotation, toplu analiz) senaryolarda %50 maliyet indirimi sağlar; 24 saat içinde tamamlanır.

## Batch oluşturma
```python
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "req-001",
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Türkiye'nin başkenti nedir?"}]
            }
        },
        {
            "custom_id": "req-002",
            "params": {
                "model": "claude-sonnet-4-6",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "2+2 kaçtır?"}]
            }
        }
    ]
)
print(batch.id)  # msgbatch_...
```

## Batch durumu izleme
```python
while True:
    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status == "ended":
        break
    print(f"İşlendi: {batch.request_counts.succeeded}/{batch.request_counts.processing}")
    time.sleep(60)
```

## Sonuçları alma
```python
for result in client.messages.batches.results(batch_id):
    if result.result.type == "succeeded":
        print(f"{result.custom_id}: {result.result.message.content[0].text}")
    elif result.result.type == "errored":
        print(f"{result.custom_id}: hata - {result.result.error.type}")
```

## Sınırlar
- Maksimum batch boyutu: 100K istek veya 256MB
- Tamamlanma süresi: 24 saate kadar
- Streaming desteklenmez

## Common mistakes
- `custom_id` değerlerini batch içinde tekrar etmek — benzersiz olmalı.
- Batch API'yi gerçek zamanlı yanıt gerektiren senaryolarda kullanmak.
- 24 saat sonra sonuçları almamanın veri kaybına yol açacağını bilmemek.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-rate-limits`
