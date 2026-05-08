---
name: llm-openai-rate-limit-retry
description: "OpenAI API'den 429 rate limit veya 503 hata alındığında Retry-After header'ını okumak, exponential backoff uygulamak ve tenacity/backoff kütüphanesiyle üretime hazır retry mekanizması kurmak gerektiğinde kullan."
---

## Purpose
OpenAI rate limit hataları TPM (token), RPM (request) veya günlük limit aşımından kaynaklanır. Her durum için aynı retry stratejisi çalışmaz.

## Hata türleri ve stratejileri

| Hata | HTTP | Strateji |
|---|---|---|
| `rate_limit_exceeded` | 429 | `Retry-After` header'ını oku |
| `server_error` | 500/503 | Backoff + tekrar dene |
| `insufficient_quota` | 429 | Tekrar deneme; kota artırma gerekli |
| `context_length_exceeded` | 400 | Tekrar deneme yok; isteği kısalt |

## Retry-After header
```python
from openai import RateLimitError
import time

try:
    response = client.chat.completions.create(...)
except RateLimitError as e:
    retry_after = float(e.response.headers.get("retry-after", 5))
    time.sleep(retry_after)
```

## tenacity ile production-ready retry
```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import RateLimitError, APIError

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(6)
)
def call_openai(**kwargs):
    return client.chat.completions.create(**kwargs)
```

## backoff kütüphanesi (daha sade)
```python
import backoff
from openai import RateLimitError

@backoff.on_exception(backoff.expo, RateLimitError, max_tries=8, jitter=backoff.full_jitter)
def create(**kwargs):
    return client.chat.completions.create(**kwargs)
```

## OpenAI SDK'nın yerleşik retry
```python
client = OpenAI(
    max_retries=3,  # varsayılan 2
    timeout=60.0
)
```
Yerleşik retry 429 ve 5xx için otomatik çalışır; özel mantık gerekmiyorsa yeterlidir.

## Common mistakes
- `Retry-After` değerini saniye olarak okumayı unutmak — bazen ISO date olabilir.
- Sabit `time.sleep(60)` kullanmak — tüm işçiler aynı anda yeniden dener (thundering herd).
- `AuthenticationError` için retry uygulamak — API key sorunu, beklemek işe yaramaz.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-anthropic-rate-limits`
