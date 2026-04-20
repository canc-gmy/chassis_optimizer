# AGENTS.md

## Project goal
Build a modular Python CLI application for early-stage monocoque chassis shell optimization using MAPDL.

## Non-negotiable rules
- Python package under src/chassis_optimizer
- Windows-only support for now
- MAPDL only, no Mechanical integration
- Geometry parameters are defined in Python, not hardcoded as APDL source-of-truth
- Use shell geometry based on control points and panel patches
- Support symmetry and keep-out zones
- Keep architecture modular so optimizers, constraints, and load cases can be swapped later
- First release focuses on linear static torsional rigidity in Nm/rad
- Use isotropic material assumptions for now
- Coarse mesh for optimization, fine mesh for validation
- SQLite for local run history and geometry database
- Generate static plots and per-design reports
- No GUI in v1, CLI only

## Architecture constraints
- Keep modules isolated: geometry, zones, mapdl, loadcases, optimization, reporting, storage
- Avoid circular imports
- Prefer dataclasses and typed interfaces
- Separate domain models from infrastructure code
- Every feature must include tests where practical
- Do not implement everything in one file
- Keep APDL generation isolated in a dedicated adapter layer

## Delivery strategy
- Implement only one issue at a time
- Keep PRs small
- Update docs when behavior changes
