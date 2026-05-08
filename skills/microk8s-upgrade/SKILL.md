---
name: microk8s-upgrade
description: "MicroK8s'i bir Kubernetes minor sürümünden diğerine yükseltmek (örn. 1.29 → 1.30), snap kanalını değiştirmek ve yükseltme sırasında yaşanan sorunları gidermek gerektiğinde kullan."
---

## Purpose
MicroK8s yükseltmesi snap kanal değişikliği ile yapılır. Yanlış sırada yapılan multi-node yükseltmesi cluster bütünlüğünü bozar.

## Yükseltme öncesi kontroller
```bash
microk8s status
microk8s kubectl get nodes  # tümü Ready olmalı
microk8s kubectl get pods -A | grep -v Running | grep -v Completed  # sorunlu pod yok mu?
# Snapshot al:
microk8s kubectl get all -A -o yaml > pre-upgrade-snapshot.yaml
```

## Tek-node yükseltme
```bash
sudo snap refresh microk8s --channel=1.30/stable
microk8s status --wait-ready
microk8s kubectl get nodes  # sürüm güncellendi mi?
```

## Multi-node yükseltme sırası
1. Control-plane node'ları birer birer yükselt (quorum korunur).
2. Worker node'ları yükselt.
3. Her adımda `microk8s status` ile sağlık doğrula.

Node drain (isteğe bağlı, üretim için önerilir):
```bash
microk8s kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
sudo snap refresh microk8s --channel=1.30/stable
microk8s kubectl uncordon <node>
```

## Geri alma
Snap geri alma yalnızca bir önceki revizyona döner:
```bash
sudo snap revert microk8s
```
Minor sürümden geriye inemezsiniz (Kubernetes downgrade desteklenmez).

## Common mistakes
- Tüm node'ları eş zamanlı yükseltmek — dqlite quorum kaybı.
- Juju controller pod'larının yükseltme sırasında tahliye edilmesi; Juju state bozulabilir.
- `snap refresh` sonrası API server'ın tamamen ayağa kalkmasını beklemeden `kubectl` çalıştırmak.

## References
- `skills/microk8s-install-snap`
- `skills/microk8s-ha-cluster`
- `skills/microk8s-snap-refresh-hold`
