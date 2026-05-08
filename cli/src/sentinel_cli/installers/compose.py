"""Docker Compose installer stub."""

from __future__ import annotations

from sentinel_cli.installers.base import BaseInstaller


class ComposeInstaller(BaseInstaller):
    def preflight(self) -> None:
        self._todo("preflight")

    def install(self) -> None:
        self._todo("install")

    def wire(self) -> None:
        self._todo("wire")

    def verify(self) -> None:
        self._todo("verify")
