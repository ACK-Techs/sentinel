---
name: k8s-core-statefulset
description: StatefulSet ile sıralı pod yönetimi kurmak (stable identity, ordered rollout), headless Service ile stable DNS sağlamak veya “pod adı değişiyor/veri kayboluyor/leader election bozuluyor” gibi stateful workload problemlerini çözmek gerektiğinde kullan. Deployment değil; **stateful semantik** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- StatefulSet + headless Service tasarım iskeleti (identity, rollout, storage bağlama)
- Volume stratejisi: PVC template, storage class, resize/backup notları
- Doğrulama: stable DNS + pod ordinal + veri sürekliliği kanıtı

## Workflow
- Stateful ihtiyacı doğrula:
  - Stable network identity mi, stable storage mı, yoksa sadece “tek replica” mı?
- Headless Service:
  - Stable DNS için headless Service kur; client’lar bunu mu kullanacak, yoksa LB Service mi?
- StatefulSet parametreleri:
  - Pod management policy (OrderedReady vs Parallel) kararını yaz.
  - Update strategy: RollingUpdate partition ile kontrollü rollout (özellikle DB).
- Storage:
  - `volumeClaimTemplates` ile per-pod PVC; retention/cleanup davranışını not et.
  - Node affinity/storage zone kısıtlarını kontrol et (pod taşınması).
- Operasyon:
  - Scale down/up sırası ve data safety.
  - Backup/restore entegrasyonu (ayrı skill’lere bağla).
- Doğrulama:
  - Pod ordinal’lar stabil mi? DNS `pod-0.<svc>` çalışıyor mu?
  - Restart sonrası data aynı PVC’den geliyor mu?

## Common mistakes
- StatefulSet’i sadece “stable pod name” için kullanıp storage’ı düşünmemek: veri kaybı sürprizi.
- Headless Service olmadan client discovery kurgulamak: bağlantılar kırılganlaşır.

## References
- `skills/k8s-storage-pvc-pv`
