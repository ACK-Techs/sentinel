---
name: juju-storage-charm
description: "Juju storage directive ile charm'a depolama talebi eklemek, StorageClass ile entegre etmek ve persistent volume yaşam döngüsünü charm'ın destroy edilmesi sonrasında yönetmek gerektiğinde kullan."
---

## Purpose
Juju storage abstraction, charm'ların PV/PVC detaylarını bilmeden depolama talep etmesini sağlar. Kubernetes modelinde Juju storage → PVC dönüşümü otomatik yapılır.

## Storage talebi (deploy sırasında)
```bash
# Varsayılan pool ile:
juju deploy prometheus-k8s --storage data=1G

# Belirli StorageClass ile:
juju deploy prometheus-k8s --storage data=kubernetes:10G
# format: data=<pool>:<boyut>
```

## Storage pool listeleme
```bash
juju storage-pools
juju storage  # mevcut tüm storage volume'lar
```

## Kubernetes'te pool oluşturma (StorageClass eşleme)
```bash
juju create-storage-pool fast-ssd kubernetes \
  storage-class=premium-ssd \
  storage-provisioner=pd.csi.storage.gke.io
```

## Storage ile deploy örnekleri
```bash
# Loki için yazma dizini:
juju deploy loki-k8s --storage logs-storage=10G

# Prometheus için TSDB:
juju deploy prometheus-k8s --storage database=20G
```

## Storage yaşam döngüsü
Charm silindiğinde storage varsayılan olarak **korunur**:
```bash
juju remove-application prometheus-k8s --destroy-storage  # storage da sil
```

## Common mistakes
- Pool adını yanlış belirtmek — `kubernetes` (K8s modelinde varsayılan pool adı).
- Charm destroy edince PVC'nin kaldığını bilmemek ve disk maliyetine dikkat etmemek.
- `--storage` yerine charm config üzerinden path ayarlamaya çalışmak.

## References
- `skills/k8s-storage-pvc-pv`
- `skills/k8s-storage-storageclass`
- `skills/juju-charm-deploy`
