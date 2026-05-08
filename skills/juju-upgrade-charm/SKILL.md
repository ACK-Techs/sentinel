---
name: juju-upgrade-charm
description: "Juju uygulama charm'ını yeni revision veya kanala yükseltmek, yükseltme öncesi hazırlık adımlarını uygulamak ve geri alma (rollback) prosedürünü bilmek gerektiğinde kullan."
---

## Purpose
`juju refresh` komutu charm revision veya kanalı günceller. Yüksek erişilebilirlik gerektiren uygulamalarda birim birim yükseltme önemlidir.

## Yükseltme komutu
```bash
# Mevcut kanaldaki son revision'a:
juju refresh prometheus-k8s

# Belirli revision:
juju refresh prometheus-k8s --revision=125

# Kanal değiştirerek:
juju refresh prometheus-k8s --channel=latest/edge

# Yerel charm ile:
juju refresh prometheus-k8s --path=./prometheus-k8s.charm
```

## Yükseltme öncesi
```bash
# Mevcut revision ve kanal bilgisi:
juju status prometheus-k8s --format=json | jq '.applications."prometheus-k8s" | {rev: .charm-rev, channel: .channel}'

# Unit başına sağlık durumu:
juju status prometheus-k8s

# Snapshot önerilir (storage varsa):
juju run prometheus-k8s/0 create-backup  # charm bunu destekliyorsa
```

## Yükseltme izleme
```bash
juju status prometheus-k8s --watch 3s
juju debug-log --include unit:prometheus-k8s/0 | grep -E "upgrade|hook"
```

## Geri alma
Juju'da otomatik charm rollback yoktur; manuel olarak önceki revision ile `juju refresh` çalıştırmak gerekir:
```bash
juju refresh prometheus-k8s --revision=123
```

## Common mistakes
- Resource'ları güncellemeden yalnızca charm revision yükseltmek — uyumsuz image hatasına yol açar.
- HA deployment'da tüm unitleri eş zamanlı yükseltmek; birer birer yapılmalı ya da charm bunu desteklemelidir.
- `juju upgrade-charm` yerine `juju refresh` kullanmak (eski komut, hâlâ çalışır ama deprecated).

## References
- `skills/juju-charm-deploy`
- `skills/juju-resources`
- `skills/juju-troubleshoot-blocked`
