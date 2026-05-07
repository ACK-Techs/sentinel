---
name: obs-prometheus-backup-restore
description: TSDB snapshot alma ve geri yükleme prosedürünü uygularken kullan. Kullanıcı “obs-prometheus-backup-restore”, “obs prometheus backup restore”, “prometheus” gibi ifadelerle Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya troubleshooting istediğinde bu skill’e başvur.
---

## Purpose
TSDB snapshot alma ve geri yükleme prosedürünü uygularken kullan

## Workflow
- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).
- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.
- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.
- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.

## References
- `skills/cos-deploy-prometheus`
- `skills/cos-relation-prometheus-grafana`
- `cli/skills/agentic-troubleshoot-prometheus`
