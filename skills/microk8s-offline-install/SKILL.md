---
name: microk8s-offline-install
description: "İnternet erişimi olmayan (air-gap) ortamda MicroK8s kurmak, gerekli snap dosyalarını ve container image'larını önceden hazırlamak ve offline cluster başlatmak gerektiğinde kullan."
---

## Purpose
Üretim ortamları çoğunlukla egress kısıtlamasına sahiptir. MicroK8s'in tüm bağımlılıkları olan bir makineden hazırlanarak kapalı ağa taşınması gerekir.

## Adımlar

### 1. İnternet erişimli makinede hazırlık
```bash
# Snap offline kurulum için gerekli dosyaları indir
snap download microk8s --channel=1.30/stable
# İki dosya üretir: microk8s_<rev>.snap ve microk8s_<rev>.assert
```

### 2. Air-gap makinesine aktar
```bash
scp microk8s_*.snap microk8s_*.assert user@airgap-host:~/
```

### 3. Air-gap makinesinde kurulum
```bash
sudo snap ack microk8s_<rev>.assert
sudo snap install microk8s_<rev>.snap --classic
```

### 4. Container image'larının preload edilmesi
```bash
# İnternet erişimli makinede image'ları kaydet
docker pull k8s.gcr.io/pause:3.9
docker save k8s.gcr.io/pause:3.9 | gzip > pause.tar.gz

# Air-gap makinesinde içe aktar
microk8s ctr images import pause.tar.gz
```

### 5. Registry mirror yapılandırması
Air-gap ortamda yerel registry'yi mirror olarak tanımla:
```toml
# /var/snap/microk8s/current/args/certs.d/docker.io/hosts.toml
server = "https://my-internal-registry.corp"
[host."https://my-internal-registry.corp"]
  capabilities = ["pull", "resolve"]
```

## Common mistakes
- Yalnızca snap'i taşıyıp temel image'ları (pause, coredns, cni) unutmak.
- DNS pod'un başlamamasını image eksikliğine bağlamayıp cluster ayarını kurcalamak.

## References
- `skills/microk8s-install-snap`
- `skills/microk8s-addon-registry`
- `skills/microk8s-container-runtime`
