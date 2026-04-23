"""Domain geometry model tests.

Tests for :class:`chassis_optimizer.domain.models.ControlPoint`,
:class:`chassis_optimizer.domain.models.SymmetryPlane`,
:class:`chassis_optimizer.domain.models.Panel`, and
:class:`chassis_optimizer.domain.models.ChassisGeometry`.
"""

from __future__ import annotations

import math

import pytest

from chassis_optimizer.domain.models import (
    ChassisGeometry,
    ControlPoint,
    Panel,
    SymmetryPlane,
)


class TestControlPoint:
    def test_valid_coordinates_are_accepted(self) -> None:
        pt = ControlPoint(x=1.0, y=2.0, z=3.0)
        assert pt.x == 1.0
        assert pt.y == 2.0
        assert pt.z == 3.0

    def test_zero_coordinates_are_accepted(self) -> None:
        pt = ControlPoint(x=0.0, y=0.0, z=0.0)
        assert pt.x == 0.0

    def test_negative_coordinates_are_accepted(self) -> None:
        ControlPoint(x=-1.5, y=-0.3, z=-0.1)

    @pytest.mark.parametrize("field,value", [
        ("x", float("nan")),
        ("y", float("inf")),
        ("z", float("-inf")),
    ])
    def test_non_finite_coordinate_raises_value_error(self, field: str, value: float) -> None:
        kwargs = {"x": 0.0, "y": 0.0, "z": 0.0}
        kwargs[field] = value
        with pytest.raises(ValueError, match=field):
            ControlPoint(**kwargs)


class TestSymmetryPlane:
    def test_all_three_planes_exist(self) -> None:
        assert SymmetryPlane.XY
        assert SymmetryPlane.YZ
        assert SymmetryPlane.XZ

    def test_values_are_upper_case_strings(self) -> None:
        assert SymmetryPlane.XY.value == "XY"
        assert SymmetryPlane.YZ.value == "YZ"
        assert SymmetryPlane.XZ.value == "XZ"

    def test_construction_from_string(self) -> None:
        assert SymmetryPlane("YZ") is SymmetryPlane.YZ

    def test_unknown_value_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            SymmetryPlane("XX")


class TestPanel:
    def test_panel_with_no_points(self) -> None:
        panel = Panel(name="empty")
        assert panel.name == "empty"
        assert panel.control_points == []
        assert panel.thickness is None

    def test_panel_with_points_and_thickness(self) -> None:
        pts = [ControlPoint(0.0, 0.0, 0.0), ControlPoint(1.0, 0.0, 0.0)]
        panel = Panel(name="floor", control_points=pts, thickness=0.003)
        assert len(panel.control_points) == 2
        assert panel.thickness == pytest.approx(0.003)


class TestChassisGeometry:
    def test_minimal_construction(self) -> None:
        pts = [ControlPoint(0.0, 0.0, 0.0), ControlPoint(1.2, 0.0, 0.0)]
        geo = ChassisGeometry(symmetry_plane=SymmetryPlane.YZ, control_points=pts)
        assert geo.symmetry_plane is SymmetryPlane.YZ
        assert len(geo.control_points) == 2
        assert geo.panels == []

    def test_geometry_with_panels(self) -> None:
        pts = [ControlPoint(0.0, 0.0, 0.0), ControlPoint(1.2, 0.0, 0.0)]
        panel = Panel(name="floor_centre", control_points=pts, thickness=0.003)
        geo = ChassisGeometry(
            symmetry_plane=SymmetryPlane.YZ,
            control_points=pts,
            panels=[panel],
        )
        assert len(geo.panels) == 1
        assert geo.panels[0].name == "floor_centre"
