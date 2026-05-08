---
name: juju-bootstrap-cloud
description: "Juju controller'ı AWS, GCE, Azure, LXD veya localhost gibi farklı cloud türlerinde bootstrap etmek, credential yapılandırmasını ve controller konfigürasyonunu yapmak gerektiğinde kullan. MicroK8s spesifik bootstrap için juju-bootstrap-microk8s skill'ini tercih et."
---

## Purpose
Juju controller, tüm charm deploy ve lifecycle operasyonlarının yönetim merkezi. Her cloud için credential ve endpoint yapılandırması farklıdır.

## Cloud credential yönetimi
```bash
juju add-credential aws
# İnteraktif: access-key ve secret-key girilir
# veya YAML dosyasından:
juju add-credential aws -f credentials.yaml
```

## Bootstrap örnekleri

### AWS
```bash
juju bootstrap aws/us-east-1 my-aws-controller \
  --constraints "instance-type=t3.medium"
```

### LXD (yerel geliştirme)
```bash
juju bootstrap localhost lxd-controller
```

### Kubernetes (genel)
```bash
juju add-k8s my-k8s-cloud --cluster-name=<context>
juju bootstrap my-k8s-cloud k8s-controller
```

### Manuel cloud (bare-metal)
```bash
juju add-cloud mycloud  # interaktif endpoint tanımı
juju bootstrap mycloud manual-controller
```

## Bootstrap sonrası
```bash
juju status
juju controllers         # tüm controller'ları listele
juju switch <controller> # context değiştir
```

## Controller kaynakları
Bootstrap sırasında controller için constraint verilmezse en küçük instance tipi seçilir; üretim için minimum 2 vCPU/4GB RAM önerilir.

## Common mistakes
- Credential eklemeden bootstrap denemek — "no credentials" hatası.
- Aynı cloud'a birden fazla controller bootstrap etmek; tek controller yeterli, modeller izolasyonu sağlar.
- `--no-gui` flag'ini atlamak → GUI agent gereksiz yere deploy edilir.

## References
- `skills/juju-model-lifecycle`
- `skills/juju-bootstrap-microk8s`
- `skills/juju-controller-backup`
