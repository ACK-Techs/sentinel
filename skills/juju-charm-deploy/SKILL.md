---
name: juju-charm-deploy
description: "Juju ile charm dağıtmak, Charmhub'dan kanal ve revision seçmek, başlangıç config değerlerini enjekte etmek, unit sayısını belirlemek ve deploy sürecini izlemek gerektiğinde kullan."
---

## Purpose
`juju deploy` tek komutla charm indirir ve başlatır. Üretimde revision sabitlemek, her güncelleme döngüsünde davranış değişikliğini önler.

## Temel deploy
```bash
juju deploy prometheus-k8s --channel=latest/stable
juju deploy grafana-k8s --channel=latest/stable -n 1
```

## Revision sabitleme
```bash
juju deploy prometheus-k8s --revision=123 --channel=latest/stable
```

## Config enjeksiyonu
```bash
# İnline:
juju deploy grafana-k8s --config admin-password=mysecret

# YAML dosyasından:
juju deploy grafana-k8s --config grafana-config.yaml
```

## Kaynak kısıtlamaları
```bash
juju deploy my-charm --constraints "mem=2G cores=2"
```

## Deploy izleme
```bash
juju status --watch 2s
juju status grafana-k8s  # tek uygulama
```

## Yerel charm deploy (geliştirme)
```bash
charmcraft build
juju deploy ./prometheus-k8s_ubuntu-22.04-amd64.charm \
  --resource prometheus-image=prom/prometheus:v2.47.0
```

## Common mistakes
- `--channel` belirtmeden deploy etmek → `latest/stable` gelir; revision kontrolü kaybolur.
- Config deploy sonrası `juju config` ile değiştirilebilir; başlangıçta hatalı değer production'da uzun lifecycle sorununa dönüşür.
- Unit saysını `-n 2` ile belirleyip sonradan resource çakışması yaşamak.

## References
- `skills/juju-model-lifecycle`
- `skills/juju-upgrade-charm`
- `skills/juju-config-management`
- `skills/cos-bundle-overview`
