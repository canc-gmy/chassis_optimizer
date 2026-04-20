"""YAML-based infrastructure adapter for reading study configurations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from chassis_optimizer.app.config import KeepOutZoneConfig, MeshConfig, StudyConfig


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

    return StudyConfig(
        study_name=study_name,
        output_dir=output_dir,
        mesh=mesh,
        geometry=geometry_raw if isinstance(geometry_raw, dict) else {},
        keep_out_zones=keep_out_zones,
    )
