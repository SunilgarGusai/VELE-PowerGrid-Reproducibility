# MATPOWER 8.1 / GNU Octave CI repeatability note

The executable MATPOWER cross-check has been repeated successfully in clean GitHub-hosted Ubuntu runners. Both runs use the same repository validation code, the same official MATPOWER 8.1 release archive, the same verified MATPOWER SHA-256, and the same declared comparison tolerances (`1e-8` degrees for bus angles and `1e-8` MW for branch active-power flows).

## Reference run

- Workflow run: **35531005040**
- Repository commit: `15b22971ed0b6fa6566faeafcb9b75eb97be7639`
- Status: **PASS**
- Maximum absolute bus-angle difference: `4.050094e-13` degrees
- Maximum absolute branch-flow difference: `5.798029e-12` MW
- Artifact: `matpower-octave-crosscheck`

The committed reference summary is `matpower_octave_crosscheck_summary.csv`.

## Independent repeat run after CI-runtime refresh

- Workflow run: **35533409590**
- Repository commit: `b2708c5fe0b4dc45a0713ca53180be1c44afca27`
- Status: **PASS**
- Maximum absolute bus-angle difference: `6.039613e-13` degrees
- Maximum absolute branch-flow difference: `6.579626e-12` MW
- Artifact: `matpower-octave-crosscheck`
- Artifact SHA-256 digest reported by GitHub: `53047b5806b8e271450937bdaebd28a90601c4c35d262f394278677305d0b953`

The six-case repeat summary is `matpower_octave_crosscheck_summary_run_35533409590.csv`.

## Interpretation

The small change in the last numerical digits is consistent with floating-point roundoff across clean runner/software-stack executions. It is not a scientific discrepancy: both complete six-case runs remain more than three orders of magnitude inside the declared `1e-8` tolerances, and both independently reproduce the intact MATPOWER DC solutions to numerical precision.

For manuscript wording, the environment-robust statement is therefore:

> Repeated executable MATPOWER 8.1/GNU Octave CI runs reproduce all six intact benchmark solutions with maximum discrepancies below `1e-12` degrees in bus angle and below `1e-11` MW in branch active-power flow.

The exact last-digit maxima from a particular CI run should be treated as run-specific numerical diagnostics rather than universal constants.

## Scope boundary

These executable checks validate the **intact MATPOWER DC equations and branch-flow implementation**. They do not convert the manuscript's custom island handling, deterministic generator redispatch, load-curtailment proxy, or branch-outage service accounting into native MATPOWER security-analysis functionality. Those study components retain their separately documented validation and sensitivity checks.
