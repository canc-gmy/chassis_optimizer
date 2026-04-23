"""Application-layer interfaces for external adapters.

Each ``Protocol`` defined here is a port in the ports-and-adapters sense.
Infrastructure modules implement these protocols; the service layer depends
only on these abstractions, never on concrete adapter classes.

Public interfaces
-----------------
StudyConfigLoader
    Port for loading a :class:`~chassis_optimizer.app.config.StudyConfig`
    from an arbitrary source (YAML file, database, network, etc.).
GeometryBuilder
    Port for constructing a
    :class:`~chassis_optimizer.domain.models.ChassisGeometry` from a
    :class:`~chassis_optimizer.app.config.StudyConfig`.

Import rules
------------
May import from ``chassis_optimizer.app.config`` and
``chassis_optimizer.domain`` only.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from chassis_optimizer.app.config import StudyConfig
from chassis_optimizer.domain.models import ChassisGeometry


class StudyConfigLoader(Protocol):
    """Port for loading study configurations from a source."""

    def load(self, config_path: Path) -> StudyConfig:
        """Load and return a typed study configuration."""


class GeometryBuilder(Protocol):
    """Port for building a ChassisGeometry from a StudyConfig."""

    def build_geometry(self, config: StudyConfig) -> ChassisGeometry:
        """Construct and return a validated ChassisGeometry."""
