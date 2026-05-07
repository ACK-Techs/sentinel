---
name: obs-prometheus-multi-tenancy
description: Prometheus metriklerinde tenant/ekip/ortam izolasyonu tasarlamak gerektiğinde kullan. “tek Prometheus’ta çok tenant”, “tenant label standardı”, “kimin neyi sorgulayacağı”, “yanlış tenant verisi karışıyor” gibi konularda **label ve erişim modeli** üretir.
---

## Purpose
Bu skill’in çıktısı:
- Tenant kimliği için **tek bir label kontratı** (örn. `tenant`, `team`, `env`)
- İzolasyon yaklaşımı seçimi: tek Prometheus + label, ayrı Prometheus per tenant, veya remote backend’de gerçek multi-tenancy
- Tenant-aware sorgu ve dashboard guardrail’leri (yanlışlıkla cross-tenant görünmesin)

## Workflow
- Önce “izolasyon seviyesi”ni seç (Prometheus’un sınırlarını açık tut):
  - **Soft izolasyon**: tek Prometheus + `tenant=` label + dashboard/query kuralları.
  - **Hard izolasyon**: tenant başına ayrı Prometheus (veri fiziksel ayrılır).
  - **Gerçek multi-tenancy**: remote backend (Cortex/Mimir vb.) tenant header/namespace ile.
- Tenant label kontratı yaz:
  - Label adı(ları): 1–2 adet; çoğaltma.
  - Değer kaynağı: instrumentation mı, scrape relabel mı? (tercihen instrumentation)
  - Boş/unknown değeri nasıl ele alınacak? (reject/drop)
- Karışmayı önle (en çok hata burada):
  - Scrape tarafında tenant label’ı garanti et (yoksa “drop” et).
  - Federation/remote_write kullanıyorsan, upstream/downstream label çakışmasını ele al.
- Sorgu ve dashboard guardrail’leri:
  - Her dashboard’da tenant değişkeni zorunlu olsun (varsayılan “all” yapma).
  - Recording rule’ları tenant label’ı düşürmeyecek şekilde tasarla (aksi halde çapraz tenant birleşir).
- Doğrulama:
  - Aynı metriği iki tenant için çek: label ayrımı gerçekten var mı?
  - “Tenant yok” seriler düşüyor mu yoksa sızıyor mu?

## Common mistakes
- Tenant’ı namespace ile “varsaymak”: cross-namespace scrape/relabel durumlarında karışır.
- Recording rule’larda tenant label’ını düşürmek: veri kalıcı olarak birleşir.

## References
- `skills/obs-prometheus-remote-write`
- `skills/obs-prometheus-federation`
