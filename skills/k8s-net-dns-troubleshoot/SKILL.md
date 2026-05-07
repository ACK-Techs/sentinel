---
name: k8s-net-dns-troubleshoot
description: "Kubernetes içinde DNS çözümleme sorunlarını (NXDOMAIN, timeout, yanlış search path, `ndots` etkisi) teşhis etmek gerektiğinde kullan. Amaç: **sorunu pod config, CoreDNS veya ağ kısıtı arasında ayırmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- DNS hata tipine göre teşhis sırası
- Pod `resolv.conf`, CoreDNS ve NetworkPolicy ayırıcı kontrol listesi
- Doğrulama: test sorgularıyla sorunun kapandığını kanıtlama

## Workflow
- Hata tipini ayır:
  - NXDOMAIN mi, timeout mu, yanlış IP mi?
- Pod içini kontrol et:
  - `resolv.conf`, search domain, `ndots` ayarı beklenen mi?
- İsim türünü ayır:
  - Kısa servis adı mı, FQDN mi, dış domain mi?
- Altyapı kontrolleri:
  - CoreDNS pod’ları sağlıklı mı?
  - DNS egress NetworkPolicy ile kesilmiş olabilir mi?
- Doğrulama:
  - Pod’dan hem cluster service adı hem dış domain çöz.

## Common mistakes
- `ndots` yüzünden dış domain sorgularının önce cluster içinde denenmesini gözden kaçırmak.
- DNS timeout’u uygulama bug’ı sanmak.

## References
- `skills/k8s-net-coredns`
- `skills/k8s-net-networkpolicy`
