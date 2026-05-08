---
name: microk8s-ip-change-recovery
description: "MicroK8s node'unun IP adresi değiştiğinde (DHCP yenileme, VM taşıma) API server sertifikası geçersiz kaldığında, kubeconfig bağlantısı koptuğunda veya Juju controller drifti oluştuğunda kurtarma prosedürünü uygulamak için kullan."
---

## Purpose
IP değişikliği MicroK8s'te en sık yaşanan kalıcı arızadır. API server TLS sertifikası eski IP'yi SAN olarak içerdiğinden yeni IP ile TLS handshake başarısız olur.

## Kurtarma adımları

### 1. Durumu tespit et
```bash
microk8s kubectl get nodes  # certificate error veya connection refused
microk8s inspect            # hata raporu oluşturur
```

### 2. API server sertifikasını yenile
```bash
# MicroK8s API server certs dosyasına yeni IP ekle
sudo bash -c 'echo "--service-cluster-ip-range=10.152.183.0/24" >> /var/snap/microk8s/current/args/kube-apiserver'
# Daha doğru yol: refresh-certs komutu (1.24+)
sudo microk8s refresh-certs --cert front-proxy-client.crt
```

### 3. Kubeconfig güncelle
```bash
microk8s config > ~/.kube/config
# veya uzak erişim için:
microk8s config | sed "s/127.0.0.1/<yeni-ip>/g" > ~/.kube/config
```

### 4. MicroK8s yeniden başlat
```bash
sudo snap restart microk8s
microk8s status --wait-ready
```

### 5. Juju drift onarımı
IP değişince Juju controller'ın endpoint kaydı güncellenmez:
```bash
juju update-credential microk8s
# veya controller'ı yeniden bootstrap etmek gerekebilir
```

## Önlem
- Statik IP veya DHCP reservation ile IP'yi sabitle.
- Hostonly network yerine bridged network.

## Common mistakes
- `microk8s stop && microk8s start` ile sertifikayı yenilemeye çalışmak — yetersiz.
- Eski kubeconfig'i kullanmaya devam edip her komutta `x509` hatası almak.

## References
- `skills/microk8s-kubeconfig-export`
- `skills/microk8s-inspect`
- `skills/microk8s-ha-cluster`
