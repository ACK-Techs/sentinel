---
name: llm-prompt-few-shot
description: "LLM'e görevin nasıl yapılacağını birkaç örnek göstererek öğretmek gerektiğinde; çıktı formatı tutarlılığı kritik olan sınıflandırma, dönüşüm veya analiz görevlerinde kullan"
---

## Purpose
Few-shot prompting, modele input→output örnek çiftleri göstererek davranışı şekillendirir. Açık talimat yazmanın zorlaştığı durumlarda örnek vermek daha etkilidir. Örnek kalitesi ve sayısı sonucu doğrudan belirler.

## Workflow

### Örnek Format
```
### Örnek 1
Girdi: "Sipariş 2 gün önce verildi ve hala gelmedi."
Çıktı: {"kategori": "teslimat_gecikme", "öncelik": "yüksek", "aksiyon": "kargo_sorgula"}

### Örnek 2
Girdi: "Ürün rengi sitede mavi ama kırmızı geldi."
Çıktı: {"kategori": "yanlış_ürün", "öncelik": "yüksek", "aksiyon": "iade_başlat"}

### Örnek 3
Girdi: "Sipariş numaramı öğrenmek istiyorum."
Çıktı: {"kategori": "bilgi_talebi", "öncelik": "düşük", "aksiyon": "sipariş_sorgula"}

### Şimdi sınıflandır:
Girdi: "Ödeme yapıldı ama onay maili gelmedi."
Çıktı:
```

### Örnek Seçim Kriterleri
```python
# Kötü: aynı kategoriden 3 örnek
examples = [positive, positive, positive]  # bias oluşturur

# İyi: çeşitli, sınır durumları içeren örnekler
examples = [
    easy_positive,
    hard_negative,     # model için zorlayıcı olan
    edge_case,         # sınır durum
]
```

### Dinamik Few-Shot (RAG ile)
```python
# Kullanıcı girdisine semantik olarak en yakın örnekleri çek
def get_few_shot_examples(query: str, k: int = 3) -> list:
    results = vector_store.similarity_search(query, k=k)
    return [(r.input, r.output) for r in results]
```

## Common mistakes
- 10+ örnek koymak: 3-5 örnek genellikle yeterli, fazlası context israf eder.
- Örneklerde tutarsız format kullanmak — model kararsız kalır.
- Örnekleri yalnızca "kolay" durumlardan seçmek — zor vakalar için genelleşemez.
- Örnekleri sabit kodlamak: domain değiştikçe örnekler de güncellenmeli.

## References
- `skills/llm-prompt-zero-shot`
- `skills/llm-prompt-classification`
- `skills/llm-context-rag-pipeline`
