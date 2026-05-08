---
name: llm-local-gpu-memory
description: "Yerel modelin VRAM gereksinimini tahmin etmek, çoklu GPU sharding stratejisi seçmek ve model + KV cache + aktivasyon belleği toplamını hesaplayarak donanım kararı vermek gerektiğinde kullan."
---

## Purpose
Modeli indirmeden önce VRAM yeterliliğini bilmek: OOM hatasıyla zaman kaybetmemek ve donanım satın alma kararlarını veri ile desteklemek için.

## Model boyutu tahmini

### Kaba hesap
```
VRAM (GB) ≈ parametre_sayısı × bayt_per_parametre × 1.2 (overhead)
```

| Format | Bayt/parametre |
|---|---|
| float32 (FP32) | 4 |
| float16 / bfloat16 | 2 |
| int8 (8-bit quant) | 1 |
| int4 (4-bit quant) | 0.5 |

Örnek: 8B parametre, Q4_K_M → `8 × 10^9 × 0.5 × 1.2 / 10^9 ≈ 4.8 GB`

### KV Cache
```
KV_cache (GB) = 2 × layers × heads × head_dim × seq_len × batch × dtype
```
Pratik kural: max_seq_len 8K, batch 1 → +1-2 GB ekle.

## Model başına referans değerler (Q4_K_M)

| Model | VRAM |
|---|---|
| Llama 3.2 3B | ~2 GB |
| Llama 3.2 8B | ~5 GB |
| Llama 3.1 70B | ~40 GB |
| Llama 3.1 405B | ~230 GB |

## Çoklu GPU (tensor parallelism)
```bash
# vLLM ile 2 GPU:
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.1-70B-Instruct \
  --tensor-parallel-size 2  # 2×A100 = 160 GB

# Ollama ile (otomatik bölüştürme):
OLLAMA_GPU_OVERHEAD=0 ollama run llama3.1:70b
```

## VRAM kullanımını izleme
```bash
nvidia-smi --query-gpu=memory.used,memory.free --format=csv -l 1
# veya sürekli:
watch -n 1 'nvidia-smi | grep MiB'
```

## Karar ağacı
- VRAM > model VRAM: direkt çalıştır
- VRAM biraz az: quantization düşür (Q5 → Q4)
- VRAM çok az: CPU offload + llama.cpp (`n_gpu_layers`)
- Birden fazla GPU: tensor parallel

## Common mistakes
- Yalnızca model boyutunu hesaplayıp KV cache'i unutmak — uzun konuşmalarda OOM.
- Shared GPU (gaming PC) ile production çıkarımı yapmak — CUDA context çakışması.

## References
- `skills/llm-local-quantization`
- `skills/llm-local-vllm-setup`
- `skills/llm-local-llama-cpp`
- `skills/microk8s-addon-gpu`
