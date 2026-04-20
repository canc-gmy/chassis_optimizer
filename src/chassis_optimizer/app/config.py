"""Typed configuration models used by application services."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class MeshConfig:
    """Mesh controls for study setup."""

    coarse_size: float
    fine_size: float


@dataclass(slots=True)
class KeepOutZoneConfig:
    """A categorized keep-out region."""

    name: str
    category: str


@dataclass(slots=True)
class StudyConfig:
    """Top-level study configuration loaded from YAML."""

    study_name: str
    output_dir: Path
    mesh: MeshConfig
    geometry: dict[str, Any] = field(default_factory=dict)
    keep_out_zones: list[KeepOutZoneConfig] = field(default_factory=list)
