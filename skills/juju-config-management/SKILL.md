---
name: juju-config-management
description: "Juju uygulama yapılandırmasını güncellemek, mevcut değerleri incelemek, YAML dosyasından toplu ayar uygulamak ya da bir config değişikliğinin uygulanıp uygulanmadığını doğrulamak gerektiğinde kullan."
---

## Purpose
`juju config` komutu, charm'ın konfigürasyon şemasını okur ve değerleri günceller. Her değişiklik `config-changed` hook'unu tetikler.

## Config okuma
```bash
juju config grafana-k8s                      # tüm config
juju config grafana-k8s admin-password       # tek değer
juju config grafana-k8s --format=json        # JSON çıktı
```

## Config güncelleme
```bash
# Tek değer:
juju config grafana-k8s admin-password=yeni-sifre

# Birden fazla değer:
juju config prometheus-k8s \
  log-level=debug \
  evaluation-interval=30s

# YAML dosyasından toplu uygulama:
juju config grafana-k8s --file grafana-prod.yaml
```

Örnek `grafana-prod.yaml`:
```yaml
grafana-k8s:
  admin-password: "üretim-şifresi"
  log-level: "warn"
```

## Config sıfırlama (varsayılana dönme)
```bash
juju config grafana-k8s --reset log-level
```

## Değişiklik doğrulama
```bash
juju status grafana-k8s  # hook tamamlandıysa active/idle
juju debug-log --include unit:grafana-k8s/0 --replay | grep config-changed
```

## Common mistakes
- Büyük/küçük harf ve tire/alt çizgi karışıklığı — `juju config <charm>` ile kesin adı doğrula.
- YAML dosyasındaki indent hatası; `juju config` sessizce kısmi uygulama yapabilir.
- Config değişikliğinin etki etmesi için birim yeniden başlatma gerekip gerekmediğini charm dokümantasyonunda kontrol etmemek.

## References
- `skills/juju-charm-deploy`
- `skills/juju-status-parsing`
- `skills/juju-actions`
