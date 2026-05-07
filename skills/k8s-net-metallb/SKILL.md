---
name: k8s-net-metallb
description: "Bare-metal veya MicroK8s ortamında `LoadBalancer` servislerine dış IP vermek için MetalLB kurmak, IP pool tasarlamak veya “EXTERNAL-IP pending” sorununu çözmek gerektiğinde kullan. Amaç: **LB IP atamasını yerel ağ gerçeklerine göre kurmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- IPAddressPool/L2Advertisement veya BGP yönüyle MetalLB tasarımı
- Uygun IP aralığı seçimi ve çakışma önleme
- Doğrulama: service EXTERNAL-IP alıyor mu, ağdan erişiliyor mu?

## Workflow
- Ağ bağlamını sabitle:
  - L2 mi, BGP mi? aynı subnet’te hangi IP’ler boş?
- Pool tasarla:
  - DHCP aralığıyla çakışmayan, reserve edilmiş IP bloğu seç.
- Advertise et:
  - L2 için announcement, BGP için peer bilgisi.
- Service testi:
  - `type: LoadBalancer` service gerçekten IP alıyor mu?
- Sorun giderme:
  - Pending ise controller/speaker çalışıyor mu?
  - ARP/BGP görünürlüğü var mı?
- Doğrulama:
  - Aynı ağdan service IP’ye ulaş.

## Common mistakes
- DHCP ile çakışan pool: IP savaşı çıkar.
- MetalLB kurup `LoadBalancer` service’i test etmemek.

## References
- `skills/microk8s-install-base`
- `skills/k8s-net-service-types`
