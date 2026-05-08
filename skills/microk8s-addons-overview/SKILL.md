---
name: microk8s-addons-overview
description: "MicroK8s addon ekosistemini, hangi addon'ın ne sağladığını ve birbirine bağımlılık sırasını anlamak; 'hangi addon'ı ne zaman etkinleştirmeliyim?' sorusuna yanıt bulmak gerektiğinde kullan."
---

## Purpose
MicroK8s addon'ları tek komutla eklenti etkinleştirir. Bağımlılık sırası yanlış kurulduğunda sonraki adımlar sessizce başarısız olur.

## Zorunlu temel sıra
```
dns → (hostpath-storage veya metallb) → ingress
```
DNS olmadan diğer addon'lar servis keşfinde başarısız olur.

## Yaygın addon'lar ve amaçları

| Addon | Amaç |
|---|---|
| `dns` | CoreDNS — her kurulumda zorunlu |
| `hostpath-storage` | Tek-node test için varsayılan StorageClass |
| `metallb` | LoadBalancer IP havuzu |
| `ingress` | nginx Ingress Controller |
| `registry` | Yerel container registry (32000 portu) |
| `gpu` | NVIDIA device plugin |
| `observability` | Prometheus+Grafana+Loki stack |
| `cert-manager` | TLS sertifika yönetimi |
| `dashboard` | Kubernetes Dashboard UI |

## Temel komutlar
```bash
microk8s enable <addon>          # etkinleştir
microk8s disable <addon>         # devre dışı bırak
microk8s status                  # tüm addon durumları
microk8s kubectl get pods -A     # bileşenleri doğrula
```

## Özel repo addon'ları
```bash
microk8s addons repo add myrepo https://github.com/org/microk8s-addons
microk8s enable myrepo/myaddon
```

## Common mistakes
- `ingress` etkinleştirmeden önce `dns` kurmamak.
- `observability` ile dışarıdan kurulan Prometheus'u çakıştırmak.

## References
- `skills/microk8s-install-snap`
- `skills/microk8s-addon-ingress`
- `skills/microk8s-addon-metallb`
- `skills/microk8s-addon-observability`
