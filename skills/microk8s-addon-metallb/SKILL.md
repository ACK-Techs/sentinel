---
name: microk8s-addon-metallb
description: "MicroK8s'te LoadBalancer tipi Kubernetes servislerine IP atamak için MetalLB addon'unu kurmak, IP aralığı tanımlamak ya da mevcut IP havuzunu güncellemek gerektiğinde kullan."
---

## Purpose
Bulut sağlayıcısı olmayan bare-metal veya VM ortamında `type: LoadBalancer` servisleri `<pending>` durumunda kalır. MetalLB bu boşluğu kapatır.

## Kurulum
```bash
# Kurulum sırasında IP aralığı girilmesi istenir
microk8s enable metallb:10.64.140.43-10.64.140.49
# Veya CIDR notasyonu:
microk8s enable metallb:192.168.1.200/29
```

## IP aralığı güncelleme (post-install)
MetalLB v0.13+ CRD tabanlı yapılandırma kullanır:
```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
    - 192.168.1.200-192.168.1.210
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: l2adv
  namespace: metallb-system
```

## Doğrulama
```bash
microk8s kubectl get svc -A | grep LoadBalancer
# EXTERNAL-IP sütununda havuzdan bir IP görünmeli
microk8s kubectl describe ipaddresspool -n metallb-system
```

## Common mistakes
- Verilen IP aralığının mevcut ağda routable olmadığını kontrol etmemek — IP atanır ama ulaşılamaz.
- BGP modunu L2 mode kurulumunda ayarlamaya çalışmak; farklı ön koşullar gerektirir.
- `metallb-system` namespace'indeki speaker pod'larının `Running` olmadığını atlamak.

## References
- `skills/microk8s-addons-overview`
- `skills/k8s-net-metallb`
- `skills/cos-ingress-troubleshoot`
