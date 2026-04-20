"""Command-line interface for chassis_optimizer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import yaml

from chassis_optimizer.infrastructure.yaml_config_loader import YamlStudyConfigLoader
from chassis_optimizer.services.study_service import StudyService


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="chassis_optimizer",
        description="Chassis Optimizer CLI (phase 1 scaffold).",
    )

    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser(
        "validate-config",
        help="Load and validate a study YAML configuration file.",
    )
    validate_parser.add_argument("config", type=Path, help="Path to study YAML file")

    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate-config":
        service = StudyService(loader=YamlStudyConfigLoader())
        try:
            study = service.load_study_config(args.config)
        except (FileNotFoundError, IsADirectoryError):
            print(f"Config path not found or invalid: {args.config}", file=sys.stderr)
            return 1
        except (yaml.YAMLError, ValueError) as exc:
            print(f"Failed to load config: {exc}", file=sys.stderr)
            return 1
        print(f"Loaded study: {study.study_name}")
        return 0

    parser.print_help()
    return 0
