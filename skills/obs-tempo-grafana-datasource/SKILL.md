---
name: obs-tempo-grafana-datasource
description: Grafana’da Tempo datasource eklemek/düzeltmek, Explore’da trace bulamama sorununu gidermek veya logs↔traces korelasyonunu (traceID linkleri) çalışır hale getirmek gerektiğinde kullan. Datasource URL/auth/tenant header ve doğrulama adımlarına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Tempo datasource bağlantı bilgisi (URL, auth, gerekiyorsa tenant header)
- Trace arama/doğrulama adımı: service.name + zaman penceresi ile canary trace bulma
- Logs↔traces korelasyonu için minimum gereksinim (trace_id taşıma ve linkleme)

## Workflow
- Bağlantıyı netleştir:
  - Grafana’nın erişebildiği Tempo endpoint’i (network/ingress).
  - Auth/TLS ve gerekiyorsa tenant header (multi-tenancy).
- “Trace yok” teşhisi:
  - Zaman aralığı yanlış mı? (retention)
  - service.name doğru mu? (OTel resource)
  - Sampling yüzünden trace düşüyor mu?
  - Tenant mismatch var mı? (header)
- Explore doğrulaması:
  - Basit arama: tek servis + kısa aralık (30–60 dk).
  - Bulunan trace’i aç; span’lar geliyor mu?
- Logs↔Traces korelasyonu:
  - Log line veya structured field içinde trace_id var mı?
  - Grafana Loki datasource’da derived field ile Tempo’ya link var mı?
- Doğrulama:
  - Log satırından trace linkine tıkla → aynı trace açılıyor mu?

## References
- `skills/obs-loki-grafana-datasource`
- `skills/obs-tempo-sampling-strategy`
