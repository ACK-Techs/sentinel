---
name: cos-ha-topology
description: "COS bileşenlerini yüksek erişilebilir (HA) topolojide çalıştırmak için replica sayısını, alert deduplication'ı ve storage HA yapılandırmasını uygulamak gerektiğinde kullan."
---

## Purpose
COS Lite varsayılan olarak tek replica ile gelir. Üretim için Prometheus, Loki ve Alertmanager'ın HA modunda çalışması gerekir.

## Prometheus HA
```bash
juju add-unit prometheus-k8s  # ikinci unit ekle
# Veya deploy sırasında:
juju deploy prometheus-k8s -n 2
```
İki Prometheus aynı target'ları scrape eder → Thanos veya `prometheus-remote-write` ile deduplication gerekir.

## Alertmanager HA
```bash
juju add-unit alertmanager-k8s  # en az 3 unit önerilir
```
Alertmanager birimler arası gossip ile duplicate alert'leri suppress eder (mesh cluster).

## Loki HA
Loki HA için `loki-k8s` charm'ında component mode yapılandırması gerekir:
```bash
juju config loki-k8s target=all  # tek binary, test
# Üretim: ayrı ingester/querier/distributor deployment (microservices mode)
```
Ingester için S3/GCS backend zorunludur.

## Grafana HA
```bash
juju add-unit grafana-k8s -n 2
# Shared SQLite yerine external PostgreSQL gerekir üretimde
```

## Anti-affinity (pod dağılımı)
Charm'ların aynı node'a yığılmaması için Juju constraints:
```bash
juju deploy prometheus-k8s -n 2 --constraints "spaces=data"
```

## Common mistakes
- 2 Alertmanager unit ile gossip kurmadan duplicate alert gönderilmesini beklemek.
- Prometheus HA'da aynı metriklerin iki kez scrape edildiğini hesaba katmadan storage boyutu planlamak.
- Grafana'da session affinity olmadan birden fazla replica çalıştırmak — login state kaybolur.

## References
- `skills/cos-bundle-overview`
- `skills/cos-resource-sizing`
- `skills/juju-charm-deploy`
