# VELE Power-Grid Vulnerability Screening — Reproducibility Repository

[![Repository verification](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/repository-validation.yml/badge.svg)](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/repository-validation.yml)
[![MATPOWER 8.1 / Octave validation](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/matpower-octave-validation.yml/badge.svg)](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/matpower-octave-validation.yml)

Public reproducibility materials for the manuscript:

**Vertex Eccentricity Labeled Energy for Power-Grid Vulnerability Screening with DC-Flow Validation**

Authors: **Sunilgar L. Gusai** and **Manoharsinh R. Jadeja**

## Scope

This repository supports a hybrid structural–electrical study of IEEE/MATPOWER benchmark power networks (IEEE 14, 30, 39, 57, 118 and 300). It contains the component-wise VELE formulation, corrected attack-AUC definitions, Direct/VCB/DCP structural line-candidate heuristics, single-bus outage screening, a complete one-at-a-time screen of all **784 active physical branch rows**, progressive attacks, structural comparators, island-aware DC-flow validation, redispatch and flow-stress sensitivity analyses, finite-benchmark statistics, runtime evidence, tables, figures and verification utilities.

VELE is evaluated as a **training-free, eccentricity-sensitive structural screening diagnostic**. It is **not** presented as a replacement for AC/DC contingency analysis, optimal power flow, dynamic stability, protection studies, cascading-failure simulation, or transmission-expansion optimization.

## Main benchmark coverage

- IEEE 14
- IEEE 30
- IEEE 39
- IEEE 57
- IEEE 118
- IEEE 300
- MATPOWER 8.1 source cases
- 558 single-bus outage cases
- 784 physical branch-outage cases
- 1,692 progressive electrical states

## Quick verification

```bash
python -m pip install -r requirements.txt
python reproduction/run_all.py --mode verify
```

To regenerate the post-review validation analyses:

```bash
python reproduction/run_all.py --mode reproduce-postreview
```

To regenerate the physical-branch outage extension:

```bash
python reproduction/run_all.py --mode reproduce-branch
```

## Executable MATPOWER validation

A GitHub Actions workflow installs **GNU Octave** in a clean Ubuntu runner, downloads the official **MATPOWER 8.1** release, executes `rundcpf`, exports bus angles and branch active-power flows, and compares them with the repository's independent Python/PYPOWER-aligned DC implementation. This is intended to provide an external, repeatable implementation cross-check rather than a self-consistency test.

See `validation/README.md` and `.github/workflows/matpower-octave-validation.yml`.

## Repository map

- `stages/01_matpower_preparation/` — pinned MATPOWER inputs and parsed electrical data
- `stages/02_structural_vele/` — structural VELE and attack/candidate analyses
- `stages/03_electrical_validation/` — single-bus and progressive DC-flow outputs
- `stages/04_correlation_analysis/` — statistical analyses
- `stages/05_runtime_analysis/` — runtime and complexity evidence
- `stages/06_postreview_validation/` — corrected AUCs, comparator analyses and sensitivities
- `stages/07_branch_outage_validation/` — complete 784-branch outage extension
- `validation/` — executable MATPOWER 8.1 / GNU Octave cross-check
- `manuscript/` — manuscript/supplement sources, tables, figures and builders
- `reproduction/` — portable reproduction entry points
- `verification/` — repository integrity checks
- `docs/` — claim traceability and technical documentation
- `provenance/` — historical development/review artifacts, separated from reviewer-facing execution paths

## Important branch-outage result

The physical-branch extension quantifies a key topology-only limitation: when one circuit of a parallel pair is removed while another remains, the simple structural edge is unchanged. In the frozen analysis, **22 active branch rows belong to parallel pairs; all 22 can have zero VELE stress while still producing non-zero DC flow redistribution**. This is one reason the paper treats VELE as complementary structural screening rather than a general transmission-line criticality index.

## Citation

Citation metadata are provided in `CITATION.cff`. A frozen GitHub release corresponding to the submitted manuscript will be tagged `v1.0.0-submission` after final validation.

## License and third-party data

Custom analysis code is released under the MIT License. MATPOWER case files and other third-party materials retain their original upstream terms; see `THIRD_PARTY_LICENSES.md` and `docs/DATA_SOURCE_MANIFEST.md`.
