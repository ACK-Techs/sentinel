"""FastAPI application entrypoint for the observability gateway."""

from __future__ import annotations

import os
from typing import Any

import httpx
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, Request
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

    async def require_gateway_auth(
        authorization: str | None = Header(default=None),
    ) -> None:
        token_env = resolved_settings.auth_token_env
        expected_token = resolved_env.get(token_env) if token_env else None
        if not expected_token:
            return

        expected_header = f"Bearer {expected_token}"
        if authorization == expected_header:
            return

        raise HTTPException(
            status_code=401,
            detail={
                "error": {
                    "backend": "gateway",
                    "status": 401,
                    "message": "Gateway authentication failed.",
                    "retryable": False,
                }
            },
        )

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

    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict) and "error" in exc.detail:
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        payload = ErrorResponse(
            error={
                "backend": "gateway",
                "status": exc.status_code,
                "message": str(exc.detail),
                "retryable": False,
            }
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    @app.get("/health", response_model=HealthResponse)
    async def health(_: None = Depends(require_gateway_auth)) -> HealthResponse:
        return HealthResponse(
            service=resolved_settings.service_name,
            version=resolved_settings.service_version,
        )

    @app.get("/api/v1/status", response_model=StatusResponse)
    async def gateway_status(_: None = Depends(require_gateway_auth)) -> StatusResponse:
        backends = await service.status()
        return StatusResponse(
            service=resolved_settings.service_name,
            version=resolved_settings.service_version,
            http=resolved_settings.http.model_dump(),
            backends=backends,
        )

    @app.post("/api/v1/metrics/query")
    async def query_metrics(
        payload: MetricsQueryRequest,
        _: None = Depends(require_gateway_auth),
    ) -> dict[str, Any]:
        return (await service.query_metrics(payload)).model_dump()

    @app.post("/api/v1/logs/query_range")
    async def query_logs(
        payload: LogsQueryRangeRequest,
        _: None = Depends(require_gateway_auth),
    ) -> dict[str, Any]:
        return (await service.query_logs(payload)).model_dump()

    @app.post("/api/v1/traces/search")
    async def search_traces(
        payload: TracesSearchRequest,
        _: None = Depends(require_gateway_auth),
    ) -> dict[str, Any]:
        return (await service.search_traces(payload)).model_dump()

    @app.get("/api/v1/traces/{trace_id}", response_model=TraceDetailResponse)
    async def get_trace(
        trace_id: str,
        _: None = Depends(require_gateway_auth),
    ) -> TraceDetailResponse:
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
