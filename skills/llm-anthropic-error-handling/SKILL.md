---
name: llm-anthropic-error-handling
description: "Anthropic API hata kodlarını (4xx, 5xx) tanımak, her hata türüne özgü retry veya fallback akışı uygulamak ve üretimde sağlam hata yönetimi kurmak gerektiğinde kullan."
---

## Purpose
Anthropic API hataları güvenli şekilde yakalanmazsa kullanıcıya ham hata mesajı gider veya uygulama çöker. Her hata kodu farklı müdahale gerektirir.

## Hata sınıfı hiyerarşisi (Python SDK)
```python
anthropic.APIError           # tüm hatalar üst sınıfı
├── APIStatusError           # HTTP hata yanıtları
│   ├── BadRequestError      # 400
│   ├── AuthenticationError  # 401
│   ├── PermissionDeniedError # 403
│   ├── NotFoundError        # 404
│   ├── UnprocessableEntityError # 422
│   ├── RateLimitError       # 429
│   └── InternalServerError  # 500/529
├── APIConnectionError       # ağ hatası
└── APITimeoutError          # timeout
```

## Hata türlerine göre strateji

| Hata | Strateji |
|---|---|
| 400 (bad request) | İsteği düzelt, tekrar deneme |
| 401 (auth) | API key kontrol et, yenile |
| 403 (permission) | İzin kapsamını kontrol et |
| 429 (rate limit) | Exponential backoff |
| 500/529 (server) | Backoff + fallback model |
| connection/timeout | Retry + circuit breaker |

## Üretim kalıbı
```python
import anthropic

def safe_complete(client, **kwargs):
    try:
        return client.messages.create(**kwargs)
    except anthropic.RateLimitError:
        return retry_with_backoff(client, **kwargs)
    except anthropic.InternalServerError:
        # Fallback: daha küçük model veya cached yanıt
        return fallback_response()
    except anthropic.AuthenticationError:
        raise  # Bu hata retry edilmez, konfigürasyon sorunu
    except anthropic.APIConnectionError as e:
        log.error(f"Ağ hatası: {e}")
        raise
```

## Hata mesajını loglamak
```python
except anthropic.APIStatusError as e:
    log.error({
        "status_code": e.status_code,
        "error_type": e.error.type,
        "message": e.error.message,
        "request_id": e.request_id  # Anthropic destek için
    })
```

## Common mistakes
- `except Exception` ile tüm hataları aynı şekilde yakalamak — 401 için retry yapmak faydasız.
- `request_id`'yi loglamayı unutmak — Anthropic destek talebinde zorunlu.

## References
- `skills/llm-anthropic-rate-limits`
- `skills/llm-anthropic-sdk-python`
