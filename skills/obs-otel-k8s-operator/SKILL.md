---
name: obs-otel-k8s-operator
description: OpenTelemetry Kubernetes Operator ile CRD tabanlı collector ve uygulama enstrümantasyonu yönetmek (Instrumentation CR, Collector CR, rollout) veya “operator inject etmiyor / sidecar gelmedi / exporter yanlış” sorunlarını çözmek gerektiğinde kullan. Helm/manifest değil; **CR tabanlı lifecycle** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Operator modeliyle yönetilen hedef durum: hangi namespace’ler, hangi Instrumentation, hangi Collector
- CR örüntüsü: Instrumentation (env/propagator/exporter) + Collector (mode/replicas)
- Doğrulama: pod’da injection ve backend’de sinyal görünürlüğü kanıtı

## Workflow
- Yerleşimi seç:
  - Collector: agent mı (DaemonSet), gateway mi (Deployment)?
  - Enstrümantasyon: auto-instrument injection mı, manuel SDK mı?
- Instrumentation CR:
  - service.name/env/exporter endpoint’i; propagators.
  - Hangi workload’lara uygulanacak (selector/annotation stratejisi).
- Collector CR:
  - Receivers/processors/exporters pipeline; scaling ve resource limit.
- Rollout ve geri dönüş:
  - Injection değişimi uygulama restart gerektirir; bakım penceresi notu.
- Teşhis:
  - Operator log’ları; webhook/injector admission hataları; namespace label/annotation.
- Doğrulama:
  - Workload pod’unda env/sidecar/init değişiklikleri var mı?
  - Tempo/Loki/metrics backend’de service görünür mü?

## Common mistakes
- Yanlış selector/annotation: injection hiç tetiklenmez.
- Operator ile manuel enstrümantasyonu karıştırıp double-instrument yapmak.

## References
- `skills/obs-otel-sdk-auto-instrument`
- `skills/obs-otel-collector-pipeline`
