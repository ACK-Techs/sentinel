---
name: microk8s-snap-refresh-hold
description: "MicroK8s'in otomatik snap güncellemesini durdurmak veya belirli bir tarihe ertelemek, kontrollü bakım penceresi planlamak ya da kanalı dondurarak sürüm sabitliğini korumak gerektiğinde kullan."
---

## Purpose
Snap, varsayılan olarak 4 saatte bir güncelleme kontrol eder. MicroK8s için plansız otomatik güncelleme, Juju controller veya uygulama iş yüklerini bozabilir.

## Güncellemeyi askıya alma

### Süresiz hold
```bash
sudo snap refresh --hold microk8s
# veya
sudo snap set system refresh.hold="$(date --date='today + 90 days' +%Y-%m-%dT%H:%M:%S%:z)"
```

### Belirli tarihe erteleme
```bash
sudo snap set system refresh.hold="2025-12-31T00:00:00+00:00"
```

### Hold kaldırma ve manuel güncelleme
```bash
sudo snap unset system refresh.hold
sudo snap refresh microk8s --channel=1.30/stable
```

## Global snap güncelleme zamanı
```bash
# Güncellemeyi belirli saatlere kısıtla (hold yerine tercih edilebilir)
sudo snap set system refresh.timer="sun,00:00-04:00"
```

## Mevcut durumu kontrol etme
```bash
snap refresh --time
snap list microk8s  # Rev ve kurulum tarihi
```

## Common mistakes
- Hold koyup unutmak ve güvenlik yamalarının defalarca atlanmasına izin vermek.
- Hold ile Juju `snap-refresh` ilişkisini karıştırmak; Juju ayrı snap lifecycle kontrolüne sahiptir.
- Minor sürüm geçişini `--channel` değiştirerek değil, otomatik refresh'e bırakmak.

## References
- `skills/microk8s-upgrade`
- `skills/microk8s-install-snap`
