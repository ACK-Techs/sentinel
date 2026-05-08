---
name: llm-prompt-code-generation
description: "LLM'den kod üretmek gerektiğinde; güvenlik kısıtlamaları, dil tutarlılığı ve üretilen kodun doğrulanması için prompt tasarımı yaparken kullan"
---

## Purpose
Kod üretimi promptları, teknik kısıtlamaları (dil sürümü, bağımlılıklar, stil kılavuzu) netleştirmeden yazılırsa modelin ürettiği kod çalışmaz veya güvensizdir. Bu skill güvenilir kod üretimi sözleşmesini kurar.

## Workflow

### Kod Üretimi Promptu Şablonu
```python
CODE_SYSTEM = """Sen bir Python 3.11+ kod üreticisisin.

ZORUNLU KURALLAR:
- Type annotation kullan (her fonksiyon için)
- Hata yönetimi: try/except, değil bare except
- Harici bağımlılık ekleme (sadece stdlib kullan, aksi belirtilmedikçe)
- SQL sorgusu varsa parameterized query kullan (SQL injection yok)
- Dosya yolu işlemlerinde pathlib kullan (os.path değil)
- Fonksiyon başına docstring yaz

ÇIKTI FORMATI:
```python
# kod buraya
```
Ardından 2-3 cümle açıklama."""
```

### Spesifik Görev Promptu
```python
def code_gen_prompt(spec: str, language: str = "python", version: str = "3.11") -> str:
    return f"""Dil: {language} {version}
Görev: {spec}

Güvenlik kontrolleri:
- Kullanıcı girdisi validate et
- Path traversal'a karşı input sanitize et  
- Credentials hard-code etme, ortam değişkeninden oku

Testler: En az 2 unit test yaz (pytest formatında)"""
```

### Üretilen Kodu Doğrulama
```python
import ast, subprocess

def validate_generated_code(code: str) -> dict:
    result = {"syntax_ok": False, "lint_ok": False, "errors": []}
    
    # Syntax kontrolü
    try:
        ast.parse(code)
        result["syntax_ok"] = True
    except SyntaxError as e:
        result["errors"].append(f"Syntax: {e}")
    
    # Güvenlik taraması (bandit)
    proc = subprocess.run(
        ["bandit", "-", "-f", "json"],
        input=code.encode(), capture_output=True
    )
    import json
    bandit_out = json.loads(proc.stdout or '{"results": []}')
    high_issues = [r for r in bandit_out["results"] if r["issue_severity"] == "HIGH"]
    if high_issues:
        result["errors"].extend([r["issue_text"] for r in high_issues])
    else:
        result["lint_ok"] = True
    
    return result
```

### Güvenli Yeniden Deneme
```python
def generate_code_with_retry(spec: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        code = extract_code_block(llm.complete(code_gen_prompt(spec)))
        validation = validate_generated_code(code)
        if not validation["errors"]:
            return code
        # Hataları prompt'a geri ver
        spec += f"\n\nÖnceki denemede hatalar:\n" + "\n".join(validation["errors"])
    raise CodeGenerationFailed("3 denemede temiz kod üretilemedi")
```

## Common mistakes
- "Kod yaz" demek — dil, versiyon, bağımlılık kısıtı olmadan model tahmin yürütür.
- Üretilen kodu syntax kontrolü yapmadan çalıştırmak — her zaman validate edin.
- SQL veya shell komutlarını doğrudan format string ile üretmek — injection riski.
- Test istemeden sadece implementation almak — test prompta dahil edilmeli.

## References
- `skills/llm-prompt-output-format`
- `skills/agentic-sec-input-validation`
- `skills/llm-eval-regression-test`
