"""Test configuration for src-layout imports.

This module is loaded automatically by pytest as a conftest.  It adds the
``src/`` directory to ``sys.path`` so that ``chassis_optimizer`` can be
imported without an editable install, and it provides shared fixtures used
across the test suite.

Fixtures
--------
example_study_path : Path
    Absolute path to ``examples/study_minimal.yaml``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture
def example_study_path() -> Path:
    return ROOT / "examples" / "study_minimal.yaml"
