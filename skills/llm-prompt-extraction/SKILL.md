---
name: llm-prompt-extraction
description: "Yapılandırılmamış metinden (fatura, CV, sözleşme, log) belirli alanları çıkarmak gerektiğinde; alan tanımları ve doğrulama dahil extraction pipeline için kullan"
---

## Purpose
LLM extraction, regex'in yetersiz kaldığı bağlamsal ve değişken formattaki belgelerden yapısal veri üretir. Schema-driven extraction, çıktı tutarlılığını garanti eder.

## Workflow

### Tool Use ile Schema-Driven Extraction
```python
extract_tool = {
    "name": "extract_invoice",
    "description": "Fatura belgesinden yapısal veri çıkar",
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_number": {"type": "string", "description": "Fatura numarası"},
            "date": {"type": "string", "format": "date", "description": "ISO format: YYYY-MM-DD"},
            "vendor_name": {"type": "string"},
            "total_amount": {"type": "number"},
            "currency": {"type": "string", "enum": ["TRY", "USD", "EUR"]},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"}
                    }
                }
            }
        },
        "required": ["invoice_number", "total_amount"]
    }
}

response = client.messages.create(
    model="claude-sonnet-4-5",
    tools=[extract_tool],
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=[{"role": "user", "content": f"Bu faturayı çıkar:\n\n{document_text}"}]
)
```

### Çok Değerli Alan Çıkarımı
```
Belgeden aşağıdaki alanları çıkar. Alan bulunamazsa null döndür.
Birden fazla değer varsa array kullan.

{
  "parties": ["Taraf isimlerinin listesi"],
  "dates": ["Tarih değerlerinin listesi (ISO format)"],
  "amounts": [{"value": number, "currency": string, "context": string}]
}
```

### Doğrulama ve Çapraz Kontrol
```python
from pydantic import BaseModel, validator
from typing import Optional
from decimal import Decimal

class InvoiceExtract(BaseModel):
    invoice_number: str
    total_amount: Decimal
    currency: str
    
    @validator("currency")
    def valid_currency(cls, v):
        assert v in ("TRY", "USD", "EUR"), f"Geçersiz para birimi: {v}"
        return v
    
    @validator("total_amount")
    def positive_amount(cls, v):
        assert v > 0, "Tutar pozitif olmalı"
        return v
```

## Common mistakes
- Null alanlar için `""` yerine `null` döndürmesini söylememek — downstream parse hataları.
- Tarih formatını belirtmemek — model "15 Ocak 2024" veya "01/15/2024" karışık üretir.
- Çok uzun belgelerde önemli alanın context sonunda kalmasına izin vermek — chunk'layın.
- Validation'ı LLM tarafında değil Python tarafında yapmamak — model hata kabul eder.

## References
- `skills/llm-prompt-output-format`
- `skills/llm-prompt-tool-descriptions`
- `skills/llm-local-multi-modal`
