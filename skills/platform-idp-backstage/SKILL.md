---
name: platform-idp-backstage
description: "Backstage ile Sentinel için Internal Developer Portal kurulumu; servis kataloğu, teknik dokümantasyon ve self-service scaffold entegrasyonu"
---

## Purpose
Sentinel ekibi büyüdükçe hangi servisin kimin tarafından sahiplenildiği, API dokümantasyonuna nasıl erişileceği ve yeni servis iskeletinin nasıl oluşturulacağı netleşmelidir. Backstage bu bilgileri tek bir portalda toplar ve geliştirici deneyimini iyileştirir.

## Workflow

### 1. Backstage kurulumu (MicroK8s)
```bash
# Helm ile Backstage deploy
helm repo add backstage https://backstage.github.io/charts
helm upgrade --install backstage backstage/backstage \
  -n platform \
  --create-namespace \
  -f helm/backstage/values.yaml
```

### 2. Sentinel servis catalog.yaml
```yaml
# services/orders/catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: orders-service
  description: Sipariş yönetimi FastAPI servisi
  tags:
    - python
    - fastapi
    - sentinel-target
  annotations:
    github.com/project-slug: sentinel/sentinel-coming
    backstage.io/techdocs-ref: dir:.
    prometheus.io/alert: "orders-high-error-rate"
spec:
  type: service
  lifecycle: production
  owner: group:platform-team
  system: sentinel-target
  dependsOn:
    - component:payments-service
    - component:inventory-service
    - resource:postgres-orders
  providesApis:
    - orders-api
```

### 3. API entity tanımı
```yaml
# services/orders/api.yaml
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: orders-api
  description: Sipariş CRUD API'si
spec:
  type: openapi
  lifecycle: production
  owner: group:platform-team
  definition:
    $text: ./openapi.json
```

### 4. Software template (yeni servis scaffold)
```yaml
# templates/new-sentinel-service/template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: sentinel-service-template
  title: Yeni Sentinel Target Servisi
spec:
  parameters:
    - title: Servis Bilgileri
      properties:
        serviceName:
          type: string
          description: Servis adı (örn: notifications)
        port:
          type: integer
          default: 8005
  steps:
    - id: fetch-template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          serviceName: ${{ parameters.serviceName }}
    - id: publish
      action: publish:github:pull-request
      input:
        repoUrl: github.com?repo=sentinel-coming
        title: "feat: new service ${{ parameters.serviceName }}"
```

### 5. TechDocs entegrasyonu
```yaml
# mkdocs.yml (her servis dizininde)
site_name: Orders Service
docs_dir: docs
plugins:
  - techdocs-core
```

### 6. Backstage plugin'leri (Sentinel için önerilen)
- `@backstage/plugin-kubernetes` — pod durumu doğrudan portalda
- `@backstage/plugin-grafana` — servis Grafana dashboard'u embed
- `@backstage/plugin-pagerduty` — on-call bilgisi

## Common mistakes
1. catalog.yaml dosyalarını servislere eklemeden Backstage kurmak — boş katalog, değer üretmez.
2. `owner` alanını generic "team" olarak bırakmak — incident sırasında kime ulaşılacağı bilinmez.
3. Backstage'i platfom ekibi dışında kimsenin bilmediği bir araç haline getirmek — developer onboarding'e dahil et.
4. TechDocs için mkdocs.yml'ı elle tutmak — `techdocs-core` plugin ile otomatik build.

## References
- `skills/platform-service-catalog`
- `skills/platform-developer-portal`
- `skills/docs-onboarding-checklist`
