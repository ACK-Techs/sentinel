---
name: llm-prompt-temperature-params
description: "LLM sampling parametrelerini (temperature, top-p, top-k, repetition_penalty) ayarlarken; görev türüne göre doğru değerleri seçmek için kullan"
---

## Purpose
Temperature ve sampling parametreleri, modelin ne kadar "yaratıcı" veya "deterministik" davranacağını belirler. Yanlış değerler ya robotik tekrarlara ya da tutarsız çıktılara yol açar.

## Workflow

### Parametre Referans Tablosu
```
Görev                        | temperature | top_p | top_k
-----------------------------|-------------|-------|-------
Kod üretimi                  | 0.0–0.2     | 0.95  | 40
Veri çıkarma (extraction)    | 0.0         | 1.0   | -
Sınıflandırma                | 0.0         | 1.0   | -
Özet yazma                   | 0.3–0.5     | 0.9   | 40
Yaratıcı yazı                | 0.8–1.2     | 0.95  | 50
Beyin fırtınası              | 1.0–1.5     | 1.0   | -
Çeviri                       | 0.1–0.3     | 0.95  | 40
```

### Parametreler Arası İlişki
```python
# temperature: logit dağılımını keskinleştirir/yumuşatır
# top_p (nucleus sampling): olasılık toplamı %p'ye kadar token seçer
# top_k: en yüksek k token arasından seçer

# KURAL: temperature=0 ise top_p ve top_k etkisiz
# KURAL: top_p ve top_k aynı anda kullanmayın (genellikle top_p yeterli)
```

### Sentinel Konfigürasyonu
```python
# api/llm_client.py
def get_sampling_params(task_type: str) -> dict:
    PROFILES = {
        "extraction": {"temperature": 0.0},
        "coding":     {"temperature": 0.1, "top_p": 0.95},
        "creative":   {"temperature": 1.0, "top_p": 0.95},
        "chat":       {"temperature": 0.7, "top_p": 0.9},
    }
    return PROFILES.get(task_type, {"temperature": 0.7})
```

### Repetition Penalty (yerel modeller)
```python
# Ollama / llama.cpp için
params = {
    "repeat_penalty": 1.1,       # 1.0=kapalı, 1.1-1.3 genellikle iyi
    "repeat_last_n": 64,         # kaç token geriye bakılır
}
```

## Common mistakes
- Her görev için aynı temperature kullanmak (`0.7`) — extraction'da hallüsinasyon üretir.
- temperature=0 ile creative yazı istemek — model her seferinde aynı başlangıcı seçer.
- top_p=1.0 ve top_k=1 aynı anda koymak — top_k=1 greedy decoding demektir, çelişir.
- Yerel modellerde `repeat_penalty` koymayı unutmak — döngüsel tekrarlar üretir.

## References
- `skills/llm-prompt-system-design`
- `skills/llm-eval-latency-cost`
