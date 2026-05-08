---
name: cos-relation-loki-alertmanager
description: "Loki ruler ile log tabanlı alerting kurmak için Loki→Alertmanager relation'ını oluşturmak, ilişkinin kurulduğunu doğrulamak ve Loki ruler alert kuralı yazmak gerektiğinde kullan."
---

## Purpose
Loki'nin ruler bileşeni, log akışı üzerinde LogQL tabanlı alert kuralları değerlendirir ve Alertmanager'a ateşler. Bu, metrik olmayan log tabanlı alarmlar için kritik bir zincirdir.

## Relation kurulumu
```bash
juju switch cos
juju integrate loki-k8s:alertmanager alertmanager-k8s:alerting
```

## Doğrulama
```bash
juju status loki-k8s alertmanager-k8s
# Her ikisi de active/idle olmalı
# Relation mevcut mu:
juju status --relations | grep -A3 loki-k8s
```

## Loki ruler alert kuralı
```yaml
# prometheusrule.yaml (Loki ruler format)
groups:
  - name: error-rate
    interval: 1m
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate({app="myapp"} |= "ERROR" [5m])) > 10
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Yüksek hata oranı tespit edildi"
```

Juju config üzerinden kural yükleme:
```bash
juju config loki-k8s alert-rules-dir=/path/to/rules
# veya charm action:
juju run loki-k8s/0 update-alert-rules
```

## Alertmanager'da Loki alert görme
```bash
curl http://<alertmanager-url>/api/v2/alerts | jq '.[] | select(.labels.app == "myapp")'
```

## Common mistakes
- Loki ruler disabled olduğunda relation kurulsa da alert ateşlenmez — `ruler.enabled: true` kontrol et.
- LogQL sorgusunda label adını yanlış yazmak; `{}` içinde en az bir label olmalı.

## References
- `skills/cos-bundle-overview`
- `skills/obs-loki-ruler-alerts`
- `skills/obs-alertmanager-routing`
