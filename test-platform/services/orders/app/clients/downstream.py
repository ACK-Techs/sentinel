from __future__ import annotations

import httpx
from app.config import settings
from fastapi import HTTPException

timeout = httpx.Timeout(2.0, connect=0.5)
payments_client = httpx.AsyncClient(base_url=settings.payments_url, timeout=timeout)
inventory_client = httpx.AsyncClient(base_url=settings.inventory_url, timeout=timeout)


async def close_clients() -> None:
    await payments_client.aclose()
    await inventory_client.aclose()


def ensure_downstream_available(blocked: bool, target: str) -> None:
    if blocked:
        raise HTTPException(status_code=502, detail=f"chaos blocked downstream service: {target}")

