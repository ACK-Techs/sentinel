"""User-facing CLI errors and exit codes."""

from __future__ import annotations

from dataclasses import dataclass


EXIT_OK = 0
EXIT_GENERAL = 1
EXIT_USAGE = 2
EXIT_LLM = 3
EXIT_TOOL = 4
EXIT_INTERRUPTED = 130


@dataclass(slots=True)
class UserFacingError(Exception):
    """Short Turkish error shown to the user."""

    message: str
    exit_code: int = EXIT_GENERAL
    detail: str | None = None

    def __str__(self) -> str:
        return self.message
