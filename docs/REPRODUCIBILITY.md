# Reproducibility guide

The VELE repository is organized around two complementary public layers:

1. the live `main` branch, which is a compact reviewer-facing validation and provenance layer; and
2. the frozen GitHub release `v1.0.0-submission`, which contains the complete public computational snapshot prepared for manuscript submission.

This distinction is intentional. It keeps the repository homepage navigable while preserving the fuller staged archive needed for traceability.

## What the live branch can verify directly

After cloning the repository, install the pinned Python dependencies:

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The same dependency set is also represented in `environment.yml`.

### Smoke-check the public DC utilities

```bash
python validation/python_dcpf_reference.py --help
python validation/compare_matpower_python.py --help
```

### Inspect the frozen numerical evidence

The live branch exposes machine-readable reviewer-facing outputs for:

- executable MATPOWER 8.1 / GNU Octave validation;
- the 784-case physical-branch outage extension;
- branch-outage redispatch sensitivity;
- VELE/electrical rank correlations;
- event-discrimination summaries;
- benchmark provenance and release hashes.

See `docs/FROZEN_RESULTS.md` for the result-to-source map.

## GitHub Actions verification

Two workflows provide independent checks.

### Repository verification

`.github/workflows/repository-validation.yml`

This workflow:

- installs the pinned Python environment;
- checks required reviewer-facing files;
- compiles the public Python utilities;
- performs CLI smoke tests;
- verifies the committed MATPOWER cross-check evidence;
- checks aggregate physical-branch invariants.

### MATPOWER 8.1 / Octave validation

`.github/workflows/matpower-octave-validation.yml`

This workflow starts from a clean Ubuntu runner, installs GNU Octave, downloads the official MATPOWER 8.1 release, verifies its checksum, executes `rundcpf` on all six intact cases, independently computes the same solutions in NumPy, and compares bus angles and branch active-power flows.

The workflow fails if the declared numerical tolerances are exceeded.

## Frozen release

The public release

`v1.0.0-submission`

contains the complete public reproducibility archive supporting the manuscript-ready study, including staged computational inputs/outputs, portable reproduction entry points, validation evidence, documentation and integrity checks.

The manuscript PDF/source, cover letter and journal-portal files are intentionally excluded from the public reproducibility release.

## What is not claimed

The repository does not claim that:

- VELE replaces AC/DC contingency analysis;
- the structural candidate heuristics are electrically feasible transmission plans;
- the executable MATPOWER intact-case check validates the custom island/redispatch/load-curtailment methodology as native MATPOWER security analysis;
- every historical development artifact is required to understand the frozen study.

The public package is designed for transparent verification of the frozen computational evidence, not for presenting development clutter as scientific output.

## Data and third-party materials

MATPOWER benchmark data and software retain their upstream terms. The repository's original analysis code is released under the repository licence, while third-party materials are documented separately in:

- `THIRD_PARTY_LICENSES.md`
- `docs/DATA_SOURCE_MANIFEST.md`

No missing electrical ratings are fabricated.

## Recommended reviewer path

1. Read `README.md` for the scientific question and headline evidence.
2. Read `docs/METHOD_PROTOCOL.md` for the frozen methodology.
3. Read `docs/FROZEN_RESULTS.md` for the numerical result map.
4. Inspect `validation/results/` and `stages/07_branch_outage_validation/outputs/` for machine-readable evidence.
5. Use the Actions tab for executable MATPOWER validation.
6. Use the `v1.0.0-submission` release for the complete public computational archive.
