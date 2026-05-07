---
name: k8s-net-calico-flannel
description: Calico ve Flannel arasında CNI seçimi yapmak, özellik/farkları anlamak veya “network policy / routing / performans için hangisi uygun?” sorusunu cevaplamak gerektiğinde kullan. Amaç: **CNI seçimini gerçek gereksinime göre yapmak**.
---

## Purpose
Bu skill’in çıktısı:
- Calico vs Flannel karar tablosu
- NetworkPolicy, routing, simplicity trade-off analizi
- Doğrulama: seçilen CNI’ın cluster hedefleriyle uyumlu olduğunun kanıtı

## Workflow
- Gereksinimi çıkar:
  - NetworkPolicy zorunlu mu? eBPF/advanced routing gerekiyor mu? yoksa sadelik mi önemli?
- Karşılaştır:
  - Flannel: basit overlay odaklı.
  - Calico: policy ve gelişmiş ağ özellikleri güçlü.
- Operasyon maliyeti:
  - Debug, upgrade, observability, performans etkisi.
- MicroK8s/yerel ortam:
  - Varsayılan addon davranışı ve geçiş riskini not et.
- Doğrulama:
  - Policy, service reachability ve node-to-node trafik hedefleri karşılanıyor mu?

## Common mistakes
- Policy ihtiyacı varken sadece “kolay” diye Flannel seçmek.
- CNI değişimini çalışan cluster’da hafife almak.

## References
- `skills/k8s-net-networkpolicy`
- `skills/microk8s-addons-dns-storage`
