---
name: llm-prompt-output-format
description: "LLM çıktısını JSON, XML veya Markdown gibi belirli bir yapıda almak gerektiğinde; downstream parse işleminin başarısız olmasını önlemek için kullan"
---

## Purpose
Format zorlama olmadan LLM çıktısı her seferinde farklı yapı üretir. Bu skill, JSON mode, yapısal prompt talimatı ve parse etme hata yönetimini kapsar.

## Workflow

### Yöntem 1: JSON Mode (Anthropic)
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="Yanıtlarını her zaman geçerli JSON formatında ver.",
    messages=[{"role": "user", "content": "3 Python kütüphanesi öner"}]
)
# Not: Claude native JSON mode için tool use kullanın
```

### Yöntem 2: Tool Use ile Yapısal Çıktı (En Güvenilir)
```python
result_tool = {
    "name": "return_result",
    "description": "Sonucu yapısal formatta döndür",
    "input_schema": {
        "type": "object",
        "properties": {
            "libraries": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "purpose": {"type": "string"},
                        "install": {"type": "string"}
                    },
                    "required": ["name", "purpose", "install"]
                }
            }
        },
        "required": ["libraries"]
    }
}
```

### Yöntem 3: Prompt ile Format Zorlama
```
Yanıtını YALNIZCA aşağıdaki JSON formatında ver, başka hiçbir metin ekleme:

{
  "libraries": [
    {"name": "...", "purpose": "...", "install": "pip install ..."}
  ]
}
```

### Parse Etme ve Hata Kurtarma
```python
import json, re

def safe_parse_json(text: str) -> dict:
    # Markdown code block içinden çıkar
    text = re.sub(r"```(?:json)?\n?(.*?)\n?```", r"\1", text, flags=re.DOTALL)
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        # JSON parçasını bul
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise
```

## Common mistakes
- "JSON döndür" deyip şema vermemek — model her seferinde farklı alan adı kullanır.
- Tool use yerine sadece prompt formatı kullanmak — tool use yüzde olarak çok daha güvenilir.
- Parse hatasını exception olarak bırakmak — fallback ile yeniden deneme ekleyin.
- XML çıktı isterken namespace prefixlerini belirtmemek — `<ns:tag>` vs `<tag>` karışır.

## References
- `skills/llm-prompt-tool-descriptions`
- `skills/llm-prompt-extraction`
