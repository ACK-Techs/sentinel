---
name: fastapi-security-apikey
description: "FastAPI API key doğrulama middleware — Sentinel servis-arası ve CLI kimlik doğrulama için"
---

## Purpose
Servis-arası iletişimde ve CLI araçlarında JWT'nin overhead'i gerekmeyebilir; API key yeterlidir. Sentinel'in internal API'leri header veya query param API key kabul eder. Key'ler hashed olarak saklanır, maskelenerek loglanır.

## Workflow

### 1. API key model ve storage

```python
# app/models/api_key.py
from pydantic import BaseModel, SecretStr
import hashlib
import secrets

class APIKey(BaseModel):
    id: str
    name: str
    key_hash: str          # bcrypt veya sha256 hash
    scopes: list[str]
    is_active: bool = True
    created_at: str

def generate_api_key() -> tuple[str, str]:
    """(raw_key, hashed_key) döndürür. raw_key yalnızca bir kez gösterilir."""
    raw = f"sk_{secrets.token_urlsafe(32)}"
    hashed = hashlib.sha256(raw.encode()).hexdigest()
    return raw, hashed

def verify_api_key(raw: str, stored_hash: str) -> bool:
    return hashlib.sha256(raw.encode()).hexdigest() == stored_hash
```

### 2. Header ve query param dual support

```python
# app/dependencies.py
from fastapi import Security, Depends, HTTPException
from fastapi.security import APIKeyHeader, APIKeyQuery

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)

async def get_api_key(
    header_key: str | None = Security(api_key_header),
    query_key: str | None = Security(api_key_query),
    key_service: APIKeyService = Depends(get_key_service),
) -> APIKey:
    raw_key = header_key or query_key
    if raw_key is None:
        raise HTTPException(403, "API key gerekli")

    api_key = await key_service.lookup(raw_key)
    if api_key is None or not api_key.is_active:
        raise HTTPException(403, "Geçersiz veya devre dışı API key")

    return api_key
```

### 3. Scope bazlı yetkilendirme

```python
def require_scope(scope: str):
    async def _check(api_key: APIKey = Depends(get_api_key)) -> APIKey:
        if scope not in api_key.scopes:
            raise HTTPException(
                403, f"Bu işlem '{scope}' scope'u gerektiriyor"
            )
        return api_key
    return _check

# Kullanım
@router.delete("/alerts/{id}")
async def delete_alert(
    alert_id: str,
    _: APIKey = Depends(require_scope("alerts:write")),
):
    ...
```

### 4. Key yönetim endpoint'i

```python
@admin_router.post("/api-keys", response_model=APIKeyCreateResponse)
async def create_api_key(
    request: APIKeyCreateRequest,
    current_user: CurrentUser = Depends(require_role("admin")),
    key_service: APIKeyService = Depends(get_key_service),
):
    raw_key, hashed = generate_api_key()
    api_key = await key_service.create(
        name=request.name,
        key_hash=hashed,
        scopes=request.scopes,
    )
    # raw_key yalnızca bu yanıtta bir kez döner
    return APIKeyCreateResponse(
        id=api_key.id,
        key=raw_key,  # Bir kez göster, saklamıyoruz
        warning="Bu key'i güvenli bir yerde saklayın. Tekrar gösterilmeyecek.",
    )
```

### 5. Rate limiting ile API key kombinasyonu

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=lambda request: request.headers.get("X-API-Key", get_remote_address(request)))

@router.get("/metrics/query")
@limiter.limit("100/minute")
async def query_metrics(request: Request, api_key: APIKey = Depends(get_api_key)):
    ...
```

## Common mistakes

- API key'i plaintext olarak veritabanında saklamak — her zaman hash'le, raw key'i yalnızca oluşturulduğunda göster
- `auto_error=True` ile query param ve header ikisini birden tanımlamak — ikisi de None ise çift 403 fırlatır
- Key'i URL'de query param olarak loglamak — access log'lara düşer, header tercih edilmeli
- Scope'ları token claim yerine DB'den her istekte çekmek — cache veya token embed kullan

## References
- `skills/fastapi-security-oauth2`
- `skills/fastapi-rate-limiting`
- `skills/python-secrets-runtime`
