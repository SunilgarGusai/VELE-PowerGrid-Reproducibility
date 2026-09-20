# Quick start

## 1. Python environment

```bash
python -m venv .venv
```

Activate the environment and install the pinned dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Verify the repository

```bash
python reproduction/run_all.py --mode verify
```

## 3. Reproduce the post-review analyses

```bash
python reproduction/run_all.py --mode reproduce-postreview
```

## 4. Reproduce the 784 physical-branch outage extension

```bash
python reproduction/run_all.py --mode reproduce-branch
```

## 5. Executable MATPOWER cross-check

The GitHub Actions workflow `.github/workflows/matpower-octave-validation.yml` runs an independent executable MATPOWER 8.1 `rundcpf` cross-check under GNU Octave in a clean Ubuntu runner. It compares MATPOWER bus angles and branch active-power flows against an independent NumPy implementation of the same DC equations.

The workflow can also be run manually from the repository's **Actions** tab.

## Notes

- Reviewer-facing scripts use repository-relative paths.
- Historical development scripts, where retained, are separated from the executable workflow.
- Hypothetical candidate lines are structural heuristics only; no reactance, thermal rating, geography or cost is invented for them.
