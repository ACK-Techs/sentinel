---
name: k8s-storage-backup-velero
description: Kubernetes kaynakları ve persistent volume verisini Velero ile yedeklemek, schedule kurmak veya disaster recovery doğrulamak gerektiğinde kullan. Amaç: **backup’u restore ile birlikte düşünmektir**.
---

## Purpose
Bu skill’in çıktısı:
- Velero ile kaynak + volume backup akışı
- Schedule ve retention kararı
- Doğrulama: test restore ile gerçekten geri dönülebilirlik kanıtı

## Workflow
- Kapsamı belirle:
  - Sadece manifest mi, PV data da mı?
- Backend ve plugin:
  - Object storage ve snapshot plugin gereksinimi.
- Yedekleme planı:
  - Full vs scheduled, namespace bazlı mı cluster bazlı mı?
- Restore planı:
  - Aynı cluster mı, başka cluster mı?
- Doğrulama:
  - Deneme restore yap; sadece backup success mesajına güvenme.

## Common mistakes
- Backup alıp restore tatbikatı yapmamak.
- App-consistency gereksinimini ihmal etmek.

## References
- `skills/k8s-storage-volume-snapshot`
- `skills/docs-runbook-template`
