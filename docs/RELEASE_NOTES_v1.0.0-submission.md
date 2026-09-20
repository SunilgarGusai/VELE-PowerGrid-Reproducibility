# v1.0.0-submission — planned frozen journal-submission release

## Purpose

This release is intended to identify the exact reproducibility state associated with the journal submission of:

**Vertex Eccentricity Labeled Energy for Power-Grid Vulnerability Screening with DC-Flow Validation**

by Sunilgar L. Gusai and Manoharsinh R. Jadeja.

## Scientific scope frozen by this release

The submitted study treats VELE as a deterministic, training-free, eccentricity-sensitive structural screening diagnostic that complements, rather than replaces, electrical contingency and security analysis.

The frozen benchmark scope comprises IEEE/MATPOWER 14, 30, 39, 57, 118 and 300 and includes:

- component-wise and bounded VELE stress definitions;
- Direct VELE, VCB-VELE and distance/cost-penalized VELE line-candidate rules;
- 558 single-bus outage cases;
- 784 one-at-a-time active physical branch-row outages;
- 1,692 progressive electrical states;
- island-aware DC-flow validation and load-curtailment proxy analysis;
- flow-stress and RATE_A-based active-power exceedance diagnostics where positive ratings exist;
- conventional structural comparator analyses;
- finite-benchmark correlations, event discrimination and runtime evidence;
- physical parallel-circuit diagnostics and branch N−1 screening;
- executable MATPOWER 8.1/GNU Octave intact-case cross-validation.

## Executable MATPOWER validation

The public GitHub Actions workflow downloads and checksum-verifies the official MATPOWER 8.1 release, executes `rundcpf` under GNU Octave on all six intact benchmark cases, independently solves the same DC equations in NumPy, and compares bus angles and branch active-power flows.

Two clean-run validations pass the declared `1e-8` tolerances. Across repeated clean CI runs, maximum discrepancies remain below:

- **1 × 10^-12 degrees** in bus voltage angle; and
- **1 × 10^-11 MW** in branch active-power flow.

Run-specific diagnostics remain preserved in `validation/results/`.

This executable check validates the intact DC equations and branch-flow implementation. It does not convert the manuscript's custom island handling, redispatch or load-curtailment proxy into native MATPOWER security analysis, and it does not constitute AC, OPF, protection, cascade or dynamic-stability validation.

## Important topology-only limitation retained in the release

The electrical layer retains physical branch multiplicity while the structural VELE graph is simple and undirected. In the frozen branch screen, 22 active branch rows belong to parallel pairs. Every one of those 22 single-circuit trips leaves the simple structural edge intact and therefore has zero VELE stress despite nonzero DC-flow redistribution. Overall, 269 of 784 physical branch outages have numerically zero bounded VELE stress.

## Planned release assets

The final `v1.0.0-submission` release should contain, at minimum:

1. `VELE_REPRODUCIBILITY_v1.0.0-submission.zip` — complete staged reproducibility archive corresponding to the submitted paper;
2. `VELE_MANUSCRIPT_SOURCE_v1.0.0-submission.zip` — exact manuscript source used for the submitted PDF;
3. `SHA256SUMS.txt` — SHA-256 checksums for every attached release asset;
4. `MAIN.pdf` — submitted manuscript PDF, when journal policy permits repository posting;
5. `SUPPLEMENTARY_MATERIAL.pdf` — submitted supplementary PDF;
6. optional raw GitHub Actions cross-check artifacts from the frozen validation run.

## Freeze rule

After the journal submission is made, this release must remain immutable. Any post-submission scientific or code change should use a new release version rather than silently replacing `v1.0.0-submission` assets.
