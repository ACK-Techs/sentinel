"""Installer base contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from rich.console import Console


@dataclass(slots=True)
class InstallContext:
    mode: str
    dry_run: bool
    skip_preflight: bool
    console: Console


class BaseInstaller(ABC):
    """Base contract for Sentinel installation backends."""

    def __init__(self, context: InstallContext) -> None:
        self.context = context

    @abstractmethod
    def preflight(self) -> None:
        """Check local prerequisites before installation."""

    @abstractmethod
    def install(self) -> None:
        """Install mode-specific components."""

    @abstractmethod
    def wire(self) -> None:
        """Connect installed components to Sentinel runtime config."""

    @abstractmethod
    def verify(self) -> None:
        """Verify the installed target is reachable and usable."""

    def _todo(self, step: str) -> None:
        prefix = "DRY-RUN TODO" if self.context.dry_run else "TODO"
        self.context.console.print(f"[yellow]{prefix}[/yellow] {self.context.mode}:{step}")
