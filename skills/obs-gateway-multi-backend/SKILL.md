---
name: obs-gateway-multi-backend
description: Gateway’e birden fazla backend eklemek (ör. iki Prometheus cluster, iki Loki tenant’ı) ve routing/failover kurallarını yazmak veya “hangi sorgu hangi backend’e gitsin?” karmaşasını çözmek gerektiğinde kullan. Odak: **backend seçimi + tutarlı sonuç**.
---

## Purpose
Bu skill’in çıktısı:
- Backend registry modeli: backend id, tür, tenant kapsamı, health bilgisi
- Routing kuralları: tenant/env/region/feature flag bazlı seçim + gerekçe
- Doğrulama: seçilen backend’in deterministik olması ve fallback’in kontrollü çalışması kanıtı

## Workflow
- Çoklu backend gerekçesini yaz:
  - Bölgesel ayrım mı, migration mı, DR mı, farklı retention mı?
- Routing anahtarını seç:
  - Tenant + env + region gibi stabil alanlar; query içeriğine göre routing’i minimum tut.
- Failover politikası:
  - Otomatik failover her zaman doğru değil (stale/yanlış veri riski).
  - Failover varsa: sadece read-only ve “degraded” işaretiyle.
- Sonuç tutarlılığı:
  - Aynı sorgu iki backend’de farklı isim/label döndürebilir; normalizasyon ihtiyacını yaz.
- Doğrulama:
  - Aynı tenant için aynı backend seçiliyor mu?
  - Primary down iken: beklenen davranış (fail fast vs controlled fallback) doğru mu?

## Common mistakes
- “Her zaman fallback” yaklaşımı: sessizce yanlış veriyle çalıştırır.
- Routing’i query string regex’ine bağlamak: kırılgan ve debug zor.

## References
- `skills/obs-gateway-health-status`
- `skills/obs-gateway-error-model`
