"""CLI behavior tests.

Tests that exercise :func:`chassis_optimizer.cli.main.run` at the argument-
parsing and exit-code level without requiring a real YAML file or solver.
"""

from __future__ import annotations

from chassis_optimizer.cli.main import run


def test_run_without_arguments_returns_success() -> None:
    assert run([]) == 0
