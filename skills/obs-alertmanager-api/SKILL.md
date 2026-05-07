---
name: obs-alertmanager-api
description: Alertmanager v2 API ile alert listeleme ve silence CRUD yaparken kullan. Kullanıcı “obs-alertmanager-api”, “obs alertmanager api”, “alertmanager” gibi ifadelerle Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya troubleshooting istediğinde bu skill’e başvur.
---

## Purpose
Alertmanager v2 API ile alert listeleme ve silence CRUD yaparken kullan

## Workflow
- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).
- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.
- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.
- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
