---
name: llm-prompt-zero-shot
description: "Örnek göstermeden doğrudan görev tanımıyla LLM'den çıktı alınacağında; hızlı prototip veya genel amaçlı görevlerde kullan"
---

## Purpose
Zero-shot prompting, örnek olmadan yalnızca talimatla model yönlendirir. Hızlı prototipleme için idealdir; ancak tutarsız çıktı riski taşır. Doğru talimat yapısı bu riski azaltır.

## Workflow

### Etkili Zero-Shot Yapısı
```
[GÖREV]: Ne yapılacağı tek cümlede
[GİRDİ]: Ne verildiği
[FORMAT]: Çıktının nasıl olacağı
[KISITLAR]: Ne yapılmayacağı (opsiyonel)
```

### Uygulama Örneği
```
GÖREV: Aşağıdaki müşteri yorumunun duygusunu sınıflandır.
GİRDİ: "Ürün beklediğimden çok daha iyi çıktı, kesinlikle tavsiye ederim."
FORMAT: Yalnızca tek kelime: pozitif, negatif veya nötr
KISIT: Açıklama yapma, yalnızca kelimeyi yaz.
```

### Zero-Shot vs Few-Shot Karar Ağacı
```
Görev basit ve tanımlı mı?       → Zero-shot dene
Çıktı formatı karmaşık mı?       → Few-shot gerekebilir
Model daha önce bu görevi gördü mü?  → Zero-shot yeterli
Domain çok spesifik mi?          → Few-shot + RAG
```

### Calibration Test
```python
# Aynı görevi 5 farklı formülasyonla test et
variations = [
    "Sınıflandır: ...",
    "Aşağıdakinin duygusu nedir: ...",
    "Pozitif mi negatif mi: ...",
    "Sentiment analizi yap: ...",
    "Yorumun tonu: ...",
]
results = [model.complete(v) for v in variations]
# En tutarlı formülasyonu seç
```

## Common mistakes
- Zero-shot'ta format belirtmemek — model format icat eder.
- Çok genel talimat ("analiz et") vermek — "hangi boyutlarda analiz et" yazın.
- Zero-shot başarısız olduğunda hemen fine-tune'a atlamak — önce few-shot deneyin.
- Türkçe göreve İngilizce talimat vermek — dil tutarlılığı önemli.

## References
- `skills/llm-prompt-few-shot`
- `skills/llm-prompt-system-design`
