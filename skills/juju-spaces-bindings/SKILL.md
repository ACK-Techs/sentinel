---
name: juju-spaces-bindings
description: "Juju network space'leri ve endpoint binding'leri ile charm'ların belirli ağ arayüzlerine (management, data plane) bağlanmasını sağlamak ya da çoklu NIC ortamında trafik izolasyonu uygulamak gerektiğinde kullan."
---

## Purpose
Juju space'leri, fiziksel/sanal ağ segmentlerini soyutlar. Binding'ler, charm endpoint'lerinin hangi space üzerinden iletişim kuracağını belirler; bu sayede yönetim trafiği ile veri trafiği ayrılır.

## Space oluşturma
```bash
# MAAS veya manuel cloud'da subnet tanımlama:
juju add-space management 10.0.0.0/24
juju add-space data 10.1.0.0/24

juju spaces  # listele
```

## Endpoint binding
```bash
# Deploy sırasında:
juju deploy myapp \
  --bind "admin=management data=data"

# Mevcut uygulamaya:
juju set-binding myapp admin=management data=data
```

## Tüm endpoint'leri bir space'e bağlama
```bash
juju deploy myapp --bind management
# Tüm endpoint'ler management space'ini kullanır
```

## Space doğrulama
```bash
juju show-space management
juju subnets  # subnet-space eşleşmesi
```

## Kubernetes modellerinde sınırlama
K8s modellerinde space kavramı ağırlıklı olarak network policy düzeyinde yönetilir; Juju space API kısıtlı destek sunar.

## Common mistakes
- Space tanımlamadan binding uygulamaya çalışmak — "space not found" hatası.
- MicroK8s üzerinde Juju space kavramını MAAS'taki gibi uygulamayı beklemek; farklı semantik.
- Binding değiştirince mevcut connection'ların sıfırlanacağını hesaba katmamak.

## References
- `skills/juju-charm-deploy`
- `skills/juju-machine-management`
- `skills/k8s-net-networkpolicy`
