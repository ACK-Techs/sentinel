---
name: llm-local-quantization
description: "GGUF, AWQ, GPTQ gibi model niceleme (quantization) formatlarını anlamak, hangi bit derinliğini seçeceğini bilmek ve kalite-boyut-hız trade-off'larını değerlendirmek gerektiğinde kullan."
---

## Purpose
Quantization, model ağırlıklarını daha düşük hassasiyetle saklar; model boyutunu ve VRAM kullanımını azaltır. Yanlış seçim ya kalite kaybı ya da gereksiz kaynak tüketimi doğurur.

## Format karşılaştırması

| Format | Araç | GPU | CPU | Açıklama |
|---|---|---|---|---|
| GGUF | llama.cpp / Ollama | Kısmi | Tam | En esnek; CPU+GPU hibrit |
| AWQ | vLLM, HF | Sadece | — | Aktivasyon-ağırlıklı; GPU çıkarım için en iyi |
| GPTQ | vLLM, AutoGPTQ | Sadece | — | Eski nesil; AWQ kadar iyi değil |
| BitsAndBytes | HF Transformers | Sadece | — | Anlık quant; eğitimde kullanılır |

## GGUF bit derinliği seçimi

| Quant | Boyut (7B) | Kalite kaybı | Ne zaman? |
|---|---|---|---|
| Q2_K | ~2.9 GB | Yüksek | Yalnızca belleksiz ortam |
| Q4_K_M | ~4.1 GB | Minimal | **Tavsiye edilen varsayılan** |
| Q5_K_M | ~4.8 GB | Çok az | Kalite öncelikli, GPU var |
| Q8_0 | ~7.2 GB | Neredeyse sıfır | Yeterli VRAM + maksimum kalite |
| F16 | ~14 GB | Sıfır | Full precision; eğitim sonrası |

**Kural:** VRAM > model boyutu → bir üst Q seç.

## GGUF model indirme
```bash
# Hugging Face'den:
huggingface-cli download bartowski/Llama-3.2-8B-Instruct-GGUF \
  --include "*Q4_K_M*" --local-dir ./models
```

## Kendi modelini quantize etme (GGUF)
```bash
cd llama.cpp
python convert_hf_to_gguf.py /path/to/hf-model --outtype f16 --outfile model-f16.gguf
./llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M
```

## AWQ quantization
```python
from awq import AutoAWQForCausalLM
model = AutoAWQForCausalLM.from_pretrained("meta-llama/Llama-3.2-8B-Instruct")
model.quantize(tokenizer, quant_config={"zero_point": True, "q_group_size": 128, "w_bit": 4})
model.save_quantized("./llama3-8b-awq")
```

## Common mistakes
- Q2/Q3 seçmek ve cevap kalitesinin düştüğünden haberdar olmamak.
- GGUF'u GPU-only vLLM'de kullanmaya çalışmak — vLLM AWQ/GPTQ/HF formatlarını tercih eder.

## References
- `skills/llm-local-llama-cpp`
- `skills/llm-local-gpu-memory`
- `skills/llm-local-vllm-setup`
