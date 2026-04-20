"""Domain entities for future structural optimization workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Study:
    """Core study entity placeholder kept independent of infrastructure."""

    name: str
