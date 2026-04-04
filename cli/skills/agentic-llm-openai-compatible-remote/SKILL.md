---
name: agentic-llm-openai-compatible-remote
description: Uzak OpenAI uyumlu API ile base_url, api_key, model ve proxy kullanımını yapılandırırken kullan.
---

## Amaç

Uzak uç kuralları: **`base_url`** (sonunda `/v1` olup olmaması proje normalizasyonu), **`api_key`** (env tercih), **`model`**. Kurumsal **proxy** ve isteğe bağlı **organization** header (OpenAI dokümantasyonunda doğrula) destekleniyorsa dokümante edilir. Örnek **`curl`** ile sağlık kontrolü (secret’ı komut satırında açma; header env’den).

## Kapsam

### Dahil

- TLS, SNI, kurumsal CA güven deposu notları (proje kararı).
- Streaming SSE davranışı (`agentic-llm-streaming-events`).

### Hariç

- Azure OpenAI adlandırma varyantları (varsa ayrı alt belge veya “proje kararı”).

## Kurallar

- `LLM_PROVIDERS.md` ile env isimleri hizalı (`SENTINEL_OPENAI_BASE_URL`, `OPENAI_BASE_URL` önceliği `agentic-config-env-reference`’ta).
- Retry sınırlıdır (`agentic-llm-retries-timeouts`); 401’de retry yapma.
- Log’da Authorization header asla düz metin yazılmaz.

## Kontrol listesi

- [ ] Örnek istek minimum scope API key ile çalışıyor mu?
- [ ] Yanlış `base_url` için anlamlı hata mesajı var mı?
- [ ] Proxy env (`HTTP_PROXY`) test edildi mi (ortam gerekiyorsa)?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| 401 Unauthorized | Key / header | Key rotate, profil kontrolü |
| SSL verify failed | CA paketi | Kurumsal CA veya `SSL_CERT_FILE` (güvenli yol) |
| 502/503 | Üst yük | Backoff + kullanıcı bilgisi |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-config-env-reference/SKILL.md`
- `../agentic-llm-streaming-events/SKILL.md`
- `../agentic-llm-retries-timeouts/SKILL.md`
- `../agentic-secrets-handling/SKILL.md`
