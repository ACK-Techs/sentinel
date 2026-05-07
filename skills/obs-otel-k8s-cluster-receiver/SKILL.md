---
name: obs-otel-k8s-cluster-receiver
description: OpenTelemetry Collector `k8s_cluster` (k8scluster) receiver ile Kubernetes cluster seviyesinde (node/pod/daemonset/deployment) “state” metriklerini toplamak veya “cluster metrics yok/çok gürültülü” sorunlarını çözmek gerektiğinde kullan. Kube-state-metrics yerine **Collector tabanlı cluster state** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- `k8scluster` receiver yapılandırma iskeleti + hangi metrik gruplarının açılacağı kararı
- RBAC ve API load riskleri (watch/list maliyeti) için güvenlik/operasyon notu
- Doğrulama: birkaç kritik “desired vs available” metriğinin görünmesi kanıtı

## Workflow
- Hedef metrikleri seç:
  - Workload kapasitesi (deployment replicas), node readiness, pod phase dağılımı.
- Yetki/RBAC:
  - Receiver’ın hangi API kaynaklarını list/watch edeceğini netleştir; least privilege uygula.
- Ölçek ve yük:
  - Büyük cluster’da liste/watch yükü artar; scrape interval ve receiver kapsamını daralt.
- Label hijyeni:
  - Namespace ve workload adı gibi gerekli label’larla sınırlı kal; UID gibi yüksek kardinaliteyi taşıma.
- Doğrulama:
  - Grafana’da deployment available/desired trend’i beklenen namespace’lerde görünüyor mu?

## Common mistakes
- Tüm namespace’leri ve tüm kaynakları izlemek: API server yükü ve maliyet artışı.
- RBAC’i “cluster-admin” yapmak: gereksiz risk.

## References
- `skills/k8s-core-rbac`
- `skills/obs-otel-collector-processors`
