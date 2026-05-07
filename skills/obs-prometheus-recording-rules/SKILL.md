---
name: obs-prometheus-recording-rules
description: Prometheus’ta ağır/tekrarlı PromQL sorgularını kalıcı, ucuz sorgulanabilir yeni bir seri olarak “precompute” etmek gerektiğinde kullan. Özellikle dashboard panellerinde aynı agregasyon tekrar ediyorsa, kuralın `record:` adını ve label set’ini standartlaştırmak istiyorsan veya “recording rule nasıl tasarlanır?” diye soruluyorsa bu skill’e başvur.
---

## Purpose
Bu skill’in çıktısı, üretimde kullanılabilir bir **recording rule grubu**dur:
- `groups[].rules[].record` isimlendirmesi (aranabilir, stable)
- `expr` (orijinal PromQL’den türetilmiş, label’ları bilinçli)
- Kullanım notu: yeni kaydın hangi dashboard/alert sorgusunu basitleştirdiği

Amaç “PromQL’i kısaltmak” değil; **maliyetli hesaplamayı tek noktada sabitleyip** (tutarlı label set’iyle) panel/alert sorgularını güvenilir hale getirmektir.

## Workflow
- Girdi topla (netleştirilmeden kural yazma):
  - Kaynak sorgu(lar): mevcut panel/alert PromQL’i
  - Hedef kullanım: panel mi, alert mi, API client mı?
  - Beklenen boyut: hangi label’lar **kalmalı**, hangileri **atılmalı**?
- Kuralın “ürün kontratı”nı tasarla:
  - `record` adı: ölçtüğü şeyi anlat (ör. `job:request_latency_seconds:p95` gibi), **rastgele** ad verme.
  - Label set’i: downstream sorguların ihtiyacı olmayan label’ları bırakma (kardinaliteyi büyütür).
  - İsimlendirme kararı: `:` ayırıcılarını **hiyerarşi** gibi kullan (ekip içinde tutarlı ol).
- `expr`’i recording’e uygun hale getir:
  - “rate/irate/window” kararını yaz: hangi pencere ile stabilize ettin?
  - Aggregation’dan sonra label’ların beklenen setini kontrol et (örn. `sum by (job)`).
  - Gerekirse `label_replace` gibi operasyonları **en aza indir** (okunabilirlik/performans).
- Deploy şekline göre hedef formatı üret:
  - Bare Prometheus: `rule_files` + YAML rule dosyası
  - Operator/COS: `PrometheusRule` CRD (bu repo bağlamında operator yoksa sadece kural içeriğini üret)
- Doğrulama (kısa ama somut):
  - Kayıtlı seriyi sorgula: `<record_name>{...}` gerçekten geliyor mu?
  - Kaynak sorgu ile farkı kontrol et: aynı zaman aralığında yaklaşık eşleşiyor mu?
  - Dashboard’da kullanım örneği ver: “eski sorgu → yeni sorgu” (1 satır).

## Common mistakes
- Recording’i ham label patlamasıyla yapmak: “her label kalsın” yaklaşımı TSDB’yi büyütür.
- “Eksik label” sürprizi: downstream `by(...)` beklerken recording’de label’ları düşürmek.
- İlk dakikalarda “boş”: recording rule yeni seri üretir; geçmişi otomatik backfill etmez.

## References
- `skills/cos-deploy-prometheus`
- `skills/obs-prometheus-unit-testing`
