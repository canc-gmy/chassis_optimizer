# Implementation Tasks

## Phase 1 — Project scaffold ✅

- [x] `src/` layout with `chassis_optimizer` package.
- [x] Layer packages: `cli`, `app`, `domain`, `services`, `infrastructure`.
- [x] `pyproject.toml` with editable install and dev dependencies.
- [x] Bootstrap script `scripts/bootstrap_venv.py`.
- [x] Typed `StudyConfig` with `MeshConfig` and `KeepOutZoneConfig`.
- [x] `YamlStudyConfigLoader` reads and validates YAML.
- [x] `StudyService.load_study_config` wires loader to application.
- [x] `validate-config` CLI command with correct exit codes.
- [x] Baseline test suite (`test_cli.py`, `test_config_loader.py`).
- [x] `AGENTS.md` and `.github/copilot-instructions.md`.

## Phase 2 — Geometry domain 🔄

- [x] `docs/spec.md`, `docs/architecture.md`, `docs/tasks.md` rewritten with correct content.
- [x] `docs/workflow.md` created with end-to-end data-flow diagram.
- [x] Module-level docstrings expanded across all Python source files.
- [x] `examples/study_minimal.yaml` annotated with inline comments.
- [x] `ControlPoint` value object in `domain/models.py` (x, y, z; non-finite rejection).
- [x] `SymmetryPlane` enum (`XY`, `YZ`, `XZ`) in `domain/models.py`.
- [x] `Panel` value object (name, control_points, optional thickness) in `domain/models.py`.
- [x] `ChassisGeometry` dataclass in `domain/models.py`.
- [x] `StudyConfig.geometry` changed from `dict` to `ChassisGeometry`.
- [x] `GeometryBuilder` port added to `app/ports.py`.
- [x] `YamlStudyConfigLoader` updated to parse typed geometry with validation.
- [x] `GeometryService.build_geometry` added in `services/geometry_service.py`.
- [x] `examples/study_minimal.yaml` updated with a `panels` section.
- [x] `tests/test_geometry_models.py` — unit tests for domain value objects.
- [x] `tests/test_config_loader.py` — extended with geometry parsing tests.
- [x] `tests/test_geometry_service.py` — smoke test for `GeometryService`.

## Phase 3 — MAPDL integration 📋

- [ ] MAPDL gateway port defined in `app/ports.py`.
- [ ] Shell entity builder translates `ChassisGeometry` to MAPDL keypoints/areas.
- [ ] MAPDL adapter in `infrastructure/` (requires ANSYS installation).
- [ ] Torsional boundary conditions applied at front and rear wheel centres.
- [ ] Torsional rigidity extracted in Nm/rad.
- [ ] Shell mass estimated from panel areas and thicknesses.
- [ ] `analyse` CLI command added.

## Phase 4 — SQLite persistence 📋

- [ ] `DesignResult` entity added to `domain/models.py`.
- [ ] `StudyRepository` port defined in `app/ports.py`.
- [ ] SQLite adapter implements `StudyRepository`.
- [ ] `StudyService` stores each result after analysis.
- [ ] Migration / schema creation on first run.

## Phase 5 — Reports and plots 📋

- [ ] `ReportWriter` port in `app/ports.py`.
- [ ] Static matplotlib plots: torsional stiffness vs design index, geometry overlay.
- [ ] Per-design text report (study name, geometry summary, Nm/rad, mass, constraints).
- [ ] Stiffness history plot across all designs in a study.
- [ ] `report` CLI command added.