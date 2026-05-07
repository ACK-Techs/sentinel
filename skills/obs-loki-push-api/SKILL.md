---
name: obs-loki-push-api
description: Loki’ye HTTP ile log göndermek için `POST /loki/api/v1/push` payload’ı hazırlamak, label string formatını doğru kurmak veya push sırasında 400/429/timeout hatalarını gidermek gerektiğinde kullan.
---

## Purpose
Bu skill’in çıktısı:
- Minimal `push` JSON örneği (streams/labels/entries) ve `curl` isteği
- Timestamp formatı ve en sık hata modları için teşhis (out-of-order, too old, rate limit)
- Label set’i için guardrail: high-cardinality’den kaçınma

## Workflow
- Payload şemasını doğru kur:
  - `streams[]`: her stream = tek label set’i
  - `streams[].labels`: Prometheus label string biçimi (`{key="value",...}`)
  - `streams[].entries[]`: `ts` + `line`
- Timestamp kararı:
  - `ts` genelde RFC3339Nano/ISO benzeri; client tarafında tek standardı seç.
  - Saat drift’i varsa “future timestamp” / out-of-order hatası çıkar.
- Label set’i:
  - Routing için küçük bir set: `cluster/namespace/app/level` gibi.
  - `trace_id`, `request_id`, `path` gibi alanları label yapma; line içinde kalsın.
- Hata modları:
  - 400: labels string parse hatası, timestamp formatı, out-of-order.
  - 429: ingest rate limit / tenant limit (backoff + batch küçült).
  - Timeout: batch boyutu/stream sayısı çok büyük; parçala.
- Doğrulama:
  - Push sonrası aynı label selector ile LogQL sorgusu yap: `{app="..."} |= "canary"`

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-label-strategy`
