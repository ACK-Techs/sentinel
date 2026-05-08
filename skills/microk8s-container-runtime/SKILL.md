---
name: microk8s-container-runtime
description: "MicroK8s'in containerd yapılandırmasını özelleştirmek, private registry mirror tanımlamak, insecure registry eklemek ya da containerd snapshot/storage ayarlarını değiştirmek gerektiğinde kullan."
---

## Purpose
MicroK8s, containerd'yi snap içinde paketlenmiş şekilde çalıştırır. Standart `/etc/containerd/config.toml` yerine snap'e özel konumda yapılandırma değişikliği yapılması gerekir.

## Yapılandırma konumları
```
/var/snap/microk8s/current/args/containerd          # containerd başlangıç argümanları
/var/snap/microk8s/current/args/containerd-env      # ortam değişkenleri
/var/snap/microk8s/current/args/certs.d/            # registry mirror ve TLS ayarları
```

## Private registry mirror ekleme
```bash
# Örnek: private-registry.corp:5000 için
sudo mkdir -p /var/snap/microk8s/current/args/certs.d/private-registry.corp:5000
sudo tee /var/snap/microk8s/current/args/certs.d/private-registry.corp:5000/hosts.toml << 'EOF'
server = "https://private-registry.corp:5000"
[host."https://private-registry.corp:5000"]
  capabilities = ["pull", "resolve"]
  ca = "/etc/ssl/certs/registry-ca.crt"
EOF
sudo snap restart microk8s
```

## Insecure registry
```toml
# /var/snap/microk8s/current/args/certs.d/myregistry:5000/hosts.toml
server = "http://myregistry:5000"
[host."http://myregistry:5000"]
  capabilities = ["pull", "resolve"]
  skip_verify = true
```

## Containerd logları
```bash
sudo journalctl -u snap.microk8s.daemon-containerd -f
microk8s ctr version  # containerd bağlantı testi
microk8s ctr images list  # yüklü image'lar
```

## Common mistakes
- `/etc/containerd/config.toml` dosyasını düzenlemek — MicroK8s bu dosyayı kullanmaz.
- Yapılandırmayı değiştirdikten sonra MicroK8s'i yeniden başlatmamak.

## References
- `skills/microk8s-addon-registry`
- `skills/microk8s-offline-install`
- `skills/microk8s-inspect`
