import logging

from app.config import settings
from sentinel_obs import (
    ChaosMiddleware,
    build_admin_router,
    chaos_settings,
    get_chaos_manager,
    init_telemetry,
    instrument_app,
    instrument_httpx,
    instrument_redis,
    instrument_sqlalchemy,
    register_db_slow_hook,
)

init_telemetry(settings.service_name, settings.service_version, settings.deployment_env)

from app.clients.downstream import close_clients  # noqa: E402
from app.db import engine, redis_client, verify_schema  # noqa: E402
from app.routes.orders import router as orders_router  # noqa: E402
from fastapi import FastAPI  # noqa: E402

app = FastAPI(title="orders")
logger = logging.getLogger("orders.startup")
manager = get_chaos_manager("orders", chaos_settings(settings.chaos_token))
app.add_middleware(ChaosMiddleware, manager=manager)
instrument_app(app)
instrument_httpx()
instrument_redis()
instrument_sqlalchemy(engine)
register_db_slow_hook(engine, manager)
app.include_router(orders_router)
app.include_router(build_admin_router(manager, settings.chaos_token))


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": settings.service_name}


@app.on_event("startup")
async def startup_event() -> None:
    if not await verify_schema():
        logger.error(
            "orders schema missing; run python scripts/seed_db.py before starting services"
        )
        raise SystemExit(1)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await close_clients()
    await redis_client.aclose()
    await engine.dispose()
