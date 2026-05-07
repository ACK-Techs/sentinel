---
name: obs-grafana-backup-restore
description: Grafana dashboard/datasource backup ve geri yükleme prosedürünü uygularken kullan. Kullanıcı “obs-grafana-backup-restore”, “obs grafana backup restore”, “grafana” gibi ifadelerle Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya troubleshooting istediğinde bu skill’e başvur.
---

## Purpose
Grafana dashboard/datasource backup ve geri yükleme prosedürünü uygularken kullan

## Workflow
- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).
- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.
- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.
- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`
