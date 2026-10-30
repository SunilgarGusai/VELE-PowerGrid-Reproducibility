# Certified physical-circuit cut validation — Version 2 candidate

This directory supports an IEEE/MATPOWER-based observability-limit study, not a claim that VELE optimizes power-system security.

## Independent evidence cohorts

1. **MATPOWER 8.1**: six IEEE topologies and 784 physical branch outages. An archived 784-row study finds 269 physical outages with nonzero DC redistribution but unchanged VELE and mean eccentricity. This is a *DC proxy*, not a proof of necessary AC load shedding. Historic material is retained in the [v1.0.0-submission release](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v1.0.0-submission).
2. **PGLib-OPF v23.07**: IEEE57 and IEEE118, each in typical and API (stressed) conditions. Four source operating cases represent **two graph topologies**, not four independent systems. Physical circuits and their original RATE_A MVA limits are preserved individually. All 532 single-circuit outages and four intact states are checked.

## Conservative necessary-curtailment lower bound

For a subset S of buses, let D(S) denote positive demand in MW, Gmax(S) total online generator active Pmax MW, and C(S) sum of surviving physical interface RATE_A MVA limits. For the four source-verified passive cases, any feasible AC point satisfies

    Unavoidable curtailed demand >= max_S [D(S) - Gmax(S) - C(S)]_+ .

This follows from nonnegative internal real losses and |P| <= |S| <= RATE_A at each rated branch end. A zero bound is inconclusive. This standard necessary inequality is neither a new OPF method nor a sufficient AC feasibility test.

All 13 strictly positive connected cases occur in the heavily loaded IEEE118 condition. Physical branch IDs: 51, 52, 53, 55, 104, 118, 121, 125, 171, 173, 174, 175 and 185. Exactly four have unchanged eccentricity/VELE: **52 >=60.29 MW; 53 >=49.29 MW; 55 >=15.10 MW; 173 >=13.49 MW**. The cut certificate uses a source-identified set of buses with insufficient local generator and physical boundary circuit capacity.

## Reproduce with Python 3

Install requirements.txt, then run in sequence:

    python fetch_pglib_v23_07_sources.py
    python build_source_cut_bounds.py
    python replay_cut_certificates_offline.py
    python independent_explicit_cut_witnesses.py

The downloader retrieves exact published PGLib-OPF v23.07 case files and verifies their recorded SHA-256. Data are supplied under upstream Creative Commons Attribution 4.0, not the parent's custom-code MIT license; see [upstream data/software license](https://github.com/power-grid-lib/pglib-opf/blob/v23.07/LICENSE) and case headers. We do not distribute the source case files through this repository directory.

The source-only regeneration creates REGENERATED_536_CUT_LOWER_BOUNDS.csv; the replay checks it against the 536 saved source-derived outputs. The independent script reconstructs all thirteen critical bus partitions using a second flow algorithm.

## Important correction to historical AC outputs

The older CasADi/IPOPT experiment had 91 of 157 positive candidate-curtailment labels from unsuccessful solver terminations. Independent primal feasibility is not a local or global minimization certificate. Even a converged local feasible point is an upper bound on unavoidable curtailment; only the strictly positive necessary cut proves a positive lower bound. Candidate-defined old AC ranking AUROCs are **not validated physical event discrimination**.

This repository preserves earlier results but does not claim superiority of VELE, a new security optimization algorithm, cascading dynamics or cost-feasible transmission reinforcement.

## Double-blind publication

The repository is author-identifying. Until journal instructions authorize public identity disclosure, upload an anonymized reproduction package alongside the double-blind manuscript. The identified final version can include a tagged Version 2 GitHub release URL once frozen and published; this working branch is not yet such a release.
