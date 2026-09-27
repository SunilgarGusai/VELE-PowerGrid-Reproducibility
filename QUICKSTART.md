# Quick start

This repository has two public layers:

1. the live `main` branch — compact reviewer-facing validation, provenance and key results; and
2. the frozen [`v1.0.0-submission`](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v1.0.0-submission) release — the complete public computational submission snapshot.

If you only want to understand the study, start with `README.md`, then `docs/METHOD_PROTOCOL.md` and `docs/FROZEN_RESULTS.md`.

## 1. Create the environment

### Conda

```bash
conda env create -f environment.yml
conda activate vele-powergrid
```

### Or pip/venv

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Validate the reviewer-facing artifact

```bash
python scripts/validate_public_artifact.py
```

This checks the curated repository manifest, key presentation/documentation assets, the six-case MATPOWER cross-check summary and the aggregate 784-branch invariants.

## 3. Smoke-check the public DC utilities

```bash
python validation/python_dcpf_reference.py --help
python validation/compare_matpower_python.py --help
```

The **Repository verification** GitHub Actions workflow performs these checks automatically on pull requests and pushes to `main`.

## 4. Inspect executable MATPOWER evidence

Reference files:

```text
validation/results/MATPOWER_OCTAVE_VALIDATION_REPORT.md
validation/results/matpower_octave_crosscheck_summary.csv
validation/results/MATPOWER_OCTAVE_REPEATABILITY_NOTE.md
validation/results/matpower_octave_crosscheck_summary_run_35533409590.csv
```

Workflow:

```text
.github/workflows/matpower-octave-validation.yml
```

The workflow downloads and checksum-verifies the official MATPOWER 8.1 release, runs `rundcpf` under GNU Octave for IEEE14/30/39/57/118/300, independently solves the same intact DC equations in NumPy, compares bus angles and branch active-power flows, and fails if the declared tolerances are exceeded.

To rerun it, open **Actions → MATPOWER 8.1 / Octave validation → Run workflow**.

## 5. Inspect the physical-branch extension

Reviewer-facing frozen outputs are under:

```text
stages/07_branch_outage_validation/outputs/
```

The most useful files are:

```text
branch_n1_network_summary.csv
branch_n1_vele_correlations.csv
branch_n1_vele_event_auc.csv
branch_n1_redispatch_sensitivity_summary.csv
```

The corresponding interpretation notes are:

```text
docs/PHASE11_BRANCH_OUTAGE_REPORT.md
stages/07_branch_outage_validation/README.md
```

These outputs cover all **784 active physical branch rows**. The documentation explicitly distinguishes this screening experiment from a full security-constrained N-1 assessment.

## 6. Follow the result map

For a compact route from claims to files, use:

```text
docs/FROZEN_RESULTS.md
REPOSITORY_MANIFEST.csv
```

The repository banner and workflow visuals are under:

```text
docs/assets/
```

## 7. Data provenance and licensing

See:

```text
docs/DATA_SOURCE_MANIFEST.md
THIRD_PARTY_LICENSES.md
LICENSE
```

No missing thermal ratings are fabricated, and the simple structural graph is kept distinct from the physical-branch electrical representation.

## 8. Complete frozen public snapshot

The `v1.0.0-submission` release contains the fuller staged computational archive, portable reproduction entry points, validation evidence, technical documentation and checksums.

The submitted manuscript PDF/source, supplementary manuscript files, cover letter and journal-submission files are intentionally excluded from the public release during peer review.

## Important interpretation notes

- VELE is evaluated as a **complementary structural diagnostic**, not a replacement for electrical security analysis.
- Hypothetical candidate lines are structural heuristics only; no unsupported reactance, rating, geography or cost is invented.
- The executable MATPOWER cross-check validates intact DC equations and branch-flow implementation. Custom island handling, redispatch and load-curtailment proxies remain separate study components.
- A simple structural graph cannot represent the loss of one circuit when a parallel circuit remains in service; this limitation is quantified explicitly in the frozen results.
