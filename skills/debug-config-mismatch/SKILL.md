---
name: debug-config-mismatch
description: "Ortam değişkenleri, YAML config dosyaları ve runtime değerleri arasındaki uyuşmazlıkları tespit eder ve kökeni belirler"
---

## Purpose
Sentinel servislerinde konfigürasyon uyuşmazlıkları; Helm values, Juju charm config, Kubernetes ConfigMap/Secret ve uygulamanın `settings.py` içindeki beklentilerin farklılaşmasından kaynaklanır. Bu skill, tüm katmanları karşılaştırarak uyuşmazlığın kaynağını hızla bulur ve düzeltme adımını üretir.

## Workflow

### 1. Katman haritası çıkar
```
Helm values.yaml
  └─> Kubernetes Deployment env / envFrom
        └─> ConfigMap / Secret
              └─> Uygulama settings (pydantic-settings, os.getenv)
                    └─> Runtime /admin/config endpoint
```

### 2. Her katmanda değeri topla
```bash
# Helm rendered değer
helm get values sentinel-target -n sentinel-target -a | grep -i database_url

# K8s runtime değer
kubectl exec -n sentinel-target deploy/orders -- env | grep DATABASE_URL

# Uygulama runtime değeri
curl -s http://orders.sentinel-target.svc/admin/config | jq '.database_url'
```

### 3. Karşılaştır
| Katman | Değer | Durum |
|--------|-------|-------|
| Helm values | `postgres://prod-db:5432/orders` | baz alınan |
| ConfigMap | `postgres://dev-db:5432/orders` | UYUŞMAZLIK |
| Runtime env | `postgres://dev-db:5432/orders` | ConfigMap'ten geliyor |

### 4. Uyuşmazlık türlerini sınıfla
- **Type 1 – Stale ConfigMap**: Helm values güncellendi ama `helm upgrade` yapılmadı
- **Type 2 – Secret rotation**: Secret güncellendi, pod restart edilmedi → eski değer bellekte
- **Type 3 – Juju override**: Juju `application-config` değeri Helm değerinin üstüne yazıyor
- **Type 4 – Default fallback**: Uygulama `os.getenv("X", default)` ile farklı default kullanıyor

### 5. Juju config çakışması kontrolü
```bash
juju config sentinel-target-orders | grep -E "database|redis|kafka"
# Helm'den farklı bir değer set edilmişse bu override eder
juju config sentinel-target-orders database_url="postgres://prod-db:5432/orders"
```

### 6. ConfigMap-Pod sync kontrolü
```bash
# ConfigMap son güncellenme zamanı
kubectl get configmap orders-config -n sentinel-target -o jsonpath='{.metadata.resourceVersion}'
# Pod başlama zamanı
kubectl get pod -n sentinel-target -l app=orders -o jsonpath='{.items[0].metadata.creationTimestamp}'
# Pod CM'den önce başladıysa restart gerekli
kubectl rollout restart deployment/orders -n sentinel-target
```

## Common mistakes
1. `helm upgrade` sonrası podların otomatik restart olmadığını varsaymak — `envFrom` kullanan pod'lar ConfigMap değişikliklerini almaz, restart şart.
2. Pydantic `model_config = SettingsConfigDict(env_file=".env")` varken Kubernetes env'in `.env` dosyasını ezip ezmediğini kontrol etmemek.
3. Juju charm'ın `config-changed` hook'unda uygulamaya env inject etmediğini varsaymak — charm config ayrı bir katmandır.
4. `kubectl describe pod` çıktısındaki env değerlerini "anlık" değer saymak — Secret değişmişse `valueFrom.secretKeyRef` eski değeri gösterir.

## References
- `skills/debug-juju-hook-failure`
- `skills/cos-deploy-prometheus`
