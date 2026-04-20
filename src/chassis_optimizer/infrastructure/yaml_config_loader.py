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

        return _build_study_config(raw_data)


def _build_study_config(raw_data: dict[str, Any]) -> StudyConfig:
    """Convert raw YAML mapping into a StudyConfig instance."""
    mesh_raw = raw_data.get("mesh", {})
    keep_out_raw = raw_data.get("keep_out_zones", [])
    geometry_raw = raw_data.get("geometry", {})

    mesh = MeshConfig(
        coarse_size=float(mesh_raw.get("coarse_size", 0.0)),
        fine_size=float(mesh_raw.get("fine_size", 0.0)),
    )

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
        study_name=str(raw_data.get("study_name", "unnamed-study")),
        output_dir=output_dir,
        mesh=mesh,
        geometry=geometry_raw if isinstance(geometry_raw, dict) else {},
        keep_out_zones=keep_out_zones,
    )
