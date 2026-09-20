# Submission-freeze status

This document tracks the final reproducibility actions required before the journal submission archive is frozen as `v1.0.0-submission`.

## Completed

- [x] Reviewer-facing repository scope aligned with the actual public `main` branch.
- [x] Repository verification workflow installs pinned dependencies and checks required files, syntax, CLI smoke tests and committed numerical invariants.
- [x] MATPOWER 8.1 / GNU Octave validation workflow passes on all six IEEE/MATPOWER benchmark systems.
- [x] Independent NumPy-vs-MATPOWER intact-case comparison is preserved in machine-readable form.
- [x] Repeat clean-run MATPOWER evidence is recorded and floating-point last-digit variability is documented.
- [x] Robust manuscript wording for executable MATPOWER validation is recorded in `docs/MANUSCRIPT_CI_WORDING_PATCH.md`.
- [x] Physical-branch N−1 scope, parallel-circuit limitation and branch summary tables are publicly documented.
- [x] MATPOWER source provenance, archive SHA-256, field usage and third-party licensing boundaries are documented.
- [x] GitHub README contains a concise research description suitable for the repository About description.
- [x] Draft `v1.0.0-submission` release notes are prepared in `docs/RELEASE_NOTES_v1.0.0-submission.md`.

## Required before creating the final release

- [ ] Apply the repeatability-safe MATPOWER wording to the actual V3.2 manuscript source.
- [ ] Recompile the manuscript and supplementary material after that wording-only patch.
- [ ] Verify that Abstract, Methods, Results §5.11, Conclusion, and Data and Code Availability are mutually consistent.
- [ ] Assemble the complete manuscript-associated reproducibility archive, including all staged inputs/outputs, reproduction entry points, manuscript builders and claim-traceability material.
- [ ] Fresh-extract the exact archive intended for release and run its verification procedure from a clean directory.
- [ ] Generate `SHA256SUMS.txt` for all release assets.
- [ ] Create GitHub Release `v1.0.0-submission` from the final frozen commit and upload the verified assets.
- [ ] Update README and `CITATION.cff` from “forthcoming release” language to the actual release reference/version.
- [ ] Confirm both CI workflows remain green on the final frozen repository commit.

## Repository About description

Use the following GitHub repository description:

> Reproducible VELE power-grid vulnerability screening with MATPOWER/DC-flow validation, islanding, load-shedding proxies, branch N−1 analysis, and corrected reinforcement heuristics.

## Scientific freeze boundary

No new VELE numerical experiments are required merely to complete the repository freeze. Scientific results should be reopened only if the final archive verification exposes a reproducibility defect or manuscript/archive inconsistency.
