---
name: k8s-core-taints-tolerations
description: "Node’ları özel iş yüklerine ayırmak için taint/toleration tasarlamak veya “pod pending kalıyor / yanlış node’a gidiyor” sorunlarını çözmek gerektiğinde kullan. Amaç: **yerleşim kuralını açıkça kısıtlamak**, affinity ile karıştırmamaktır."
---

## Purpose
Bu skill’in çıktısı:
- Taint anahtarı/değeri/efekti ve gerekli toleration seti
- “Dışlama” mı, “tercih” mi kararının netleşmesi
- Doğrulama: scheduler event’leri ve node yerleşimi ile kanıt

## Workflow
- Hedefi netleştir:
  - Node havuzu gerçekten ayrılmalı mı? (GPU, infra, batch, regulated workload)
  - Sorun “yasaklamak” mı, yoksa sadece “tercih etmek” mi?
- Taint tasarla:
  - `NoSchedule`, `PreferNoSchedule`, `NoExecute` farkını kullanım senaryosuna göre seç.
  - Anahtarları ekip standardına göre isimlendir (`dedicated=infra`, `gpu=true` gibi).
- Toleration yaz:
  - Sadece gerekli workload’lara ekle; tüm namespace’e kopyalama.
  - `NoExecute` kullanıyorsan `tolerationSeconds` gerekip gerekmediğini not et.
- Affinity ile sınırı çiz:
  - Toleration pod’a “girebilir” hakkı verir; node seçimini garanti etmez. Gerekirse node affinity ekle.
- Doğrulama:
  - `kubectl describe pod` event’lerinde scheduler nedeni.
  - Pod gerçekten beklenen node havuzuna mı gitti?

## Common mistakes
- Toleration verip affinity eklememek: pod “her yere” gidebilir.
- `NoExecute` etkisini anlamadan kullanmak: çalışan pod’lar da atılabilir.

## References
- `skills/k8s-core-affinity-antiaffinity`
- `skills/k8s-scale-node-affinity-spread`
