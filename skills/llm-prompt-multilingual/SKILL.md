---
name: llm-prompt-multilingual
description: "Çok dilli kullanıcı girdisini işlemek veya farklı dillerde yanıt üretmek gerektiğinde; dil tespiti, yönlendirme ve lokalizasyon stratejisi için kullan"
---

## Purpose
Çok dilli sistemlerde LLM, dili tespit edip o dilde yanıt vermelidir. Yanlış dil tespiti veya tutarsız kod-switching kullanıcı deneyimini bozar. Bu skill dil yönetimi katmanını kapsar.

## Workflow

### Dil Tespiti
```python
def detect_language(text: str) -> str:
    """LLM ile dil tespiti — kısa metinler için daha güvenilir."""
    resp = llm.complete(
        system="Yalnızca ISO 639-1 dil kodunu döndür (tr, en, de, fr, ar, ...).",
        user=f"Bu metnin dili nedir: '{text[:200]}'"
    )
    return resp.strip().lower()[:2]

# veya langdetect kütüphanesi (hızlı)
from langdetect import detect as detect_lang_lib
```

### Dil Yönlendirme Sistemi
```python
SYSTEM_BY_LANG = {
    "tr": "Türkçe yanıt ver. Teknik terimleri Türkçe açıkla.",
    "en": "Respond in English. Use technical terminology appropriately.",
    "de": "Antworte auf Deutsch. Fachbegriffe auf Englisch sind akzeptabel.",
}

def get_system_for_lang(lang: str) -> str:
    return SYSTEM_BY_LANG.get(lang, SYSTEM_BY_LANG["en"])
```

### Explicit Dil Yönlendirme
```
GÖREV: Kullanıcının mesajındaki dili tespit et ve AYNI DİLDE yanıt ver.
Kullanıcı Türkçe yazıyorsa Türkçe, İngilizce yazıyorsa İngilizce yanıt ver.
Dil karıştırma. Teknik terimler için kaynak dildeki standart terimi kullan.
```

### Lokalizasyon: Tarih, Para Birimi
```python
LOCALE_HINTS = {
    "tr": "Tarihler DD.MM.YYYY formatında, para birimi TRY",
    "en": "Dates in MM/DD/YYYY, currency USD unless specified",
    "de": "Datumsformat DD.MM.YYYY, Währung EUR",
}
```

### Çeviri Görevi Promptu
```
{source_text}

Yukarıdaki metni {target_lang} diline çevir.
- Anlam öncelikli, kelimesi kelimesine çeviri değil
- Teknik terimler için hedefteki yaygın kullanımı tercih et
- Kültürel referanslar için eşdeğer yerel ifade kullan
```

## Common mistakes
- Dil tespitini kısa metinlerde (< 20 karakter) güvenilir saymak — fallback ekleyin.
- Sistem promptunu sabit İngilizce yazıp "Türkçe yanıt ver" eklemek — model İngilizce düşünüp tercüme eder.
- Sağdan sola (RTL) dillerde (Arapça, Farsça) UI tarafında LTR render etmek — CSS dir="rtl" gerekli.
- Teknik terimleri hedef dilde zorla çevirmek — "API" Türkçede de "API"dir.

## References
- `skills/llm-prompt-system-design`
- `skills/llm-prompt-classification`
