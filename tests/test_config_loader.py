"""Configuration loader tests."""

from __future__ import annotations

from pathlib import Path

from chassis_optimizer.infrastructure.yaml_config_loader import YamlStudyConfigLoader


def test_example_config_loads() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    example_path = repo_root / "examples" / "study_minimal.yaml"

    config = YamlStudyConfigLoader().load(example_path)

    assert config.study_name == "phase1_baseline"
    assert config.mesh.coarse_size > 0
    assert config.mesh.fine_size > 0
