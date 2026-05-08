---
name: juju-controller-backup
description: "Juju controller veritabanını yedeklemek, yedekten geri yüklemek ve controller kaybı senaryosu için disaster recovery prosedürünü uygulamak gerektiğinde kullan."
---

## Purpose
Juju controller tüm model, uygulama ve relation durumunu saklar. Controller kaybı = tüm Juju yönetim bilgisinin kaybı (pod'lar çalışmaya devam eder ama Juju kontrolü gider).

## Yedekleme
```bash
juju create-backup
# /tmp/juju-backup-<timestamp>.tar.gz üretir
# veya hedef belirt:
juju create-backup --filename=~/backups/juju-$(date +%Y%m%d).tar.gz
```

## Yedekleri listele
```bash
juju backups
```

## Geri yükleme
```bash
# Controller çalışıyorsa:
juju restore-backup -b <backup-id>

# Controller çökmüşse (bootstrap sonrası):
juju bootstrap <cloud> temp-controller
juju restore-backup --file=/path/to/backup.tar.gz -m controller
```

## Otomatik yedekleme planı
Juju'nun yerleşik cronjob özelliği yoktur; harici script ile:
```bash
# /etc/cron.daily/juju-backup
#!/bin/bash
juju create-backup --filename=/backups/juju-$(date +%Y%m%d).tar.gz
find /backups -name "juju-*.tar.gz" -mtime +7 -delete
```

## Dikkat noktaları
- Yedek alırken controller kısa süre (saniyeler) yavaşlayabilir.
- K8s modellerinde charm'ların kendi state'i (PVC verileri) ayrıca yedeklenmeli.
- Geri yükleme için yedek alındığındaki controller sürümüyle eşleşen MicroK8s/cloud ortamı gerekir.

## Common mistakes
- Yalnızca `juju create-backup` çalıştırıp çıktının kaydedildiği yeri doğrulamamak.
- Yedek test restore yapmamak — yedek bozuk olabilir.

## References
- `skills/juju-bootstrap-cloud`
- `skills/juju-model-lifecycle`
- `skills/cos-backup-strategy`
