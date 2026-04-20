# Chassis Optimizer

Chassis Optimizer is a Python CLI project for early-stage monocoque shell studies using ANSYS MAPDL, focused on torsional rigidity in Nm/rad, relative mass reduction, keep-out volume constraints, and persistent design history.[1][2]

## What this repository is

This repository is the top-level entry point for the project. It explains what the software does, what problem it solves, who it is for, how the repository is organized, and how to start contributing. It is intentionally high-level and should help a new reader understand the project in a few minutes.

## Project intent

The first target is a shell-based monocoque workflow for concept-stage structural exploration, not final detailed certification. The user defines geometry in Python, the application translates that geometry into MAPDL-ready entities, runs a linear static torsional analysis, estimates mass, stores the design in SQLite, and generates plots and reports for later comparison.[1][2]

## First-version capabilities

- CLI-based workflow for local Windows use.
- Shell geometry built from parameterized control points and panels.[1]
- MAPDL-only linear static torsional evaluation.[1]
- Wheel-center-based stiffness extraction in Nm/rad.
- Symmetry and categorized keep-out zones.
- Coarse optimization mesh and fine validation mesh.
- SQLite-backed study and design history.
- Static plots and per-design reports.

## Repository map

```text
.
├─ README.md
├─ AGENTS.md
├─ .github/
│  └─ copilot-instructions.md
├─ docs/
│  ├─ spec.md
│  ├─ architecture.md
│  └─ tasks.md
├─ src/
├─ tests/
└─ examples/
```

## Which file to read next

- Read `AGENTS.md` if an AI coding agent will work in this repository.
- Read `.github/copilot-instructions.md` for repository-wide coding guidance.
- Read `docs/spec.md` for product requirements.
- Read `docs/architecture.md` for module boundaries and design rules.
- Read `docs/tasks.md` for phased implementation steps.

## Contribution philosophy

The project should grow through small, reviewable increments. Large one-shot changes are discouraged because they usually damage modularity, traceability, and reproducibility in engineering software.[3][4]sh and fidelity

- The system must support a coarse mesh for optimization.
- The system must support a finer mesh for validation.
- The first implementation must prioritize fast turnaround over maximum fidelity.

### Data and outputs

- The system must store results in a database.
- The system must store geometry in a form suitable for future export.
- The system must produce static plots and reports for each tested design.
- The system must support torsional stiffness history plots and geometry history plotting.

### User interface

- The first version must be a CLI.
- The design should allow a future GUI or web dashboard without rewriting the core.

## Out of scope for version 1

- GUI implementation.
- Web dashboard implementation.
- Composite laminate optimization.
- Nonlinear analysis.
- Distributed solve execution.
- Detailed CAD reconstruction inside version 1.

## Acceptance criteria

The first usable version is complete when a user can define a study, generate one or more monocoque shell candidates, evaluate them in MAPDL, compute torsional rigidity in Nm/rad, estimate mass, assess symmetry and keep-out constraints, save everything in SQLite, and generate basic plots and reports.[1][2]