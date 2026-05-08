"""Kubernetes Helm installer."""

from __future__ import annotations

import os
import shutil
import subprocess
from importlib import resources
from pathlib import Path

from sentinel_cli.cli.errors import EXIT_TOOL, UserFacingError
from sentinel_cli.discovery import discover_and_write_config
from sentinel_cli.installers.base import BaseInstaller


class K8sInstaller(BaseInstaller):
    release_name = "sentinel"
    namespace = "sentinel"
    target_dir = Path(".sentinel/charts/sentinel")

    def preflight(self) -> None:
        if self.context.dry_run:
            self.context.console.print("[yellow]DRY-RUN[/yellow] helm version")
            self.context.console.print("[yellow]DRY-RUN[/yellow] kubectl version --client")
            return

        for command in ("helm", "kubectl"):
            if shutil.which(command) is None:
                raise UserFacingError(
                    f"{command} bulunamadi. K8s kurulumu icin {command} gerekli.",
                    EXIT_TOOL,
                )

        self._run(["helm", "version"], cwd=Path.cwd())
        self._run(["kubectl", "version", "--client"], cwd=Path.cwd())

    def install(self) -> None:
        chart_dir = Path.cwd() / self.target_dir
        self._copy_chart(chart_dir)
        gateway_token = os.environ.get("SENTINEL_OBSERVABILITY_GATEWAY_TOKEN", "lab-gateway-token")

        dependency_command = ["helm", "dependency", "update", str(chart_dir)]
        install_command = [
            "helm",
            "upgrade",
            "--install",
            self.release_name,
            str(chart_dir),
            "--create-namespace",
            "-n",
            self.namespace,
            "--wait",
            "--timeout",
            "10m",
            "--set-string",
            f"gateway.token={gateway_token}",
        ]

        if self.context.dry_run:
            self.context.console.print(f"[yellow]DRY-RUN[/yellow] {' '.join(dependency_command)}")
            redacted_install_command = [
                "gateway.token=***" if item.startswith("gateway.token=") else item
                for item in install_command
            ]
            self.context.console.print(
                f"[yellow]DRY-RUN[/yellow] {' '.join(redacted_install_command)}"
            )
            return

        self._run(dependency_command, cwd=Path.cwd())
        self._run(install_command, cwd=Path.cwd())

    def wire(self) -> None:
        if self.context.dry_run:
            self.context.console.print(
                "[yellow]DRY-RUN[/yellow] discover Kubernetes endpoints and write ~/.sentinel/config.yaml"
            )
            return

        endpoints, config_path = discover_and_write_config("k8s")
        self.context.console.print(f"Grafana: {endpoints.grafana_url}")
        self.context.console.print(f"Gateway: {endpoints.gateway_url}")
        self.context.console.print(f"Sentinel config: [bold]{config_path}[/bold]")
        for warning in endpoints.warnings:
            self.context.console.print(f"[yellow]Discovery warning:[/yellow] {warning}")

    def verify(self) -> None:
        command = ["kubectl", "get", "pods", "-n", self.namespace]
        if self.context.dry_run:
            self.context.console.print(f"[yellow]DRY-RUN[/yellow] {' '.join(command)}")
            return

        self._run(command, cwd=Path.cwd())

    def _copy_chart(self, target: Path) -> None:
        if self.context.dry_run:
            self.context.console.print(
                f"[yellow]DRY-RUN[/yellow] copy packaged Helm chart to {target}"
            )
            return

        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            shutil.rmtree(target)

        source = resources.files("sentinel_cli.assets").joinpath("charts", "sentinel")
        shutil.copytree(source, target)

    def _run(self, command: list[str], *, cwd: Path) -> None:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=os.environ.copy(),
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
            f"K8s komutu basarisiz oldu: {' '.join(command)}",
            EXIT_TOOL,
            detail=detail or None,
        )
