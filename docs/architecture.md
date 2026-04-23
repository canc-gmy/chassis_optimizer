# Architecture

## Layer diagram

```
┌──────────────────────────────────────────────────────────┐
│  cli  (chassis_optimizer.cli)                            │
│  Entry point. Parses arguments. Calls application        │
│  services. Owns no business logic.                       │
└─────────────────────────┬────────────────────────────────┘
                          │ uses
┌─────────────────────────▼────────────────────────────────┐
│  app  (chassis_optimizer.app)                            │
│  Application services, typed config models, and port     │
│  interfaces (Protocols). Depends only on domain.         │
└────────────┬────────────────────────┬────────────────────┘
             │ uses                   │ defines ports
┌────────────▼──────────┐  ┌──────────▼─────────────────────┐
│  domain               │  │  infrastructure                │
│  (chassis_optimizer   │  │  (chassis_optimizer            │
│   .domain)            │  │   .infrastructure)             │
│  Pure value objects,  │  │  Adapters implementing ports:  │
│  enums, and entities. │  │  YAML loader, SQLite repo,     │
│  Zero dependencies.   │  │  MAPDL gateway (future).       │
└───────────────────────┘  └────────────────────────────────┘
             ▲
             │ uses
┌────────────┴──────────────────────────────────────────────┐
│  services (chassis_optimizer.services)                    │
│  Thin orchestrators. Wire app config + domain objects.    │
│  Depend on app layer ports, never on infrastructure.      │
└───────────────────────────────────────────────────────────┘
```

## Dependency rules

- `domain` has zero imports from other project layers.
- `app` imports from `domain` only.
- `services` import from `app` and `domain` only.
- `cli` imports from `services` and `app`.
- `infrastructure` imports from `app` (to implement ports) and `domain`.
- No layer may import from `cli`.
- No layer may import from `infrastructure` except `cli` (for wiring at startup).

Violation of these rules constitutes a hard boundary break and must not be merged.

## Package map

| Package | Key modules | Responsibility |
|---------|-------------|----------------|
| `cli` | `main.py` | Argument parsing, top-level error handling, exit codes |
| `app` | `config.py`, `ports.py` | Typed config dataclasses; Protocol port interfaces |
| `domain` | `models.py` | `ControlPoint`, `Panel`, `ChassisGeometry`, `SymmetryPlane`, `Study` |
| `services` | `study_service.py`, `geometry_service.py` | Thin orchestration: load config, build geometry |
| `infrastructure` | `yaml_config_loader.py` | YAML → typed config; future: SQLite, MAPDL adapters |

## Coordinate convention

| Axis | Direction |
|------|-----------|
| X | Forward (towards front axle) |
| Y | Left (driver's left) |
| Z | Up |

All coordinate values are in SI metres. Angles are in radians unless stated otherwise.

## Geometry model

A `ChassisGeometry` groups:
- `symmetry_plane` — a `SymmetryPlane` enum value (`XY`, `YZ`, `XZ`).
- `control_points` — an ordered list of `ControlPoint` objects (x, y, z in metres).
- `panels` — a list of `Panel` objects. Each panel has a name, a list of
  `ControlPoint` positions, and an optional shell thickness in metres.

Panels reference control points directly (by value, not by index), so the domain layer
remains independent of YAML parsing details.

## Adding a new module

1. Place it in the correct layer package.
2. Add a module-level docstring describing purpose and import rules.
3. Do not import from a layer above your own.
4. Add unit tests under `tests/`.
5. Update `docs/tasks.md` if this satisfies a planned task.