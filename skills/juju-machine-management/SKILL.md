---
name: juju-machine-management
description: "Juju modelinde manuel makine eklemek/çıkarmak, donanım kısıtlamaları (constraints) belirlemek ve mevcut unit'leri makinelere yerleştirme kurallarını uygulamak gerektiğinde kullan. Kubernetes modeli değil, bare-metal veya VM cloud'larında kullanılır."
---

## Purpose
Kubernetes olmayan Juju modellerinde (bare-metal, AWS EC2, LXD) makineler bağımsız kaynak olarak yönetilir. Charm'lar belirli makinelere veya kısıtlara göre yerleştirilebilir.

## Makine ekleme
```bash
# Cloud'da otomatik provision:
juju add-machine

# Manuel (mevcut SSH erişimli host):
juju add-machine ssh:ubuntu@10.0.0.5

# Kısıtla:
juju add-machine --constraints "cores=4 mem=8G"
juju add-machine --constraints "instance-type=t3.large"  # AWS
```

## Makine listeleme
```bash
juju status  # machines bölümü
juju machines
```

## Belirli makineye deploy
```bash
juju deploy myapp --to 0          # makine ID
juju deploy myapp --to lxd:0      # makine 0'da LXD container
juju add-unit myapp --to 2        # mevcut uygulamayı makine 2'ye genişlet
```

## Makine kaldırma
```bash
juju remove-machine 3
juju remove-machine 3 --force     # birimler üstünde olsa da zorla
```

## Common mistakes
- `--to` olmadan deploy etmek: Juju makineyi kendisi seçer; kritik servisler için kontrol kaybı.
- Kubernetes modelinde `add-machine` denemek — K8s modelinde makine değil pod mantığı geçerlidir.
- `--force` ile makine kaldırırken üstündeki charm'ın silinmeyeceğini unutmak.

## References
- `skills/juju-charm-deploy`
- `skills/juju-bootstrap-cloud`
- `skills/juju-constraints`
