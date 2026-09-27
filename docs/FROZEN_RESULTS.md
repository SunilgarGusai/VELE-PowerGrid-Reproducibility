# Frozen results guide

This document is a reviewer-facing map to the numerical evidence preserved in the VELE power-grid reproducibility package. It summarizes the frozen submission evidence without replacing the machine-readable CSV files or the release archive.

## Study scale

| Evidence block | Frozen coverage |
|---|---:|
| IEEE/MATPOWER benchmark systems | 6 |
| Benchmark buses | 14, 30, 39, 57, 118, 300 |
| Single-bus outage cases | 558 |
| Active physical branch-outage cases | 784 |
| Progressive electrical states | 1,692 |
| Physical branch outages causing residual disconnection | 114 / 784 |
| Physical branch outages causing secondary surviving-load shedding | 47 / 784 |
| Active branch rows belonging to parallel pairs | 22 |

The six benchmark systems are IEEE14, IEEE30, IEEE39, IEEE57, IEEE118 and IEEE300, using MATPOWER 8.1 as the frozen source representation.

## Selected physical-branch results

The complete branch-outage summaries are under `stages/07_branch_outage_validation/outputs/`.

### VELE versus DC flow redistribution

- IEEE118: Spearman rho = **0.2866**, FDR q = **0.0012**.
- IEEE300: Spearman rho = **0.2553**, FDR q = **0.0012**.

These are modest positive associations, not evidence that VELE predicts branch flows.

### Event discrimination

Eligible VELE ROC-AUC results include:

- IEEE118 residual disconnection: **0.8449**.
- IEEE300 residual disconnection: **0.8775**.
- IEEE300 secondary surviving-load shedding: **0.8383**.
- IEEE39 residual disconnection: **0.3844**.
- IEEE39 `RATE_A` active-power exceedance: **0.5198**.

The unfavorable IEEE39 results are retained deliberately. VELE is presented as a target-dependent structural signal rather than a universally superior criticality metric.

## Parallel-circuit limitation

A simple graph does not retain physical circuit multiplicity. In the frozen physical-branch screen:

- **22** active branch rows belong to parallel pairs;
- removing one circuit leaves the corresponding simple structural edge present;
- all **22** therefore have zero VELE structural stress while producing nonzero DC-flow redistribution;
- more broadly, **269 / 784** physical branch outages produce numerically zero bounded VELE stress.

See `docs/assets/parallel-circuit-blindspot.svg` for a compact visual explanation and `stages/07_branch_outage_validation/README.md` for the interpretation boundary.

## Executable MATPOWER cross-check

The intact DC implementation is independently checked in GitHub Actions against executable MATPOWER 8.1 under GNU Octave.

Across repeated clean CI runs, the six intact benchmark solutions agree within:

- **1e-12 degrees** in bus voltage angle;
- **1e-11 MW** in branch active-power flow.

The detailed reference and repeat summaries are in:

- `validation/results/matpower_octave_crosscheck_summary.csv`
- `validation/results/matpower_octave_crosscheck_summary_run_35533409590.csv`
- `validation/results/MATPOWER_OCTAVE_VALIDATION_REPORT.md`
- `validation/results/MATPOWER_OCTAVE_REPEATABILITY_NOTE.md`

This executable validation covers the intact DC equations and branch-flow implementation. The study's island handling, redispatch and load-curtailment proxies remain custom methodology and are not represented as native MATPOWER security-analysis functionality.

## Result-to-source map

| Evidence | Machine-readable source |
|---|---|
| Branch-outage network totals | `stages/07_branch_outage_validation/outputs/branch_n1_network_summary.csv` |
| Branch VELE/electrical correlations | `stages/07_branch_outage_validation/outputs/branch_n1_vele_correlations.csv` |
| Branch event ROC-AUC | `stages/07_branch_outage_validation/outputs/branch_n1_vele_event_auc.csv` |
| Redispatch sensitivity | `stages/07_branch_outage_validation/outputs/branch_n1_redispatch_sensitivity_summary.csv` |
| Executable MATPOWER reference run | `validation/results/matpower_octave_crosscheck_summary.csv` |
| Executable MATPOWER repeat run | `validation/results/matpower_octave_crosscheck_summary_run_35533409590.csv` |
| Benchmark/data provenance | `docs/DATA_SOURCE_MANIFEST.md` |
| Complete public submission snapshot | GitHub release `v1.0.0-submission` |

## Interpretation boundary

The frozen results support VELE as a **training-free, eccentricity-sensitive structural screening diagnostic** that can complement electrical analysis. They do not support claims that VELE replaces AC/DC contingency analysis, OPF, dynamic stability, protection studies, cascading-failure simulation or transmission-expansion optimization.
