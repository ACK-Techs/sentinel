---
name: cos-deploy-catalogue
description: "Juju ile catalogue-k8s charm'ını COS modeline dağıtmak, Grafana ve diğer bileşenlerin URL'lerini merkezi bir serviste toplamak ve ekip içi servis keşfini sağlamak gerektiğinde kullan."
---

## Purpose
`catalogue-k8s`, COS bileşenlerinin ingress URL'lerini listeleyen basit bir web kataloğu sunar. Ekip üyelerinin Grafana, Prometheus, Alertmanager adreslerini sürekli sormadan bulabileceği tek nokta.

## Deploy
```bash
juju switch cos
juju deploy catalogue-k8s --channel=latest/stable
```

## Relation'lar
```bash
# Grafana servis girişi:
juju integrate catalogue-k8s:catalogue grafana-k8s:catalogue

# Alertmanager servis girişi:
juju integrate catalogue-k8s:catalogue alertmanager-k8s:catalogue

# Prometheus:
juju integrate catalogue-k8s:catalogue prometheus-k8s:catalogue

# Ingress:
juju integrate catalogue-k8s:ingress traefik-k8s:ingress-per-unit
```

## URL alma
```bash
juju run traefik-k8s/0 show-proxied-endpoints --format=json | jq '.result'
# Çıktıda catalogue URL dahil tüm servisler listelenir
```

## Catalogue web arayüzü
Catalogue URL'sine tarayıcıdan git: Tüm COS bileşenlerinin tıklanabilir linklerini gösterir.

## Common mistakes
- Traefik relation eklemeden catalogue'un external URL almayacağını unutmak — ClusterIP dahilinde kalır.
- Catalogue silince sadece URL dizininin kaybolacağını, Grafana/Prometheus'un etkilenmeyeceğini bilmemek.

## References
- `skills/cos-bundle-overview`
- `skills/cos-ingress-troubleshoot`
- `skills/juju-relation-add-remove`
