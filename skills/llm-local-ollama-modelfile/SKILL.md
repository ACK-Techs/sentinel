---
name: llm-local-ollama-modelfile
description: "Ollama Modelfile ile mevcut modele özel sistem promptu, parametreler ve şablon ekleyerek yeni türetilmiş model oluşturmak ya da mevcut modeli ince ayarlamak gerektiğinde kullan."
---

## Purpose
Modelfile, Docker'ın Dockerfile'ı gibi çalışır. Temel model üzerine katmanlar ekleyerek domain-specific veya davranış-özelleştirilmiş model türetilir.

## Temel Modelfile yapısı
```dockerfile
FROM llama3.2:8b

SYSTEM """
Sen Sentinel observability platformunun uzman asistanısın.
PromQL, LogQL, Kubernetes ve Juju konularında derinlemesine bilgin var.
Türkçe soru gelirse Türkçe yanıtla; İngilizce gelirse İngilizce yanıtla.
Her zaman çalışır kod örnekleri ver.
"""

PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 8192   # context window
PARAMETER stop "<|end|>"
```

## Model oluşturma
```bash
ollama create sentinel-assistant -f ./Modelfile
ollama list  # yeni model görünmeli
ollama run sentinel-assistant
```

## Parametreler

| Parametre | Etki | Örnek |
|---|---|---|
| `temperature` | Yaratıcılık | 0.1 (deterministik) – 1.0 |
| `num_ctx` | Context window | 4096, 8192, 32768 |
| `num_predict` | Maksimum token | -1 (sınırsız) |
| `stop` | Durma dizisi | `"</answer>"` |
| `top_k` | Token havuzu | 40 |

## GGUF dosyasından model oluşturma
```dockerfile
FROM ./my-model.gguf

SYSTEM "Özel model sistemi"
PARAMETER temperature 0.5
```

## Model güncelleme
```bash
# Modelfile değişince:
ollama create sentinel-assistant -f ./Modelfile
# Otomatik yeniden oluşturulur
```

## Common mistakes
- `num_ctx`'i modelin VRAM kapasitesinden büyük seçmek — OOM veya yavaş çalışma.
- SYSTEM promptu `"""` ile kapatmayı unutmak.
- Her değişiklik için `ollama rm + create` yerine sadece `create` çalıştırmanın yeterli olduğunu bilmemek.

## References
- `skills/llm-local-ollama-setup`
- `skills/llm-local-ollama-openai-compat`
- `skills/llm-anthropic-system-prompt`
