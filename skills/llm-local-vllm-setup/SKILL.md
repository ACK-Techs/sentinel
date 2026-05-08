---
name: llm-local-vllm-setup
description: "vLLM ile yüksek performanslı yerel LLM sunucusu kurmak, GPU bellek yapılandırması ve tensor parallelism ayarlamak, OpenAI-compatible API açmak gerektiğinde kullan. Ollama'dan daha yüksek throughput için tercih edilir."
---

## Purpose
vLLM, PagedAttention ile GPU bellek verimliliğini artırır; Ollama'dan 2-10x daha yüksek token/s sağlar. Üretim çıkarım sunucusu için tercih edilir.

## Kurulum
```bash
pip install vllm
# CUDA 12.1+ gerekli
```

## Sunucu başlatma
```bash
# Temel:
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-8B-Instruct \
  --port 8000

# GPU bellek oranı:
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-8B-Instruct \
  --gpu-memory-utilization 0.90 \
  --max-model-len 8192 \
  --port 8000

# Çoklu GPU (tensor parallelism):
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-70B-Instruct \
  --tensor-parallel-size 4 \  # 4 GPU
  --port 8000
```

## GGUF / AWQ / GPTQ model
```bash
python -m vllm.entrypoints.openai.api_server \
  --model ./llama3-8b-instruct.Q4_K_M.gguf \
  --quantization gguf
```

## HuggingFace token
```bash
export HUGGING_FACE_HUB_TOKEN="hf_..."
# Gate'li model için gerekli (Llama, Gemma)
```

## Doğrulama
```bash
curl http://localhost:8000/v1/models
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"meta-llama/Llama-3.2-8B-Instruct","messages":[{"role":"user","content":"test"}]}'
```

## Kubernetes Deployment
```yaml
spec:
  containers:
    - name: vllm
      image: vllm/vllm-openai:latest
      args: ["--model", "meta-llama/Llama-3.2-8B-Instruct", "--port", "8000"]
      resources:
        limits:
          nvidia.com/gpu: "1"
```

## Common mistakes
- `--max-model-len` belirtmeden büyük model için OOM almak.
- `gpu-memory-utilization 1.0` ayarlamak — OS için %5-10 boşluk bırak.
- Model indirmeden sunucuyu başlatmak ve uzun bekleme sürpriziyle karşılaşmak.

## References
- `skills/llm-local-ollama-setup`
- `skills/llm-local-gpu-memory`
- `skills/llm-openai-compatible-server`
- `skills/microk8s-addon-gpu`
