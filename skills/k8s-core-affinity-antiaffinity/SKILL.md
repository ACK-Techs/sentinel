---
name: k8s-core-affinity-antiaffinity
description: Pod yerleşimini node/pod affinity/anti-affinity ve topologySpreadConstraints ile kontrol etmek veya “pod’lar aynı node’a yığılıyor / zone dağılımı bozuk” sorunlarını çözmek gerektiğinde kullan. Odak: **yüksek erişilebilirlik yerleşimi** ve scheduler davranışıdır.
---

## Purpose
Bu skill’in çıktısı:
- Yerleşim hedefi: zone/hostname dağılımı, colocation/anti-colocation gerekçesi
- `required` vs `preferred` kararları ve scheduler başarısızlık risk analizi
- Doğrulama: node/zone dağılımının `kubectl` ile kanıtı

## Workflow
- Yerleşim hedefini yaz:
  - “Aynı node’a gelmesin” mi? “Aynı zone’da kalsın” mı? “İş yükü yakın olsun” mu?
- Affinity türü seç:
  - Node affinity: donanım/zone/label bazlı.
  - Pod anti-affinity: aynı app replica’larını dağıtmak için.
  - Topology spread: dengeli dağılım (modern tercih).
- Required vs preferred:
  - Required: hard kural; kapasite yetmezse Pending.
  - Preferred: yumuşak kural; kapasite yoksa toleranslı.
- Taints/tolerations etkileşimi:
  - Node kısıtlarını iki kere kilitleme (toleration + required affinity).
- Doğrulama:
  - Pod’ların node/zone dağılımını listele; skew beklendiği gibi mi?
  - Pending varsa scheduler event’inden “neden”i çıkar.

## Common mistakes
- Hard anti-affinity + az node: pod’lar Pending kalır.
- Topology key yanlış: spread çalışmıyor gibi görünür.

## References
- `skills/k8s-core-taints-tolerations`
- `skills/k8s-scale-node-affinity-spread`
