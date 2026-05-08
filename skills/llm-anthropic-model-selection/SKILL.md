---
name: llm-anthropic-model-selection
description: "Claude model ailesindeki Opus, Sonnet ve Haiku arasında göreve uygun modeli seçmek; maliyet, hız ve yetenek trade-off'larını değerlendirmek gerektiğinde kullan."
---

## Purpose
Yanlış model seçimi ya gereksiz maliyet ya da yetersiz kalite üretir. Görev türüne göre model seçimi bütçe ve kullanıcı deneyimini doğrudan etkiler.

## Model ailesi (2025)

| Model | Güçlü yan | Tipik kullanım |
|---|---|---|
| `claude-opus-4-7` | En yüksek zeka, extended thinking | Karmaşık analiz, araştırma, stratejik planlama |
| `claude-sonnet-4-6` | Yetenek/maliyet dengesi | Üretim uygulamaları, kod, genel görevler |
| `claude-haiku-4-5` | En hızlı ve ucuz | Sınıflandırma, basit Q&A, yüksek hacim |

## Karar çerçevesi

**Opus kullan:**
- 100+ sayfalık belge analizi ve çıkarım
- Çok adımlı matematik/mantık problemleri
- Extended thinking gerektiren görevler
- Yanlış yanıtın maliyetinin yüksek olduğu durumlar

**Sonnet kullan:**
- API entegrasyonlu üretim servisleri (varsayılan tercih)
- Kod yazma ve review
- Çok turlu konuşma
- Tool use ağırlıklı agent

**Haiku kullan:**
- Sınıflandırma, etiketleme, sentiment analizi
- Kısa içerik üretimi ve basit dönüşüm
- Anlık yanıt gerektiren kullanıcı etkileşimleri
- Maliyet kritik yüksek hacim pipeline

## Hibrit yaklaşım
```python
# Önce Haiku ile filtrele, karmaşık vakayı Sonnet'a yönlendir
routing_response = quick_classify(query, model="claude-haiku-4-5-20251001")
if routing_response.needs_deep_analysis:
    final_response = analyze(query, model="claude-sonnet-4-6")
```

## Common mistakes
- Her görev için Opus kullanmak — 5x daha pahalı, çoğu görev için gereksiz.
- Haiku ile karmaşık çok adımlı görev çözdürmeye çalışmak — kalite düşer.
- Model seçimini değiştirip mevcut promptları test etmemek; farklı modeller farklı davranır.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-rate-limits`
- `skills/llm-anthropic-token-counting`
