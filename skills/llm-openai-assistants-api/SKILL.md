---
name: llm-openai-assistants-api
description: "OpenAI Assistants API ile kalıcı asistan, Thread ve Run nesneleri oluşturmak, file_search ve code_interpreter built-in araçlarını kullanmak ve run döngüsünü yönetmek gerektiğinde kullan."
---

## Purpose
Assistants API, durum yönetimini (Thread geçmişi) ve dosya bağlamını API tarafında saklar. Özellikle kod çalıştırma ve doküman arama gerektiren uygulamalar için uygundur.

## Asistan oluşturma
```python
assistant = client.beta.assistants.create(
    name="Observability Uzmanı",
    instructions="Prometheus, Loki ve Grafana konularında yardımcı ol.",
    model="gpt-4o",
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"}
    ]
)
assistant_id = assistant.id
```

## Thread ve mesaj
```python
# Yeni konuşma başlat:
thread = client.beta.threads.create()

# Mesaj ekle:
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Bu Prometheus datasının trendi nedir?",
    attachments=[{"file_id": file_id, "tools": [{"type": "code_interpreter"}]}]
)
```

## Run döngüsü
```python
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

while run.status not in ["completed", "failed", "cancelled"]:
    time.sleep(2)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status == "requires_action":
        # Tool call işleme:
        tool_outputs = []
        for tc in run.required_action.submit_tool_outputs.tool_calls:
            result = call_tool(tc.function.name, json.loads(tc.function.arguments))
            tool_outputs.append({"tool_call_id": tc.id, "output": str(result)})
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
        )
```

## Yanıt okuma
```python
messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc")
print(messages.data[0].content[0].text.value)
```

## Common mistakes
- Run bitmeden mesajları okumak — yanıt henüz eklenmemiş.
- `requires_action` durumunu yönetmeden döngüyü sonlandırmak — run takılı kalır.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-openai-function-calling`
- `skills/llm-openai-responses-api`
