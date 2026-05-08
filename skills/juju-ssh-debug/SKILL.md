---
name: juju-ssh-debug
description: "Juju unit'e SSH ile bağlanarak dosya sistemi inceleme, servis durumu kontrol etme ya da `juju debug-hooks` ile hook yürütme sırasında canlı hata ayıklama yapmak gerektiğinde kullan."
---

## Purpose
Log analizi yetmediğinde unit içine girerek gerçek durumu görmek ve hook'ları interaktif olarak çalıştırmak en hızlı teşhis yöntemidir.

## Unit'e SSH bağlantısı
```bash
juju ssh prometheus-k8s/0
juju ssh --pty prometheus-k8s/0 bash
```

Kubernetes charm'larında (k8s model):
```bash
juju ssh --container prometheus prometheus-k8s/0 bash
```

## Unit içinde kullanışlı komutlar
```bash
# Charm dizini
ls /var/lib/juju/agents/unit-prometheus-k8s-0/charm/
# Servis durumu (non-k8s)
systemctl status jujud-unit-*
# Relation verileri
relation-ids --format=json
```

## debug-hooks ile interaktif hook yakalama
```bash
juju debug-hooks prometheus-k8s/0 config-changed
# Yeni terminal açılır; hook çalıştığında buraya düşer
# Hata sonrası:
juju debug-hooks prometheus-k8s/0 *  # tüm hook'lar
```

`debug-hooks` oturumunda:
- `exit 0` → hook başarılı tamamlandı
- `exit 1` → hook başarısız; retry'a düşer
- `tmux` pencerelerinde hook kodu + ortam görünür

## Kubernetes charm'larında konteyner erişimi
```bash
microk8s kubectl exec -n <namespace> <pod> -c <container> -- bash
# Juju namespace'ini bulmak için:
juju status --format=json | jq '.model.name'
```

## Common mistakes
- `juju ssh` ile bağlanırken SSH key'in controller'a kayıtlı olmadığını kontrol etmemek.
- `debug-hooks` oturumunu açık bırakıp hook'ların bloke olmasına neden olmak.

## References
- `skills/juju-debug-log`
- `skills/juju-troubleshoot-blocked`
