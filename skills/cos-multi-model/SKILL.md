---
name: cos-multi-model
description: "COS bileşenlerini ayrı bir Juju modele dağıtıp cross-model relation (CMR) ile uygulama modelindeki servisleri izlemek; bu tasarım kararını ne zaman tercih edeceğini bilmek gerektiğinde kullan."
---

## Purpose
COS ve uygulama iş yüklerini ayrı modelde tutmak: izolasyon, farklı lifecycle, ve ayrı ekiplerin bağımsız yönetimi için tercih edilir. Tek model kurulumdan daha karmaşık ama üretim için önerilir.

## Tasarım kararı
| Seçenek | Ne zaman? |
|---|---|
| Tek model | Geliştirme/deney ortamı, hızlı prototip |
| Ayrı COS modeli | Üretim, farklı yaşam döngüsü, multi-tenant |

## Kurulum
```bash
# 1. COS modeli oluştur ve deploy et:
juju add-model cos
juju deploy cos-lite  # veya tek tek deploy

# 2. COS modelinde offer oluştur:
juju switch cos
juju offer prometheus-k8s:receive-remote-write prometheus-remote-write
juju offer loki-k8s:logging loki-logging
juju offer grafana-k8s:grafana-dashboard grafana-dashboard

# 3. Uygulama modeli:
juju add-model production
juju switch production
juju deploy myapp

# 4. CMR bağlantısı:
juju integrate myapp:send-remote-write admin/cos.prometheus-remote-write
juju integrate myapp:logging admin/cos.loki-logging
juju integrate myapp:grafana-dashboard admin/cos.grafana-dashboard
```

## Multi-tenant senaryosu
```bash
# Her uygulama ekibi kendi modelinde:
juju add-model team-a
juju add-model team-b
# Her iki model de COS offer'larına bağlanır
```

## Common mistakes
- CMR offer'larını oluştururken yanlış endpoint adı kullanmak.
- COS modelini silerken tüm CMR'lerin kopacağını hesaba katmamak.
- Her uygulama modelinde ayrı COS deploy etmek — tek COS + CMR daha verimli.

## References
- `skills/juju-cross-model-relations`
- `skills/cos-bundle-overview`
- `skills/juju-model-lifecycle`
