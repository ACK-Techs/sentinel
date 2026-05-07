---
name: obs-loki-troubleshoot-ingest
description: “Loki’ye log gelmiyor” semptomunda ingestion zincirini (promtail/otel → loki push → ingester → storage) adım adım teşhis etmek için kullan. 400/429/out-of-order, tenant header mismatch ve label/selector hatalarını hızlı ayırır.
---

## Purpose
Bu skill’in çıktısı:
- Semptom → olası neden → doğrulama adımı şeklinde kısa bir teşhis akışı
- Minimum canary testi (push edip query ile görmek)
- En sık 3 kök neden: yanlış label set, tenant header, push hataları

## Workflow
- 0) “Hiç mi gelmiyor, yoksa ben mi sorgulayamadım?”
  - En geniş makul selector + kısa zaman aralığı ile dene (yanlış label/tenant olabilir).
- 1) Push client tarafı (promtail/collector/custom):
  - Client loglarında push error var mı? (429/4xx/timeout)
  - Timestamp drift var mı? (future/out-of-order)
- 2) Tenant header (varsa):
  - Push isteklerinde `X-Scope-OrgID` var mı?
  - Grafana/query tarafı aynı tenant’ı kullanıyor mu?
- 3) Label/selector doğrulaması:
  - Hedef label’lar gerçekten üretiliyor mu? (promtail pipeline stages)
  - Query’de `{app="..."}...` yazıyorsan `app` label’ı yoksa hep boş döner.
- 4) Loki tarafı:
  - Loki/ingester loglarında reject var mı? (too old, out-of-order, rate limit)
  - Storage erişim hatası var mı? (disk/object storage)
- 5) Canary (en hızlı kapanış):
  - Tek bir sabit label set’iyle küçük bir log line push et.
  - Aynı selector ile LogQL: `{app="canary"} |= "hello"` görünüyor mu?

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-push-api`
- `skills/obs-loki-multi-tenancy`
- `skills/obs-loki-promtail-config`
