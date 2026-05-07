---
name: obs-prometheus-multi-tenancy
description: Label tabanlı izolasyon ve tenant-aware sorgulama kurallarını uygularken kullan. Kullanıcı “obs-prometheus-multi-tenancy”, “obs prometheus multi tenancy”, “prometheus” gibi ifadelerle Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya troubleshooting istediğinde bu skill’e başvur.
---

## Purpose
Label tabanlı izolasyon ve tenant-aware sorgulama kurallarını uygularken kullan

## Workflow
- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).
- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.
- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.
- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.

## References
- `skills/cos-deploy-prometheus`
- `skills/cos-relation-prometheus-grafana`
- `cli/skills/agentic-troubleshoot-prometheus`
