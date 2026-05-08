---
name: juju-model-lifecycle
description: "Juju modeli oluşturmak, modeli izolasyon birimi olarak kullanmak, credential ve cloud ayarlarını model düzeyinde yapılandırmak, modeli silmek ya da model listesini yönetmek gerektiğinde kullan."
---

## Purpose
Juju modeli, uygulama ve makine grubu için namespace görevi görür. Tek bir controller birden fazla modeli barındırır; COS ve uygulama ortamlarını modelle ayırmak en iyi pratiktir.

## Model oluşturma
```bash
juju add-model cos microk8s/localhost
juju add-model production aws/us-east-1
# Mevcut controller'da varsayılan cloud/region:
juju add-model staging
```

## Model listeleme ve geçiş
```bash
juju models                  # tüm modeller
juju switch cos              # model bağlamına geç
juju switch controller:cos   # controller + model
```

## Model yapılandırması
```bash
# Default series/charm base ayarla
juju model-config default-base=ubuntu@22.04

# Logging seviyesi
juju model-config logging-config="<root>=WARNING;unit=DEBUG"

# Güvenlik grubu kuralları (cloud spesifik)
juju model-config firewall-mode=instance
```

## Model silme
```bash
juju destroy-model staging --yes
# Tüm kaynaklarla (force):
juju destroy-model staging --yes --destroy-storage --force
```

## Model izolasyonu
- COS bileşenlerini ayrı modelde tutmak, cross-model relation ile uygulama modeline bağlamak ideal tasarımdır.
- Her model kendi namespace'ini alır (Kubernetes cloud'da).

## Common mistakes
- `default` modeline üretim uygulaması deploy etmek — isimlendirme ve izolasyon kaybı.
- Model silerken persistent storage'ın da silineceğini göz ardı etmek.
- `juju switch` ile yalnızca model değil controller+model bağlamını değiştirdiğini unutmak.

## References
- `skills/juju-bootstrap-cloud`
- `skills/juju-model-cos`
- `skills/cos-multi-model`
