---
name: llm-openai-realtime-api
description: "OpenAI Realtime API ile WebSocket üzerinden düşük gecikmeli ses konuşması veya metin tabanlı gerçek zamanlı etkileşim kurmak; session, input_audio_buffer ve response event döngüsünü yönetmek gerektiğinde kullan."
---

## Purpose
Realtime API, WebSocket üzerinden ses giriş/çıkışını mümkün kılar. Standart TTS+Whisper zincirinden 10x daha düşük gecikme sağlar; ses asistanı ve canlı tercüme için kullanılır.

## Bağlantı kurulumu
```python
import websockets
import json

WS_URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"

async with websockets.connect(
    WS_URL,
    extra_headers={
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "OpenAI-Beta": "realtime=v1"
    }
) as ws:
    # Session başlatma
    await ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "modalities": ["text", "audio"],
            "voice": "alloy",
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "turn_detection": {"type": "server_vad"}
        }
    }))
```

## Ses gönderme
```python
# 16-bit PCM, 24kHz, mono audio chunk'larını base64 ile gönder:
await ws.send(json.dumps({
    "type": "input_audio_buffer.append",
    "audio": base64.b64encode(pcm_chunk).decode()
}))

# Konuşma bitince:
await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
await ws.send(json.dumps({"type": "response.create"}))
```

## Event akışı
```
→ session.created
← input_audio_buffer.committed
← response.created
← response.audio.delta     (ses parçaları)
← response.audio.done
← response.done
```

## Tool use ile Realtime
Session yapılandırmasına `tools` listesi eklenebilir; model `response.function_call_arguments.done` event'i üretir.

## Common mistakes
- PCM yerine MP3 göndermeye çalışmak — Realtime API yalnızca PCM/G711 destekler.
- `server_vad` olmadan konuşma sonu belirleme yapmak — manuel commit gerekir.
- Yüksek ağ gecikmeli ortamda latency beklentisini sıfıra koymak.

## References
- `skills/llm-openai-audio`
- `skills/llm-openai-chat-completion`
