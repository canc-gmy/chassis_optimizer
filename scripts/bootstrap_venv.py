#!/usr/bin/env python3
"""Create a local virtual environment and install project dependencies."""

from __future__ import annotations

import os
import subprocess
import sys
import venv
from pathlib import Path


def _venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    venv_dir = repo_root / ".venv"

    if not venv_dir.exists():
        print(f"Creating virtual environment at: {venv_dir}")
        venv.EnvBuilder(with_pip=True).create(venv_dir)
    else:
        print(f"Using existing virtual environment at: {venv_dir}")

    venv_python = _venv_python(venv_dir)
    if not venv_python.exists():
        print(f"Could not find virtual environment python: {venv_python}", file=sys.stderr)
        return 1

    print("Upgrading pip in virtual environment...")
    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
        cwd=repo_root,
        check=True,
    )
    print("Installing project in editable mode with dev dependencies...")
    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "-e", ".[dev]"],
        cwd=repo_root,
        check=True,
    )

    print("\nEnvironment ready.")
    if os.name == "nt":
        print(r"Activate with: .\.venv\Scripts\activate")
    else:
        print("Activate with: source .venv/bin/activate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
