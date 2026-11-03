# VELE power-grid reproducibility — reviewer quick start

This repository contains **three immutable historical/review snapshots with distinct roles**:

1. [`v2.1.0-review-freeze`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v2.1.0-review-freeze) — **final public software/data/figure snapshot for AUT peer review** (the manuscript itself remains private).
2. [`v2.0.0`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v2.0.0) — original independently validated 536-state PGLib source-rated cut analysis. The identified manuscript may cite this original numerical evidence release.
3. [`v1.0.0-submission`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v1.0.0-submission) — historical six-system MATPOWER/DC full staged reproducibility archive.

The final review snapshot **adds no new scientific results**: only production-quality visual figures, explicit reviewer navigation, release and license/citation clarifications, and additional validation controls. The 2025 published VELE invariant and ordinary maximum-flow/minimum-cut inequality are not claimed as new.

## Reproduce the paper's source-rated electrical certificates

Install Python 3.11 (recommended for the PGLib scripts). Starting in the repository root:

```bash
python -m pip install -r certified_cut_v2/requirements.txt
python certified_cut_v2/fetch_pglib_v23_07_sources.py
python certified_cut_v2/build_source_cut_bounds.py
python certified_cut_v2/replay_cut_certificates_offline.py
python certified_cut_v2/independent_explicit_cut_witnesses.py
```

The source downloader checks **four original PGLib-OPF v23.07 source-file SHA-256 hashes**, then the calculations check **532 physical single-circuit outages plus four intact conditions**. There are two topologies (IEEE57 and IEEE118), not four independent networks. Thirteen connected stressed IEEE118 outages have strictly positive **necessary-curtailment lower bounds**, including zero-VELE circuit 52 (≥60.29 MW), 53 (≥49.29 MW), 55 (≥15.10 MW), and 173 (≥13.49 MW). A zero cut bound does **not** certify security.

The `certified_cut_v2/` module requires NumPy, pandas and NetworkX. The four publication figures also require Matplotlib:

```bash
python -m pip install "matplotlib>=3.9,<4"
python scripts/generate_v2_scientific_figures.py
```

The generator writes editable SVG and PDF figures plus ≥300-DPI PNG equivalents under `docs/assets/v2-figures/`. It asserts the underlying case IDs, surviving physical circuit ratings, key bounds and certificate count. See [the visual atlas](docs/V2_VISUAL_EVIDENCE.md).

## Validate the historic six-IEEE-network MATPOWER/DC study

For the current public source tree, use Python 3.13 and the pinned root `requirements.txt` (or `environment.yml`):

```bash
python -m pip install -r requirements.txt
python scripts/validate_public_artifact.py
python validation/python_dcpf_reference.py --help
python validation/compare_matpower_python.py --help
```

The six MATPOWER case counts, committed MATLAB/Octave-to-NumPy DC cross-check summaries and aggregated physical branch-outage invariants are independently checked by GitHub Actions. The separate [`matpower-octave-validation.yml`](.github/workflows/matpower-octave-validation.yml) performs a full official MATPOWER 8.1 executable intact DC cross-check.

The historical six-system study evaluates 784 physical line outages (and, separately, 558 stylized bus removals); **269/784** physical outages show DC redistribution while leaving eccentricity-derived structural sensitivity unchanged. This is *not* a certified AC shedding claim.

## Reviewer orientation

Read [the method protocol](docs/METHOD_PROTOCOL.md), [the historical evidence map](docs/FROZEN_RESULTS.md), [the final visual evidence atlas](docs/V2_VISUAL_EVIDENCE.md), [the Version 2 source-rated method](certified_cut_v2/README.md) and [third-party licensing](THIRD_PARTY_LICENSES.md).

**Do not use the author-identifying public repository link inside a double-anonymous manuscript** without the journal editor's explicit permission. The repository intentionally contains no unpublished manuscript files, cover letter, author declarations or editor-only supplemental files.

The prior nonlinear AC candidate outputs lack adequate convergence/global-optimality evidence for necessary curtailment labels; do not cite their candidate-defined AUROCs as validated AC-security results.
