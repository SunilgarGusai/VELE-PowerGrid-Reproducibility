# v1.0.0-submission — Frozen reproducibility archive

This release freezes the public computational reproducibility materials supporting the study **“Vertex Eccentricity Labeled Energy for Power-Grid Vulnerability Screening with DC-Flow Validation.”**

The archive covers IEEE/MATPOWER 14, 30, 39, 57, 118 and 300 and includes the staged structural VELE analyses, island-aware DC-flow validation, load-curtailment proxy analyses, complete 784-row physical branch N−1 screening, progressive attacks, structural comparators, correlation/ranking analyses, runtime evidence, and executable MATPOWER 8.1/GNU Octave cross-validation.

Across repeated clean executable MATPOWER CI runs, maximum discrepancies between the independent NumPy DC solution and MATPOWER 8.1 remain below **1 × 10^-12 degrees** in bus angle and **1 × 10^-11 MW** in branch active-power flow.

The public reproducibility archive intentionally **does not include the submitted manuscript PDF, LaTeX manuscript source, supplementary manuscript PDF/source, cover letter, or other journal-submission files** while the article is under peer review.

## Release assets

- `VELE_REPRODUCIBILITY_PUBLIC_v1.0.0-submission.zip` — public-safe frozen code/data/output archive
- `MATPOWER_reference_run_35531005040.zip` — reference executable MATPOWER CI artifact
- `MATPOWER_repeat_run_35533409590.zip` — independent repeat executable MATPOWER CI artifact
- `SHA256SUMS_PUBLIC.txt` — SHA-256 checksums for the three binary release assets

## Scope boundary

VELE is provided as an eccentricity-sensitive structural screening diagnostic. It does not replace AC/DC contingency analysis, OPF, protection studies, cascading-failure simulation, voltage-security analysis, or dynamic-stability analysis. The executable MATPOWER check validates the intact DC equations and branch-flow implementation; custom island handling, redispatch and load-curtailment proxies remain separately documented study components.

## Freeze rule

This `v1.0.0-submission` release should remain immutable after publication. Any later scientific or code correction should use a new release version.
