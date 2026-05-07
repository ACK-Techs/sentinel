---
name: obs-gateway-deployment-k8s
description: Observability gateway’i Kubernetes Deployment olarak konuşlandırmak (resources, probes, HPA, config/secret, network policy) veya “gateway crashloop/ready olmuyor/latency yüksek” sorunlarını çözmek gerektiğinde kullan. Odak: **prod-ready deployment** ve doğrulama adımlarıdır.
---

## Purpose
Bu skill’in çıktısı:
- Gateway için Deployment iskeleti: env/config, secrets, ports, probes, resources
- Operasyon checklist’i: rollout/rollback, HPA sinyali, network policy
- Doğrulama: readiness + temel adapter çağrılarıyla “servis çalışıyor” kanıtı

## Workflow
- Konfig ve secret yönetimi:
  - Token doğrulama anahtarları, backend URL’leri, cache ayarları; secret’lar ayrı.
- Pod güvenilirliği:
  - `startupProbe` (ağ ısınması), `readinessProbe` (trafik), `livenessProbe` (process).
- Kaynaklar ve ölçek:
  - CPU/RAM requests/limits; concurrency ve timeout’a göre ayarla.
  - HPA: CPU + (opsiyonel) request latency/queue metriği.
- Network:
  - Backend’lere egress allowlist; status endpoint’leri internal kısıt.
- Rollout:
  - RollingUpdate ayarları; canary gerekiyorsa ayrı strateji.
- Doğrulama:
  - `/health` liveness OK.
  - `/api/v1/status` backend’leri doğru gösteriyor mu?
  - 1 PromQL + 1 LogQL + (varsa) 1 trace-by-id çağrısı 200 mü?

## Common mistakes
- Readiness’i backend dependency’ye bağlayıp outage’ta tüm pod’ları “not ready” yapmak: thundering herd.
- Secret’ları ConfigMap’e koymak: sızıntı riski.

## References
- `skills/k8s-core-pod-lifecycle`
- `skills/obs-gateway-health-status`
