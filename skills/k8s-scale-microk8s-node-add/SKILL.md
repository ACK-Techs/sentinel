---
name: k8s-scale-microk8s-node-add
description: "MicroK8s tek-node cluster'a ek worker veya control-plane node eklemek, çok-node cluster kurmak ya da node join/leave sürecinin takıldığı sorunu gidermek gerektiğinde kullan."
---

## Purpose
MicroK8s'i birden fazla node'a genişletmek: pod sayısı arttıkça tek node kapasiteyi aşar veya HA quorum için 3 control-plane node gerekir.

## Workflow

### 1. Mevcut node'da join token üret
```bash
# Primary node üzerinde
microk8s add-node
# Çıktıda join komutu verilir:
# microk8s join <ip>:25000/<token>
```
Token tek kullanımlıktır, 24 saat geçerlidir.

### 2. Yeni node'da join çalıştır
```bash
# Yeni makine üzerinde (MicroK8s kurulu olmalı)
microk8s join <primary-ip>:25000/<token>
```
Worker-only join için `--worker` flag'i ekle: cluster etcd'sine dahil olmaz.

### 3. Doğrulama
```bash
microk8s kubectl get nodes -o wide
microk8s status
```

### Ön koşullar
- 25000/tcp ve 16443/tcp portları node'lar arası açık olmalı.
- Tüm node'larda aynı MicroK8s sürümü kurulu olmalı.
- Hostname çakışması olmamalı (`hostnamectl set-hostname <benzersiz-ad>`).

### Node çıkarma
```bash
# Çıkarılacak node üzerinde
microk8s leave
# Primary node üzerinde
microk8s remove-node <node-adı>
```

## Common mistakes
- Firewall kuralını açmadan join denemek; "connection refused" hatası DNS sorunu gibi görünür.
- Worker node'da `microk8s add-node` komutu çalıştırmak — token üretimi primary üzerinde yapılır.
- HA geçiş için 3. node eklenmeden önce dqlite migration'ı beklemeden işlem yapmak.

## References
- `skills/microk8s-ha-cluster`
- `skills/microk8s-install-snap`
- `skills/k8s-scale-cluster-autoscaler`
