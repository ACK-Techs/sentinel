---
name: juju-cross-model-relations
description: "Farklı Juju modellerindeki uygulamalar arasında cross-model relation (CMR) kurarak servis bağlantısı oluşturmak; özellikle COS modelindeki observability bileşenlerini uygulama modelinden tüketmek gerektiğinde kullan."
---

## Purpose
Cross-model relation, tek controller'daki iki model veya farklı controller'daki modeller arasında endpoint paylaşımını sağlar. COS'u ayrı modele izole edip uygulama modellerinden grafana-source/prometheus gibi endpointleri tüketmek en yaygın senaryodur.

## Offer oluşturma (sağlayan taraf)
```bash
# COS modelinde prometheus'u paylaş:
juju switch cos
juju offer prometheus-k8s:receive-remote-write prometheus-remote-write

# Offer listesi:
juju offers
```

## Offer'a bağlanma (tüketen taraf)
```bash
juju switch myapp-model
# Aynı controller:
juju integrate myapp:send-remote-write admin/cos.prometheus-remote-write
# Farklı controller:
juju integrate myapp:send-remote-write <controller>:admin/cos.prometheus-remote-write
```

## CMR durumu görüntüleme
```bash
juju status --relations
# "Remote applications" bölümünde CMR ilişkileri listelenir
```

## Offer kaldırma
```bash
juju switch cos
juju remove-offer admin/cos.prometheus-remote-write --force
```

## Güvenlik
CMR üzerinden hangi model/controller'ın bağlanabileceğini kısıtlamak için:
```bash
juju grant-offer admin/cos.prometheus-remote-write myuser consume
```

## Common mistakes
- Offer adı ile endpoint adını karıştırmak — offer adı `juju offers` çıktısında görünür.
- Farklı controller'lar arası CMR için controller endpoint'ini açmayı unutmak.
- Offer silerken bağlı tüm ilişkilerin kopacağını hesaba katmamak.

## References
- `skills/juju-model-lifecycle`
- `skills/cos-multi-model`
- `skills/juju-relation-add-remove`
