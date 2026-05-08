---
name: llm-anthropic-sdk-python
description: "Anthropic Python SDK'yı kurarak temel ve ileri kullanım kalıplarını (sync, async, streaming, retry) uygulamak; SDK'nın en iyi pratiklerini Sentinel codebase'inde kullanmak gerektiğinde kullan."
---

## Purpose
Python SDK, ham HTTP'yi soyutlar. Sync, async ve streaming için farklı client'lar vardır; doğru seçim uygulama mimarisini etkiler.

## Kurulum
```bash
pip install anthropic
# veya proje bağımlılığına:
pip install "anthropic[vertex]"  # Google Vertex AI için
```

## Sync client
```python
import anthropic

client = anthropic.Anthropic(
    api_key="sk-ant-...",  # veya ANTHROPIC_API_KEY env var
    max_retries=3,
    timeout=30.0
)

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Merhaba"}]
)
print(response.content[0].text)
```

## Async client
```python
import asyncio
import anthropic

async def main():
    async with anthropic.AsyncAnthropic() as client:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Merhaba"}]
        )
    return response

asyncio.run(main())
```

## Concurrent async istekler
```python
async def process_many(prompts):
    async with anthropic.AsyncAnthropic() as client:
        tasks = [
            client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=512,
                messages=[{"role": "user", "content": p}]
            )
            for p in prompts
        ]
        return await asyncio.gather(*tasks)
```

## Best practices
- API key'i environment variable'dan oku: `ANTHROPIC_API_KEY`
- `max_retries=3` production'da standart
- Büyük timeout gerektiren görevler için `timeout=httpx.Timeout(60.0, connect=5.0)`

## Common mistakes
- Sync client'ı async context'de çağırmak — event loop bloke olur.
- `client = anthropic.Anthropic()` çağrısını her istek için yineleyin — global veya singleton kullan.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-error-handling`
- `skills/llm-anthropic-streaming`
