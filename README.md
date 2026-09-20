# VELE Power-Grid Vulnerability Screening — Reproducibility Repository

[![Repository verification](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/repository-validation.yml/badge.svg)](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/repository-validation.yml)
[![MATPOWER 8.1 / Octave validation](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/matpower-octave-validation.yml/badge.svg)](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/matpower-octave-validation.yml)

Public reproducibility materials for the manuscript:

**Vertex Eccentricity Labeled Energy for Power-Grid Vulnerability Screening with DC-Flow Validation**

Authors: **Sunilgar L. Gusai** and **Manoharsinh R. Jadeja**

## Scope

This repository supports a hybrid structural–electrical study of IEEE/MATPOWER benchmark power networks (IEEE 14, 30, 39, 57, 118 and 300). The frozen study contains component-wise VELE, corrected attack-AUC definitions, Direct/VCB/DCP structural line-candidate heuristics, single-bus outage screening, a complete one-at-a-time screen of all **784 active physical branch rows**, progressive attacks, structural comparators, island-aware DC-flow validation, redispatch and flow-stress sensitivity analyses, finite-benchmark statistics, runtime evidence, tables, figures and verification utilities.

VELE is evaluated as a **training-free, eccentricity-sensitive structural screening diagnostic**. It is **not** presented as a replacement for AC/DC contingency analysis, optimal power flow, dynamic stability, protection studies, cascading-failure simulation, or transmission-expansion optimization.

## Main benchmark coverage

- IEEE 14, 30, 39, 57, 118 and 300
- MATPOWER 8.1 benchmark source
- 558 single-bus outage cases
- 784 physical branch-outage cases
- 1,692 progressive electrical states

## Executable MATPOWER 8.1 validation — PASS

The repository now includes a fully automated GitHub Actions cross-check that:

1. starts from a clean Ubuntu runner;
2. installs GNU Octave;
3. downloads the official MATPOWER 8.1 release and verifies its published SHA-256 digest;
4. executes MATPOWER `rundcpf` on all six intact benchmark systems;
5. independently parses the same MATPOWER case matrices in NumPy without importing MATPOWER or PYPOWER;
6. compares bus voltage angles and branch active-power flows.

The successful cloud run reports:

- maximum absolute bus-angle difference: **4.050094e-13 degrees**;
- maximum absolute from-end branch-flow difference: **5.798029e-12 MW**;
- maximum absolute to-end branch-flow difference: **5.798029e-12 MW**.

These are numerical-roundoff differences. See `validation/results/MATPOWER_OCTAVE_VALIDATION_REPORT.md` and the green workflow badge above.

This executable cross-check validates the intact DC equations. The manuscript's custom island handling, redispatch and load-curtailment proxies remain separately tested by the analysis/verification stages and are not represented as native MATPOWER security-analysis functionality.

## Public repository organization

The GitHub tree is being kept deliberately reviewer-facing rather than as a dump of development scratch files. It contains:

- `validation/` — executable MATPOWER 8.1 / GNU Octave cross-check;
- `stages/` — reproducible scientific stages and frozen summary outputs;
- `docs/` — data provenance, Phase-11 branch validation and claim-level documentation;
- `manuscript/` — current public manuscript/reproducibility metadata when frozen;
- `reproduction/` — portable entry points in the frozen submission release;
- `.github/workflows/` — cloud validation and integrity checks.

The exact full submission archive will be attached to the frozen **`v1.0.0-submission`** GitHub release after the final manuscript/repository consistency check.

## Important branch-outage result

The physical-branch extension quantifies a key topology-only limitation: when one circuit of a parallel pair is removed while another remains, the simple structural edge is unchanged. In the frozen analysis, **22 active branch rows belong to parallel pairs; all 22 have zero VELE stress while producing non-zero DC flow redistribution**. More broadly, 269/784 physical branch outages have numerically zero bounded VELE stress. This is one reason the paper treats VELE as complementary structural screening rather than a general transmission-line criticality index.

## Citation

Citation metadata are provided in `CITATION.cff`. The exact manuscript-associated repository state will be frozen as `v1.0.0-submission` after the current import and verification work is complete.

## License and third-party data

Custom analysis code is released under the MIT License. MATPOWER software and benchmark materials retain their original upstream terms; see `THIRD_PARTY_LICENSES.md` and `docs/DATA_SOURCE_MANIFEST.md`. The repository does not relicense MATPOWER case data.
