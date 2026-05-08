---
name: docs-post-mortem-template
description: "Sentinel olayları için blameless post-mortem raporu şablonu; kök neden analizi ve önleyici aksiyon takibi"
---

## Purpose
Post-mortem kültürü, Sentinel ekibinin aynı olayı tekrar yaşamamasını sağlar. Blameless yaklaşım bireyleri değil sistemsel nedenleri hedef alır. Bu skill, olay sonrası 48 saat içinde yazılacak post-mortem'in formatını ve review sürecini tanımlar.

## Workflow

### 1. Dizin yapısı
```
sentinel-coming/
└── documentations/
    └── post-mortems/
        ├── 2024-01-15-orders-outage.md
        ├── 2024-02-03-cos-loki-ingestion-stall.md
        └── template.md
```

### 2. Post-mortem şablonu
```markdown
# Post-Mortem: {Olay Başlığı}

**Tarih**: YYYY-MM-DD  
**Severity**: P1 / P2  
**Süre**: {başlangıç} – {bitiş} ({toplam süre})  
**Hazırlayan**: @kullanici  
**Reviewer(lar)**: @kullanici2, @kullanici3  
**Durum**: Taslak | İncelemede | Tamamlandı  

---

## Özet
[2-3 cümle: ne oldu, ne kadar etkilendi, nasıl düzeldi]

## Etki
- **Kullanıcı etkisi**: X kullanıcı Y özelliğe erişemedi
- **Servis etkisi**: orders servisi %85 error rate, 23 dakika
- **İş etkisi**: ~150 başarısız sipariş (saga ile telafi edildi/edilmedi)

## Zaman Çizelgesi
| Zaman (UTC) | Olay |
|-------------|------|
| 10:05:23 | orders pod'u OOMKilled — ilk restart |
| 10:05:45 | Prometheus alert tetiklendi (P1) |
| 10:07:00 | Nöbetçi PagerDuty'den uyarı aldı |
| 10:12:00 | orders servisi tanımlandı, chaos state kontrol edildi |
| 10:18:00 | Memory limit artırıldı, deployment restart |
| 10:28:00 | Servis tamamen düzeldi, hata oranı sıfırlandı |

## Kök Neden Analizi (5-Why)

**Belirti**: orders pod'u OOMKilled ile yeniden başladı

1. Neden? → Python process bellek limitini aştı (512Mi)
2. Neden? → SQLAlchemy connection pool beklenmedik şekilde büyüdü
3. Neden? → Connection `pool_pre_ping=True` ile her request'te yeni bağlantı açılıyordu
4. Neden? → `pool_size` varsayılan 5 iken concurrent request 200'e çıktı
5. Neden? → Load test öncesi capacity review yapılmadı

**Kök neden**: Connection pool konfigürasyonu load test senaryosu için ayarlanmamıştı.

## Katkıda Bulunan Faktörler
- Memory limit son 6 aydır güncellenmemişti
- Load test uyarısı ekip içinde paylaşılmamıştı
- Alerting threshold çok geç tetiklendi (5 dakika)

## Neler İyi Gitti
- Saga pattern stok tutarsızlığını önledi
- Grafana dashboard hızlı tanıya yardımcı oldu
- Runbook takip edildi, rollback temiz yapıldı

## Aksiyon Planı
| # | Aksiyon | Sahip | Son Tarih | Durum |
|---|---------|-------|-----------|-------|
| 1 | SQLAlchemy pool_size ve max_overflow parametrelerini tune et | @dev1 | 2024-01-22 | Açık |
| 2 | Load test öncesi capacity review checklist oluştur | @dev2 | 2024-01-25 | Açık |
| 3 | OOM alert threshold'u 5m'den 2m'ye düşür | @dev1 | 2024-01-18 | Tamamlandı |
| 4 | Memory rightsizing runbook'u güncelle | @dev3 | 2024-01-20 | Açık |

## Blameless Prensip
Bu dokümanda hiçbir kişisel eleştiri yer almaz. Tüm aksiyonlar sistemsel iyileştirmeyi hedefler.
```

### 3. Post-mortem review süreci
1. **0-24 saat**: Olay sahibi taslak yazar, zaman çizelgesi doldurulur
2. **24-48 saat**: Etkilenen ekip üyeleri yorum ekler, kök neden üzerinde uzlaşılır
3. **48-72 saat**: Aksiyonlar ticket'lara dönüştürülür (GitHub Issues / Jira)
4. **Haftalık**: Aksiyon kapatma toplantısı

### 4. Metrik takibi
```bash
# Açık post-mortem aksiyonlarını say
grep -l "Açık" documentations/post-mortems/*.md | wc -l

# Ortalama MTTR hesapla
grep "Süre:" documentations/post-mortems/*.md
```

## Common mistakes
1. Post-mortem'i 1 haftadan sonra yazmak — detaylar ve duygusal hafıza solmaya başlar.
2. "Birisi test etmedi" gibi kişi odaklı ifadeler kullanmak — blameless ihlal eder.
3. Aksiyon planındaki maddeleri ticket'a dönüştürmemek — takip edilemez, kapanmaz.
4. "Neler iyi gitti" bölümünü atlamak — post-mortem sadece hata analizi değil, öğrenme döngüsüdür.

## References
- `skills/platform-incident-management`
- `skills/docs-runbook-template`
