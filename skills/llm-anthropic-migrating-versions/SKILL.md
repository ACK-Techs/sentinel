---
name: llm-anthropic-migrating-versions
description: "Eski Claude model sürümünden (claude-2, claude-3-opus-20240229 vb.) yenisine geçiş yaparken model ID'sini güncellemek, davranış farklarını yönetmek ve regresyon testlerini çalıştırmak gerektiğinde kullan."
---

## Purpose
Model ID değiştirmek bir satır gibi görünür ama yanıt kalitesi, format ve araç çağrısı davranışı değişebilir. Geçiş öncesi test ve sonrası izleme şarttır.

## Model ID güncelleme

### Yaygın migration yolları
```python
# Claude 2 → 3 Sonnet
"claude-2.1" → "claude-sonnet-4-6"

# Claude 3 Opus → Claude 4 Opus
"claude-3-opus-20240229" → "claude-opus-4-7"

# Claude 3 Haiku → Claude 4 Haiku
"claude-3-haiku-20240307" → "claude-haiku-4-5-20251001"
```

### Kod içinde merkezi model tanımı
```python
# config.py
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

# Her yerde:
client.messages.create(model=CLAUDE_MODEL, ...)
```
Migration = yalnızca environment variable değişimi.

## Bilinen davranış farkları

### Tool use formatı
Claude 3+ araç çağrısında `stop_reason: "tool_use"` döner; eski modellerde metin içi çağrı vardı.

### System prompt
Claude 3+ system prompt ayrı alan; eski modellerde `\n\nHuman:` formatı gerekiyordu.

### Çıktı uzunluğu
Yeni modeller daha özlü yanıt üretir; `max_tokens` değerini yeniden kalibre etmek gerekebilir.

## Regresyon test stratejisi
```python
# Golden test seti (girdi + beklenen çıktı formatı):
test_cases = [
    {"input": "PromQL sorgusu yaz", "check": lambda r: "rate(" in r},
    {"input": "JSON döndür", "check": lambda r: json.loads(r) is not None},
]

for case in test_cases:
    response = client.messages.create(model=NEW_MODEL, ...)
    assert case["check"](response.content[0].text), f"Başarısız: {case['input']}"
```

## Kademeli geçiş
1. Yeni modeli shadow modda çalıştır (production isteği ikiye kat, karşılaştır).
2. Küçük trafik dilimi ile A/B testi.
3. Anomali yoksa tam geçiş.

## Common mistakes
- Tüm model ID'lerini `grep -r "claude-3"` ile bulup tek seferde değiştirmek — prompt uyumluluk testini atlamak.
- Yeni modelin daha uzun düşünme süresi (latency) olabileceğini kullanıcı deneyimine yansıtmamak.

## References
- `skills/llm-anthropic-model-selection`
- `skills/llm-anthropic-sdk-python`
- `skills/llm-eval-regression-test`
