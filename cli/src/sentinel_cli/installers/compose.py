"""Docker Compose installer."""

from __future__ import annotations

import os
import shutil
import subprocess
from importlib import resources
from pathlib import Path

from sentinel_cli.cli.errors import EXIT_TOOL, UserFacingError
from sentinel_cli.discovery import discover_and_write_config
from sentinel_cli.installers.base import BaseInstaller


class ComposeInstaller(BaseInstaller):
    target_dir = Path("sentinel-compose")

    def preflight(self) -> None:
        if self.context.dry_run:
            self.context.console.print("[yellow]DRY-RUN[/yellow] docker compose version")
            return

        if shutil.which("docker") is None:
            raise UserFacingError(
                "Docker bulunamadi. Compose kurulumu icin docker CLI gerekli.",
                EXIT_TOOL,
            )

        self._run(["docker", "compose", "version"], cwd=Path.cwd())

    def install(self) -> None:
        target = Path.cwd() / self.target_dir
        self._copy_assets(target)

        command = ["docker", "compose", "up", "-d"]
        if self.context.dry_run:
            self.context.console.print(
                f"[yellow]DRY-RUN[/yellow] cd {target} && {' '.join(command)}"
            )
            return

        self._run(command, cwd=target)

    def wire(self) -> None:
        target = Path.cwd() / self.target_dir
        self.context.console.print(f"Compose bundle: [bold]{target}[/bold]")
        if self.context.dry_run:
            self.context.console.print(
                "[yellow]DRY-RUN[/yellow] discover endpoints and write ~/.sentinel/config.yaml"
            )
            return

        endpoints, config_path = discover_and_write_config("compose", cwd=Path.cwd())
        self.context.console.print(f"Grafana: {endpoints.grafana_url}")
        self.context.console.print(f"Gateway: {endpoints.gateway_url}")
        self.context.console.print(f"Sentinel config: [bold]{config_path}[/bold]")
        for warning in endpoints.warnings:
            self.context.console.print(f"[yellow]Discovery warning:[/yellow] {warning}")

    def verify(self) -> None:
        target = Path.cwd() / self.target_dir
        command = ["docker", "compose", "ps"]
        if self.context.dry_run:
            self.context.console.print(
                f"[yellow]DRY-RUN[/yellow] cd {target} && {' '.join(command)}"
            )
            return

        self._run(command, cwd=target)

    def _copy_assets(self, target: Path) -> None:
        if self.context.dry_run:
            self.context.console.print(
                f"[yellow]DRY-RUN[/yellow] copy packaged compose assets to {target}"
            )
            return

        target.mkdir(parents=True, exist_ok=True)
        source = resources.files("sentinel_cli.assets.compose")
        for item in source.iterdir():
            if item.name == "__init__.py":
                continue

            destination = target / item.name
            if item.is_dir():
                shutil.copytree(item, destination, dirs_exist_ok=True)
                continue
            shutil.copy2(item, destination)

    def _run(self, command: list[str], *, cwd: Path) -> None:
        env = os.environ.copy()
        token = env.get("SENTINEL_OBSERVABILITY_GATEWAY_TOKEN")
        if not token or token == "<set>":
            env["SENTINEL_OBSERVABILITY_GATEWAY_TOKEN"] = "lab-gateway-token"

        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                self.context.console.print(output)
            return

        detail = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)
        raise UserFacingError(
            f"Compose komutu basarisiz oldu: {' '.join(command)}",
            EXIT_TOOL,
            detail=detail or None,
        )
