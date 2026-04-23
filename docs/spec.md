# Product Specification

## Problem statement

Formula SAE and similar competition vehicle programmes need a monocoque chassis design
that is structurally stiff in torsion, as light as possible, and free from clashes with
mandatory keep-out volumes (driver cell, suspension pick-ups, powertrain envelope).
Today this exploration is done manually: one-at-a-time FEA runs, disconnected
spreadsheets, and no design history. The result is slow iteration and poor traceability.

Chassis Optimizer provides a scriptable, CLI-driven shell for concept-stage monocoque
studies using ANSYS MAPDL, giving a small team the ability to evaluate dozens of
parameterised shell variants in one sitting and to compare results over time.

## Context

- Target vehicle class: FSAE / FS monocoque chassis, aluminium honeycomb or CFRP shell.
- Analysis fidelity: linear static torsional loading only (concept stage, not certification).
- Primary metric: torsional rigidity in Nm/rad measured between front and rear wheel centres.
- Secondary metric: relative shell mass as a proxy for weight.
- Constraint system: categorised keep-out zones (occupant, hardpoint, powertrain).

## First-version capability list

- CLI-based workflow for local Windows use with ANSYS installed.
- Shell geometry built from parameterised control points and named panels.
- MAPDL-only linear static torsional evaluation.
- Wheel-centre-based torsional stiffness extraction in Nm/rad.
- Symmetry plane declaration and categorised keep-out zones.
- Coarse optimisation mesh and fine validation mesh sizes.
- SQLite-backed study and design-history storage.
- Static matplotlib plots and per-design text reports.

## Requirements

### Geometry

- The system must accept control-point coordinates in SI metres (X forward, Y left, Z up).
- The system must accept a symmetry plane declaration (`XY`, `YZ`, or `XZ`).
- The system must accept named shell panels referencing control points by position index.
- The system must validate geometry before submitting to MAPDL.

### Analysis

- The system must run a linear static analysis using ANSYS MAPDL.
- The system must extract torsional rigidity in Nm/rad from wheel-centre displacements.
- The system must estimate shell mass from panel area and assigned thickness.

### Mesh and fidelity

- The system must support a coarse mesh for optimisation runs.
- The system must support a finer mesh for validation runs.
- The first implementation must prioritise fast turnaround over maximum fidelity.

### Data and outputs

- The system must store each study run in an SQLite database.
- The system must store geometry in a form suitable for later export or replay.
- The system must produce static plots and reports for each tested design.
- The system must support torsional stiffness history plots across designs.

### User interface

- The first version must be a CLI accepting a YAML configuration file.
- The architecture must allow a future GUI or web dashboard without rewriting the core.

## Out of scope for version 1

- GUI or web dashboard.
- Composite laminate optimisation (fibre angle, stack-up).
- Nonlinear or dynamic analysis.
- Distributed or cloud-based solve execution.
- Detailed CAD reconstruction or export to STEP/IGES.

## Acceptance criteria

Version 1 is complete when a user can:

1. Author a YAML study file with geometry, mesh, and keep-out zone declarations.
2. Run the CLI to validate and load that file without errors.
3. Invoke the geometry service to obtain a fully typed `ChassisGeometry` object.
4. (Future) Submit the geometry to MAPDL, run a torsional analysis, and receive Nm/rad.
5. (Future) Save the result to SQLite and render a basic plot and report.