---
name: obs-prometheus-recording-rules
description: Sık sorgulanan metrikleri önceden hesaplayan recording rule yazarken kullan. Kullanıcı “obs-prometheus-recording-rules”, “obs prometheus recording rules”, “prometheus” gibi ifadelerle Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya troubleshooting istediğinde bu skill’e başvur.
---

## Purpose
Sık sorgulanan metrikleri önceden hesaplayan recording rule yazarken kullan

## Workflow
- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).
- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.
- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.
- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.

## References
- `skills/cos-deploy-prometheus`
- `skills/cos-relation-prometheus-grafana`
- `cli/skills/agentic-troubleshoot-prometheus`
