---
name: llm-eval-hallucination-detect
description: LLM veya agent davranışını sayılaştırılmış metriklerle değerlendirmek, regresyon yakalamak ve ürün kararlarını ölçüme dayandırmak istendiğinde kullan.
---

## Değerlendirme hedefi
`llm-eval-hallucination-detect` konusu, model kalitesini sezgiden çıkarıp kanıta taşımayı hedefler. "Daha iyi hissettiriyor" yerine tekrarlanabilir benchmark, karar eşikleri ve regressionsız teslim hedeflenir.

## Değerlendirme planı
- **Soru seti üret:** gerçek Sentinel kullanımından gelen görevleri etiketli veri haline getir.
- **Rubrik tanımla:** doğruluk, güvenlik, format uyumu, araç çağrısı başarısı gibi boyutları net puanla.
- **Karşılaştırma koş:** baseline model/prompt ile aday model/prompt’u aynı veri üzerinde çalıştır.
- **Analiz et:** sadece ortalama skor değil, hata kümeleri ve kırılgan alt segmentleri incele.
- **Gate koy:** belirlenen eşiğin altına düşen sürümü merge veya release hattında engelle.

## Operasyonel pratik
- Değerlendirme dataseti versiyonlu olmalı (`v1`, `v2` ...).
- İnsan anotasyonu varsa anotatör uyumu (agreement) takip edilmeli.
- Maliyet ve gecikme metrikleri kalite skoruyla birlikte raporlanmalı.

## Sık görülen yanlışlar
- Tek benchmark sonucu ile ürün kararı almak.
- Sadece iyi sonuç örneklerini raporlamak.
- Tool-call başarısını yalnızca "çağırdı/çağırmadı" düzeyinde ölçmek.

## Skill-spesifik kararlar
- Hallucination tespitinde kaynakta olmayan iddialari ayiklayan kural seti tanimla. Kaynak-siz cevaplari dusuk guven modunda etiketle.

## Referanslar
- `cli/skills/agentic-testing-integration-mock-llm/SKILL.md`
- `cli/skills/agentic-testing-unit/SKILL.md`
- `cli/documantations/TESTING_GRAFANA.md`
- `cli/documantations/IMPLEMENTATION_PLAN_PHASE2.md`
