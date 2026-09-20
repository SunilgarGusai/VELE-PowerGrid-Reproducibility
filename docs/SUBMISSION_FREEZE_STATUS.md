# Submission-freeze status

The public computational reproducibility archive is now frozen as GitHub release `v1.0.0-submission`.

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
- [x] Public release/tag `v1.0.0-submission` published from the frozen public-safe repository state.
- [x] The release contains only the public reproducibility ZIP, the two executable MATPOWER CI artifacts and `SHA256SUMS_PUBLIC.txt`, in addition to GitHub's automatic source snapshots of the tagged public repository.
- [x] Release asset names and SHA-256 digests verified against the prepared public package.
- [x] README/QUICKSTART maintain the boundary between public reproducibility materials and private journal-submission files.
- [x] CITATION metadata updated to the actual `v1.0.0-submission` release.

## Repository About description

> Reproducible VELE power-grid vulnerability screening with MATPOWER/DC-flow validation, islanding, load-shedding proxies, branch N−1 analysis, and corrected reinforcement heuristics.

## Private submission boundary

The final manuscript PDF/source, supplementary manuscript PDF/source, cover letter and other journal-submission files are retained privately for journal submission. They are not part of the public GitHub release during peer review.

## Scientific freeze boundary

No new VELE numerical experiments are required for the submission package. Scientific results should be reopened only if a reproducibility defect or technical inconsistency is discovered. Any post-submission scientific or code correction should use a new release version rather than silently replacing `v1.0.0-submission`.
