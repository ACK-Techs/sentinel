from __future__ import annotations

from app.clients import inventory_client, orders_client
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/api/orders")
async def create_order(payload: dict) -> dict:
    response = await orders_client.post("/orders", json=payload)
    if response.is_error:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


@router.get("/api/orders/{order_id}")
async def get_order(order_id: str) -> dict:
    response = await orders_client.get(f"/orders/{order_id}")
    if response.is_error:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


@router.get("/api/inventory/{sku}")
async def get_inventory(sku: str) -> dict:
    response = await inventory_client.get(f"/inventory/{sku}")
    if response.is_error:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
