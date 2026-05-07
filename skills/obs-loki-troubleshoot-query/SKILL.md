---
name: obs-loki-troubleshoot-query
description: Loki’de LogQL sorguları boş dönüyor, timeout oluyor veya beklenmedik hata veriyorsa kullan. Semptomu (empty/slow/error) sınıflandırıp; selector/label, zaman aralığı, parse maliyeti, query-frontend/cache ve storage etkilerini adım adım izole eder.
---

## Purpose
Bu skill’in çıktısı:
- Semptom → olası neden → doğrulama adımı şeklinde kısa teşhis akışı
- Sorunu küçültmek için “minimal query” (selector + basit filter)
- Performans sorunlarında “en yüksek kaldıraç” önerisi (label, range, frontend/cache)

## Workflow
- 1) “Empty” mi, “Slow/timeout” mı, “Error” mı?
- 2) Minimal query ile küçült:
  - Sadece selector: `{namespace="...", app="..."}` (label yoksa sorgu hep boş)
  - Sonra basit filter: `|= "error"` (parse/regex’i en sona bırak)
- 3) Zaman aralığı kontrolü:
  - Çok geniş aralık + geniş selector → timeout.
  - Incident penceresi ile dene (30–120 dk).
- 4) Parse/regex maliyeti:
  - `| json`/regex ekleyince yavaşlıyorsa ingestion tarafında normalizasyon düşün.
- 5) Multi-tenancy (varsa):
  - Tenant header yanlışsa her şey boş görünür; query inspector ile header’ı doğrula.
- 6) Sistem bileşenleri:
  - Query-frontend var mı? splitting/caching düzgün mü?
  - Cache hit rate düşükse cache’in faydası olmayabilir.
  - Storage backend sorunu (object store latency) query’i vurabilir.
- 7) Doğrulama:
  - Aynı sorguyu adım adım büyüt: selector → filter → parse → aggregation.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-query-logql`
- `skills/obs-loki-query-frontend`
- `skills/obs-loki-multi-tenancy`
