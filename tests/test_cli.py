"""CLI behavior tests."""

from __future__ import annotations

from chassis_optimizer.cli.main import run


def test_run_without_arguments_returns_success() -> None:
    assert run([]) == 0
