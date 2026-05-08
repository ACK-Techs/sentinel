---
name: fastapi-dependency-injection
description: "FastAPI Depends() ile bağımlılık enjeksiyonu — Sentinel servislerinde test edilebilir, override edilebilir dependency mimarisi"
---

## Purpose
FastAPI'nin `Depends()` sistemi, route handler'lardan servis nesnelerini, veritabanı session'larını, kimlik doğrulama bilgilerini ve konfigürasyon değerlerini ayırır. Sentinel'de her bağımlılık ayrı factory fonksiyonu olarak tanımlanır; testlerde `app.dependency_overrides` ile kolayca mock'lanır.

## Workflow

### 1. Temel dependency factory

```python
# app/dependencies.py
from functools import lru_cache
from fastapi import Depends, HTTPException, Header
from app.config import SentinelSettings
from app.clients.tempo_client import TempoClient
from app.services.tempo_service import TempoService

@lru_cache
def get_settings() -> SentinelSettings:
    return SentinelSettings()

async def get_tempo_client(
    settings: SentinelSettings = Depends(get_settings),
) -> TempoClient:
    return TempoClient(
        base_url=settings.tempo_url,
        timeout=settings.tempo_timeout,
    )

async def get_tempo_service(
    client: TempoClient = Depends(get_tempo_client),
) -> TempoService:
    return TempoService(client=client)
```

### 2. Kimlik doğrulama dependency

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import verify_jwt_token
from app.models.auth import CurrentUser

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    settings: SentinelSettings = Depends(get_settings),
) -> CurrentUser:
    token = credentials.credentials
    payload = verify_jwt_token(token, secret=settings.jwt_secret.get_secret_value())
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    return CurrentUser(id=payload["sub"], roles=payload.get("roles", []))

# Route'da kullanım
@router.get("/traces/{id}")
async def get_trace(
    trace_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    service: TempoService = Depends(get_tempo_service),
):
    ...
```

### 3. Zincirleme dependency ve scope

```python
# Request başına bir kez oluşturulan DB session
from contextlib import asynccontextmanager
import asyncpg

async def get_db_pool(
    settings: SentinelSettings = Depends(get_settings),
) -> asyncpg.Pool:
    # Connection pool global state'te tutulur, lifespan'da oluşturulur
    from app.state import db_pool
    return db_pool

async def get_db_session(
    pool: asyncpg.Pool = Depends(get_db_pool),
) -> asyncpg.Connection:
    async with pool.acquire() as conn:
        yield conn  # generator: request bittikten sonra release
```

### 4. Test override

```python
# tests/conftest.py
from unittest.mock import AsyncMock
from app.dependencies import get_tempo_service
from app.main import create_app

@pytest_asyncio.fixture
async def client_with_mock_tempo():
    mock_service = AsyncMock(spec=TempoService)
    mock_service.get_trace.return_value = TraceResponse(id="test-123", spans=[])

    app = create_app()
    app.dependency_overrides[get_tempo_service] = lambda: mock_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac, mock_service
```

### 5. Dependency parametreli (closure factory)

```python
def require_role(role: str):
    """Belirli bir role sahip kullanıcı gerektirir."""
    async def _check(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if role not in user.roles:
            raise HTTPException(403, f"{role} yetkisi gerekli")
        return user
    return _check

@router.delete("/alerts/{id}")
async def delete_alert(
    alert_id: str,
    _: CurrentUser = Depends(require_role("admin")),
):
    ...
```

## Common mistakes

- `Depends(get_settings())` — parantez fazla, her request'te yeni instance oluşturur
- Async olmayan generator'ı `async def` ile karıştırmak — `yield` içeren dependency ya tamamen sync ya tamamen async olmalı
- `lru_cache` ile async dependency kullanmak — `lru_cache` async fonksiyonlarla çalışmaz, sadece sync factory'lerde kullan
- `dependency_overrides` temizlememek test sonrası — fixture scope sonunda `app.dependency_overrides.clear()` çağır

## References
- `skills/fastapi-app-structure`
- `skills/fastapi-security-oauth2`
- `skills/fastapi-testing`
