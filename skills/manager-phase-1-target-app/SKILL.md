---
name: manager-phase-1-target-app
description: >-
  Sentinel Faz 1 yöneticisi: Sentinel'in test platformu olan çok servisli FastAPI
  target-app'ini (gateway/orders/payments/inventory/worker + Postgres + Redis + OTEL
  push + chaos API + load generator + ground-truth annotator) planlar ve alt-AI
  prompt'larına böler. Kullanıcı "target-app", "sentinel-target", "chaos senaryo",
  "OTEL SDK push", "ground truth" gibi Faz 1 konularını açtığında tetiklenir.
---

## Purpose

Bu skill yönetici ajan içindir; doğrudan kod yazmaz, alt-AI prompt'u üretir.
Faz 1'in tek hedefi: Sentinel'in üstünde çalışacağı **kontrollü test platformu**nu
ayağa kaldırmak. Çıktı, kasıtlı arıza senaryoları üretebilen ve telemetri akıtan
bir mikroservis topolojisidir. Namespace: `sentinel-target`.

## Scope (In / Out)

In:
- FastAPI servisleri: gateway, orders, payments, inventory, worker
- Postgres + Redis bağımlılıkları, k8s manifest/Helm iskeletleri
- OTEL SDK entegrasyonu (yalnız OTLP/gRPC push; metric + log + trace)
- `/admin/chaos` runtime toggle API + YAML tabanlı senaryo profilleri
- Load generator + ground-truth annotator

Out:
- Prometheus scrape, ServiceMonitor, Promtail, `prometheus_client`
- COS/microk8s cluster kurulumu (Faz 2)
- Sentinel CLI (Faz 3)

## Deliverables / Exit Criteria

- Beş servis `sentinel-target` namespace'inde sağlıklı kalkar.
- OTLP endpoint'e metric/log/trace uçtan uca akar (cardinality kontrollü).
- Chaos profilleri YAML'dan yüklenip runtime'da uygulanabilir.
- Altı senaryo koşulur: downstream-outage, slow-db, memory-leak,
  cache-stampede, cascading, healthy-baseline.
- Her senaryo için ground-truth annotation dosyası üretilir ve doğrulanır.

## Sub-task Breakdown Template

1. **Observability lib + servis iskeletleri**: ortak OTEL SDK wrapper,
   4 FastAPI servisi + worker, Postgres/Redis bağlantıları, health endpoint'leri.
2. **Chaos API + load generator + senaryo YAML'leri**: `/admin/chaos` toggle,
   6 senaryonun YAML tanımı, trafik üretici profilleri.
3. **Ground-truth annotator + doğrulama**: senaryo koşumunda beklenen anomali
   pencerelerini yazan annotator, sonuç doğrulama scriptleri.

Her alt göreve: hedef dosya yolu, kabul kriteri, dokunulmayacak alan ve kısa
referans listesi verilir.

## Key References

- `sentinel-coming/documantations/PROJECT_ROOT.md`
- `sentinel-coming/documantations/IMPLEMENTATION_PLAN*.md`
- `sentinel-coming/documantations/PHASE1_SKILL_AND_DOC_INDEX.md`
- `sentinel-coming/skills/` (varsa target-app ile ilgili alt skill'ler)

## Risks

- Over-engineering: servisler sade kalmalı, gerçek iş mantığı değil arıza yüzeyi üretilir.
- OTEL cardinality patlaması: label seti sıkı tutulur, request-id gibi alanlar etiket yapılmaz.
- Chaos API'nin dışa açılması: sadece cluster içi, auth veya network policy ile kapalı.
- Kaynak limitleri: memory-leak senaryosu node'u boğmamalı, limits/requests net.

## Coordination Checkpoints

- Alt görev 1 biter bitmez OTLP akışı tek servisle doğrulanır; 2'ye geçilmez.
- Alt görev 2'de her senaryo YAML'ı eklenirken healthy-baseline bozulmamalı.
- Alt görev 3'ün çıktısı Faz 2 doğrulamasının girdisidir; format dondurulur.
- Kapsam dışı istekler (scrape, CLI) reddedilir, ilgili faza devredilir.
