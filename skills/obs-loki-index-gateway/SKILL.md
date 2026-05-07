---
name: obs-loki-index-gateway
description: Loki index gateway bileşenini ayrı node olarak konuşlandırırken kullan. Kullanıcı “obs-loki-index-gateway”, “obs loki index gateway”, “loki” gibi ifadelerle Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya troubleshooting istediğinde bu skill’e başvur.
---

## Purpose
Loki index gateway bileşenini ayrı node olarak konuşlandırırken kullan

## Workflow
- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).
- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.
- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.
- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.

## References
- `skills/cos-deploy-loki`
- `skills/cos-relation-loki-grafana`
- `cli/skills/agentic-troubleshoot-loki`
