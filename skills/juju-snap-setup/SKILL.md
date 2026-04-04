---
name: juju-snap-setup
description: Juju CLI snap kurulumu, sürüm kanalı ve istemci hazırlığı; MicroK8s bulutuna bootstrap öncesi adımdır.
---

## Purpose
**Juju** istemcisini snap ile kurmak, `juju version` ile doğrulamak ve COS dağıtımı için komut satırı ortamını hazırlamak.

## Rules
- Kurulum: `sudo snap install juju` — kararlılık için `--channel` (ör. `3.6/stable` veya proje standardınıza uygun 3.x) kullanın; tutorial örnekleri **Juju 3.6.x** ile uyumludur.
- `juju` komutunun PATH’te olduğundan emin olun; snap sürümünü `snap info juju` ile doğrulayın.
- İlk kurulumda hesap/kimlik: `juju login` gerekebilir (Charmhub ile entegrasyon senaryolarında).
- Bu skill **bootstrap** yapmaz; yalnızca istemci. Denetleyici için `juju-bootstrap-microk8s` kullanılır.
- Tam operasyon akışı: [Juju — Manage your deployment](https://documentation.ubuntu.com/juju/3.6/howto/manage-your-deployment/).

## References
- `skills/juju-bootstrap-microk8s`
- `skills/juju-model-cos`
- `documantations/PROJECT_ROOT.md`
