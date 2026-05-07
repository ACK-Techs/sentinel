---
name: obs-prometheus-labels-strategy
description: Bir metrik için label set’i tasarlamak, kardinalite patlamasını önlemek veya mevcut metriklerde “çok seri var / Prometheus şişiyor” probleminde kök nedeni label düzeyinde analiz etmek gerektiğinde kullan. “hangi label’lar olmalı?”, “high-cardinality label”, “normalizasyon”, “dimension budget” gibi sorular için.
---

## Purpose
Bu skill’in çıktısı, “label tasarım kararı”dır:
- Hangi label’lar **kalmalı**, hangileri **yasak** veya **normalize** edilmeli
- Kardinalite risk analizi (hangi label kaç farklı değer üretir?)
- Gerekirse mitigation planı: drop/rename/relabel, recording rule ile boyut azaltma

## Workflow
- Önce “sorgu ihtiyaçları”nı çıkar:
  - Dashboard/alert hangi kırılımları istiyor? (service, endpoint class, status class, instance vs)
  - “Drilldown” gerçekten gerekli mi, yoksa logs/traces ile mi yapılmalı?
- Label kategorilerini ayır:
  - **Stabil kimlik**: `service`, `job`, `namespace`, `instance` (az değer, uzun ömür)
  - **Sınıflandırma**: `status_class=2xx/5xx`, `method`, `endpoint_group`
  - **Tehlikeli boyutlar** (genelde yasak): raw `path`, `user_id`, `trace_id`, `query`, `pod_uid`
- Kardinaliteyi ölç (varsa canlı Prometheus’ta):
  - Bir metriğin seri sayısını kabaca kontrol et: `count(<metric_name>)`
  - Hangi label patlatıyor: `topk(10, count by (<label>)(<metric_name>))` benzeri yaklaşımla adayları bul.
- Normalizasyon stratejisi üret:
  - URL path’i sınıfa indir: `/users/{id}` → `/users/:id` gibi (uygulama tarafında).
  - HTTP status’u sınıfa indir: `200` yerine `2xx` (gerekirse ek label).
  - Kubernetes pod adını saklamak yerine `deployment`/`app` gibi daha stabil label’lara dön.
- Uygulama/collector/scrape katmanı kararını yaz:
  - En doğru yer çoğu zaman **instrumentation** katmanıdır; scrape relabel “son çare”.
- Sonuç olarak “label contract” yaz:
  - 5–10 satırlık: allowed + forbidden + normalize kuralları (ekip standardı gibi).

## Red flags
- Etiket değeri kullanıcı girdisinden geliyorsa (ID, e‑posta, URL query) neredeyse kesin yasak.
- Bir label’ın değer sayısı zamanla sınırsız büyüyorsa (pod adı gibi) stabilize etmeden kullanma.

## References
- `skills/obs-prometheus-storage-tsdb`
