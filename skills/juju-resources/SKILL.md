---
name: juju-resources
description: "Juju resource mekanizmasıyla charm'a ek dosya veya container image sağlamak, mevcut resource'u güncellemek ve özel image ile production charm çalıştırmak gerektiğinde kullan."
---

## Purpose
Juju resource'ları, charm ile birlikte dağıtılan ekler: binary, config dosyası veya OCI image. Özellikle charm'ın kullandığı container image'ı override etmek için kritiktir.

## Resource listeleme
```bash
juju resources prometheus-k8s
# NAME           REVISION  FINGERPRINT  SIZE  DESCRIPTION
# prometheus-image  5       sha256:...   45MB  Prometheus OCI image
```

## Deploy sırasında resource belirtme
```bash
juju deploy prometheus-k8s \
  --resource prometheus-image=prom/prometheus:v2.47.0
```

## Deploy sonrası güncelleme
```bash
# Yeni image ile:
juju attach-resource prometheus-k8s prometheus-image=prom/prometheus:v2.48.0

# Yerel dosya ile:
juju attach-resource mycharm myconfig=./config.yaml
```

## Charmhub'dan belirli revision:
```bash
juju deploy prometheus-k8s --resource prometheus-image=23
```

## Air-gap ortamında resource yönetimi
```bash
# Image'ı yerel registry'ye push et
docker tag prom/prometheus:v2.47.0 localhost:32000/prometheus:v2.47.0
docker push localhost:32000/prometheus:v2.47.0
# Deploy sırasında:
juju deploy prometheus-k8s --resource prometheus-image=localhost:32000/prometheus:v2.47.0
```

## Common mistakes
- Resource güncellemesinin yalnızca `upgrade-charm` ile değil `attach-resource` ile de yapılabileceğini bilmemek.
- Image tag yerine digest kullanmak production'da önerilir: `sha256:...` değişmez.
- Resource fingerprint doğrulaması olmadan güvenilmeyen kaynak kullanmak.

## References
- `skills/juju-charm-deploy`
- `skills/juju-upgrade-charm`
- `skills/microk8s-offline-install`
