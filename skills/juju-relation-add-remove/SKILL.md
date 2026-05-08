---
name: juju-relation-add-remove
description: "İki Juju uygulaması arasında integration (relation) oluşturmak veya kaldırmak, relation endpoint adlarını bulmak ve relation üzerinden akan veriyi incelemek gerektiğinde kullan."
---

## Purpose
Juju relation'ları, uygulamalar arası bağlantı ve konfigürasyon veri paylaşımını otomatikleştirir. COS'ta tüm bileşen bağlantıları relation ile kurulur.

## Relation ekleme
```bash
# Basit form (Juju eşleşen endpoint'i bulur):
juju integrate prometheus-k8s grafana-k8s

# Açık endpoint belirtme:
juju integrate prometheus-k8s:grafana-source grafana-k8s:grafana-source

# Cross-model relation:
juju integrate cos.prometheus-k8s:receive-remote-write myapp:send-remote-write
```

## Endpoint adlarını bulma
```bash
juju info prometheus-k8s | grep -A20 "relations:"
# veya
juju status prometheus-k8s --format=json | jq '.applications."prometheus-k8s".relations'
```

## Relation kaldırma
```bash
juju remove-relation prometheus-k8s grafana-k8s
# Endpoint belirtilerek:
juju remove-relation prometheus-k8s:grafana-source grafana-k8s:grafana-source
```

## Relation verisi inceleme
```bash
# Unit içinde relation-get ile:
juju run prometheus-k8s/0 -- relation-get -r <relation-id> - grafana-k8s/0
# Daha hızlı: show-unit ile
juju show-unit prometheus-k8s/0 | grep -A20 "relation-info"
```

## Common mistakes
- Yanlış endpoint adı kullanmak — `juju info` çıktısına bakılmadan varsayım yapmak.
- Relation eklemeden önce her iki uygulamanın `active/idle` durumda olmaması; hook çakışması olur.
- Bir relation'ı kaldırınca diğer uygulamanın config'inin geri alınacağını hesaba katmamak.

## References
- `skills/juju-charm-deploy`
- `skills/juju-status-parsing`
- `skills/cos-bundle-overview`
