---
name: agentic-llm-retries-timeouts
description: LLM HTTP çağrıları için retry sınıfı, exponential backoff ve idempotency uyarılarını tanımlarken kullan.
---

## Amaç

**Retry**: genelde **429**, seçili **5xx**, geçici **ağ kesintisi**; **401/403/400** için retry yok. **Exponential backoff** + jitter; **maksimum deneme** sabit. **Timeout katmanları**: connect vs read (stream’de read daha uzun). **İdempotency**: aynı istek tekrarı yanlışlıkla çift ücretlendirme yaratabilir; kullanıcıya “tekrar denendi” log’u (secret yok).

## Kapsam

### Dahil

- Stream yarıda kesilirse: kullanıcıya durum + yeniden deneme politikası.
- Global default timeout env (proje kararı, örn. `SENTINEL_HTTP_TIMEOUT_SEC`).

### Hariç

- Sınırsız retry (yasak).

## Kurallar

- Toplam bekleme süresi üst sınırı (örn. 60s) aşılmamalı.
- Retry sayısı log’da: `attempt`, `reason` (kod), `session_id`.
- Rate limit header’ları varsa (`Retry-After`) öncelik.

## Kontrol listesi

- [ ] Her retry edilebilir kod için test var mı?
- [ ] Sonsuz döngü önlemi (max attempts) kodda zorunlu mu?
- [ ] `agentic-cli-user-errors` mesajları retry sonrası net mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Sonsuz 429 | Anahtar/plan limiti | Kullanıcıyı bilgilendir, bekle |
| Read timeout | Büyük model | Timeout artır veya model değiştir |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-cli-user-errors/SKILL.md`
- `../agentic-llm-openai-compatible-remote/SKILL.md`
- `../agentic-secrets-handling/SKILL.md`
