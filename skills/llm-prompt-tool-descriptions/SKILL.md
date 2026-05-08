---
name: llm-prompt-tool-descriptions
description: "LLM agent'ına verilecek araç açıklamaları ve JSON Schema parametre tanımları yazılırken; modelin doğru aracı seçip doğru parametreyle çağırmasını sağlamak için kullan"
---

## Purpose
Araç açıklaması, modelin hangi aracı seçeceğini ve parametreleri nasıl dolduracağını belirler. Zayıf açıklamalar yanlış araç seçimine veya hatalı parametre değerlerine yol açar. Bu skill, etkin araç açıklaması şablonunu ve test yaklaşımını kapsar.

## Workflow

### Araç Tanımı Şablonu (Anthropic format)
```python
tools = [
    {
        "name": "search_orders",
        "description": (
            "Müşteri siparişlerini veritabanında arar. "
            "Sipariş numarası, müşteri e-postası veya tarih aralığıyla sorgu yapılabilir. "
            "Sipariş durumu, kargo bilgisi ve ürün listesini döndürür. "
            "Kullanıcı sipariş durumu veya kargo takibi sorduğunda bu aracı kullan."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Sipariş numarası, örnek: ORD-2024-001234"
                },
                "customer_email": {
                    "type": "string",
                    "format": "email",
                    "description": "Müşteri e-posta adresi"
                },
                "date_from": {
                    "type": "string",
                    "format": "date",
                    "description": "Başlangıç tarihi, ISO 8601: 2024-01-15"
                }
            },
            "required": []   # hepsi opsiyonel — en az biri gerekli
        }
    }
]
```

### Açıklama Kalite Kontrol Listesi
```
[x] Ne yapar? (1 cümle)
[x] Ne zaman kullanılmalı? (trigger koşul)
[x] Hangi veriyi döndürür? (output tipi)
[x] Her parametre için örnek değer var mı?
[x] required vs optional doğru mu?
[x] Başka araçla çakışma var mı?
```

### Araç Seçim Testi
```python
# Ambiguous case: model hangi aracı seçiyor?
test_queries = [
    ("Siparişim nerede?", "search_orders"),
    ("İade etmek istiyorum", "create_return"),
    ("Adresimi güncelle", "update_profile"),
]
for query, expected_tool in test_queries:
    resp = llm.complete(messages=[{"role":"user","content":query}], tools=tools)
    actual = resp.tool_calls[0].name if resp.tool_calls else "none"
    assert actual == expected_tool, f"Beklenen: {expected_tool}, Alınan: {actual}"
```

## Common mistakes
- Açıklamayı tek kelimeyle bırakmak ("Arama yapar") — trigger koşulu olmadan model seçemiyor.
- `required` listesini boş bırakmayı unutmak — model boş çağrı yapar.
- İki araç açıklaması aynı anlama geldiğinde model keyfi seçer — birini kaldırın veya açıklamaları ayırın.
- `format: date` gibi hint'leri koymamak — model farklı date formatları üretir.

## References
- `skills/llm-prompt-react-pattern`
- `skills/agentic-mcp-tool-schema`
- `skills/llm-eval-tool-call-accuracy`
