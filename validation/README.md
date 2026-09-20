# Executable MATPOWER 8.1 cross-validation

This directory provides an external implementation check for the manuscript's DC power-flow equations.

The GitHub Actions workflow:

1. starts from a clean Ubuntu runner;
2. installs GNU Octave;
3. downloads the official MATPOWER 8.1 release archive;
4. verifies the published MATPOWER 8.1 SHA-256 digest;
5. computes intact-case DC solutions independently in Python/NumPy from the MATPOWER case matrices;
6. executes MATPOWER 8.1 `rundcpf` under GNU Octave for IEEE 14, 30, 39, 57, 118 and 300;
7. compares bus voltage angles and branch active-power flows case-by-case;
8. fails automatically if the numerical discrepancy exceeds the declared tolerance.

## Why this matters

The main paper uses an independent Python implementation of the MATPOWER DC equations for its island-aware screening workflow. Agreement with the PYPOWER core was already checked during development. This workflow adds an **executable MATPOWER 8.1 check in a clean environment**, avoiding reliance on the same Python code path for validation.

The cross-check is intentionally limited to the intact benchmark equations. The manuscript's custom island handling, redispatch and load-curtailment proxies remain separately verified by repository tests and are not represented as native MATPOWER security-analysis functionality.

## Files

- `python_dcpf_reference.py` — independent NumPy implementation using MATPOWER case matrices
- `run_matpower_crosscheck.m` — executable MATPOWER 8.1 / Octave run
- `compare_matpower_python.py` — numerical comparison and pass/fail report
- `artifacts/` — generated during CI; not required to be committed

## Tolerance

The default pass threshold is `1e-8` for both bus-angle differences (degrees) and active-power-flow differences (MW). The workflow reports the observed maximum errors; the manuscript should quote only values actually produced by a successful CI run.
