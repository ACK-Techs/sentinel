---
name: microk8s-ha-cluster
description: "MicroK8s'te 3-node yüksek erişilebilirlik (HA) cluster kurmak, dqlite Raft quorum'unu anlamak ve node kayıplarında cluster sağlığını koruma stratejisini uygulamak gerektiğinde kullan."
---

## Purpose
MicroK8s HA'sı, etcd yerine gömülü dqlite kullanır. 3 control-plane node = Raft quorum sağlanır; 1 node kaybında cluster çalışmaya devam eder.

## HA kurulum sırası
```bash
# Node 1 (primary) — başlatma
microk8s status  # önce tek node çalışıyor olmalı

# Node 1'de join token üret
microk8s add-node
# Çıktı: microk8s join <ip>:25000/<token>

# Node 2'de join et
microk8s join <node1-ip>:25000/<token>

# Node 1'de tekrar token üret (tek kullanımlık)
microk8s add-node
# Node 3'te join et
microk8s join <node1-ip>:25000/<token>
```

## HA durumu doğrulama
```bash
microk8s status
# "high-availability: yes" satırını kontrol et
microk8s kubectl get nodes
# Tüm node'lar Ready ve role=control-plane
```

## Quorum kuralları
- 3 node: 1 kayba tolerans
- 5 node: 2 kayba tolerans
- Çift sayı node (2, 4) önerilmez — split-brain riski

## Node kurtarma
```bash
# Arızalı node'u kümeden çıkar
microk8s remove-node <node-adı>
# Yeni node ekle
microk8s add-node  # yeni token
```

## Common mistakes
- 2 node ile HA kurmak — quorum yok, tek node kayıpla cluster çalışmaz.
- dqlite repair gerektiren durumlarda `microk8s reset` ile veri silmek.
- Juju controller HA ile MicroK8s HA'yı karıştırmak — bunlar bağımsız katmanlardır.

## References
- `skills/k8s-scale-microk8s-node-add`
- `skills/microk8s-upgrade`
- `skills/microk8s-ip-change-recovery`
