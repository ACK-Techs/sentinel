---
name: microk8s-install-base
description: MicroK8s snap kurulumu ve kümenin temel hazır hale getirilmesi için kullanılır; COS öncesi zorunlu adımdır.
---

## Purpose
Host üzerinde **MicroK8s** Kubernetes dağıtımını kurmak, `microk8s status` ile doğrulamak ve COS/Juju öncesi tek düğümlü (veya POC) küme tabanını oluşturmak.

## Rules
- Kurulum için resmi yol: **snap** — `sudo snap install microk8s --classic` (sürüm ihtiyacına göre `--channel` kullanılabilir).
- Kullanıcıyı `microk8s` grubuna ekleyin; oturum yenilemeden `newgrp microk8s` veya çıkış/giriş gerekebilir.
- Kaynak: [COS Lite on MicroK8s](https://documentation.ubuntu.com/observability/track-2/tutorial/installation/cos-lite-microk8s-sandbox/) en az **4 vCPU, 8 GiB RAM, ~40 GiB disk** önerir.
- HTTP vekil kullanılıyorsa MicroK8s [proxy dokümantasyonu](https://microk8s.io/docs/install-proxy) uygulanmalıdır.
- Bu skill **dns** / **storage** / **metallb** eklentilerini açmaz; bunlar `microk8s-addons-dns-storage` skill’indedir.

## References
- `skills/microk8s-addons-dns-storage`
- `skills/juju-bootstrap-microk8s`
- `documantations/PROJECT_ROOT.md`, `documantations/ARCHITECTURE_COS.md`
