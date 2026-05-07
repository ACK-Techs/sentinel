---
name: obs-tempo-service-graph
description: Trace’lerden “servis → servis” çağrı topolojisi (service graph) üretmek, bu metrikleri Prometheus’a aktarmak ve Grafana’da service graph görselleştirmesini çalıştırmak gerektiğinde kullan. “service graph boş”, “bağlantılar çıkmıyor”, “hangi ön koşullar lazım?” gibi konulara odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Service graph üretimi için gerekli ön koşullar listesi (trace attribute’ları ve pipeline)
- Prometheus tarafında görülecek metrik beklentisi ve doğrulama sorgusu
- Grafana’da topoloji paneli için minimum kurulum/doğrulama adımı

## Workflow
- Ön koşullar:
  - Trace’lerde `service.name` doğru mu? (OTel resource)
  - Client/server span ilişkisi ve peer/host bilgileri tutarlı mı? (aksi halde edge çıkarımı zorlaşır)
- Service graph üretim yolunu seç:
  - Tempo’nun kendi mekanizması mı, yoksa OTel Collector “span metrics/service graph” üretimi mi?
  - Bu repo bağlamında hedef: Prometheus’a metrik akıtmak → Grafana’da çizmek.
- Prometheus doğrulaması:
  - Service graph metrikleri geliyor mu? (önce “metrik var mı” kontrol et)
  - Bir edge’in (A→B) oluştuğunu kanıtla (kısa zaman penceresi).
- Grafana doğrulaması:
  - Service graph paneli/topoloji görünümü aç.
  - Edge sayısı 0 ise: trace üretimi mi yok, yoksa pipeline mı eksik? ayır.

## Common mistakes
- `service.name` yok/yanlış: tüm graph “unknown” olur veya hiç çıkmaz.
- Sampling çok agresif: edge’ler seyrek görünür.

## References
- `skills/obs-tempo-sampling-strategy`
- `skills/obs-tempo-grafana-datasource`
