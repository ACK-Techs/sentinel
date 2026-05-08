---
name: juju-actions
description: "Juju charm'larında tanımlı operasyonel aksiyonları (backup, restore, rotate-encryption-key vb.) çalıştırmak, parametre geçirmek ve sonucu izlemek gerektiğinde kullan."
---

## Purpose
Juju action'ları, charm lifecycle hook'larının dışında çağrılan idempotent operasyonlardır. Backup, key rotation, veritabanı migration gibi tek seferlik görevler için kullanılır.

## Mevcut action'ları listeleme
```bash
juju actions <application>
juju actions prometheus-k8s --format=yaml  # parametre şemasıyla
```

## Action çalıştırma
```bash
# Parametre olmadan:
juju run prometheus-k8s/0 get-password

# Parametre ile:
juju run grafana-k8s/0 set-admin-password password=yeni-sifre

# Tüm unitlerde:
juju run prometheus-k8s/* scrape-config-reload
```

## Sonuç izleme
```bash
# --wait ile anlık bekle:
juju run prometheus-k8s/0 get-password --wait=2m

# Sonradan sorgulama (eski yöntem):
juju show-action-output <task-id>
```

## Action durumları
- `pending`: kuyruğa alındı
- `running`: çalışıyor
- `completed`: başarıyla tamamlandı
- `failed`: hata; `juju show-action-output` ile detaya bak

## Common mistakes
- Unit numarası yerine uygulama adıyla action çalıştırmaya çalışmak — `<app>/0` biçimi gerekir.
- `--wait` süresini çok kısa belirleyip action henüz tamamlanmadan "failed" zannetmek.
- Aynı action'ı iki kez çalıştırmanın idempotent olmayabileceğini (örn. backup) göz ardı etmek.

## References
- `skills/juju-charm-deploy`
- `skills/juju-config-management`
- `skills/juju-debug-log`
