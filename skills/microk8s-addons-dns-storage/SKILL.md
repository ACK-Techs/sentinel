---
name: microk8s-addons-dns-storage
description: COS Lite için zorunlu MicroK8s eklentilerini (dns, hostpath-storage, metallb) etkinleştirir ve rollout doğrular.
---

## Purpose
**dns**, **hostpath-storage** ve Traefik için **metallb** eklentilerini açıp COS Lite bundle’ının PVC ve LoadBalancer gereksinimlerini karşılamak.

## Rules
- Etkin eklentiler: `dns`, `hostpath-storage`, `metallb` — `microk8s status` ile kontrol edin.
- Komut sırası örneği (Ubuntu dokümantasyonu ile uyumlu):
  - `microk8s enable dns`
  - `microk8s enable hostpath-storage`
  - `IPADDR=$(ip -4 -j route get 2.2.2.2 | jq -r '.[] | .prefsrc')` ardından `microk8s enable metallb:$IPADDR-$IPADDR` (tek IP sandbox için yeterli).
- Rollout bekleme (tutorial): `hostpath-provisioner`, `coredns`, MetalLB `speaker` daemonset — `kubectl rollout status` ile **Ready** olana kadar bekleyin.
- Üretimde dayanıklı depolama için hostPath yerine [MicroCeph / Ceph](https://microk8s.io/docs/how-to-ceph) değerlendirin; `storage-small` overlay yalnızca **ilk** `cos-lite` deploy’unda uygulanır.
- DNS upstream varsayılanları `8.8.8.8` / `8.8.4.4`; gerekiyorsa [addon-dns](https://microk8s.io/docs/addon-dns) ile değiştirin.

## References
- `skills/microk8s-install-base`
- `skills/juju-bootstrap-microk8s`, `skills/juju-model-cos`
- [COS Lite on MicroK8s — Configure MicroK8s](https://documentation.ubuntu.com/observability/track-2/tutorial/installation/cos-lite-microk8s-sandbox/#configure-microk8s)
