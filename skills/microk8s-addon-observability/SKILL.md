---
name: microk8s-addon-observability
description: "MicroK8s'in dahili observability addon'unu (Prometheus + Grafana + Loki + Tempo stack) hızlıca kurmak, mevcut COS Lite ile çakışma durumunu anlamak ve ne zaman hangi stack'i tercih etmek gerektiğini belirlemek için kullan."
---

## Purpose
`microk8s enable observability` ile tek komutla kube-prometheus-stack ve Loki kurulur. Hızlı prototip ve geliştirme için yeterli; üretimde Juju/COS Lite tercih edilir.

## Kurulum
```bash
microk8s enable observability
# Namespace: observability
# Grafana: port-forward ile erişilir
microk8s kubectl port-forward -n observability svc/kube-prometheus-stack-grafana 3000:80
```
Varsayılan Grafana kimlik: `admin / prom-operator`

## Ne içerir?
- **Prometheus** (kube-prometheus-stack): node, pod, kubelet metrikleri otomatik toplanır.
- **Grafana**: önceden yüklenmiş Kubernetes dashboard'ları.
- **Loki** + **Promtail**: pod log'ları otomatik toplanır.
- **Alertmanager**: temel alert route yapılandırması.

## COS Lite ile karşılaştırma

| Kriter | microk8s observability | COS Lite (Juju) |
|---|---|---|
| Kurulum kolaylığı | Tek komut | Juju model + bundle deploy |
| Üretim uygunluğu | Sınırlı | Evet |
| Charm lifecycle | Yok | Tam |
| Özelleştirme | Helm values | Juju config/relations |

## Dikkat
- `observability` addon ile Juju COS Lite'ı aynı kümeye kurmak port ve resource çakışması yaratır.
- Yalnızca biri aktif olmalı.

## Common mistakes
- `observability` ve ayrıca `prometheus-operator` helm chart kurmak — çift Prometheus devreye girer.
- Addon'u devre dışı bırakmadan COS Lite kurumaya çalışmak.

## References
- `skills/microk8s-addons-overview`
- `skills/cos-bundle-overview`
- `skills/obs-grafana-provisioning`
