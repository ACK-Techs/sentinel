---
name: obs-prometheus-backup-restore
description: Prometheus TSDB verisini yedeklemek veya geri yüklemek gerektiğinde kullan. “TSDB snapshot”, “data dir kopyalama”, “WAL tutarlılığı”, “restore sonrası veri eksik/bozuk” gibi pratik restore senaryolarında **adım adım** prosedür üretir.
---

## Purpose
Bu skill’in çıktısı:
- Backup kapsamı ayrımı: **TSDB data** (blocks+WAL) vs **config/rules** (ayrı yedeklenir)
- Güvenli backup prosedürü (tutarlılık riskini minimize ederek)
- Restore sonrası doğrulama: “veri var mı, gap var mı, cardinality patladı mı?”

## Workflow
- Önce hedefi netleştir:
  - DR için tam geri dönüş mü, yoksa “adli inceleme / geçmiş veri” mi?
  - Prometheus’u aynı kimlikle mi ayağa kaldıracaksın (label’lar) yoksa yeni bir instance mı?
- Backup stratejisi seç:
  - **En güvenlisi**: Prometheus’u kısa süre durdurup data dir’i kopyalamak (tutarlılık en iyi).
  - Çalışırken kopyalama: WAL/compaction nedeniyle riskli; bunu açıkça “riskli” diye işaretle.
- Neyi yedekleyeceğini ayır:
  - TSDB: `data/` (blocks) + `wal/`
  - Konfig: `prometheus.yml`, rule dosyaları/CRD’ler, scrape/SD kaynakları (file SD dosyaları)
- Restore:
  - Boş bir data dir’e restore et (mevcut data ile karıştırma).
  - İlk açılışta WAL replay süresi uzayabilir; disk ve CPU planla.
  - Aynı “external labels”/instance kimliği ile mi çalışacak? (federation/remote backend çakışması)
- Restore sonrası doğrulama:
  - Prometheus up mı, TSDB okuyor mu?
  - Basit sorgu: `up` ve geçmiş aralıkta birkaç kritik seri.
  - TSDB boyutu ve series/head davranışı normal mi? (anormal artış varsa label sorunu olabilir)

## When NOT to do this
- Uzun süreli saklama gerekiyorsa: TSDB kopyalamak yerine `remote_write` + remote backend düşün (operasyonel olarak daha sürdürülebilir).

## References
- `skills/obs-prometheus-storage-tsdb`
- `skills/obs-prometheus-remote-write`
