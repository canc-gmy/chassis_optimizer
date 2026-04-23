"""Configuration loader tests.

Tests for :class:`chassis_optimizer.infrastructure.yaml_config_loader.YamlStudyConfigLoader`.
Covers the happy path using the canonical example YAML, as well as error paths
for invalid geometry sections introduced in Phase 2.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from chassis_optimizer.domain.models import SymmetryPlane
from chassis_optimizer.infrastructure.yaml_config_loader import YamlStudyConfigLoader


def test_example_config_loads(example_study_path) -> None:
    config = YamlStudyConfigLoader().load(example_study_path)

    assert config.study_name == "phase1_baseline"
    assert config.mesh.coarse_size == 0.08
    assert config.mesh.fine_size == 0.03


def test_example_config_geometry_symmetry_plane(example_study_path) -> None:
    config = YamlStudyConfigLoader().load(example_study_path)
    assert config.geometry.symmetry_plane is SymmetryPlane.YZ


def test_example_config_geometry_control_points(example_study_path) -> None:
    config = YamlStudyConfigLoader().load(example_study_path)
    pts = config.geometry.control_points
    assert len(pts) == 2
    assert pts[0].x == pytest.approx(0.0)
    assert pts[1].x == pytest.approx(1.2)


def test_example_config_geometry_panels(example_study_path) -> None:
    config = YamlStudyConfigLoader().load(example_study_path)
    assert len(config.geometry.panels) == 1
    panel = config.geometry.panels[0]
    assert panel.name == "floor_centre"
    assert len(panel.control_points) == 2
    assert panel.thickness == pytest.approx(0.003)


def _load_yaml_string(tmp_path: Path, content: str) -> Path:
    """Write *content* to a temp YAML file and return its path."""
    p = tmp_path / "study.yaml"
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


def test_unknown_symmetry_plane_raises_value_error(tmp_path: Path) -> None:
    yaml_text = """
        study_name: test
        output_dir: results
        geometry:
          symmetry_plane: XX
          control_points:
            - [0.0, 0.0, 0.0]
        mesh:
          coarse_size: 0.1
          fine_size: 0.05
    """
    path = _load_yaml_string(tmp_path, yaml_text)
    with pytest.raises(ValueError, match="symmetry_plane"):
        YamlStudyConfigLoader().load(path)


def test_malformed_control_point_wrong_length_raises_value_error(tmp_path: Path) -> None:
    yaml_text = """
        study_name: test
        output_dir: results
        geometry:
          symmetry_plane: yz
          control_points:
            - [0.0, 0.0]
        mesh:
          coarse_size: 0.1
          fine_size: 0.05
    """
    path = _load_yaml_string(tmp_path, yaml_text)
    with pytest.raises(ValueError, match="3-element"):
        YamlStudyConfigLoader().load(path)


def test_malformed_control_point_non_numeric_raises_value_error(tmp_path: Path) -> None:
    yaml_text = """
        study_name: test
        output_dir: results
        geometry:
          symmetry_plane: yz
          control_points:
            - [0.0, "bad", 0.0]
        mesh:
          coarse_size: 0.1
          fine_size: 0.05
    """
    path = _load_yaml_string(tmp_path, yaml_text)
    with pytest.raises(ValueError, match="non-numeric"):
        YamlStudyConfigLoader().load(path)


def test_panel_out_of_range_index_raises_value_error(tmp_path: Path) -> None:
    yaml_text = """
        study_name: test
        output_dir: results
        geometry:
          symmetry_plane: yz
          control_points:
            - [0.0, 0.0, 0.0]
          panels:
            - name: bad_panel
              indices: [0, 99]
        mesh:
          coarse_size: 0.1
          fine_size: 0.05
    """
    path = _load_yaml_string(tmp_path, yaml_text)
    with pytest.raises(ValueError, match="out of range"):
        YamlStudyConfigLoader().load(path)
