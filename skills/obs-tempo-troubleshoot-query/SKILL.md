---
name: obs-tempo-troubleshoot-query
description: Tempo’da trace araması boş dönüyor, TraceQL timeout oluyor veya Grafana Explore trace açamıyorsa kullan. Semptomu (empty/slow/error) sınıflandırıp; zaman penceresi, service.name, tenant header, sampling ve datasource bağlantısını adım adım izole eder.
---

## Purpose
Bu skill’in çıktısı:
- Minimal arama stratejisi (tek servis + kısa zaman penceresi) ve büyütme adımları
- En sık boş sonuç nedenleri için kontrol listesi (sampling, service.name, retention, tenant)
- Timeout için daraltma önerileri (query scope, attribute filtreleri)

## Workflow
- 1) Semptomu sınıflandır:
  - Empty mi, slow/timeout mı, error mı?
- 2) Minimal arama ile başla:
  - Tek `service.name` + son 30–60 dk.
  - Sonra attribute filtreleri ekle (status/route), en sona regex.
- 3) Boş sonuç teşhisi:
  - Service adı yanlış mı? (resource attribute)
  - Sampling yüzünden trace düşüyor mu?
  - Retention dışında mı arıyorsun?
  - Tenant mismatch var mı? (multi-tenancy)
- 4) Timeout teşhisi:
  - Aramayı daralt (zaman, servis, limit).
  - Advanced TraceQL’e geçmeden önce scope’u küçült.
- 5) Grafana datasource:
  - Grafana’dan Tempo endpoint’e erişim var mı? auth/tenant header doğru mu?
- 6) Doğrulama:
  - Bulduğun bir trace’i aç; span’lar eksik/boş ise ingest tarafına dön.

## References
- `skills/obs-tempo-trace-query`
- `skills/obs-tempo-grafana-datasource`
- `skills/obs-tempo-multi-tenancy`
