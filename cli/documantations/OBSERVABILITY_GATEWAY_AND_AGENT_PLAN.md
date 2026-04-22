# Observability Gateway ve Agent Planı

Bu dosya, eski Faz 3/4 planlarının yerine geçen **tek aktif plan** dokümanıdır.

Amaç iki parçadır:

1. Tamamlanan işi tek yerde özetlemek
2. Bir sonraki turda Sentinel CLI ajanının `observability-gateway` üzerinden canlı veri kullanmasını planlamak

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
- `doctor` çıktısı gateway sağlığını gösteriyor
- `test-platform/scripts/run_cos_stack_check.sh` canlı smoke akışında:
  - test-platform servislerini kaldırıyor
  - gateway’i başlatıyor
  - CLI komutlarını gerçek veriyle doğruluyor

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
- Ajanın doğal dil turunda gateway verisini otomatik kullanması

## Sonraki Hedef

Bir sonraki iş, mevcut `obs` alt komutlarını büyütmek değil; **ajanın kendisini** gateway üzerinden canlı veri okuyabilir hale getirmektir.

Başka deyişle:

- Bugün: kullanıcı `sentinel-cli obs ...` diyerek veri alıyor
- Sonraki tur: kullanıcı `sentinel-cli run "orders servisinde ne bozuk?"` dediğinde ajan gateway araçlarını kullanabiliyor

## Sonraki Faz Planı

### 1. Gateway Tool Yüzeyi

CLI ajanı için read-only tool yüzeyi eklenir:

- `obs_metric_query`
- `obs_logs_query`
- `obs_traces_search`
- `obs_trace_get`

Kurallar:

- Bu tool’lar doğrudan backend değil sadece gateway çağırır
- Token veya hassas header model çıktısına düşmez
- Gateway kapalıysa ajan anlamlı kısa hata verir

### 2. Agent Döngüsüne Entegrasyon

`run` ve `repl` akışında ajan gerektiğinde bu tool’ları çağırabilir hale getirilir.

Beklenen kullanıcı örnekleri:

- `orders servisinde hata var mi bak`
- `gateway loglarinda son 5 dakikayi ozetle`
- `orders trace tarafinda timeout izi var mi`

### 3. Kısa Operasyonel Bağlam

REPL veya tek seferlik ajan turu başlamadan önce opsiyonel kısa snapshot eklenir:

- gateway health
- hangi backend’ler reachable
- hangi backend configured

Bu snapshot:

- secret-safe olur
- session’a kısa JSON özet olarak girer
- canlı veri yerine “durum çerçevesi” verir

### 4. UX Kuralı

Ajan şu ayrımı korur:

- `doctor` = bağlantı ve sağlık özeti
- `obs ...` = kullanıcı kontrollü ham veri
- `run/repl` = gerektiğinde gateway tool kullanarak yorumlama

### 5. Test ve Smoke

Sonraki turda başarı kriteri:

- unit testler
- CLI agent loop testleri
- mevcut `run_cos_stack_check.sh` içine agentik kullanım adımı eklenmesi

Örnek smoke:

```bash
python -m sentinel_cli run --profile local "gateway ve orders tarafinda son durumu ozetle"
```

## Kabul Kriteri

Bir sonraki tur “tamamlandı” sayılmak için:

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
- sonraki adım agent/repl canlı veri entegrasyonu
