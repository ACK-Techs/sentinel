---
name: juju-model-cos
description: COS Lite için ayrılmış Juju modeli oluşturur ve bağlamı bu modele alır; bundle veya charm deploy öncesi zorunludur.
---

## Purpose
Gözlemlenebilirlik yığınını diğer uygulamalardan izole etmek için **`cos`** (veya ekip adı) adlı modelde çalışmak.

## Rules
- Model oluştur: `juju add-model cos` (veya `juju add-model cos --config ...`).
- Bağlam: `juju switch cos` — tüm `juju deploy` / `juju status` komutları bu modelde çalışmalı.
- Model adı Terraform ile uyumlu tutulabilir; `observability-stack` Terraform modülü varsayılan olarak `cos` modeli oluşturabilir ([tutorial Terraform bölümü](https://documentation.ubuntu.com/observability/track-2/tutorial/installation/cos-lite-microk8s-sandbox/#deploy-cos-lite-using-terraform)).
- Cross-model relations için `offers-overlay.yaml` kullanımında model adı ve offer isimleri tutarlı olmalıdır.
- SLA: sandbox’ta `unsupported` görülebilir; üretimde SLA/destek politikasına göre yapılandırın.

## References
- `skills/juju-bootstrap-microk8s`
- `skills/cos-deploy-prometheus` … `skills/cos-deploy-traefik` (bundle veya ayrı deploy)
- [cos-lite-bundle overlays](https://github.com/canonical/cos-lite-bundle/tree/main/overlays)
