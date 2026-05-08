"""COS installer stub."""

from __future__ import annotations

from sentinel_cli.discovery import discover_and_write_config
from sentinel_cli.installers.base import BaseInstaller


class CosInstaller(BaseInstaller):
    def preflight(self) -> None:
        self._todo("preflight")

    def install(self) -> None:
        self._todo("install")

    def wire(self) -> None:
        endpoints, config_path = discover_and_write_config("cos")
        self.context.console.print(f"Grafana: {endpoints.grafana_url}")
        self.context.console.print(f"Gateway: {endpoints.gateway_url}")
        self.context.console.print(f"Sentinel config: [bold]{config_path}[/bold]")
        for warning in endpoints.warnings:
            self.context.console.print(f"[yellow]Discovery warning:[/yellow] {warning}")

    def verify(self) -> None:
        self._todo("verify")
