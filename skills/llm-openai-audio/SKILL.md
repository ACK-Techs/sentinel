---
name: llm-openai-audio
description: "OpenAI Whisper ile ses dosyasını metne dönüştürmek (transcription/translation) veya TTS API ile metni sese çevirmek gerektiğinde kullan."
---

## Purpose
İki farklı audio API: Whisper (speech-to-text) ve TTS (text-to-speech). İkisi de Chat Completions'tan bağımsız endpoint'ler kullanır.

## Whisper — Ses'ten Metne
```python
with open("konusma.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="tr",        # opsiyonel; otomatik tespit
        response_format="text"  # "json" | "text" | "srt" | "vtt" | "verbose_json"
    )
print(transcript)
```

### Çeviri (translation) — Direkt İngilizce'ye
```python
translation = client.audio.translations.create(
    model="whisper-1",
    file=audio_file
)
```

### Timestamp ile VTT/SRT altyazı
```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="srt",
    timestamp_granularities=["word"]  # verbose_json ile
)
```

## TTS — Metinden Ses
```python
response = client.audio.speech.create(
    model="tts-1",        # "tts-1-hd" (yüksek kalite)
    voice="alloy",        # alloy | echo | fable | onyx | nova | shimmer
    input="Merhaba, bu bir test mesajıdır.",
    speed=1.0             # 0.25–4.0
)
response.stream_to_file("output.mp3")
```

## Desteklenen formatlar
- Giriş: mp3, mp4, mpeg, mpga, m4a, wav, webm (maks 25MB)
- Çıktı: mp3, opus, aac, flac, wav, pcm

## Common mistakes
- 25MB'dan büyük ses dosyasını doğrudan göndermek — dosyayı ffmpeg ile bölmek gerekir.
- TTS'te `tts-1-hd` yerine `tts-1` kullanmak gerçek zamanlı uygulamalar için daha hızlı.
- Whisper'ın `language` parametresi olmadan çok dilli audio'da karışık çıktı üretmesi.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-openai-realtime-api`
