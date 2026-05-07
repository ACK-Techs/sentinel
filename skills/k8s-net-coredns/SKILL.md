---
name: k8s-net-coredns
description: "CoreDNS davranışını anlamak, plugin zinciri veya stub zone yapılandırmak ya da “cluster DNS yavaş/yanlış çözümlüyor” sorunlarını çözmek gerektiğinde kullan. Amaç: **DNS çözüm yolunu ve Corefile etkisini netleştirmektir**."
---

## Purpose
Bu skill’in çıktısı:
- CoreDNS rolü ve plugin zinciri okuması
- Stub/forward/custom domain yapılandırma yaklaşımı
- Doğrulama: pod içinden isim çözümlemesi ve CoreDNS health kanıtı

## Workflow
- Soruyu sınıflandır:
  - İç servis adı mı çözülmüyor, dış domain mi, özel stub zone mu?
- Corefile mantığını oku:
  - `kubernetes`, `forward`, `cache`, `loop`, `reload` gibi plugin’ler ne yapıyor?
- Özel yönlendirme:
  - Belirli domain’leri on-prem DNS’e veya özel resolver’a göndermek gerekiyorsa stub zone tasarla.
- Performans:
  - Cache ve upstream timeout davranışını dikkate al.
- Doğrulama:
  - Test pod’dan `nslookup/dig`.
  - CoreDNS log/metrics ve readiness durumu.

## Common mistakes
- CoreDNS sorunu sanıp aslında NetworkPolicy ile DNS’i kesmiş olmak.
- Corefile değiştirip rollout/validation yapmamak.

## References
- `skills/k8s-net-dns-troubleshoot`
- `skills/k8s-net-networkpolicy`
