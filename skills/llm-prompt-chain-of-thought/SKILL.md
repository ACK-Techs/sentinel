---
name: llm-prompt-chain-of-thought
description: "Modelin adım adım düşünerek doğru sonuca ulaşmasını istediğinde; matematiksel akıl yürütme, çok adımlı karar ve karmaşık analiz görevlerinde kullan"
---

## Purpose
Chain-of-Thought (CoT), modeli ara adımları göstererek düşündürür. Tek adım cevap yerine akıl yürütme zinciri oluşturulur. Bu, doğruluğu artırır ama token tüketimini yükseltir — üretim kararlarında denge gereklidir.

## Workflow

### Temel CoT Trigger
```
Soruyu çözmeden önce adım adım düşün, her adımı yaz.

Soru: Bir trenin 240 km mesafeyi 2 saat 30 dakikada aldığını biliyoruz.
Arabanın aynı mesafeyi %20 daha yavaş hızda aldığı kaç saattir?
```

### Yapılandırılmış CoT (Üretim İçin)
```python
SYSTEM = """Her analizi şu formatta yap:
<reasoning>
Adım 1: ...
Adım 2: ...
Adım N: ...
</reasoning>
<answer>
[Kısa kesin cevap]
</answer>
"""
```

### Zero-Shot CoT
```
"Let's think step by step." → modeli CoT moduna geçirir
"Türkçe: Adım adım düşünelim."
```

### Few-Shot CoT (Güvenilirlik için)
```
S: 5+3*2 nedir?
D:
Adım 1: Çarpma önce gelir → 3*2=6
Adım 2: Toplama → 5+6=11
Cevap: 11

S: 10-4/2 nedir?
D:
```

### Sentinel'de Kullanım
CoT'yi test ortamında `<reasoning>` bloğuyla açık tutun. Üretimde yalnızca `<answer>` bloğunu parse edin:
```python
import re
def extract_answer(text: str) -> str:
    m = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
    return m.group(1).strip() if m else text
```

## Common mistakes
- Basit lookup sorularında CoT kullanmak — gereksiz token harcar, gecikme artırır.
- Akıl yürütmeyi parse etmeden kullanıcıya aynen göndermek — verbose ve kafa karıştırıcı.
- "Adım adım düşün" deyip format belirtmemek — her model farklı format üretir.
- Temperature=0'da CoT beklemek — biraz varyasyon (0.1-0.3) daha zengin akıl yürütme üretir.

## References
- `skills/llm-prompt-system-design`
- `skills/llm-prompt-few-shot`
- `skills/llm-prompt-react-pattern`
