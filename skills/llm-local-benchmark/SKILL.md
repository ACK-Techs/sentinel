---
name: llm-local-benchmark
description: "Yerel modelin çıkarım hızını (tokens/saniye), Time-to-First-Token (TTFT) gecikmesini ve domain doğruluğunu ölçmek; farklı quantization/backend konfigürasyonlarını karşılaştırmak gerektiğinde kullan."
---

## Purpose
Model seçimi ve yapılandırma kararlarını subjektif izlenim yerine ölçüme dayandırmak. Throughput, latency ve doğruluk farklı senaryolarda farklı öneme sahiptir.

## Temel performans metrikleri
- **TTFT** (Time to First Token): kullanıcı deneyimi için kritik
- **Throughput** (tokens/s): toplu işlem için kritik
- **Memory** (VRAM/RAM): donanım gereksinimi

## Ollama ile hız ölçümü
```bash
# Builtin benchmark:
ollama run llama3.2 "Kısa bir test." --verbose 2>&1 | grep -E "eval rate|load duration|total duration"

# Çıktı örneği:
# eval rate:         34.52 tokens/s
# load duration:     1.2s
```

## llama.cpp benchmark
```bash
./llama-bench -m ./models/llama3.2-Q4_K_M.gguf \
  -p 512 -n 128 -t 8 --no-mmap
# pp (prompt processing): tok/s
# tg (token generation): tok/s
```

## Python ile özel benchmark
```python
import time
from llama_cpp import Llama

llm = Llama(model_path="model.gguf", n_ctx=2048)

prompt = "Kubernetes HPA nedir? Detaylıca açıkla."
start = time.perf_counter()

output = llm(prompt, max_tokens=256, stream=False)
elapsed = time.perf_counter() - start

tokens = output["usage"]["completion_tokens"]
print(f"Hız: {tokens/elapsed:.1f} tok/s | TTFT: ~{elapsed*0.1:.2f}s")
```

## vLLM benchmark
```bash
python benchmarks/benchmark_throughput.py \
  --model meta-llama/Llama-3.2-8B-Instruct \
  --num-prompts 100 \
  --input-len 256 \
  --output-len 128
```

## Doğruluk değerlendirmesi (domain spesifik)
```python
test_cases = [
    ("CPU kullanımı PromQL", lambda r: "rate(" in r and "cpu" in r.lower()),
    ("Pod restart sayısı", lambda r: "kube_pod_container_restarts_total" in r),
]
passed = sum(check(llm(q)["choices"][0]["text"]) for q, check in test_cases)
print(f"Doğruluk: {passed}/{len(test_cases)}")
```

## Common mistakes
- Tek bir prompt ile hız ölçmek — warm-up etkisi ilk çağrıda yüksek TTFT verir.
- Throughput'u tek başına optimize edip TTFT'yi göz ardı etmek — kullanıcı donan.
- CPU/GPU ısısını izlememek; thermal throttling benchmark sonuçlarını bozar.

## References
- `skills/llm-local-quantization`
- `skills/llm-local-gpu-memory`
- `skills/llm-eval-latency-cost`
