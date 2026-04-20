"""Application-layer interfaces for external adapters."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from chassis_optimizer.app.config import StudyConfig


class StudyConfigLoader(Protocol):
    """Port for loading study configurations from a source."""

    def load(self, config_path: Path) -> StudyConfig:
        """Load and return a typed study configuration."""
