---
name: docs-runbook-template
description: "Sentinel operasyonları için standart runbook şablonu ve içerik standartları; olay müdahalesinde kullanılacak adım adım kılavuz"
---

## Purpose
Sentinel'de bir servis çöktüğünde veya anomali tespiti yanlış alarm verdiğinde, nöbetçi mühendis runbook'a bakarak dakikalar içinde müdahale edebilmeli. Bu skill, tutarlı, eyleme dönüştürülebilir runbook'lar üretmenin standart yolunu tanımlar.

## Workflow

### 1. Runbook dizin yapısı
```
sentinel-coming/
└── documentations/
    └── runbooks/
        ├── README.md
        ├── svc-orders-high-error-rate.md
        ├── svc-payments-latency-spike.md
        ├── cos-prometheus-disk-full.md
        ├── cos-loki-ingestion-stall.md
        └── infra-microk8s-node-notready.md
```

### 2. Runbook şablonu
```markdown
# Runbook: {Alert Adı}

**Servis**: {servis-adı}  
**Alert**: {Prometheus alert rule adı}  
**Severity**: P1 / P2 / P3  
**Son Güncelleme**: YYYY-MM-DD  
**Sahibi**: @kullanici  

---

## Özet
[Bu runbook hangi durumda kullanılır? 2-3 cümle.]

## Alert Koşulu
```promql
# Tetikleyen PromQL sorgusu
rate(http_requests_total{status=~"5..", service="orders"}[5m]) > 0.05
```

## Olası Nedenler
1. Veritabanı bağlantı havuzu doldu
2. Downstream payments servisi yanıt vermiyor
3. OOM killer pod'u öldürdü
4. Chaos middleware aktif

## Tanı Adımları

### Adım 1: Pod durumunu kontrol et
```bash
kubectl get pods -n sentinel-target -l app=orders
kubectl describe pod <pod-name> -n sentinel-target | tail -30
```
Beklenen: tüm pod'lar Running.  
Anormal: CrashLoopBackOff → OOM veya uygulama hatası.

### Adım 2: Hata oranını görselleştir
Grafana → Sentinel Overview → Orders Error Rate paneline git.

### Adım 3: Chaos state kontrol et
```bash
curl http://orders.sentinel-target.svc/admin/chaos | jq '.error_rate'
```
> 0 ise chaos tetiklenmiş → `POST /admin/chaos '{"error_rate":0}'` ile sıfırla.

### Adım 4: Log'lara bak
```bash
logcli query '{service="orders", level="error"}' --since=10m | head -20
```

## Müdahale Adımları

### Fix 1: Pod restart
```bash
kubectl rollout restart deployment/orders -n sentinel-target
kubectl rollout status deployment/orders -n sentinel-target
```

### Fix 2: Devre kesici (circuit breaker) sıfırlama
```bash
curl -X POST http://orders.sentinel-target.svc/admin/circuit-breaker/reset
```

## Olay Sonrası
- [ ] Post-mortem ticket aç: `skills/docs-post-mortem-template`
- [ ] Alert threshold doğru mu? Gürültülü ise ayarla.
- [ ] Runbook bu olaydan sonra güncellendi mi?
```

### 3. Runbook kalite kriterleri
Her runbook şu testleri geçmeli:
- [ ] Tüm komutlar kopyala-yapıştır çalışır (env var'lar belirtilmiş)
- [ ] Her adımın "beklenen çıktısı" yazılı
- [ ] Ortalama çözüm süresi (MTTR hedefi) belirtilmiş
- [ ] Son 3 ayda test edilmiş tarihi var

### 4. Runbook index otomasyonu
```bash
# README.md index'i güncelle
ls documentations/runbooks/*.md | grep -v README | while read f; do
  title=$(grep "^# Runbook:" "$f" | sed 's/# Runbook: //')
  severity=$(grep "^\*\*Severity\*\*" "$f" | sed 's/.*: //')
  echo "| [$title]($f) | $severity |"
done
```

## Common mistakes
1. "Log'lara bak" gibi muğlak adımlar yazmak — hangi log, hangi filtre, ne aranıyor belirt.
2. Runbook'u müdahale sırasında güncellemek — müdahale bittikten sonra güncelle, baskı altında hata yaratır.
3. Tek bir "Fix: her şeyi restart et" adımıyla geçiştirmek — restart neden çalışıyor, asıl neden nedir?
4. Runbook'u sentetik test etmemek — chaos ile alarmı tetikle ve runbook'u takip ederek çöz.

## References
- `skills/docs-post-mortem-template`
- `skills/platform-incident-management`
- `skills/target-app-chaos-api`
