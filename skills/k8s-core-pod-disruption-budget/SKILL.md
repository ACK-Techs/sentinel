---
name: k8s-core-pod-disruption-budget
description: Gönüllü kesintiler sırasında minimum pod sayısını korumak için PodDisruptionBudget tasarlamak veya drain/upgrade sırasında uygulamanın neden kesildiğini anlamak gerektiğinde kullan. Amaç: **bakım anında hizmet sürekliliği eşiğini netleştirmek**.
---

## Purpose
Bu skill’in çıktısı:
- `minAvailable` vs `maxUnavailable` kararı
- Replica sayısı ile PDB uyum kontrolü
- Doğrulama: drain/eviction sırasında beklenen davranış kanıtı

## Workflow
- Replica ve SLO’yu sabitle:
  - 1 replica ise PDB neyi gerçekten koruyabilir?
  - Kaç pod düşerse hizmet bozulur?
- PDB biçimini seç:
  - “En az N hazır kalsın” → `minAvailable`
  - “En fazla N düşebilir” → `maxUnavailable`
- Operasyonel etkiyi değerlendir:
  - Cluster upgrade, node drain, autoscaler scale-down PDB yüzünden bloklanır mı?
- Selector doğrula:
  - Yanlış label set’i PDB’yi boşa düşürür veya alakasız pod’ları kapsar.
- Doğrulama:
  - `kubectl drain --dry-run` düşün.
  - Eviction denemesinde “cannot evict pod” beklenen mi?

## Common mistakes
- 2 replica + `minAvailable: 2`: bakım imkansız hale gelir.
- PDB’yi istemsiz kesintilere karşı koruma sanmak: sadece voluntary disruption içindir.

## References
- `skills/k8s-core-deployment-strategy`
- `skills/k8s-scale-cluster-autoscaler`
