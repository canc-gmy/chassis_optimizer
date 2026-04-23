"""Domain entities for chassis geometry and structural optimization workflows.

This module defines the pure value objects and enums that represent monocoque
shell geometry concepts.  It has no dependencies on any other project layer.

Public classes
--------------
ControlPoint
    A three-dimensional point in SI metres (X forward, Y left, Z up).
    Construction raises ``ValueError`` for any non-finite coordinate.
SymmetryPlane
    Enumeration of the three axis-aligned symmetry planes: ``XY``, ``YZ``,
    ``XZ``.
Panel
    A named shell panel with an ordered list of ``ControlPoint`` corner
    positions and an optional thickness in metres.
ChassisGeometry
    Top-level geometry container holding a symmetry plane, a list of
    control points, and a list of panels.
Study
    Core study entity placeholder kept independent of infrastructure.

Import rules
------------
Must have zero imports from any other project layer.  Standard-library
imports are permitted.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum


class SymmetryPlane(str, Enum):
    """Axis-aligned symmetry plane for the monocoque shell.

    Values are upper-case to match YAML convention (``yz`` is normalised to
    ``YZ`` by the loader before construction).
    """

    XY = "XY"
    YZ = "YZ"
    XZ = "XZ"


@dataclass(slots=True)
class ControlPoint:
    """A three-dimensional point in SI metres.

    Coordinates follow the project convention: X forward, Y left, Z up.

    Raises
    ------
    ValueError
        If any coordinate is non-finite (NaN, +inf, or -inf).
    """

    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        for name, value in (("x", self.x), ("y", self.y), ("z", self.z)):
            if not math.isfinite(value):
                raise ValueError(
                    f"ControlPoint coordinate '{name}' must be finite, got {value!r}."
                )


@dataclass(slots=True)
class Panel:
    """A named shell panel defined by an ordered list of corner control points.

    Parameters
    ----------
    name:
        Human-readable identifier for the panel (e.g. ``"floor"``).
    control_points:
        Ordered list of corner :class:`ControlPoint` objects.
    thickness:
        Optional shell thickness in metres.  ``None`` means unassigned.
    """

    name: str
    control_points: list[ControlPoint] = field(default_factory=list)
    thickness: float | None = None


@dataclass(slots=True)
class ChassisGeometry:
    """Top-level geometry container for a monocoque chassis shell study.

    Parameters
    ----------
    symmetry_plane:
        The axis-aligned plane about which the geometry is symmetric.
    control_points:
        Ordered list of all control points that define the shell envelope.
    panels:
        List of named shell panels, each referencing a subset of control
        points.
    """

    symmetry_plane: SymmetryPlane
    control_points: list[ControlPoint] = field(default_factory=list)
    panels: list[Panel] = field(default_factory=list)


@dataclass(slots=True)
class Study:
    """Core study entity placeholder kept independent of infrastructure."""

    name: str
