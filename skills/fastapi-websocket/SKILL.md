---
name: fastapi-websocket
description: "FastAPI WebSocket endpoint ve bağlantı yönetimi — Sentinel canlı alert ve metrik akışı için"
---

## Purpose
Sentinel'in dashboard'u anlık alert durumunu ve metrik güncellemelerini WebSocket üzerinden alır. Bu skill bağlantı havuzu yönetimi, kimlik doğrulama, heartbeat ve graceful disconnect kalıplarını kapsar.

## Workflow

### 1. Connection manager

```python
# app/ws/manager.py
from fastapi import WebSocket
import asyncio
import structlog

log = structlog.get_logger()

class ConnectionManager:
    def __init__(self):
        self._connections: dict[str, set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, room: str, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._connections.setdefault(room, set()).add(ws)
        log.info("ws_connected", room=room, total=self.count(room))

    async def disconnect(self, room: str, ws: WebSocket) -> None:
        async with self._lock:
            self._connections.get(room, set()).discard(ws)
        log.info("ws_disconnected", room=room)

    async def broadcast(self, room: str, data: dict) -> None:
        dead: list[WebSocket] = []
        for ws in list(self._connections.get(room, [])):
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            await self.disconnect(room, ws)

    def count(self, room: str) -> int:
        return len(self._connections.get(room, set()))

manager = ConnectionManager()
```

### 2. WebSocket endpoint

```python
# app/api/v1/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from app.ws.manager import manager
from app.auth.ws import verify_ws_token

router = APIRouter()

@router.websocket("/ws/alerts")
async def alerts_ws(
    websocket: WebSocket,
    token: str = Query(...),
):
    user = await verify_ws_token(token)
    if user is None:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    room = f"alerts:{user.org_id}"
    await manager.connect(room, websocket)
    try:
        while True:
            # Heartbeat — client'tan ping bekle
            data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            if data == "ping":
                await websocket.send_text("pong")
    except asyncio.TimeoutError:
        log.warning("ws_heartbeat_timeout", room=room)
    except WebSocketDisconnect:
        pass
    finally:
        await manager.disconnect(room, websocket)
```

### 3. Alertmanager → WebSocket broadcast

```python
# app/services/alert_broadcaster.py
import asyncio
from app.ws.manager import manager

async def broadcast_alert_event(alert: Alert) -> None:
    payload = {
        "type": "alert",
        "severity": alert.severity,
        "name": alert.name,
        "status": alert.status,
        "fired_at": alert.fired_at.isoformat(),
    }
    await manager.broadcast(f"alerts:{alert.org_id}", payload)

# Periyodik metrik push
async def metric_push_loop():
    while True:
        metrics = await prometheus_service.get_summary()
        await manager.broadcast("metrics:global", {"type": "metrics", "data": metrics})
        await asyncio.sleep(5)
```

### 4. WS token doğrulama

```python
# app/auth/ws.py
from app.auth.jwt import decode_token
from app.models.auth import CurrentUser

async def verify_ws_token(token: str) -> CurrentUser | None:
    payload = decode_token(token)
    if payload is None:
        return None
    return CurrentUser(id=payload["sub"], roles=payload["roles"])
```

## Common mistakes

- WebSocket'i JWT header ile doğrulamaya çalışmak — browser WebSocket API header desteklemez; query param veya ilk mesaj olarak gönder
- `manager.broadcast` sırasında dead connection'ları temizlememek — bellek sızıntısı
- `receive_text()` için timeout koymamak — client sessiz kaldığında goroutine sonsuza kadar bloklanır
- `WebSocketDisconnect` catch etmemek — normal disconnect durumunda unhandled exception logu dolar

## References
- `skills/fastapi-security-oauth2`
- `skills/fastapi-streaming-response`
- `skills/fastapi-observability`
