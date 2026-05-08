---
name: llm-anthropic-computer-use
description: "Anthropic computer use (bilgisayar kullanımı) API'sini entegre etmek; screenshot, mouse_move, left_click, type ve key araçlarıyla modelin GUI otomasyonu yapmasını sağlamak gerektiğinde kullan."
---

## Purpose
Computer use, Claude'a ekran görüntüsü alıp GUI elementlerine tıklatma, metin yazma ve klavye kısayolları kullandırma yeteneği verir. Otomasyon ve RPA senaryoları için kullanılır.

## Araçlar
```python
tools = [
    {"type": "computer_20241022", "name": "computer", "display_width_px": 1280, "display_height_px": 768},
    {"type": "bash_20241022", "name": "bash"},
    {"type": "text_editor_20241022", "name": "str_replace_editor"}
]
```

## İstek yapısı
```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    tools=tools,
    messages=[{"role": "user", "content": "Tarayıcıyı aç ve Google'a git."}]
)
```

## Araç action'ları
```json
// screenshot
{"type": "computer", "action": "screenshot"}

// tıklama
{"type": "computer", "action": "left_click", "coordinate": [640, 400]}

// metin yazma
{"type": "computer", "action": "type", "text": "Hello world"}

// klavye kısayolu
{"type": "computer", "action": "key", "text": "ctrl+c"}
```

## Döngü implementasyonu
```python
while True:
    response = client.messages.create(...)
    if response.stop_reason == "end_turn":
        break
    # tool_use block'larını işle
    # screenshot sonucunu base64 ile tool_result olarak döndür
```

## Dikkat noktaları
- Her screenshot base64 encode edilir; token maliyeti yüksektir.
- Gerçek bir desktop ortamı (VNC, xvfb) veya Docker container gerekmektedir.
- Model koordinat tahmini yapabilir ama yanılabilir; hata toleransı tasarla.

## Common mistakes
- Screenshot sıklığını her adımda zorunlu tutmak — maliyet patlar; yalnızca gerektiğinde al.
- Güvenlik denetimi olmadan modelin terminal/bash araçlarına erişim vermek.

## References
- `skills/llm-anthropic-tool-use`
- `skills/llm-anthropic-messages-api`
