"""Geometry service tests.

Smoke tests for :class:`chassis_optimizer.services.geometry_service.GeometryService`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from chassis_optimizer.domain.models import ChassisGeometry, SymmetryPlane
from chassis_optimizer.infrastructure.yaml_config_loader import YamlStudyConfigLoader
from chassis_optimizer.services.geometry_service import GeometryService


@pytest.fixture
def example_config(example_study_path: Path):
    return YamlStudyConfigLoader().load(example_study_path)


def test_build_geometry_returns_chassis_geometry(example_config) -> None:
    service = GeometryService()
    geometry = service.build_geometry(example_config)
    assert isinstance(geometry, ChassisGeometry)


def test_build_geometry_control_point_count(example_config) -> None:
    service = GeometryService()
    geometry = service.build_geometry(example_config)
    assert len(geometry.control_points) == 2


def test_build_geometry_symmetry_plane(example_config) -> None:
    service = GeometryService()
    geometry = service.build_geometry(example_config)
    assert geometry.symmetry_plane is SymmetryPlane.YZ


def test_build_geometry_panels(example_config) -> None:
    service = GeometryService()
    geometry = service.build_geometry(example_config)
    assert len(geometry.panels) == 1
    assert geometry.panels[0].name == "floor_centre"
