---
name: obs-prometheus-operator-crds
description: Prometheus Operator (kube-prometheus-stack vb.) kullanıyorsan metrik scrape ve kural yönetimini `ServiceMonitor`, `PodMonitor`, `PrometheusRule` CRD’leriyle k8s-native yapmak gerektiğinde kullan. “ServiceMonitor yaz”, “selector çalışmıyor”, “endpoint/port seçimi”, “PrometheusRule nereye bağlanır?” gibi durumlar için.
---

## Purpose
Bu skill’in çıktısı, Operator dünyasına uygun **CRD manifestleri** ve “neden böyle?” notudur:
- `ServiceMonitor` veya `PodMonitor`: hedef seçimi + endpoint tanımı + relabelings
- `PrometheusRule`: recording/alerting rule grupları
- En sık hataya düşülen yerler: selector/namespaceSelector, port adı, label match

## Workflow
- Ön koşulu doğrula:
  - Cluster’da Operator CRD’leri var mı? (yoksa bu skill yerine scrape-config/SD kullan)
- Doğru CRD’yi seç:
  - Service üzerinden scrape ediyorsan `ServiceMonitor`
  - Pod’ları doğrudan hedefliyorsan `PodMonitor`
  - Kural dağıtıyorsan `PrometheusRule`
- Selector tasarımı (en sık bug burada):
  - `spec.selector.matchLabels` sadece “etiketi olanları” seçer; etiketi yoksa hedef gelmez.
  - `spec.namespaceSelector`: aynı namespace mi, cross-namespace mi? (açıkça yaz)
- Endpoint tasarımı:
  - `endpoints[].port` çoğunlukla **service port adı** ister; number/targetPort ile karıştırma.
  - `path`, `scheme`, `interval`, `scrapeTimeout` değerlerini ihtiyaca göre ayarla.
  - Auth/TLS gerekiyorsa secret değerlerini embed etme; referans yolunu ver.
- Relabelings:
  - “opt-in” seçimi için label/annotation tabanlı filtreyi relabelings ile pekiştir.
  - Kardinaliteyi artıran label’ları otomatik taşımamaya dikkat et.
- PrometheusRule bağlanması:
  - Kuralın “hangi Prometheus” tarafından alınacağını belirleyen label/selector mekanizması stack’e göre değişir; bu yüzden rule manifestinde kullanılan label’ı ve beklentiyi açık yaz.
- Doğrulama:
  - Targets sayısı (Prometheus UI/targets) ve `up{...}` ile hızlı kontrol.
  - Rule’lar yüklendi mi: yeni record/alert ismi görünüyor mu?

## Common mistakes
- Service port adı yerine container port numarası yazmak (hedef bulunur ama scrape etmez veya hiç görünmez).
- `namespaceSelector`’ı unutmak: farklı namespace’teki Service’ler görünmez.

## References
- `skills/obs-prometheus-service-discovery`
- `skills/obs-prometheus-alerting-rules`
