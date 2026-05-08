---
name: llm-prompt-critique-revision
description: "LLM çıktısını aynı veya farklı modele eleştirtip revize ettirmek gerektiğinde; tek geçişte düşük kalite elde edilen yazı, kod veya analiz görevlerinde kullan"
---

## Purpose
Critique-Revision pipeline, modelin kendi çıktısını değerlendirmesini ve iyileştirmesini sağlar. Bu, tek geçişe kıyasla daha yüksek kaliteli çıktı üretir; özellikle uzun metin, karmaşık kod ve çok kriterli değerlendirmelerde etkilidir.

## Workflow

### İki Aşamalı Pipeline
```python
def critique_and_revise(task: str, initial_output: str, criteria: list[str]) -> str:
    # Aşama 1: Eleştiri
    criteria_text = "\n".join(f"- {c}" for c in criteria)
    critique_prompt = f"""Aşağıdaki çıktıyı şu kriterlere göre eleştir:
{criteria_text}

Çıktı:
{initial_output}

Her kriter için: [İYİ/GELİŞTİRİLEBİLİR/ZAYIF] ve gerekçe yaz."""

    critique = llm.complete(critique_prompt)
    
    # Aşama 2: Revizyon
    revision_prompt = f"""Orijinal görev: {task}

Mevcut çıktı:
{initial_output}

Eleştiri:
{critique}

Eleştiriyi dikkate alarak çıktıyı yeniden yaz. Yalnızca revize edilmiş versiyonu ver."""

    return llm.complete(revision_prompt)
```

### Öz-Eleştiri (Self-Critique)
```
Yukarıdaki yanıtını şu açılardan değerlendir:
1. Doğruluk: Faktüel hata var mı?
2. Eksiklik: Önemli bir nokta atlandı mı?  
3. Netlik: Kullanıcı için anlaşılır mı?

Değerlendirmeni [SORUN] ve [ÖNERI] etiketleriyle yaz, ardından
iyileştirilmiş versiyonu [REVİZYON] bloğunda sun.
```

### Kod Revizyonu Örneği
```python
CRITIQUE_CRITERIA_CODE = [
    "Hata yönetimi eksiksiz mi?",
    "Edge case'ler ele alındı mı?",
    "Performans iyileştirme fırsatı var mı?",
    "Güvenlik açığı (injection, path traversal) mevcut mu?",
    "Type annotation'lar doğru mu?",
]
```

### Ne Zaman Durulur?
```python
MAX_REVISIONS = 3
quality_score = evaluate(output)  # LLM-as-judge ile puanla
if quality_score >= 0.85 or revision_count >= MAX_REVISIONS:
    break
```

## Common mistakes
- Eleştiriyi sonraki turu için contexte eklemeden revizyon istemek — model önceki sorunları bilmez.
- Sınırsız döngü kurmak — 2-3 turdan sonra getiri azalır.
- Çok genel eleştiri kriterleri vermek — "iyi mi?" yerine spesifik kriterler daha etkili.
- Eleştiri ile revizyonu aynı promptta istemek — ayrı çağrılar daha temiz sonuç verir.

## References
- `skills/llm-eval-llm-as-judge`
- `skills/llm-prompt-chain-of-thought`
