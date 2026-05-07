---
name: obs-tempo-trace-query
description: Tempo’da trace aramak için TraceQL yazmak veya Tempo HTTP API ile trace search/trace get çağrısı tasarlamak gerektiğinde kullan. “TraceQL örneği”, “trace’i nasıl bulurum?”, “hangi attribute ile filtrelenir?”, “boş sonuç” gibi sorgu odaklı problemlere odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Use-case’e uygun 1–3 adet TraceQL sorgusu (minimal ama işe yarar)
- Arama daraltma stratejisi: zaman penceresi + service + span attribute
- Sık hata modları: “hiç trace yok”, “çok trace”, “attribute yok” için teşhis adımı

## Workflow
- Önce hedefi belirle:
  - “Belirli bir request’i bul” mu, yoksa “yavaş istekleri tara” mı?
  - Hangi servis(ler) ve hangi zaman aralığı?
- Sorguyu daralt (çok geniş arama pahalıdır):
  - Servis adı / span adı gibi en stabil filtreyle başla.
  - Sonra attribute filtre ekle (örn. HTTP method/status/route gibi).
- TraceQL yaz:
  - Amaç: “span’ları bul” → sonra “trace’i aç” (tek trace id).
  - Eğer attribute yoksa: önce instrumentation/collector tarafında “hangi attr’lar geliyor?”u doğrula.
- API kullanıyorsan:
  - Search endpoint’in parametrelerini (zaman aralığı, limit) küçük tut; sayfalama/limit stratejisini yaz.
  - Trace get ile tek bir trace’i çekip doğrula.
- Boş sonuç teşhisi:
  - Zaman aralığı yanlış mı? (retention)
  - Servis adı yanlış mı? (resource/service.name)
  - Sampling yüzünden trace düşüyor mu?

## Common mistakes
- “Tüm cluster’da tüm zamanı ara”: aşırı maliyet ve genelde timeout.
- Instrumentation attribute’ları gelmiyorken TraceQL ile attribute filtrelemeye çalışmak.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
