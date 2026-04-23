# Workflow

## User workflow

```
1.  Author a study YAML file   (e.g. examples/study_minimal.yaml)
2.  Run the CLI                chassis_optimizer validate-config study.yaml
3.  CLI validates and prints   "Loaded study: <name>"
4.  (Future) Run analysis      chassis_optimizer analyse study.yaml
5.  (Future) Run report        chassis_optimizer report study.yaml
```

## End-to-end data flow

```
  ┌──────────┐   path    ┌────────────────────┐  raw dict  ┌─────────────────┐
  │  User /  │ ────────► │ YamlStudyConfig-   │ ─────────► │  _build_study_  │
  │  CLI     │           │ Loader.load()       │            │  config()       │
  └──────────┘           └────────────────────┘            └────────┬────────┘
                                                                     │ StudyConfig
                                                                     ▼
                                                          ┌──────────────────────┐
                                                          │ StudyService         │
                                                          │ .load_study_config() │
                                                          └──────────┬───────────┘
                                                                     │ StudyConfig
                                                                     ▼
                                                          ┌──────────────────────┐
                                                          │ GeometryService      │
                                                          │ .build_geometry()    │
                                                          └──────────┬───────────┘
                                                                     │ ChassisGeometry
                                                                     ▼
                                                          ┌──────────────────────┐
                                                          │ (Future)             │
                                                          │ MapdlGateway         │
                                                          │ .run_torsion()       │
                                                          └──────────┬───────────┘
                                                                     │ DesignResult
                                                                     ▼
                                                          ┌──────────────────────┐
                                                          │ (Future)             │
                                                          │ StudyRepository      │
                                                          │ .save()              │
                                                          └──────────┬───────────┘
                                                                     │
                                                                     ▼
                                                          ┌──────────────────────┐
                                                          │ (Future)             │
                                                          │ ReportWriter         │
                                                          │ .write()             │
                                                          └──────────────────────┘
```

## YAML → typed models mapping

```
study_minimal.yaml                  Python type
──────────────────────────────────  ─────────────────────────────────────
study_name: phase1_baseline         StudyConfig.study_name: str
output_dir: results/…               StudyConfig.output_dir: Path
geometry:
  symmetry_plane: yz                ChassisGeometry.symmetry_plane: SymmetryPlane
  control_points:
    - [0.0, 0.0, 0.0]               ChassisGeometry.control_points: list[ControlPoint]
  panels:
    - name: floor                   Panel.name: str
      indices: [0, 1]               Panel.control_points: list[ControlPoint]
      thickness: 0.003              Panel.thickness: float | None
mesh:
  coarse_size: 0.08                 MeshConfig.coarse_size: float
  fine_size:   0.03                 MeshConfig.fine_size:   float
keep_out_zones:
  - name: driver_cell               KeepOutZoneConfig.name: str
    category: occupant              KeepOutZoneConfig.category: str
```

## How to add a new CLI command

1. Add a `subparsers.add_parser(...)` block in `cli/main.py:build_parser`.
2. Add an `elif args.command == "…":` branch in `cli/main.py:run`.
3. Instantiate only services and infrastructure adapters inside that branch.
4. Return `0` on success, `1` on expected errors.
5. Add a test in `tests/test_cli.py`.

## How to add a new geometry section

1. Add the new value-object or field to `domain/models.py`.
2. Extend `ChassisGeometry` (or create a new dataclass) in `domain/models.py`.
3. Update `StudyConfig` in `app/config.py` if the new field belongs to config.
4. Add a parsing helper in `infrastructure/yaml_config_loader.py` following
   the existing guard pattern (check type, raise `ValueError` with a clear message).
5. Update `examples/study_minimal.yaml` with an annotated example entry.
6. Add or extend tests in `tests/test_geometry_models.py` and
   `tests/test_config_loader.py`.

## How to add a new infrastructure adapter

1. Define a `Protocol` port in `app/ports.py`.
2. Create a new module in `infrastructure/` that implements the protocol.
3. Wire the adapter in `cli/main.py` (or a factory function) at startup.
4. Never import the adapter directly from `services/` or `domain/`.
5. Add tests in `tests/` using a fake or in-memory implementation if the
   real adapter requires external software (MAPDL, a database file, etc.).
