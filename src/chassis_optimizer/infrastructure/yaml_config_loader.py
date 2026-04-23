"""YAML-based infrastructure adapter for reading study configurations.

This module implements the :class:`~chassis_optimizer.app.ports.StudyConfigLoader`
protocol.  It reads a YAML file from disk and converts the raw mapping into a
fully typed :class:`~chassis_optimizer.app.config.StudyConfig`, including a
:class:`~chassis_optimizer.domain.models.ChassisGeometry` with validated
:class:`~chassis_optimizer.domain.models.ControlPoint` and
:class:`~chassis_optimizer.domain.models.Panel` objects.

Public classes
--------------
YamlStudyConfigLoader
    Stateless loader; call :meth:`~YamlStudyConfigLoader.load` with a
    :class:`pathlib.Path` to obtain a :class:`~chassis_optimizer.app.config.StudyConfig`.

Raises
------
ValueError
    Raised for any structural or semantic validation failure (missing required
    fields, unknown symmetry plane, non-finite coordinate, etc.).
yaml.YAMLError
    Re-raised from the underlying ``pyyaml`` parser for malformed YAML.

Import rules
------------
May import from ``chassis_optimizer.app`` and ``chassis_optimizer.domain``
only.  Must not import from ``chassis_optimizer.services`` or ``cli``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from chassis_optimizer.app.config import KeepOutZoneConfig, MeshConfig, StudyConfig
from chassis_optimizer.domain.models import (
    ChassisGeometry,
    ControlPoint,
    Panel,
    SymmetryPlane,
)


class YamlStudyConfigLoader:
    """Loads study configuration from a YAML file into typed models."""

    def load(self, config_path: Path) -> StudyConfig:
        """Read and parse a YAML study config file."""
        with config_path.open("r", encoding="utf-8") as handle:
            raw_data = yaml.safe_load(handle) or {}

        if not isinstance(raw_data, dict):
            raise ValueError("Configuration root must be a YAML mapping.")

        return _build_study_config(raw_data)


def _build_study_config(raw_data: dict[str, Any]) -> StudyConfig:
    """Convert raw YAML mapping into a StudyConfig instance."""
    mesh_raw = raw_data.get("mesh", {})
    keep_out_raw = raw_data.get("keep_out_zones", [])
    geometry_raw = raw_data.get("geometry", {})

    study_name = str(raw_data.get("study_name", "")).strip()
    if not study_name:
        raise ValueError("Missing required field: study_name")

    if not isinstance(mesh_raw, dict):
        raise ValueError("Field 'mesh' must be a mapping.")
    if "coarse_size" not in mesh_raw or "fine_size" not in mesh_raw:
        raise ValueError("Missing required mesh fields: coarse_size and fine_size")

    mesh = MeshConfig(
        coarse_size=float(mesh_raw.get("coarse_size")),
        fine_size=float(mesh_raw.get("fine_size")),
    )
    if mesh.coarse_size <= 0 or mesh.fine_size <= 0:
        raise ValueError("Mesh sizes must be positive values.")

    keep_out_zones = [
        KeepOutZoneConfig(
            name=str(item.get("name", "")),
            category=str(item.get("category", "")),
        )
        for item in keep_out_raw
        if isinstance(item, dict)
    ]

    output_dir = Path(str(raw_data.get("output_dir", "results")))
    geometry = _build_chassis_geometry(geometry_raw)

    return StudyConfig(
        study_name=study_name,
        output_dir=output_dir,
        mesh=mesh,
        geometry=geometry,
        keep_out_zones=keep_out_zones,
    )


def _build_chassis_geometry(geometry_raw: Any) -> ChassisGeometry:
    """Parse the geometry section of the YAML into a ChassisGeometry."""
    if not isinstance(geometry_raw, dict):
        raise ValueError("Field 'geometry' must be a mapping.")

    symmetry_plane = _parse_symmetry_plane(geometry_raw.get("symmetry_plane"))
    control_points = _parse_control_points(geometry_raw.get("control_points", []))
    panels = _parse_panels(geometry_raw.get("panels", []), control_points)

    return ChassisGeometry(
        symmetry_plane=symmetry_plane,
        control_points=control_points,
        panels=panels,
    )


def _parse_symmetry_plane(raw: Any) -> SymmetryPlane:
    """Parse a symmetry plane value (case-insensitive) into a SymmetryPlane enum."""
    if raw is None:
        raise ValueError("Missing required geometry field: symmetry_plane")
    normalised = str(raw).upper()
    try:
        return SymmetryPlane(normalised)
    except ValueError:
        valid = ", ".join(sp.value for sp in SymmetryPlane)
        raise ValueError(
            f"Unknown symmetry_plane {raw!r}. Valid values are: {valid}."
        )


def _parse_control_points(raw: Any) -> list[ControlPoint]:
    """Parse a YAML list of [x, y, z] entries into ControlPoint objects."""
    if not isinstance(raw, list):
        raise ValueError("Field 'geometry.control_points' must be a list.")
    points: list[ControlPoint] = []
    for index, entry in enumerate(raw):
        if not isinstance(entry, (list, tuple)) or len(entry) != 3:
            raise ValueError(
                f"control_points[{index}] must be a 3-element list [x, y, z], "
                f"got {entry!r}."
            )
        try:
            x, y, z = float(entry[0]), float(entry[1]), float(entry[2])
        except (TypeError, ValueError):
            raise ValueError(
                f"control_points[{index}] contains a non-numeric value: {entry!r}."
            )
        points.append(ControlPoint(x=x, y=y, z=z))
    return points


def _parse_panels(raw: Any, control_points: list[ControlPoint]) -> list[Panel]:
    """Parse an optional YAML list of panel definitions into Panel objects."""
    if not isinstance(raw, list):
        raise ValueError("Field 'geometry.panels' must be a list.")
    panels: list[Panel] = []
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise ValueError(f"panels[{index}] must be a mapping, got {entry!r}.")

        name = str(entry.get("name", "")).strip()
        if not name:
            raise ValueError(f"panels[{index}] is missing a 'name' field.")

        indices_raw = entry.get("indices", [])
        if not isinstance(indices_raw, list):
            raise ValueError(f"panels[{index}].indices must be a list.")
        panel_points: list[ControlPoint] = []
        for pos, idx in enumerate(indices_raw):
            if not isinstance(idx, int) or idx < 0 or idx >= len(control_points):
                raise ValueError(
                    f"panels[{index}].indices[{pos}] value {idx!r} is out of range "
                    f"for {len(control_points)} control point(s)."
                )
            panel_points.append(control_points[idx])

        thickness_raw = entry.get("thickness")
        thickness: float | None = None
        if thickness_raw is not None:
            thickness = float(thickness_raw)

        panels.append(Panel(name=name, control_points=panel_points, thickness=thickness))
    return panels
