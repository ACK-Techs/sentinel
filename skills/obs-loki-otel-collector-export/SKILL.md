---
name: obs-loki-otel-collector-export
description: OpenTelemetry Collector’dan Loki’ye log export etmek için pipeline kurmak veya “OTLP geliyor ama Loki’de görünmüyor” sorununu çözmek gerektiğinde kullan. Receiver/processor/exporter zinciri, attribute→label kararı ve tenant header gibi Loki’ye özgü noktaları kapsar.
---

## Purpose
Bu skill’in çıktısı:
- OTel Collector logs pipeline taslağı (receiver → processors → loki exporter)
- Loki label stratejisine uygun “hangi attribute label olacak?” kararı
- Doğrulama: canary log + Loki’de LogQL ile görünürlük kontrolü

## Workflow
- Girdiyi seç:
  - OTLP receiver mı (app/agent), filelog receiver mı, başka kaynak mı?
- Processor’lar:
  - `batch` ve gerekirse `memory_limiter` ile stabilizasyon.
  - Attribute normalizasyonu: `service.name`, `deployment.environment`, `k8s.namespace.name` gibi alanları standardize et.
- Loki exporter:
  - Loki endpoint (URL) ve auth/TLS (secret değerlerini yazma).
  - Tenant gerekiyorsa header akışını planla (X-Scope-OrgID).
- Attribute → label kararı:
  - Sadece routing için stabil alanlar label olsun (namespace/app/level).
  - `trace_id`, `request_id`, `user_id` gibi alanları label yapma.
- Doğrulama:
  - Collector loglarında export error var mı?
  - Loki’de `{app="..."} |= "canary"` ile görünür mü?

## Common mistakes
- “Her attribute label olsun”: Loki index’i şişer.
- Tenant header push var ama query tarafında yok (Grafana datasource).

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-label-strategy`
- `skills/obs-loki-multi-tenancy`
