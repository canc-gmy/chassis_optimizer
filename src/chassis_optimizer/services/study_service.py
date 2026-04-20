"""Application services for study lifecycle operations."""

from __future__ import annotations

from pathlib import Path

from chassis_optimizer.app.config import StudyConfig
from chassis_optimizer.app.ports import StudyConfigLoader


class StudyService:
    """Coordinates study-related application actions."""

    def __init__(self, loader: StudyConfigLoader) -> None:
        self._loader = loader

    def load_study_config(self, path: Path) -> StudyConfig:
        """Load a study configuration from the configured adapter."""
        return self._loader.load(path)
