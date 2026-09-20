# Manuscript wording patch after repeated executable MATPOWER CI

This patch is a **numerical-reporting refinement**, not a change to the frozen scientific conclusions.

Two clean GitHub Actions executions of the executable MATPOWER 8.1/GNU Octave cross-check both pass all six intact benchmark systems by many orders of magnitude inside the declared `1e-8` angle/flow tolerances. The exact last digits differ slightly between hosted-runner executions, as expected for floating-point linear algebra:

| Run | max bus-angle difference | max branch-flow difference |
|---|---:|---:|
| 35531005040 | 4.050094e-13 deg | 5.798029e-12 MW |
| 35533409590 | 6.039613e-13 deg | 6.579626e-12 MW |

Therefore, the manuscript should not present `4.05e-13 deg` and `5.80e-12 MW` as environment-invariant constants. Use the repeatable bound **below `1e-12` degrees and below `1e-11` MW across repeated clean CI runs**.

## Abstract

Replace the run-specific wording:

> Executable MATPOWER 8.1 cross-validation under GNU Octave reproduces all six intact-case branch flows within 5.80 × 10−12 MW and bus angles within 4.05 × 10−13 degrees; independent PYPOWER-core checks of representative outage states agree within 1.74 × 10−11 MW.

with:

> Executable MATPOWER 8.1 cross-validation under GNU Octave reproduces all six intact-case solutions to numerical precision; across repeated clean CI runs, maximum discrepancies remain below 1 × 10−11 MW in branch active-power flow and 1 × 10−12 degrees in bus angle. Independent PYPOWER-core checks of representative outage states agree within 1.74 × 10−11 MW.

## Electrical-model validation methodology

Where the current text gives a single-run maximum of `4.05 × 10−13 degrees` and `5.80 × 10−12 MW`, replace that sentence with:

> Across repeated clean GitHub Actions executions, the independent NumPy solution and executable MATPOWER 8.1 agree for all six intact benchmark systems with maximum absolute discrepancies below 1 × 10−12 degrees in bus angle and below 1 × 10−11 MW in branch active-power flow; the exact run-specific diagnostics and artifacts are preserved in the public repository.

Keep the following boundary statement unchanged in substance:

> The executable MATPOWER check validates the intact DC equations, while the PYPOWER comparison additionally exercises representative custom island/outage states; neither check turns the subsequent redispatch or load-curtailment proxy into native MATPOWER security analysis.

## Results subsection on electrical-model cross-checks

Replace the run-specific exact maxima with:

> Repeated executable MATPOWER 8.1/GNU Octave workflows provide an external implementation check of the intact DC equations in clean cloud runners. Across IEEE14, IEEE30, IEEE39, IEEE57, IEEE118 and IEEE300, repeated runs remain below 1 × 10−12 degrees in maximum absolute bus-angle discrepancy and below 1 × 10−11 MW in maximum absolute branch-flow discrepancy relative to the independent NumPy solution. Run-specific reports and raw comparison artifacts are archived with the public repository.

The PYPOWER outage-state result `1.74 × 10−11 MW` may remain as currently reported because it comes from the separately frozen representative-outage cross-check.

## Conclusion

No substantive conclusion change is needed. Wording such as “executable MATPOWER 8.1/GNU Octave checks reproduce all six intact DC solutions to numerical precision” is already correct.

## Data and Code Availability

The current manuscript language is acceptable **only after** the complete manuscript-associated archive is frozen as the `v1.0.0-submission` GitHub release. The live `main` branch is presently a validated provenance/CI layer and does not contain every staged output/manuscript-builder file claimed for the full submission archive.

Before journal submission, either:

1. create the `v1.0.0-submission` release and attach the complete frozen reproducibility archive (preferred; then the current availability claim becomes true), or
2. if submitting before that release exists, narrow the Data and Code Availability paragraph so it describes `main` only as the public validation/provenance layer.

Do not describe the intact MATPOWER executable check as validation of the custom redispatch/load-shedding proxy, AC security, OPF, cascading behavior, or dynamic stability.
