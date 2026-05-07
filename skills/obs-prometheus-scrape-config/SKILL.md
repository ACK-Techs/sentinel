---
name: obs-prometheus-scrape-config
description: Prometheus için yeni bir scrape job tanımlamak veya mevcut job’ı düzeltmek gerektiğinde kullan. Özellikle “scrape_configs”, “static/file SD”, “kubernetes_sd_configs”, “relabel_configs”, “scrape_interval/timeout”, “targets up değil” gibi durumlarda doğru hedef seçimi ve relabel stratejisi üretmek için.
---

## Purpose
Bu skill’in çıktısı, **Prometheus’un gerçekten scrape edeceği hedef setini** (SD + filtre + relabel) netleştiren ve yanlış hedef/kardinalite riskini azaltan bir **scrape konfigürasyonu** üretmektir:
- Bare Prometheus için `scrape_configs` YAML snippet’i (job_name + discovery + relabel + auth/TLS)
- Operator kullanılıyorsa: `ServiceMonitor` / `PodMonitor` (selector/namespaceSelector + endpoints + relabelings)

## Workflow
- Önce bağlamı sabitle:
  - Prometheus dağıtımı: **bare** mi, COS/Juju `prometheus-k8s` mı, **Prometheus Operator** mı?
  - Hedef tipi: **node/service/pod** mı? Endpoint: `metrics_path`, port, scheme.
- Discovery seç (yalnız birini seçmeye zorlanma; ama gerekçesini yaz):
  - **Static**: az sayıda sabit hedef için `static_configs`.
  - **File SD**: otomasyon dışarıdan üretiyorsa `file_sd_configs` (yenileme periyodu + dosya formatı).
  - **Kubernetes SD**: label/annotation tabanlı dinamik keşif (`kubernetes_sd_configs` + `relabel_configs`).
  - **Operator**: aynı amaç için `ServiceMonitor/PodMonitor` tercih et (k8s-native lifecycle).
- Filtre ve relabel’i “ne için” kurgula:
  - Keşiften sonra **sadece istenen hedefleri bırak** (`keep/drop`).
  - Label’ları minimal tut: `pod`, `container`, `path`, `query` gibi **kardinalite patlatacak** label’ları “default ekleme”.
  - `instance` tutarlılığı: IP:port mu, DNS mi? (Grafana drilldown için).
- Zamanlama ve hata modu:
  - `scrape_interval` ve `scrape_timeout` oranını koru (timeout < interval).
  - Yük/limit: çok sık scrape + çok hedef → Prometheus CPU/TSDB büyümesi (bu skill sadece scrape tarafını yazar; kapasite için ayrı skill’e git).
- Güvenlik:
  - Basic auth / bearer token / mTLS kullanıyorsan **secret değerlerini yazma**; placeholder kullan ve nereden geleceğini belirt.
- Doğrulama adımları (en az birini yaz):
  - Hedef “UP” mı: `up{job="<job_name>"}`
  - Hedef sayısı beklenen mi: `count(up{job="<job_name>"})`
  - Relabel filtresi çalışıyor mu: `scrape_samples_scraped{job="<job_name>"}`

## Anti-patterns
- “Her şeyi scrape et”: tüm pod’ları/servisleri keşfedip sadece Grafana’da filtrelemeye bırakma.
- Her şeye label eklemek: request path, user id, dynamic hostname gibi alanları label’a dönüştürme.
- `scrape_timeout`’ı interval’e eşitlemek: Prometheus scheduler ve target starvation yaratır.

## References
- `skills/cos-deploy-prometheus`
- `skills/cos-relation-prometheus-grafana`
- `cli/skills/agentic-troubleshoot-prometheus`
