---
name: k8s-scale-warm-pool
description: "Cluster Autoscaler ile yeni node provision gecikmesini (1-3 dk) azaltmak için warm/standby node havuzu tutmak ya da uygulama pod'larının soğuk başlama süresini (image pull + JVM ısınma) önceden kısaltmak gerektiğinde kullan."
---

## Purpose
İki farklı warm pool problemi çözülür: (1) node düzeyinde — boşta hazır node tutmak, (2) pod düzeyinde — önceden başlatılmış pod'ları trafiğe hazır bekletmek.

## Node-level warm pool (Cluster Autoscaler)

### Overprovisioning ile boşta pod yerleştirme
Cluster Autoscaler node'u yalnızca "unschedulable pod" olduğunda ekler. Sahte düşük öncelikli pod'lar ile node'ları doldurup hazır tutmak sık kullanılan yöntemdir:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: overprovisioning
spec:
  replicas: 3
  template:
    spec:
      priorityClassName: overprovisioning  # value: -1
      containers:
        - name: pause
          image: registry.k8s.io/pause:3.9
          resources:
            requests:
              cpu: "1"
              memory: "1Gi"
```
Gerçek iş yükü gelince bu pause pod'lar tahliye edilir, node zaten hazırdır.

### Karpenter (alternatif)
Karpenter'ın `consolidationPolicy: WhenUnderutilized` ve `expireAfter` ayarları ile düğüm yaşam döngüsünü daha ince kontrol etmek mümkündür.

## Pod-level warm pool
```yaml
# KEDA ScaledObject ile minimum replica'yı trafiksiz saatlerde de tut
spec:
  minReplicaCount: 2
  cooldownPeriod: 300
```
Uygulamanın kendisi JVM gibi ısınma gerektiriyorsa readinessProbe başarılı olana kadar trafik almaz — minReplicas sayısı pool boyutunu belirler.

## Common mistakes
- Pause pod'ların resource request'lerini gerçek iş yükünden düşük ayarlamak; gerçek pod gelince yer bulamaz.
- Warm pool maliyetini hesaba katmamak — sürekli boşta node çalıştırmak masraflıdır.

## References
- `skills/k8s-scale-pod-preemption`
- `skills/k8s-scale-cluster-autoscaler`
- `skills/k8s-scale-hpa`
