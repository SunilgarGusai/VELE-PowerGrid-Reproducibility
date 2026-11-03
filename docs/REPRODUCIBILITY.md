# Versioned scientific reproducibility and review-freeze guide

## Exact releases and what they establish

- **Final review snapshot:** [`v2.1.0-review-freeze`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v2.1.0-review-freeze). This is the reviewer-facing **code/data/visuals documentation** freeze. It contains no unpublished manuscript, coauthor forms or private reviewer package. After its verification, changes will be deferred until review unless a material integrity/security defect is discovered; any correction would be transparently versioned, never a silent replacement of the tag or assets.
- **Certified numerical source snapshot:** [`v2.0.0`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v2.0.0). A separate immutable package with pinned PGLib-OPF v23.07 source hashes, 532 physical outages, four intact conditions, 536 verified necessary-capacity-cut records and 13 connected positively certified IEEE118 stressed events.
- **Historical MATPOWER/DC snapshot:** [`v1.0.0-submission`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v1.0.0-submission). Original staged six-benchmark MATPOWER/DC electrical-proxy results and source verification.

## Source-rated necessary-curtailment replication

From the repository root, with Python 3.11 and the `certified_cut_v2/requirements.txt` environment:

```bash
python certified_cut_v2/fetch_pglib_v23_07_sources.py
python certified_cut_v2/build_source_cut_bounds.py
python certified_cut_v2/replay_cut_certificates_offline.py
python certified_cut_v2/independent_explicit_cut_witnesses.py
```

Do not pool the PGLib IEEE57/118 typical/API source cases with historic MATPOWER 8.1 electrical outputs: the case conditions and measured endpoints differ. The measured positive capacity-cut quantity is a **necessary lower bound**, not an AC-OPF optimum. Its zero value gives **no security assurance**. All thirteen connected positive certificates are independently checked with two network-flow algorithms.

## Final scientific figures

The [visual evidence atlas](V2_VISUAL_EVIDENCE.md) includes four SVG figures with equivalent vector PDF and 340-DPI PNG generation:

```bash
python -m pip install -r certified_cut_v2/requirements.txt
python -m pip install "matplotlib>=3.9,<4"
python certified_cut_v2/fetch_pglib_v23_07_sources.py
python scripts/generate_v2_scientific_figures.py
```

The generator validates case IDs, physical branch-52 cut boundary and parallel circuit ratings, and the archived 13-positive and four-condition outputs before writing graphics. Generated graphics are not a new scientific experiment.

## MATPOWER 8.1/DC reproducibility

The `main` and final review snapshot retain the historical validation utilities and selected outputs. With the pinned root `requirements.txt` environment:

```bash
python scripts/validate_public_artifact.py
python validation/python_dcpf_reference.py --help
python validation/compare_matpower_python.py --help
```

The full public staged workflow is separately preserved in the historical v1 release. The dedicated [MATPOWER validation workflow](../.github/workflows/matpower-octave-validation.yml) fetches checksum-pinned MATPOWER 8.1 and independently compares the intact DC equations against NumPy for IEEE14/30/39/57/118/300. **Historical DC redistribution and island-adequacy proxies do not establish global optimality or unavoidable AC load shedding.**

## CI and release-asset integrity

Repository verification checks the curator manifest, critical paths, Python syntax and MATPOWER/DC numerical invariants. The source-rated and final review workflows separately regenerate or replay original source-rated PGLib cases. GitHub release assets include a public-only ZIP, a checksum file and per-file hash inventory. The final archive is created from tracked files and refuses DOCX, PDF, LaTeX and other manuscript-format files.

Benchmark licensing remains source-specific: original repository software MIT; PGLib source case data CC BY 4.0; original MATPOWER case provenance and upstream license boundaries apply. See [third-party terms](../THIRD_PARTY_LICENSES.md).

## Publication and blind-review boundaries

This repository **does not** claim that the current journal article is published or accepted. It is author-identifying. The journal's anonymous manuscript and private reviewer supplement must be supplied through its authorized editorial workflow, not published in GitHub. Cite an exact release, tag and/or SHA instead of the moving `main` branch. No silent amendments to the review-frozen release are permitted.
