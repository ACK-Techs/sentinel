---
name: k8s-scale-pod-preemption
description: "Yüksek öncelikli iş yüklerinin node kaynaklarını düşük öncelikli pod'lardan geri almasını sağlamak için PriorityClass tanımlamak, preemption politikasını ayarlamak ya da bir pod'un beklenmedik şekilde tahliye edildiğini araştırmak gerektiğinde kullan."
---

## Purpose
Kubernetes preemption: cluster dolu olduğunda yüksek öncelikli pod'un scheduler tarafından kabul edilebilmesi için düşük öncelikli pod'ların tahliye edilmesi mekanizması. Doğru tasarlanmadığında kritik iş yükü açlık çekerken batch job'lar node'u tutar.

## Workflow

### PriorityClass tanımlama
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
preemptionPolicy: PreemptLowerPriority  # varsayılan
globalDefault: false
description: "Üretim kritik servisler için"
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: batch-low
value: 100
preemptionPolicy: Never  # tahliye etmez, beklemeyi tercih eder
globalDefault: false
```

### Pod'a öncelik atama
```yaml
spec:
  priorityClassName: high-priority
```

### Preemption akışı
1. Yüksek öncelikli pod `Pending` → scheduler yer açmak için düşük öncelikli kurban seç.
2. Kurban pod'lar `Terminating` → graceful shutdown süresi `terminationGracePeriodSeconds`.
3. Tahliye edilen pod Graceful shutdown'dan sonra yeniden schedule edilir (PDB'ye saygı gösterilir).

### Doğrulama ve izleme
```bash
kubectl get events --field-selector reason=Preempting -A
kubectl describe pod <pending-pod> | grep -A5 "Events:"
```

## Common mistakes
- `preemptionPolicy: Never` olan bir PriorityClass'ın tahliye etmeyeceğini bilmemek — bu pod sadece öncelikli sıraya girer.
- PodDisruptionBudget olmayan batch iş yüklerini tahliyeye açık bırakmak; uzun işler ortada kesilir.
- Sistem pod'larının `system-cluster-critical` (2000001000) veya `system-node-critical` önceliğine sahip olduğunu unutmak.

## References
- `skills/k8s-core-pod-disruption-budget`
- `skills/k8s-scale-warm-pool`
- `skills/k8s-core-resource-requests-limits`
