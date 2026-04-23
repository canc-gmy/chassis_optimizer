"""Geometry service for chassis shell studies.

This service is the application-layer seam for all geometry construction
logic.  In Phase 2 it simply returns the already-parsed
:class:`~chassis_optimizer.domain.models.ChassisGeometry` from the
:class:`~chassis_optimizer.app.config.StudyConfig`.  Future phases will add
symmetry mirroring, panel inferral, and MAPDL entity mapping here without
changing the public interface.

Public classes
--------------
GeometryService
    Implements :class:`~chassis_optimizer.app.ports.GeometryBuilder`.
    Accepts a :class:`~chassis_optimizer.app.config.StudyConfig` and returns
    a :class:`~chassis_optimizer.domain.models.ChassisGeometry`.

Import rules
------------
May import from ``chassis_optimizer.app`` and ``chassis_optimizer.domain``
only.  Must not import from ``chassis_optimizer.infrastructure`` or ``cli``.
"""

from __future__ import annotations

from chassis_optimizer.app.config import StudyConfig
from chassis_optimizer.domain.models import ChassisGeometry


class GeometryService:
    """Builds and validates the chassis geometry from a study configuration.

    This service acts as the single authoritative entry point for geometry
    construction.  Inject it wherever a
    :class:`~chassis_optimizer.app.ports.GeometryBuilder` port is required.
    """

    def build_geometry(self, config: StudyConfig) -> ChassisGeometry:
        """Return the chassis geometry embedded in *config*.

        Parameters
        ----------
        config:
            A fully parsed and validated
            :class:`~chassis_optimizer.app.config.StudyConfig` whose
            ``geometry`` field already holds a typed
            :class:`~chassis_optimizer.domain.models.ChassisGeometry`.

        Returns
        -------
        ChassisGeometry
            The geometry object from *config*, ready for further processing.
        """
        return config.geometry
