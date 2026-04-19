from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Annotated, cast
from uuid import uuid4

import httpx
from app.clients.downstream import ensure_downstream_available, inventory_client, payments_client
from app.config import settings
from app.db import cache_order, get_cached_order, get_order, get_session, redis_client
from app.models import Order
from fastapi import APIRouter, Depends, HTTPException
from sentinel_obs import chaos_settings, downstream_behavior, get_chaos_manager, get_meter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = logging.getLogger("orders")
meter = get_meter("orders")
orders_created = meter.create_counter("app.orders.created", unit="1")
order_latency = meter.create_histogram("app.order.latency", unit="ms")
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/orders", status_code=201)
async def create_order(payload: dict, session: SessionDep) -> dict:
    sku = str(payload["sku"])
    qty = int(payload["qty"])
    amount = int(payload.get("amount", qty * 10))
    order_id = str(payload.get("order_id") or uuid4())
    start = datetime.now(UTC)
    manager = get_chaos_manager("orders", chaos_settings(settings.chaos_token))
    pay_blocked, pay_timeout = downstream_behavior(manager, "payments")
    inv_blocked, inv_timeout = downstream_behavior(manager, "inventory")
    ensure_downstream_available(pay_blocked, "payments")
    ensure_downstream_available(inv_blocked, "inventory")
    pay_task = payments_client.post(
        "/charge",
        json={"order_id": order_id, "amount": amount},
        timeout=httpx.Timeout(pay_timeout or 2.0, connect=0.5),
    )
    inv_task = inventory_client.post(
        "/reserve",
        json={"sku": sku, "qty": qty},
        timeout=httpx.Timeout(inv_timeout or 2.0, connect=0.5),
    )
    raw_results = await asyncio.gather(pay_task, inv_task, return_exceptions=True)
    pay_result, inv_result = cast(
        tuple[httpx.Response | Exception, httpx.Response | Exception],
        tuple(raw_results),
    )
    for result in (pay_result, inv_result):
        if isinstance(result, Exception):
            logger.exception("downstream request failed", exc_info=result)
            raise HTTPException(status_code=502, detail="downstream request failure") from result
        if isinstance(result, httpx.Response) and result.status_code >= 400:
            raise HTTPException(status_code=502, detail="downstream returned error")

    order = Order(id=order_id, sku=sku, qty=qty, amount=amount, status="created")
    session.add(order)
    await session.commit()
    await cache_order(order)
    await redis_client.xadd(
        settings.orders_stream,
        {
            "event_type": "order.created",
            "order_id": order_id,
            "created_at": datetime.now(UTC).isoformat(),
        },
    )
    latency_ms = (datetime.now(UTC) - start).total_seconds() * 1000
    orders_created.add(1, {"status": "created"})
    order_latency.record(latency_ms, {"status": "created"})
    return {"order_id": order_id, "status": "created"}


@router.get("/orders/{order_id}")
async def fetch_order(order_id: str, session: SessionDep) -> dict:
    cached = await get_cached_order(order_id)
    if cached:
        return cached
    order = await get_order(session, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    await cache_order(order)
    return {
        "id": order.id,
        "sku": order.sku,
        "qty": order.qty,
        "amount": order.amount,
        "status": order.status,
    }
