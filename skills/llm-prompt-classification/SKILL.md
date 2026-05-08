---
name: llm-prompt-classification
description: "Metin sınıflandırma görevi için LLM prompt tasarlanacağında; kategori tanımları, sınır durumlar ve çıktı doğrulama dahil end-to-end yaklaşım için kullan"
---

## Purpose
LLM tabanlı sınıflandırma, kural tabanlı sistemlerin zorlandığı belirsiz ve bağlamsal metinlerde üstündür. Bu skill, kategori tanımı, prompt yapısı, çıktı doğrulama ve edge case yönetimini kapsar.

## Workflow

### Kategori Tanım Şablonu
```python
CATEGORIES = {
    "teknik_sorun": (
        "Kullanıcı bir ürün veya hizmetle teknik bir sorun yaşıyor. "
        "Hata mesajları, çalışmama durumları, beklenen davranışın gerçekleşmemesi. "
        "Örnek: 'Uygulama açılmıyor', 'Hata kodu 500 alıyorum'"
    ),
    "fatura_odeme": (
        "Fatura, ödeme, iade veya fiyatlandırmayla ilgili sorular. "
        "Örnek: 'Faturamda yanlış tutar var', 'Para iademi ne zaman alırım'"
    ),
    "bilgi_talebi": (
        "Kullanım kılavuzu, özellik açıklaması veya süreç hakkında bilgi. "
        "Eylem gerektirmez. Örnek: 'Bu özellik nasıl çalışır'"
    ),
}
```

### Sınıflandırma Promptu
```python
def build_classification_prompt(text: str, categories: dict) -> str:
    cat_descriptions = "\n".join(
        f"- {k}: {v}" for k, v in categories.items()
    )
    return f"""Aşağıdaki müşteri mesajını sınıflandır.

KATEGORİLER:
{cat_descriptions}
- diger: Hiçbir kategoriye uymayan

Mesaj: "{text}"

Yalnızca kategori adını yaz (küçük harf, alt çizgili). Başka metin ekleme."""
```

### Çıktı Doğrulama
```python
VALID_CATEGORIES = set(CATEGORIES.keys()) | {"diger"}

def classify(text: str) -> str:
    raw = llm.complete(build_classification_prompt(text, CATEGORIES))
    result = raw.strip().lower()
    
    if result not in VALID_CATEGORIES:
        # Fuzzy match dene
        from difflib import get_close_matches
        matches = get_close_matches(result, VALID_CATEGORIES, n=1, cutoff=0.6)
        result = matches[0] if matches else "diger"
    
    return result
```

### Çok Etiketli Sınıflandırma
```
Mesaj birden fazla kategoriye girebilir. JSON array döndür:
["teknik_sorun", "fatura_odeme"]
Emin değilsen en olası iki kategoriyi ver.
```

## Common mistakes
- Kategori açıklamalarını çok kısa tutmak — model sınır durumları karıştırır.
- Sadece "Geçerli kategori" yazmadan çıktı doğrulaması yapmamak — model bazen açıklama ekler.
- Tüm kategorileri eşit örnekle test etmemek — nadir kategoriler daha kötü performans gösterir.
- `diger` kategorisini koymamak — model zorla bir kategori seçer.

## References
- `skills/llm-prompt-few-shot`
- `skills/llm-prompt-output-format`
- `skills/llm-eval-domain-specific`
