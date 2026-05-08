---
name: llm-local-model-registry
description: "Ekip paylaşımlı yerel model deposu kurmak, model versiyonlamayı yönetmek, SHA256 doğrulaması uygulamak ve hangi modelin hangi ortamda kullanıldığını merkezi olarak izlemek gerektiğinde kullan."
---

## Purpose
Birden fazla ekip üyesi veya CI/CD pipeline aynı modeli kullandığında her kişinin ayrı ayrı indirip depolaması hem israf hem de tutarsızlık kaynağıdır. Merkezi model deposu bu sorunu çözer.

## Basit NFS/S3 tabanlı registry

### Dizin yapısı
```
/shared/models/
├── manifest.json           # tüm modellerin metadata'sı
├── llama3.2/
│   ├── 8b-Q4_K_M/
│   │   ├── model.gguf      # ~4.1 GB
│   │   └── model.sha256    # bütünlük doğrulama
│   └── 3b-Q4_K_M/
│       └── model.gguf
└── nomic-embed-text/
    └── v1.5/
        └── model.gguf
```

### manifest.json formatı
```json
{
  "models": [
    {
      "name": "llama3.2",
      "variant": "8b-Q4_K_M",
      "path": "llama3.2/8b-Q4_K_M/model.gguf",
      "sha256": "abc123...",
      "size_gb": 4.1,
      "source": "huggingface:bartowski/Llama-3.2-8B-Instruct-GGUF",
      "added_by": "engineer@team",
      "added_date": "2025-01-15",
      "recommended_for": ["sentinel-dev", "qa"]
    }
  ]
}
```

## Model indirme ve doğrulama scripti
```bash
#!/bin/bash
MODEL_PATH=$1
REGISTRY_BASE="/shared/models"

# SHA256 doğrulama:
sha256sum -c "${REGISTRY_BASE}/${MODEL_PATH}.sha256" || {
  echo "SHA256 eşleşmiyor! Model bozuk olabilir."
  exit 1
}
echo "Model doğrulandı: ${MODEL_PATH}"
```

## Ollama ile registry entegrasyonu
```bash
# Registry'den Ollama cache'ine sembolik link:
mkdir -p ~/.ollama/models/blobs/
ln -sf /shared/models/llama3.2/8b-Q4_K_M/model.gguf \
       ~/.ollama/models/blobs/sha256-<hash>
```

## Sentinel için model profil dosyası
```yaml
# .sentinel-models.yaml
default: llama3.2-8b-q4
models:
  llama3.2-8b-q4:
    path: /shared/models/llama3.2/8b-Q4_K_M/model.gguf
    backend: ollama
    context_length: 8192
  production:
    provider: anthropic
    model: claude-sonnet-4-6
```

## Common mistakes
- SHA256 doğrulamasını atlamak — corrupt download sessizce yanlış sonuç üretir.
- Model path'ini hardcode etmek; ortam değişkeni veya config dosyasına taşı.
- Eski modelleri silmeden birikmesine izin vermek — disk dolmasını izle.

## References
- `skills/llm-local-ollama-setup`
- `skills/llm-local-quantization`
- `skills/llm-local-benchmark`
- `skills/microk8s-offline-install`
