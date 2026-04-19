from app.config import settings
from sentinel_obs import (
    ChaosMiddleware,
    build_admin_router,
    chaos_settings,
    get_chaos_manager,
    init_telemetry,
    instrument_app,
    instrument_httpx,
)

init_telemetry(settings.service_name, settings.service_version, settings.deployment_env)

from app.clients import close_clients  # noqa: E402
from app.routes.api import router as api_router  # noqa: E402
from fastapi import FastAPI  # noqa: E402

app = FastAPI(title="gateway")
manager = get_chaos_manager("gateway", chaos_settings(settings.chaos_token))
app.add_middleware(ChaosMiddleware, manager=manager)
instrument_app(app)
instrument_httpx()
app.include_router(api_router)
app.include_router(build_admin_router(manager, settings.chaos_token))


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": settings.service_name}


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await close_clients()

