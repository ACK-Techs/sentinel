---
name: llm-anthropic-rate-limits
description: "Anthropic API rate limit (429) hatalarını yönetmek, RPM/TPM limitlerini izlemek ve exponential backoff ile retry stratejisi kodlamak gerektiğinde kullan."
---

## Purpose
Üretim uygulamalarında rate limit kaçınılmazdır. Doğru retry stratejisi olmadan 429 hatası son kullanıcıya yansır.

## Rate limit türleri
- **RPM** (Requests Per Minute): API çağrı sayısı
- **TPM** (Tokens Per Minute): toplam token akışı
- **TPD** (Tokens Per Day): günlük toplam

Limit, model ve tier'a göre değişir. Mevcut limitler: `x-ratelimit-*` response header'larında.

## Response header'ları okuma
```python
# SDK ile:
response = client.messages.create(...)
# Header'lara şu an doğrudan erişim yok (SDK soyutlar)
# Raw HTTP ile:
import httpx
# x-ratelimit-limit-requests, x-ratelimit-remaining-requests
# x-ratelimit-reset-requests (ISO 8601 timestamp)
```

## Exponential backoff implementasyonu
```python
import time
import anthropic
from anthropic import RateLimitError

def create_with_retry(client, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            wait = (2 ** attempt) + (random.random() * 0.5)  # jitter
            print(f"Rate limited. {wait:.1f}s bekleniyor...")
            time.sleep(wait)
```

## SDK'nın otomatik retry
```python
# Anthropic Python SDK retry'ı destekler:
client = anthropic.Anthropic(
    max_retries=3  # varsayılan 2
)
```

## Önleyici stratejiler
- Batch API: %50 maliyet düşüşü + farklı limit pool
- İstek kuyruklama: token bucket veya leaky bucket implementasyonu
- Tier upgrade: hesap sayfasından limit artırma talebi

## Common mistakes
- `time.sleep(60)` sabit bekleme — basit ama verimsiz.
- Sadece 429'u yakalamak; `529` (overloaded) da benzer retry gerektiri.
- Jitter eklemeksizin backoff kullanmak — herd effect yaratır.

## References
- `skills/llm-anthropic-error-handling`
- `skills/llm-anthropic-batch-api`
- `skills/llm-anthropic-sdk-python`
