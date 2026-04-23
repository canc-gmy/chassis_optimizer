"""Typed configuration models used by application services.

These dataclasses are the contract between the infrastructure layer (which
reads YAML) and the service layer (which uses the parsed values).  They must
remain free of I/O and infrastructure imports.

Public classes
--------------
MeshConfig
    Mesh size controls (coarse and fine element sizes in metres).
KeepOutZoneConfig
    A named, categorised keep-out region.
StudyConfig
    Top-level study configuration assembled from a YAML file.

Import rules
------------
May import from ``chassis_optimizer.domain`` only.  No infrastructure or
service imports are permitted here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from chassis_optimizer.domain.models import ChassisGeometry


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
    geometry: ChassisGeometry
    keep_out_zones: list[KeepOutZoneConfig] = field(default_factory=list)
