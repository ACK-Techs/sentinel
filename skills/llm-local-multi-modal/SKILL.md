---
name: llm-local-multi-modal
description: "LLaVA, Gemma3 veya BakLLaVA gibi yerel multimodal modelle görüntü+metin çıkarımı yapılacağında; Ollama veya llama.cpp image API kullanılırken kullan"
---

## Purpose
Yerel multimodal modeller, görüntü encode edip metin yanıtı üretir. Bu skill, modeli Ollama üzerinden çalıştırmayı, base64 görüntü göndermeyi ve çıktıyı Sentinel aracına entegre etmeyi kapsar.

## Workflow

### 1. Modeli Kur
```bash
ollama pull llava:13b
# veya hafif seçenek:
ollama pull moondream:1.8b
```

### 2. Görüntü Gönder (Ollama API)
```python
import base64, requests

with open("screenshot.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llava:13b",
    "prompt": "Bu ekran görüntüsünde ne görüyorsun? Hataları listele.",
    "images": [img_b64],
    "stream": False
})
print(response.json()["response"])
```

### 3. OpenAI-compat Formatı (LM Studio / llama.cpp server)
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="local")
resp = client.chat.completions.create(
    model="llava-v1.6-mistral-7b",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Görseldeki tabloyu JSON olarak çıkar."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
        ]
    }]
)
```

### 4. Sentinel Tool'a Sarma
```python
# tools/vision_extract.py
def describe_image(image_path: str) -> str:
    """Görüntüden yapısal veri çıkar."""
    # base64 encode → POST → return text
```

## Common mistakes
- LLaVA'nın her versiyonunun farklı image token formatı beklediğini unutmak (`<image>` vs `[img-N]`).
- Çok büyük görüntü göndermek: 1024x1024 üzeri genellikle yeniden boyutlandırılır, önceden resize edin.
- Ollama'nın `/api/generate`'i streaming döndürdüğünü bilmemek — `"stream": false` ekleyin.
- Gemma3'ün vision kabiliyetini quantized versiyonda kaybedebileceğini göz ardı etmek.

## References
- `skills/llm-local-lm-studio`
- `skills/llm-prompt-extraction`
