# v2.1.0-review-freeze — final public research reproducibility snapshot

**Release date:** 3 November 2026. **Scope:** original reproducible software, data summaries and source-generated figures for the manuscript *Electrical Consequences Invisible to Eccentricity-Based Spectral Screening in Power-Grid Contingencies*, currently unpublished and not accepted.

**This is the final pre-submission code/data/visual evidence freeze. No repository modifications are planned during initial peer review.** Changes, if compelled by a referee or a verified material integrity/security defect, would be explained in a separately versioned release, never an in-place replacement of original assets.

## Immutable scientific provenance

The exact prior [`v2.0.0` release](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v2.0.0) records the original PGLib-OPF v23.07 source-rated calculation: **four electrical conditions on IEEE57/IEEE118 (two topologies), 532 physical single-circuit outages plus four intact conditions (536 states)**. Thirteen connected IEEE118 stressed physical outages carry independently reconstructed **necessary** curtailed-load lower bounds. Four have exactly unchanged unweighted VELE: circuit **52 ≥60.29 MW**, **53 ≥49.29 MW**, **55 ≥15.10 MW** and **173 ≥13.49 MW**. A zero necessary-curtailment lower bound is inconclusive. The existing numerical sources, case source checksums and source-rated calculations are **unchanged** in this review-freeze release.

The separate historical [`v1.0.0-submission` release](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v1.0.0-submission) retains the six-system MATPOWER 8.1/DC experiment including 784 physical-line contingency cases; 269 caused DC flow redistribution while leaving VELE and mean eccentricity unchanged. This is a **DC redistribution proxy**, not itself a proof of AC security violations or mandatory shedding.

## Final pre-review improvements

- Four source-asserting scientific SVG figures: two independent evidence streams, the exact branch-52 physical cut and parallel-circuit interface, the full 13-case necessary-shortage chart, and the four-condition positive-certificate census.
- Portable, independently replayable scientific-figure generator; Matplotlib requirements and exact source-case provenance documented.
- `CITATION.cff` now cites software **rather than suggesting that the unpublished AUT article is already a published reference**.
- Complete public tracked-file manifest, link/integrity/privacy scan, 536-state and 13-witness record checks, source-specified bounds and figure-content assertions.
- Updated `README.md`, `QUICKSTART.md`, `docs/REPRODUCIBILITY.md`, `docs/METHOD_PROTOCOL.md`, `docs/SUBMISSION_FREEZE_STATUS.md` and third-party licence boundary reminders, with clear distinctions between three immutable release roles.

## Reproduction

For source-rated electrical validation (Python 3.11):

```bash
python -m pip install -r certified_cut_v2/requirements.txt
python certified_cut_v2/fetch_pglib_v23_07_sources.py
python certified_cut_v2/build_source_cut_bounds.py
python certified_cut_v2/replay_cut_certificates_offline.py
python certified_cut_v2/independent_explicit_cut_witnesses.py
```

For scientific figures:

```bash
python -m pip install "matplotlib>=3.9,<4"
python scripts/generate_v2_scientific_figures.py
```

For stdlib-only final inventory/documentation and certificate evidence checks (requires Git checkout):

```bash
python scripts/audit_final_reproducibility.py
```

## Scientific and editorial restrictions

The 2025 VELE invariant is previously published; the cut-bound and maximum-flow/minimum-cut inequality are standard. The cut lower bound does not solve AC OPF or certify safety when zero. The old nonconverged AC optimizer's candidate-curtailment AUROCs are not valid necessary-security labels. **This repository is author-identifying**, so the anonymous journal manuscript and editor-only review supplement are not included. Unpublished manuscript, personal author details/forms, cover letters and confidential supplements are excluded from the public release ZIP.

## Release assets, verification, and licensing

The attached archive `VELE_REPRODUCIBILITY_PUBLIC_v2.1.0-review-freeze.zip` is a tracked-source-only checksum-verified copy, with accompanying SHA-256 checksum and complete per-file source inventory. GitHub-generated automatic source archives also represent the exact tag. The final automated source replay and public-tree audit ran before release.

Custom repository code uses MIT. PGLib v23.07 **benchmark data** retain upstream CC BY 4.0, distinct from PGLib software MIT, and original MATPOWER case-data terms remain distinct from MATPOWER software BSD. No benchmark data are relicensed.

**No journal submission is represented by this public release.**
