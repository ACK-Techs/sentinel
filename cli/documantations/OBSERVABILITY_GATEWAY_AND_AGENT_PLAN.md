# Observability Gateway ve Agent Planı

Bu dosya, eski Faz 3/4 planlarının yerine geçen **tek aktif plan** dokümanıdır.

Amaç iki parçadır:

1. Tamamlanan işi tek yerde özetlemek
2. Sentinel CLI ajanının `observability-gateway` üzerinden canlı veri kullanma entegrasyonunu özetlemek

## Tamamlanan Durum

Bu repo turunda 3 ayrı prompt hattı ile şu entegrasyon tamamlandı:

- Yeni ürün: `sentinel-coming/observability-gateway/`
- Gateway, Prometheus + Loki + Tempo için tek read-only giriş noktası sağlıyor
- Gateway kendi bearer token doğrulamasını yapıyor
- Gateway secret-safe hata modeli dönüyor
- Sentinel CLI artık backend URL’lerini doğrudan bilmeden gateway’e bağlanıyor
- Yeni CLI komutları var:
  - `sentinel-cli obs metric`
  - `sentinel-cli obs logs`
  - `sentinel-cli obs traces`
- Agent `run/repl` akışı yeni read-only gateway tool'larini kullanabiliyor:
  - `obs_metric_query`
  - `obs_logs_query`
  - `obs_traces_search`
  - `obs_trace_get`
- Agent session icine secret-safe kisa observability snapshot giriyor:
  - gateway health
  - configured backend listesi
  - reachable backend listesi
- `doctor` çıktısı gateway sağlığını gösteriyor
- `test-platform/scripts/run_cos_stack_check.sh` canlı smoke akışında:
  - test-platform servislerini kaldırıyor
  - gateway’i başlatıyor
  - CLI `obs` komutlarını gerçek veriyle doğruluyor
  - CLI `run` akışında agent tool entegrasyonunu doğruluyor

## Mevcut Mimari

```text
Sentinel CLI
    |
    v
observability-gateway
    |------> Prometheus
    |------> Loki
    \------> Tempo
```

Kural:

- CLI doğrudan Prometheus/Loki/Tempo konuşmaz
- Backend’e özel sorgu biçimleri mümkün olduğunca gateway içinde tutulur
- Gateway read-only kalır

## Bu Turda Bilinçli Olarak Yapılmayanlar

- Gateway üzerinden write / admin işlemleri
- Alert yönetimi
- Dashboard yönetimi
- Grafana datasource proxy katmanı

## Tamamlanan Agent Entegrasyonu

Bu tur sonunda agent artik `run` ve `repl` akışında gerektiğinde gateway tool'larini cagirabilir.

Başka deyişle:

- Kullanıcı `sentinel-cli obs ...` diyerek ham veri alabilir
- Kullanıcı `sentinel-cli run "orders servisinde ne bozuk?"` dediğinde ajan gateway araçlarını kullanabilir

## Operasyonel Baglam

REPL veya tek seferlik ajan turu baslamadan once session'a kisa bir snapshot eklenir:

- gateway health
- hangi backend’ler reachable
- hangi backend configured

Bu snapshot:

- secret-safe olur
- session’a kısa JSON özet olarak girer
- canlı veri yerine “durum çerçevesi” verir

## UX Kuralı

Ajan şu ayrımı korur:

- `doctor` = bağlantı ve sağlık özeti
- `obs ...` = kullanıcı kontrollü ham veri
- `run/repl` = gerektiğinde gateway tool kullanarak yorumlama

## Test ve Smoke

Doğrulama yüzeyi:

- unit testler
- CLI agent loop testleri
- `run_cos_stack_check.sh` içinde agentik kullanım adımı

Operator dostu manuel smoke:

```bash
cd sentinel-coming/test-platform
./scripts/run_cos_stack_check.sh
```

## Kabul Kriteri

Bu tur sonunda karsilanan kriterler:

- ajan gateway tool’larını çağırabiliyor olmalı
- gateway dışında doğrudan backend HTTP çağrısı eklenmemeli
- `run` veya `repl` içinde en az bir canlı observability teşhis akışı çalışmalı
- smoke akışında bu davranış doğrulanmalı

## Korunacak Teknik Referanslar

Eski faz planları kaldırıldı; ama aşağıdaki teknik referanslar yaşamaya devam eder:

- `ARCHITECTURE_AGENTIC_CLI.md`
- `IMPLEMENTATION_PLAN_PHASE2.md`
- `GRAFANA_HTTP_PHASE4.md`
- `GRAFANA_AI_PLATFORM_RESEARCH.md`
- `LLM_PROVIDERS.md`

## Durum

Aktif durum:

- gateway + CLI `obs` entegrasyonu tamam
- agent/repl canli veri entegrasyonu tamam
- smoke ve dokumantasyon bu davranisla hizali
