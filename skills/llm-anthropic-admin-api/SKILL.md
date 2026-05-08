---
name: llm-anthropic-admin-api
description: "Anthropic Admin API ile API key yönetimi yapmak, organizasyon üyelerini listelemek, kullanım istatistiklerini çekmek ve programatik hesap yönetimi kurmak gerektiğinde kullan."
---

## Purpose
Admin API, bireysel API key'in değil organizasyon yöneticisinin erişim yetkisiyle API key oluşturma, kota izleme ve kullanım verisi çekme işlemlerini sağlar.

## Kimlik doğrulama
```python
import anthropic

admin_client = anthropic.Anthropic(
    api_key=os.environ["ANTHROPIC_ADMIN_KEY"]  # Admin API key (farklı!)
)
```

## API Key yönetimi
```python
# Yeni API key oluştur:
new_key = admin_client.admin.api_keys.create(
    name="production-service",
    workspace_id="wrkspc_..."  # opsiyonel
)
print(new_key.secret)  # Yalnızca bir kez görünür!

# Mevcut key'leri listele:
keys = admin_client.admin.api_keys.list()
for key in keys.data:
    print(key.id, key.name, key.status)

# Key devre dışı bırak:
admin_client.admin.api_keys.update(key_id, status="inactive")
```

## Kullanım istatistikleri
```python
usage = admin_client.admin.usage.messages.get(
    start_time="2024-01-01T00:00:00Z",
    end_time="2024-01-31T23:59:59Z"
)
print(f"Toplam input tokens: {usage.input_tokens}")
print(f"Toplam maliyet: ${usage.total_cost:.4f}")
```

## Workspace yönetimi
```python
workspaces = admin_client.admin.workspaces.list()
for ws in workspaces.data:
    print(ws.id, ws.name)
```

## Common mistakes
- Normal API key ile Admin API'ye erişmeye çalışmak — 403 hatası.
- Yeni oluşturulan API key'in `secret` alanını kaydetmemek — bir daha görüntülenemez.
- Admin API'yi production servis kodu içinde kullanmak — ayrı yönetim script'inde tutulmalı.

## References
- `skills/llm-anthropic-sdk-python`
- `skills/llm-anthropic-rate-limits`
