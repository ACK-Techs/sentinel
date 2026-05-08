---
name: juju-terraform-provider
description: "Juju Terraform provider ile charm dağıtımını, model ve relation yönetimini infrastructure-as-code yaklaşımıyla yapmak; Terraform state üzerinden Juju ortamının bakımını tutmak gerektiğinde kullan."
---

## Purpose
Juju Terraform provider, `juju_application`, `juju_model`, `juju_integration` resource'larıyla Juju operasyonlarını Terraform HCL içinde yönetir. GitOps ve IaC pipeline'larına entegrasyon sağlar.

## Provider yapılandırması
```hcl
terraform {
  required_providers {
    juju = {
      source  = "juju/juju"
      version = "~> 0.13"
    }
  }
}

provider "juju" {
  controller_addresses = ["10.0.0.1:17070"]
  username             = "admin"
  password             = var.juju_password
  ca_certificate       = file("~/.local/share/juju/certs/controller-ca.crt")
}
```

## Temel resource'lar

### Model
```hcl
resource "juju_model" "cos" {
  name = "cos"
}
```

### Uygulama
```hcl
resource "juju_application" "prometheus" {
  model = juju_model.cos.name
  name  = "prometheus-k8s"
  charm {
    name    = "prometheus-k8s"
    channel = "latest/stable"
    revision = 150
  }
  units = 1
}
```

### Integration (relation)
```hcl
resource "juju_integration" "prom_grafana" {
  model = juju_model.cos.name
  application {
    name     = juju_application.prometheus.name
    endpoint = "grafana-source"
  }
  application {
    name     = juju_application.grafana.name
    endpoint = "grafana-source"
  }
}
```

## Dikkat noktaları
- `terraform destroy` tüm modeli ve uygulamaları kaldırır — üretim ortamında `prevent_destroy = true` kullan.
- Terraform state ile Juju out-of-band değişiklik yaptığında drift oluşur; `terraform refresh` gerekir.

## Common mistakes
- Revision belirtmeden deploy etmek — her `apply` farklı revision deploy edebilir.
- Terraform'dan bağımsız `juju config` değişikliği sonrası state'in senkronize olmadığını fark etmemek.

## References
- `skills/juju-charm-deploy`
- `skills/juju-model-lifecycle`
- `skills/juju-bundle-deploy`
