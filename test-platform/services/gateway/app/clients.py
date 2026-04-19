from __future__ import annotations

import httpx
from app.config import settings

timeout = httpx.Timeout(2.0, connect=0.5)
orders_client = httpx.AsyncClient(base_url=settings.orders_url, timeout=timeout)
inventory_client = httpx.AsyncClient(base_url=settings.inventory_url, timeout=timeout)


async def close_clients() -> None:
    await orders_client.aclose()
    await inventory_client.aclose()

