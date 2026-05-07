---
name: obs-tempo-storage-backend
description: Tempo depolama backend seçimi (local, S3, GCS) ve parça yönetimini yapılandırırken kullan. Kullanıcı “obs-tempo-storage-backend”, “obs tempo storage backend”, “tempo” gibi ifadelerle Prometheus/Loki/Tempo/Grafana/Alertmanager/OTel yapılandırması, sorgu, kural yazımı veya troubleshooting istediğinde bu skill’e başvur.
---

## Purpose
Tempo depolama backend seçimi (local, S3, GCS) ve parça yönetimini yapılandırırken kullan

## Workflow
- Hedef bileşeni ve çalışma modunu belirle (COS/Juju charm vs bare vs k8s-operator).
- İstenen çıktıyı seç: YAML config/manifest, API çağrısı örneği, PromQL/LogQL/TraceQL, kural dosyası, veya checklist.
- Güvenlik/izolasyon: secret (token, kubeconfig) sızdırma; header/auth bilgilerini maskele.
- Doğrulama adımı ekle: ilgili API endpoint/health, örnek sorgu, veya “beklenen sinyal” kontrolü.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
