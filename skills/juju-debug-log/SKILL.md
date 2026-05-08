---
name: juju-debug-log
description: "Juju model log akışını izlemek, belirli uygulama/unit/log seviyesine göre filtrelemek ve geçmiş log kayıtlarını araştırmak gerektiğinde kullan."
---

## Purpose
`juju debug-log` tüm Juju agent ve hook log'larını tek akışta sunar. Doğru filtre olmadan içinde kaybolmak kolaydır.

## Temel kullanım
```bash
juju debug-log                          # canlı akış
juju debug-log --tail 100               # son 100 satır
juju debug-log --replay                 # model başından itibaren
```

## Filtreleme

### Uygulamaya göre
```bash
juju debug-log --include unit:prometheus-k8s/0
juju debug-log --include unit:grafana-k8s/*  # tüm unitler
```

### Log seviyesine göre
```bash
juju debug-log --level ERROR
juju debug-log --level DEBUG  # çok fazla çıktı üretir
```

### Bileşen ve seviye kombinasyonu
```bash
juju debug-log --include unit:prometheus-k8s/0 --level WARNING
```

### Hook log'ları
```bash
juju debug-log --include unit:prometheus-k8s/0 --replay | grep "running hook"
```

## Belirli zaman aralığı
```bash
# Son 30 dakika:
juju debug-log --replay | grep "$(date -d '30 minutes ago' '+%Y-%m-%d %H:%M')"
```

## Hata ayıklama ipuçları
- `blocked` durumundaki app için: `--include unit:<app>/0 --replay | grep -E "ERROR|WARN|blocked"`
- Hook hatası sonrası: `--include unit:<app>/0 --replay | grep -A5 "hook failed"`

## Common mistakes
- Filtre olmadan `--replay` çalıştırmak — büyük modellerde GB'larca log akar.
- `--level DEBUG` ile filtreleme yapmadan çalıştırmak; Juju framework DEBUG satırları asıl sorunu gizler.

## References
- `skills/juju-troubleshoot-blocked`
- `skills/juju-ssh-debug`
- `skills/juju-status-parsing`
