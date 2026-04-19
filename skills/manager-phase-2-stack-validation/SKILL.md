---
name: manager-phase-2-stack-validation
description: >-
  Sentinel Faz 2 yöneticisi: microk8s + Juju COS stack'inin (Prometheus, Loki,
  Tempo, Grafana, Alertmanager) açık cluster üzerinde doğrulanmasını planlar ve
  alt-AI prompt'larına böler. Faz 1 target-app'inin sinyallerinin uçtan uca
  göründüğünü kanıtlar. "COS doğrulama", "Grafana dashboard kontrol",
  "log-trace korelasyon", "Tempo arama" gibi konularda tetiklenir.
---

## Purpose

Bu skill yönetici ajan içindir; doğrudan kod yazmaz, alt-AI prompt'u üretir.
Faz 2'nin hedefi, halihazırda kurulu COS stack'inin Faz 1 target-app'i ile
uçtan uca çalıştığını doğrulamaktır. Yeni bileşen geliştirilmez, yalnız
entegrasyon ve gözlemlenebilirlik kanıtlanır.

## Scope (In / Out)

In:
- microk8s cluster ve Juju COS bundle sağlık kontrolü
- Prometheus scrape, Loki log pipeline, Tempo trace ingest, Grafana datasource
- RED metrics + log↔trace korelasyon + Tempo trace arama E2E smoke
- Faz 1 senaryolarının sinyal beklentileriyle eşleştirilmesi

Out:
- Yeni servis veya telemetri üretici geliştirme
- Sentinel CLI (Faz 3)
- Target-app kod değişikliği (Faz 1'e devredilir)

## Deliverables / Exit Criteria

- `juju status` ve relations beklenen active/idle durumda.
- Grafana'da target-app için RED metrics dashboard canlı veri gösterir.
- Log↔trace korelasyonu (trace_id ile Loki→Tempo atlama) çalışır.
- Tempo'da trace id ile arama ve servis bazlı sorgu sonuç döner.
- Her senaryo (6 tanesi) başlatıldığında ilgili sinyaller beklendiği gibi belirir;
  sonuçlar kısa doğrulama raporunda dondurulur.

## Sub-task Breakdown Template

1. **Cluster health + relations check**: microk8s node/pod sağlığı, COS charm
   relations, datasource bağlantıları.
2. **Signal ingestion doğrulama**: metric, log, trace için ayrı ayrı smoke
   (örnek sorgu + beklenen alan listesi).
3. **Senaryo-bazlı E2E smoke**: 6 Faz 1 senaryosunun tetiklenmesi ve sinyal
   imzalarının Grafana/Loki/Tempo'da doğrulanması.

Her alt göreve: komut örneği, beklenen çıktı şekli, başarısızlık halinde
raporlama formatı verilir.

## Key References

- `sentinel-coming/documantations/ARCHITECTURE_COS.md`
- `sentinel-coming/skills/cos-deploy-*`
- `sentinel-coming/skills/cos-relation-*`
- `sentinel-coming/documantations/PHASE*_SKILL_AND_DOC_INDEX.md`

## Risks

- Stack'in partial-degraded durumda "çalışıyor" sanılması; her sinyal tipi ayrı doğrulanmalı.
- Tempo sampling kaybı: baseline trafikte örnekleme oranı kontrol edilir.
- Loki label cardinality'sinin Faz 1 etiketleriyle çelişmesi.
- Relations sessizce düşerse alarm üretmeyebilir; `juju status` zorunlu adımdır.

## Coordination Checkpoints

- Alt görev 1 yeşile dönmeden 2'ye geçilmez.
- Alt görev 2'nin çıktısı (örnek sorgu seti) Faz 3 CLI sorgu katmanına girdi olur.
- Senaryo doğrulamalarında sapma varsa Faz 1'e düzeltme prompt'u olarak geri
  gönderilir; Faz 2 skill'i kendi içinde patch yapmaz.
