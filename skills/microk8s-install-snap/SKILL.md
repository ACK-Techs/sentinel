---
name: microk8s-install-snap
description: "MicroK8s'i snap ile yüklemek, Kubernetes kanalını seçmek (1.29/stable, 1.30/stable vb.), kullanıcıyı microk8s grubuna eklemek ve temel hazırlığı tamamlamak gerektiğinde kullan. microk8s-install-base ile çakışmaz; bu skill snap spesifik kanal ve grup yönetimine odaklanır."
---

## Purpose
Yeni bir Ubuntu/Debian makinesinde MicroK8s'i doğru kanal ve izin yapılandırmasıyla kurmak; sonraki Juju/COS adımları için zemin hazırlamak.

## Workflow

### Kurulum
```bash
sudo snap install microk8s --classic --channel=1.30/stable
```
Kanal seçimi: üretim ortamında sabit minor versiyon (`1.30/stable`), deney için `latest/edge`.

### Kullanıcı grubu
```bash
sudo usermod -aG microk8s $USER
mkdir -p ~/.kube
sudo chown -R $USER ~/.kube
newgrp microk8s   # veya oturumu yenile
```
`microk8s kubectl` komutları `sudo` gerektirmez hâle gelir.

### Durum doğrulama
```bash
microk8s status --wait-ready
microk8s kubectl get nodes
```

### Temel addon'lar (DNS zorunlu)
```bash
microk8s enable dns
microk8s enable hostpath-storage
```

### Firewall
```bash
sudo ufw allow in on cni0
sudo ufw allow out on cni0
```

## Common mistakes
- `--classic` flag'ini unutmak — MicroK8s strict snap ile çalışmaz.
- Kullanıcıyı gruba ekledikten sonra oturum yenilemeden `permission denied` hatası almak.
- Kanal belirtmeden kurmak → `latest/stable` gelebilir; sürüm kontrolü kaybolur.

## References
- `skills/microk8s-addons-overview`
- `skills/microk8s-upgrade`
- `skills/k8s-scale-microk8s-node-add`
