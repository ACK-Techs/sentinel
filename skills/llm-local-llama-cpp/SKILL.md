---
name: llm-local-llama-cpp
description: "llama.cpp ile CPU veya GPU üzerinde GGUF format modeli yüklemek, çıkarım parametrelerini ayarlamak ve Python llama-cpp-python wrapper'ı üzerinden entegrasyon yapmak gerektiğinde kullan."
---

## Purpose
llama.cpp, GPU olmayan veya sınırlı VRAM'li ortamlarda quantize edilmiş GGUF modellerini CPU ile çalıştırmak için tercih edilen araçtır. Minimal bağımlılık, maksimum taşınabilirlik.

## Derleme ve kurulum
```bash
# Temel (CPU):
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
make -j$(nproc)

# CUDA ile:
make GGML_CUDA=1 -j$(nproc)

# Python wrapper:
pip install llama-cpp-python
# CUDA ile:
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --no-cache-dir
```

## Model indirme (GGUF)
```bash
# Hugging Face CLI:
pip install huggingface-hub
huggingface-cli download bartowski/Llama-3.2-8B-Instruct-GGUF \
  --include "Llama-3.2-8B-Instruct-Q4_K_M.gguf" \
  --local-dir ./models
```

## CLI çıkarımı
```bash
./llama-cli -m ./models/Llama-3.2-8B-Instruct-Q4_K_M.gguf \
  -p "PromQL nedir?" \
  --n-gpu-layers 35 \  # GPU katman sayısı (0=tam CPU)
  -c 4096 \            # context length
  -n 512               # maksimum yeni token
```

## Python wrapper
```python
from llama_cpp import Llama

llm = Llama(
    model_path="./models/Llama-3.2-8B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,          # context window
    n_gpu_layers=35,     # GPU'ya yüklenecek katman (-1=tümü)
    n_threads=8          # CPU thread sayısı
)

output = llm.create_chat_completion(
    messages=[{"role": "user", "content": "Prometheus nedir?"}],
    max_tokens=256,
    temperature=0.3
)
print(output["choices"][0]["message"]["content"])
```

## OpenAI-compatible server
```bash
python -m llama_cpp.server --model ./models/model.gguf --port 8080
# → http://localhost:8080/v1/chat/completions
```

## Common mistakes
- `n_gpu_layers` ayarlamadan tüm modeli CPU'ya yüklemek — VRAM'de yer varsa GPU kullanmak 5-10x hızlandırır.
- Q2 quantization seçmek aşırı kalite düşüşü — Q4_K_M veya Q5_K_M iyi denge noktası.

## References
- `skills/llm-local-quantization`
- `skills/llm-local-ollama-setup`
- `skills/llm-local-gpu-memory`
