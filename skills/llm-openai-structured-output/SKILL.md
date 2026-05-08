---
name: llm-openai-structured-output
description: "OpenAI structured output ile model yanıtının belirli bir Pydantic/JSON Schema'ya garantili uymasını sağlamak, parse hatasını ortadan kaldırmak ve agent pipeline'da güvenilir veri çıkarımı yapmak gerektiğinde kullan."
---

## Purpose
Structured output, `response_format` ile modelin kesinlikle belirtilen şemaya uyan JSON döndürmesini garanti eder. `json_mode`'dan farklı: şema ihlali imkânsızdır.

## Pydantic ile kullanım (önerilen)
```python
from pydantic import BaseModel
from openai import OpenAI

class AlertRule(BaseModel):
    name: str
    expr: str
    severity: str
    for_duration: str
    summary: str

response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",  # structured output destekleyen model
    messages=[
        {"role": "system", "content": "Prometheus alerting kuralı oluştur."},
        {"role": "user", "content": "CPU %90 üstünde 5 dakika kalırsa uyar."}
    ],
    response_format=AlertRule
)

rule = response.choices[0].message.parsed
print(rule.name, rule.expr)  # doğrudan Pydantic nesnesi
```

## JSON Schema ile (SDK'sız)
```python
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "alert_rule",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "expr": {"type": "string"}
                },
                "required": ["name", "expr"],
                "additionalProperties": False
            }
        }
    },
    messages=[...]
)
import json
data = json.loads(response.choices[0].message.content)
```

## json_mode vs structured output
- `json_mode` (`{"type": "json_object"}`): JSON üretir ama şemaya uymayı garanti etmez.
- `json_schema` ile `strict: true`: şema ihlali yok; model gerekirse kısa cevap verir.

## Common mistakes
- `strict: true` ile `additionalProperties: false` koymayı unutmak — şema zorunlulukları farklılaşır.
- `.parse()` metodunu desteklemeyen eski model sürümüyle kullanmak.
- Çok karmaşık nested şema vermek — model şemayı doğru doldurmak için ek instruction'a ihtiyaç duyabilir.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-openai-function-calling`
- `skills/llm-prompt-output-format`
