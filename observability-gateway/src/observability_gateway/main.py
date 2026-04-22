"""FastAPI application entrypoint for the observability gateway."""

from __future__ import annotations

import os
from typing import Any

import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from observability_gateway.config import GatewaySettings, load_settings
from observability_gateway.models import (
    ErrorResponse,
    HealthResponse,
    LogsQueryRangeRequest,
    MetricsQueryRequest,
    StatusResponse,
    TraceDetailResponse,
    TracesSearchRequest,
)
from observability_gateway.service import BackendRequestError, ObservabilityService


def create_app(
    settings: GatewaySettings | None = None,
    *,
    env: dict[str, str] | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
) -> FastAPI:
    """Build a configured FastAPI app instance."""

    resolved_env = dict(env or os.environ)
    resolved_settings = settings or load_settings(env=resolved_env)
    service = ObservabilityService(resolved_settings, env=resolved_env, transport=transport)

    app = FastAPI(title=resolved_settings.service_name, version=resolved_settings.service_version)
    app.state.gateway_settings = resolved_settings
    app.state.gateway_service = service

    @app.exception_handler(BackendRequestError)
    async def handle_backend_error(_: Request, exc: BackendRequestError) -> JSONResponse:
        payload = ErrorResponse(
            error={
                "backend": exc.backend,
                "status": exc.status,
                "message": exc.message,
                "retryable": exc.retryable,
            }
        )
        return JSONResponse(status_code=exc.status, content=payload.model_dump())

    @app.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(
            service=resolved_settings.service_name,
            version=resolved_settings.service_version,
        )

    @app.get("/api/v1/status", response_model=StatusResponse)
    async def status() -> StatusResponse:
        backends = await service.status()
        return StatusResponse(
            service=resolved_settings.service_name,
            version=resolved_settings.service_version,
            http=resolved_settings.http.model_dump(),
            backends=backends,
        )

    @app.post("/api/v1/metrics/query")
    async def query_metrics(payload: MetricsQueryRequest) -> dict[str, Any]:
        return (await service.query_metrics(payload)).model_dump()

    @app.post("/api/v1/logs/query_range")
    async def query_logs(payload: LogsQueryRangeRequest) -> dict[str, Any]:
        return (await service.query_logs(payload)).model_dump()

    @app.post("/api/v1/traces/search")
    async def search_traces(payload: TracesSearchRequest) -> dict[str, Any]:
        return (await service.search_traces(payload)).model_dump()

    @app.get("/api/v1/traces/{trace_id}", response_model=TraceDetailResponse)
    async def get_trace(trace_id: str) -> TraceDetailResponse:
        return await service.get_trace(trace_id)

    return app


app = create_app()


def run() -> None:
    """Run the development server."""

    uvicorn.run(
        "observability_gateway.main:app",
        host="0.0.0.0",
        port=8091,
        reload=False,
    )
