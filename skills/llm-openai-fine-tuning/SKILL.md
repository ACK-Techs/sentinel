---
name: llm-openai-fine-tuning
description: "OpenAI fine-tuning job oluşturmak, JSONL dataset formatını hazırlamak, eğitim sürecini izlemek ve fine-tuned modeli değerlendirmek gerektiğinde kullan."
---

## Purpose
Fine-tuning, belirli format, ton veya domain bilgisi için prompt engineering'in yetersiz kaldığı durumlarda modeli özelleştirmek için kullanılır. Her zaman gerekli değildir.

## Dataset formatı (JSONL)
```jsonl
{"messages": [{"role": "system", "content": "Sen bir PromQL uzmanısın."}, {"role": "user", "content": "CPU kullanımı metrigi"}, {"role": "assistant", "content": "rate(container_cpu_usage_seconds_total[5m])"}]}
{"messages": [{"role": "user", "content": "Bellek kullanımı"}, {"role": "assistant", "content": "container_memory_working_set_bytes"}]}
```

Minimum 10 örnek; 50-100+ için daha iyi sonuç.

## Fine-tuning job oluşturma
```python
# Önce dataset dosyasını yükle:
with open("training_data.jsonl", "rb") as f:
    file_response = client.files.create(file=f, purpose="fine-tune")

# Job başlat:
job = client.fine_tuning.jobs.create(
    training_file=file_response.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": "auto",
        "learning_rate_multiplier": "auto"
    }
)
print(job.id)  # ftjob-...
```

## Job izleme
```python
while True:
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(job.status, job.trained_tokens)
    if job.status in ["succeeded", "failed"]:
        break
    time.sleep(60)

fine_tuned_model = job.fine_tuned_model  # ft:gpt-4o-mini-...:org:suffix:id
```

## Fine-tuned model kullanımı
```python
response = client.chat.completions.create(
    model=fine_tuned_model,
    messages=[{"role": "user", "content": "Bellek kullanımı"}]
)
```

## Ne zaman fine-tuning gerekmez?
- Sistematik prompt + few-shot yeterliyse → fine-tuning daha pahalı.
- Çok küçük dataset (<50 örnek) → overfitting riski.
- RAG ile dinamik bilgi gerekiyorsa → fine-tuning statik bilgiyi şifreler.

## Common mistakes
- Validation seti olmadan eğitmek — overfitting'i göremezsin.
- Dataset'te tutarsız format kullanmak — model şaşırır.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-eval-benchmark-design`
