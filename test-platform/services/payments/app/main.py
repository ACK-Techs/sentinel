import logging

from app.config import settings
from sentinel_obs import (
    ChaosMiddleware,
    build_admin_router,
    chaos_settings,
    get_chaos_manager,
    init_telemetry,
    instrument_app,
    instrument_redis,
    instrument_sqlalchemy,
    register_db_slow_hook,
)

init_telemetry(settings.service_name, settings.service_version, settings.deployment_env)

from app.db import engine, redis_client, verify_schema  # noqa: E402
from app.routes.payments import router as payments_router  # noqa: E402
from fastapi import FastAPI  # noqa: E402

app = FastAPI(title="payments")
logger = logging.getLogger("payments.startup")
manager = get_chaos_manager("payments", chaos_settings(settings.chaos_token))
app.add_middleware(ChaosMiddleware, manager=manager)
instrument_app(app)
instrument_redis()
instrument_sqlalchemy(engine)
register_db_slow_hook(engine, manager)
app.include_router(payments_router)
app.include_router(build_admin_router(manager, settings.chaos_token))


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": settings.service_name}


@app.on_event("startup")
async def startup_event() -> None:
    if not await verify_schema():
        logger.error(
            "payments schema missing; run python scripts/seed_db.py before starting services"
        )
        raise SystemExit(1)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await redis_client.aclose()
    await engine.dispose()
