# Submission-freeze status

This document tracks the final actions required before the public computational reproducibility archive is published as `v1.0.0-submission`.

## Completed

- [x] Reviewer-facing repository scope aligned with the actual public `main` branch.
- [x] Repository verification workflow installs pinned dependencies and checks required files, syntax, CLI smoke tests and committed numerical invariants.
- [x] MATPOWER 8.1 / GNU Octave validation workflow passes on all six IEEE/MATPOWER benchmark systems.
- [x] Independent NumPy-vs-MATPOWER intact-case comparison is preserved in machine-readable form.
- [x] Repeat clean-run MATPOWER evidence is recorded and floating-point last-digit variability is documented.
- [x] Physical-branch N−1 scope, parallel-circuit limitation and branch summary tables are publicly documented.
- [x] MATPOWER source provenance, archive SHA-256, field usage and third-party licensing boundaries are documented.
- [x] Public-safe reproducibility archive assembled with all seven technical stages and executable MATPOWER evidence.
- [x] Exact public archive fresh-extracted and `python reproduction/run_all.py --mode verify` passed.
- [x] Explicit privacy check confirms that `MAIN.pdf`, `MAIN.tex`, supplementary manuscript PDF/source, legacy manuscript source, cover letter and journal-submission files are not included.
- [x] Public release SHA-256 hashes recorded in `docs/RELEASE_ASSET_SHA256SUMS.txt`.
- [x] Public release notes revised so no manuscript PDF/source is listed as a release asset.
- [x] README and QUICKSTART revised to distinguish the public reproducibility archive from the private journal-submission package.

## Remaining before the release is public

- [ ] Create/publish GitHub Release/tag `v1.0.0-submission` from the current `main` branch.
- [ ] Upload only the four public release assets documented in the release notes: the public reproducibility ZIP, two MATPOWER CI artifacts and `SHA256SUMS_PUBLIC.txt`.
- [ ] Set the GitHub repository About description field to the text below.
- [ ] After publication, verify the release page, uploaded asset names/hashes and final repository CI state.

## Repository About description

> Reproducible VELE power-grid vulnerability screening with MATPOWER/DC-flow validation, islanding, load-shedding proxies, branch N−1 analysis, and corrected reinforcement heuristics.

## Private submission boundary

The reconstructed manuscript PDF/source and supplementary manuscript files are retained privately for journal submission. They are not part of the public GitHub release during peer review.

## Scientific freeze boundary

No new VELE numerical experiments are required merely to complete the repository freeze. Scientific results should be reopened only if release verification exposes a reproducibility defect or technical inconsistency.
