"""Read-only observability tools backed by the observability gateway."""

from __future__ import annotations

import os

from pydantic import BaseModel, ConfigDict, Field, model_validator

from sentinel_cli.config.models import ObservabilityGatewaySettings
from sentinel_cli.observability import GatewayClient, GatewayClientError
from sentinel_cli.tools.base import ToolContext, ToolResult


class ObsMetricQueryArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str


class ObsLogsQueryArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str | None = None
    query: str | None = None
    limit: int = Field(default=20, ge=1, le=5000)

    @model_validator(mode="after")
    def validate_selector(self) -> "ObsLogsQueryArgs":
        if not self.service and not self.query:
            raise ValueError("service veya query alanlarindan biri gerekli.")
        return self


class ObsTracesSearchArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str | None = None
    query: str | None = None
    limit: int = Field(default=20, ge=1, le=500)

    @model_validator(mode="after")
    def validate_selector(self) -> "ObsTracesSearchArgs":
        if not self.service and not self.query:
            raise ValueError("service veya query alanlarindan biri gerekli.")
        return self


class ObsTraceGetArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trace_id: str


class _ObservabilityGatewayTool:
    risk_level = "read-safe"

    def __init__(self, settings: ObservabilityGatewaySettings) -> None:
        self._settings = settings

    def definition(self):
        from sentinel_cli.llm.types import ToolDefinition

        return ToolDefinition(
            name=self.name,
            description=self.description,
            input_schema=self.args_model.model_json_schema(),
        )

    def _client(self) -> GatewayClient:
        return GatewayClient(self._settings, env=dict(os.environ))


class ObsMetricQueryTool(_ObservabilityGatewayTool):
    name = "obs_metric_query"
    description = "Observability gateway uzerinden read-only metric sorgusu yapar."
    args_model = ObsMetricQueryArgs

    def execute(self, arguments: ObsMetricQueryArgs, context: ToolContext) -> ToolResult:
        del context
        try:
            payload = self._client().query_metric(arguments.query)
        except GatewayClientError as exc:
            return ToolResult(False, "GATEWAY_ERROR", exc.message, data=None)
        return ToolResult(True, "OK", "Metric sorgusu tamamlandi.", data=payload)


class ObsLogsQueryTool(_ObservabilityGatewayTool):
    name = "obs_logs_query"
    description = "Observability gateway uzerinden read-only log sorgusu yapar."
    args_model = ObsLogsQueryArgs

    def execute(self, arguments: ObsLogsQueryArgs, context: ToolContext) -> ToolResult:
        del context
        try:
            payload = self._client().query_logs(
                service=arguments.service,
                query=arguments.query,
                limit=arguments.limit,
            )
        except GatewayClientError as exc:
            return ToolResult(False, "GATEWAY_ERROR", exc.message, data=None)
        return ToolResult(True, "OK", "Log sorgusu tamamlandi.", data=payload)


class ObsTracesSearchTool(_ObservabilityGatewayTool):
    name = "obs_traces_search"
    description = "Observability gateway uzerinden read-only trace aramasi yapar."
    args_model = ObsTracesSearchArgs

    def execute(self, arguments: ObsTracesSearchArgs, context: ToolContext) -> ToolResult:
        del context
        try:
            payload = self._client().search_traces(
                service=arguments.service,
                query=arguments.query,
                limit=arguments.limit,
            )
        except GatewayClientError as exc:
            return ToolResult(False, "GATEWAY_ERROR", exc.message, data=None)
        return ToolResult(True, "OK", "Trace aramasi tamamlandi.", data=payload)


class ObsTraceGetTool(_ObservabilityGatewayTool):
    name = "obs_trace_get"
    description = "Observability gateway uzerinden read-only trace detayi getirir."
    args_model = ObsTraceGetArgs

    def execute(self, arguments: ObsTraceGetArgs, context: ToolContext) -> ToolResult:
        del context
        try:
            payload = self._client().get_trace(arguments.trace_id)
        except GatewayClientError as exc:
            return ToolResult(False, "GATEWAY_ERROR", exc.message, data=None)
        return ToolResult(True, "OK", "Trace detayi alindi.", data=payload)
