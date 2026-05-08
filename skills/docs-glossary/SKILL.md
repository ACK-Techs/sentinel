---
name: docs-glossary
description: "Sentinel projesine özgü terimler glossary'si oluşturur ve tüm dokümanlarda terim tutarlılığını sağlar"
---

## Purpose
Sentinel ekibinde "service mesh", "trace", "anomaly", "chaos" gibi terimlerin farklı anlamlarda kullanılması iletişim kopukluğuna yol açar. Bu skill, projeye özgü terim sözlüğünü oluşturur, terimlerin dokümanlardaki kullanımını standart hale getirir.

## Workflow

### 1. Glossary dosyası yapısı
```
sentinel-coming/
└── documentations/
    └── glossary.md
```

### 2. Glossary şablonu
```markdown
# Sentinel Proje Glossary'si

Alfabetik sıra. Her terim: kısa tanım + Sentinel bağlamındaki kullanım + ilgili linkler.

---

## A

### Anomaly (Anomali)
Sentinel bağlamında: gözlemlenebilirlik metriklerinde (latency, error rate, memory) beklenen banttan sapma.  
Sentinel'in anomaly detector'ı bu sapmaları tespit eder.  
Bkz: `documentations/adr/0003-anomaly-detection-strategy.md`

---

## C

### Chaos Profile (Kaos Profili)
Target servislere `/admin/chaos` endpoint'i aracılığıyla uygulanan hata enjeksiyon konfigürasyonu.  
Önceden tanımlı profiller: `normal`, `degraded`, `outage`, `slow-burn`, `spike`.  
Bkz: `skills/target-app-chaos-api`

### COS (Canonical Observability Stack)
Prometheus, Grafana, Loki, Tempo ve OTel Collector'dan oluşan Juju charm tabanlı gözlemlenebilirlik yığını.  
Bkz: `skills/cos-bundle-overview`

### Correlation ID
Dağıtık bir işlemi tüm servisler arasında izlemek için kullanılan benzersiz tanımlayıcı.  
Sentinel'de W3C `traceparent` header'ı trace ID olarak kullanılır.

---

## E

### Error Budget (Hata Bütçesi)
SLO'nun izin verdiği toplam hata miktarı. %99.9 availability SLO → aylık 43.8 dakika hata bütçesi.  
Bkz: `skills/platform-slo-framework`

---

## G

### Ground Truth (Gerçek Değer)
Anomali tespitinin kalitesini değerlendirmek için kullanılan referans etiket verisi.  
Chaos injection zamanlamalarından ve servis log'larından otomatik üretilir.  
Bkz: `skills/target-app-ground-truth-annotator`

---

## S

### Saga Pattern
Dağıtık işlemlerde her adımın bağımsız olduğu ve başarısız adımın compensating transaction ile geri alındığı pattern.  
Orders servisi saga orchestrator rolündedir.  
Bkz: `skills/target-app-orders-simulation`

### Span
OpenTelemetry'de tek bir işlem birimini temsil eden yapı. Trace içinde parent-child hiyerarşisi oluşturur.

### SLI / SLO / SLA
- **SLI** (Service Level Indicator): ölçülen metrik (ör. %99.5 başarılı istek)
- **SLO** (Service Level Objective): hedef değer (ör. SLI ≥ %99.9)
- **SLA** (Service Level Agreement): müşteri ile sözleşme

---

## T

### Target App (Hedef Uygulama)
Sentinel'in anomali tespitini test etmek için kullanılan FastAPI tabanlı demo servisler topluluğu.  
Servisler: gateway, orders, payments, inventory, worker.

### Toil
Site Reliability Engineering'de: değer üretmeyen, manuel, tekrarlayan operasyonel iş.  
Bkz: `skills/platform-toil-reduction`

### Trace ID
Bir dağıtık işlemi başından sonuna kadar takip eden 128-bit benzersiz tanımlayıcı.  
W3C Trace Context standardına göre `traceparent` header'ında taşınır.
```

### 3. Terim tutarlılığı kontrolü
```bash
# Farklı yazım varyantlarını bul
grep -rin "error budget\|error-budget\|hata bütçesi" documentations/ | \
  grep -v glossary.md

# Yanlış kısaltmaları bul
grep -rn "\bSRE\b" documentations/ | grep -v "glossary\|Site Reliability"
```

### 4. Otomatik glossary linki ekleme
```python
# scripts/link_glossary.py
# Dokümantasyon dosyalarında glossary terimlerini otomatik linkle
import re, json

terms = json.load(open("documentations/glossary_terms.json"))  # {term: anchor}
for doc_file in glob.glob("documentations/**/*.md", recursive=True):
    if "glossary" in doc_file: continue
    content = open(doc_file).read()
    for term, anchor in terms.items():
        link = f"[{term}](../glossary.md#{anchor})"
        content = re.sub(rf'\b{term}\b(?!\])', link, content, count=1)
    open(doc_file, 'w').write(content)
```

## Common mistakes
1. Teknik terimleri tanımlarken başka teknik terimler kullanmak — yeni katılımcı yine anlamaz.
2. Glossary'yi sadece bir kere oluşturup hiç güncellemememk — yeni kavramlar (yeni charm, yeni pattern) eklenmeli.
3. Aynı kavram için iki farklı terim kullanmak — "anomaly" ve "irregularity" aynı şey mi? Glossary bağlar.
4. İngilizce ve Türkçe karışık kullanmak — Sentinel dokümantasyonunda hangi dilin kullanılacağı tutarlı olmalı.

## References
- `skills/docs-adr-workflow`
- `skills/docs-contributing-guide`
