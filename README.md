# VELE Power-Grid Vulnerability Screening — Reproducibility Repository

[![Repository verification](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/repository-validation.yml/badge.svg)](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/repository-validation.yml)
[![MATPOWER 8.1 / Octave validation](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/matpower-octave-validation.yml/badge.svg)](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/actions/workflows/matpower-octave-validation.yml)

**Reproducible VELE power-grid vulnerability screening with MATPOWER/DC-flow validation, islanding, load-shedding proxies, branch N−1 analysis, and corrected reinforcement heuristics.**

Public reproducibility and validation materials supporting the study:

**Vertex Eccentricity Labeled Energy for Power-Grid Vulnerability Screening with DC-Flow Validation**

Authors: **Sunilgar L. Gusai** and **Manoharsinh R. Jadeja**

## Scope

The study evaluates a hybrid structural–electrical vulnerability-screening framework on IEEE/MATPOWER 14, 30, 39, 57, 118 and 300. The frozen analysis includes component-wise VELE, corrected attack-AUC definitions, Direct/VCB/DCP structural line-candidate heuristics, 558 single-bus outage cases, a complete one-at-a-time screen of all **784 active physical branch rows**, progressive attacks, conventional structural comparators, island-aware DC-flow analysis, redispatch and flow-stress sensitivity, finite-benchmark statistics and runtime evidence.

VELE is evaluated as a **training-free, eccentricity-sensitive structural screening diagnostic**. It is **not** presented as a replacement for AC/DC contingency analysis, optimal power flow, dynamic stability, protection studies, cascading-failure simulation or transmission-expansion optimization.

## Benchmark coverage

- IEEE 14, 30, 39, 57, 118 and 300
- MATPOWER **8.1** as the frozen benchmark source
- 558 single-bus outage cases
- 784 physical branch-outage cases
- 1,692 progressive electrical states

## Executable MATPOWER 8.1 validation — PASS

A GitHub Actions workflow independently checks the intact DC implementation in a clean cloud environment. It:

1. starts from a clean Ubuntu runner;
2. installs GNU Octave;
3. downloads the official MATPOWER 8.1 release and verifies SHA-256;
4. executes MATPOWER `rundcpf` on all six intact benchmark systems;
5. independently parses the same MATPOWER case matrices in NumPy without importing MATPOWER or PYPOWER;
6. compares bus voltage angles and branch active-power flows.

Reference workflow run **35531005040** reports maximum absolute differences of **4.050094e-13 degrees** in bus angle and **5.798029e-12 MW** in branch active-power flow. A fresh clean-run repeat after the CI runtime refresh, workflow run **35533409590**, also passes all six cases and reports maxima of **6.039613e-13 degrees** and **6.579626e-12 MW**.

The last digits vary slightly across hosted runner/software-stack executions, as expected for floating-point linear algebra, but both complete runs remain far inside the declared `1e-8` tolerances. The environment-robust statement is therefore that repeated executable checks agree within **1e-12 degrees** for bus angles and **1e-11 MW** for branch active-power flows.

The reference six-case results are committed in `validation/results/MATPOWER_OCTAVE_VALIDATION_REPORT.md` and `validation/results/matpower_octave_crosscheck_summary.csv`. The repeat-run summary and interpretation are recorded in `validation/results/matpower_octave_crosscheck_summary_run_35533409590.csv` and `validation/results/MATPOWER_OCTAVE_REPEATABILITY_NOTE.md`.

This executable check validates the **intact benchmark DC equations and branch-flow implementation**. The study's custom island handling, generator redispatch and load-curtailment proxies remain separately tested components and are not represented as native MATPOWER security-analysis functionality.

## Current public `main` branch

The live `main` branch is deliberately kept as a reviewer-facing **validation and provenance layer** rather than as an unexplained dump of every development artifact. Its principal contents are:

- `.github/workflows/` — Repository verification and MATPOWER/Octave validation CI;
- `validation/` — independent NumPy reference, executable MATPOWER/Octave driver, comparator and committed validation reports;
- `stages/01_matpower_preparation/` — portable MATPOWER preparation code;
- `stages/07_branch_outage_validation/` — branch-outage scope documentation and frozen physical-branch summary tables;
- `docs/` — benchmark provenance and Phase-11 branch-outage documentation;
- `QUICKSTART.md` — commands that are valid for the files actually present on `main`;
- `CITATION.cff`, `LICENSE`, `THIRD_PARTY_LICENSES.md`, `requirements.txt` — citation, licensing and pinned environment metadata.

The frozen **[`v1.0.0-submission`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v1.0.0-submission)** release contains the complete public computational reproducibility archive: staged inputs/outputs, portable reproduction entry points, executable validation evidence, technical documentation and checksums. **The submitted manuscript PDF, LaTeX manuscript source, supplementary manuscript PDF/source, cover letter and journal-submission files are intentionally excluded from the public release while the article is under peer review.**

## Important physical-branch result

The branch-outage extension quantifies a key topology-only limitation. When one circuit of a parallel pair is removed while another remains, the simple structural edge is unchanged. In the frozen analysis, **22 active branch rows belong to parallel pairs; all 22 have zero VELE stress while producing nonzero DC flow redistribution**. More broadly, **269/784** physical branch outages have numerically zero bounded VELE stress. This is one reason the paper treats VELE as complementary structural screening rather than a general critical-transmission-line index.

See `stages/07_branch_outage_validation/README.md` and `docs/PHASE11_BRANCH_OUTAGE_REPORT.md` for scope, results and limitations.

## Reproducibility status

The **Repository verification** workflow checks the pinned Python environment, required reviewer-facing files, script syntax, CLI smoke tests and committed numerical validation evidence. The **MATPOWER 8.1 / Octave validation** workflow independently executes MATPOWER on a clean runner and uploads the raw cross-check artifact.

See `QUICKSTART.md` for the current reproducibility commands and the boundary between the live `main` branch and the frozen public reproducibility release.

## Data provenance

`docs/DATA_SOURCE_MANIFEST.md` records the pinned MATPOWER release, release-archive SHA-256, benchmark systems, electrical fields used, treatment of `RATE_A`, original bus identifiers, and the distinction between simple structural edges and physical electrical branch rows.

No missing thermal ratings are fabricated.

## License and third-party data

Custom analysis code is released under the MIT License. MATPOWER software and benchmark materials retain their original upstream terms; see `THIRD_PARTY_LICENSES.md` and `docs/DATA_SOURCE_MANIFEST.md`. The repository does not relicense MATPOWER case data.

## Citation

Citation metadata are provided in `CITATION.cff`. Cite the frozen computational state from the public [`v1.0.0-submission`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v1.0.0-submission) release.

## Academic profile and related research

This repository is part of the open-research programme of **Dr. Sunilgar L. Gusai**, spanning spectral graph theory, network science and reproducible computational modelling.

- Academic portfolio: https://sunilgargusai.github.io/sunilgar-portfolio/
- GitHub profile: https://github.com/SunilgarGusai
- ORCID: https://orcid.org/0009-0004-0739-4812
- Related reproducibility repository: https://github.com/SunilgarGusai/PAPER-JCMM-reproducibility
