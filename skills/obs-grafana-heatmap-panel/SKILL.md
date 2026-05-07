---
name: obs-grafana-heatmap-panel
description: Grafana heatmap panel ile histogram dağılımı ve latency band görselleştirmesini yaparken kullan. Kullanıcı “obs-grafana-heatmap-panel”, “obs grafana heatmap panel”, “grafana” gibi ifadelerle Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya troubleshooting istediğinde bu skill’e başvur.
---

## Purpose
Grafana heatmap panel ile histogram dağılımı ve latency band görselleştirmesini yaparken kullan

## Workflow
- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).
- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.
- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.
- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`
