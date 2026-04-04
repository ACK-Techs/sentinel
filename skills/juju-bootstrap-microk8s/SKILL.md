---
name: juju-bootstrap-microk8s
description: MicroK8s’i Kubernetes bulutu olarak kaydedip Juju denetleyicisini bootstrap eder; COS modelinden önce bir kez çalıştırılır.
---

## Purpose
`microk8s` üzerinde **Juju controller** oluşturmak ve charm dağıtımları için hazır bir bulut/model altyapısı sağlamak.

## Rules
- MicroK8s kubeconfig erişilebilir olmalı: `microk8s config` ile `KUBECONFIG` veya `juju add-k8s microk8s --client` (sürüme göre komut; `juju add-k8s --help` doğrulayın).
- Bootstrap: `juju bootstrap microk8s <controller-adı>` — yaygın adı `microk8s` veya ekip politikası.
- Aynı kümede **tek denetleyici** yeterlidir; birden fazla bootstrap yerine yeni **model** kullanın (`juju-model-cos`).
- Hata ayıklama: `juju status`, `juju controllers`, `microk8s kubectl get pods -A` (Juju konteynerleri).
- Juju’nun **universal OLM** rolü: [Universal operators](https://juju.is/universal-operators).

## References
- `skills/juju-snap-setup`
- `skills/microk8s-addons-dns-storage`
- `skills/juju-model-cos`
- `documantations/ARCHITECTURE_COS.md`
