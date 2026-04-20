"""Configuration loader tests."""

from __future__ import annotations

from chassis_optimizer.infrastructure.yaml_config_loader import YamlStudyConfigLoader


def test_example_config_loads(example_study_path) -> None:
    config = YamlStudyConfigLoader().load(example_study_path)

    assert config.study_name == "phase1_baseline"
    assert config.mesh.coarse_size == 0.08
    assert config.mesh.fine_size == 0.03
