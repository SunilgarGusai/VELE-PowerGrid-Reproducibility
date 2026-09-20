# Submission-freeze status

This document tracks the final reproducibility actions required before the journal submission archive is published as `v1.0.0-submission`.

## Completed

- [x] Reviewer-facing repository scope aligned with the actual public `main` branch.
- [x] Repository verification workflow installs pinned dependencies and checks required files, syntax, CLI smoke tests and committed numerical invariants.
- [x] MATPOWER 8.1 / GNU Octave validation workflow passes on all six IEEE/MATPOWER benchmark systems.
- [x] Independent NumPy-vs-MATPOWER intact-case comparison is preserved in machine-readable form.
- [x] Repeat clean-run MATPOWER evidence is recorded and floating-point last-digit variability is documented.
- [x] Repeatability-safe MATPOWER wording reconstructed in the manuscript source from the complete V3.1 source base and the documented V3.2 CI changes.
- [x] Manuscript and supplementary material recompiled successfully after the wording update.
- [x] Abstract, Methods, Results §5.11, Conclusion and Data/Code Availability checked for mutual consistency.
- [x] Abstract rechecked against the package gate and reduced to 236 words without removing headline numerical results.
- [x] Complete manuscript-associated reproducibility archive assembled from the verified 493-file V3.1 technical base plus executable MATPOWER validation evidence.
- [x] Frozen archive expanded to 509 manifested files and passes all seven technical-stage verifiers, literature audit, manuscript checks, CI-evidence checks and portability checks.
- [x] Exact release ZIP fresh-extracted into a clean directory and `python reproduction/run_all.py --mode verify` passed from the extracted copy.
- [x] `SHA256SUMS.txt` generated for all release assets; the hashes are also recorded in `docs/RELEASE_ASSET_SHA256SUMS.txt`.
- [x] Physical-branch N−1 scope, parallel-circuit limitation and branch summary tables publicly documented.
- [x] MATPOWER source provenance, archive SHA-256, field usage and third-party licensing boundaries documented.
- [x] GitHub README contains a concise research description suitable for the repository About description.
- [x] `v1.0.0-submission` release notes prepared.

## Remaining before the release is public

- [ ] Create GitHub Release/tag `v1.0.0-submission` and upload the verified release assets whose hashes are recorded in `docs/RELEASE_ASSET_SHA256SUMS.txt`.
- [ ] After the release exists, change README/CITATION wording from forthcoming/planned release to the actual public release reference.
- [ ] Confirm repository verification remains green on the final post-release documentation commit.
- [ ] Set the GitHub repository About description field to the text below; the connected GitHub integration used for this audit does not expose repository-settings metadata mutation.

## Repository About description

> Reproducible VELE power-grid vulnerability screening with MATPOWER/DC-flow validation, islanding, load-shedding proxies, branch N−1 analysis, and corrected reinforcement heuristics.

## Reproduction-test note

The frozen ZIP itself has passed the complete non-regenerating integrity verification from a clean extraction. A stronger `reproduce-postreview` execution also successfully regenerated the conventional-baseline comparison, independent PYPOWER cross-check and redispatch sensitivity before the execution session timed out during the longer method-update chain. No frozen scientific output was changed by that test. The authoritative release gate remains the complete stage/invariant verifier, which passes.

## Scientific freeze boundary

No new VELE numerical experiments are required merely to complete the repository freeze. Scientific results should be reopened only if release verification exposes a reproducibility defect or manuscript/archive inconsistency.
