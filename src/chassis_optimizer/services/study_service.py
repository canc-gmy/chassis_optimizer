"""Application services for study lifecycle operations.

Services are thin orchestrators.  They accept port interfaces injected at
construction time and co-ordinate calls between the infrastructure and
domain layers without containing business logic themselves.

Public classes
--------------
StudyService
    Manages study configuration loading via an injected
    :class:`~chassis_optimizer.app.ports.StudyConfigLoader` adapter.

Import rules
------------
May import from ``chassis_optimizer.app`` and ``chassis_optimizer.domain``
only.  Must not import from ``chassis_optimizer.infrastructure`` or ``cli``.
"""

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
