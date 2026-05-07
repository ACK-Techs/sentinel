---
name: obs-prometheus-scrape-config
description: Prometheus scrape job’ları, scrape interval/timeout ve hedef keşfi (static/file/kubernetes SD) kurarken kullan. Kullanıcı “scrape config”, “job”, “targets”, “service discovery”, “ServiceMonitor/PodMonitor”, “PrometheusConfig” gibi ifadelerle metrik toplama hedeflerini ayarlamak istediğinde bu skill’e başvur.
---

## Purpose
Prometheus’un hangi hedeflerden, hangi aralıklarla metrik toplayacağını doğru ve düşük kardinalite riskiyle tanımlamak.

## Workflow
- İstenen ortamı netleştir: bare Prometheus mu, COS/Juju `prometheus-k8s` mı, yoksa Prometheus Operator CRD (ServiceMonitor/PodMonitor) mı?
- Hedef tipini seç: `static_configs`, `file_sd_configs`, `kubernetes_sd_configs` (gerekirse relabel ile filtrele).
- Scrape parametrelerini belirle: `scrape_interval`, `scrape_timeout`, `metrics_path`, `scheme`, auth/TLS.
- Label/relabel risklerini kontrol et: gereksiz label ekleme (kardinalite) ve `instance`/`job` tutarlılığı.
- Çıktıyı üret:
  - Bare Prometheus için `scrape_configs` YAML snippet’i, veya
  - Operator için `ServiceMonitor` / `PodMonitor` manifest’i (ve gerekli namespace/selector).

## References
- `skills/cos-deploy-prometheus`
- `skills/cos-relation-prometheus-grafana`
- `cli/skills/agentic-troubleshoot-prometheus`
