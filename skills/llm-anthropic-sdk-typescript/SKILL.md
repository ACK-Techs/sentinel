---
name: llm-anthropic-sdk-typescript
description: "Anthropic TypeScript SDK'yı Node.js veya frontend projelerinde kurup kullanmak, streaming ile React/Next.js entegrasyonu yapmak ve SDK tip tanımlarından yararlanmak gerektiğinde kullan."
---

## Purpose
TypeScript SDK, Python SDK ile paralel API sunar. Tip güvenliği sayesinde IDE otomatik tamamlama ve derleme zamanı hata tespiti sağlar.

## Kurulum
```bash
npm install @anthropic-ai/sdk
# veya
yarn add @anthropic-ai/sdk
```

## Temel kullanım
```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
  maxRetries: 3,
  timeout: 30000,
});

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Merhaba" }],
});

const text = response.content[0];
if (text.type === "text") {
  console.log(text.text);
}
```

## Streaming (Node.js)
```typescript
const stream = await client.messages.stream({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Kısa hikaye yaz." }],
});

for await (const chunk of stream) {
  if (chunk.type === "content_block_delta" && chunk.delta.type === "text_delta") {
    process.stdout.write(chunk.delta.text);
  }
}

const finalMessage = await stream.finalMessage();
console.log("Tokens:", finalMessage.usage);
```

## Next.js API route (streaming)
```typescript
// app/api/chat/route.ts
import Anthropic from "@anthropic-ai/sdk";

export async function POST(req: Request) {
  const { message } = await req.json();
  const client = new Anthropic();

  const stream = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    stream: true,
    messages: [{ role: "user", content: message }],
  });

  return new Response(stream.toReadableStream());
}
```

## Common mistakes
- `content[0].text` yerine type guard olmadan doğrudan erişim; tool_use block gelince runtime hatası.
- Browser ortamında API key'i client-side JavaScript'e gömmek — büyük güvenlik açığı.

## References
- `skills/llm-anthropic-messages-api`
- `skills/llm-anthropic-streaming`
- `skills/llm-anthropic-sdk-python`
