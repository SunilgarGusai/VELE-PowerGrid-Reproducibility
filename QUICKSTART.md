# Quick start

This `main` branch is the live reviewer-facing verification layer for the VELE power-grid study. It contains the executable MATPOWER/Octave cross-check, pinned environment information, benchmark provenance, selected portable stage code, and frozen branch-outage summary outputs. The complete public reproducibility snapshot is frozen separately as the `v1.0.0-submission` release.

## 1. Python environment

```bash
python -m venv .venv
```

Activate the environment, then install the pinned dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Local smoke checks

The public validation utilities should import and expose their command-line interfaces:

```bash
python validation/python_dcpf_reference.py --help
python validation/compare_matpower_python.py --help
```

The repository's **Repository verification** GitHub Actions workflow performs these checks automatically on every push to `main` and on pull requests.

## 3. Inspect the executable MATPOWER evidence

The successful MATPOWER 8.1 / GNU Octave run is summarized in:

```text
validation/results/MATPOWER_OCTAVE_VALIDATION_REPORT.md
validation/results/matpower_octave_crosscheck_summary.csv
```

The workflow itself is:

```text
.github/workflows/matpower-octave-validation.yml
```

It downloads and SHA-256 verifies the official MATPOWER 8.1 release, runs `rundcpf` under GNU Octave for IEEE14/30/39/57/118/300, independently computes the same intact DC solutions in NumPy, compares bus angles and branch active-power flows, and fails if the declared tolerances are exceeded.

To rerun it, use the repository **Actions** tab and choose **MATPOWER 8.1 / Octave validation → Run workflow**.

## 4. Inspect the physical-branch outage extension

Reviewer-facing frozen summaries are under:

```text
stages/07_branch_outage_validation/outputs/
```

The main network summary is:

```text
branch_n1_network_summary.csv
```

and the associated methodology/interpretation note is:

```text
docs/PHASE11_BRANCH_OUTAGE_REPORT.md
```

These outputs cover all 784 active physical branch rows. The public documentation explicitly distinguishes branch N-1 screening from a full security-constrained N-1 assessment.

## 5. Data provenance and licensing

See:

```text
docs/DATA_SOURCE_MANIFEST.md
THIRD_PARTY_LICENSES.md
LICENSE
```

No missing thermal ratings are fabricated, and the simple structural graph is kept distinct from the physical-branch electrical representation.

## 6. Frozen public reproducibility release

The `v1.0.0-submission` release contains the complete public computational archive: staged inputs/outputs, portable reproduction entry points, validation evidence, technical documentation and checksums.

The submitted manuscript PDF, LaTeX manuscript source, supplementary manuscript PDF/source, cover letter and other journal-submission files are intentionally excluded from the public release while the article is under peer review.

## Notes

- Reviewer-facing scripts use repository-relative paths.
- Hypothetical candidate lines are structural heuristics only; no reactance, thermal rating, geography, or cost is invented for them.
- The executable MATPOWER check validates the intact DC equations and branch-flow implementation. Custom island handling, redispatch, and load-curtailment proxies are separate study components and are not represented as native MATPOWER security-analysis functionality.
