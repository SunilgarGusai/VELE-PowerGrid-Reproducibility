# Frozen method protocol

This document summarizes the computational protocol represented by the public VELE reproducibility repository and the frozen `v1.0.0-submission` release.

## 1. Benchmark systems

The study uses six MATPOWER 8.1 benchmark systems:

- IEEE14
- IEEE30
- IEEE39
- IEEE57
- IEEE118
- IEEE300

The electrical representation retains the MATPOWER bus, branch, generator and demand data needed by the DC-flow workflow. The structural representation is a simple graph derived from the corresponding network connectivity.

## 2. Structural VELE layer

The structural analysis includes:

1. component-wise VELE for disconnected residual graphs;
2. a bounded VELE structural stress/stability transformation;
3. the exact connected-component identity `VELE = 2 * lambda_max(M_VEL)`;
4. progressive node-removal trajectories;
5. structural line-candidate heuristics:
   - Direct-VELE;
   - centrality-balanced VCB-VELE;
   - distance-penalized DCP-VELE;
6. conventional structural comparators and natural-connectivity perturbation evidence where applicable.

Candidate-line heuristics are structural screening rules only. No unsupported reactance, rating, geographic length or cost is invented for proposed lines.

## 3. Single-bus outage screening

Every bus in each benchmark system is removed once, producing **558 single-bus outage cases** in total.

For each case, the study evaluates the residual structural graph and an island-aware DC-flow consequence model. Removing a bus also removes its incident physical branches and attached load/generation, so this is a stylized bus/substation-loss screening experiment rather than conventional line/generator N-1 security compliance.

## 4. Physical branch-outage screening

Every active MATPOWER physical branch row is removed once, producing **784 physical branch-outage cases**.

The branch experiment explicitly preserves the distinction between:

- physical electrical branch rows, including parallel circuits; and
- simple structural graph edges.

This distinction exposes the parallel-circuit blind spot quantified in the paper and repository.

## 5. Progressive attacks

Progressive electrical trajectories are evaluated under random, adaptive-degree and adaptive-betweenness node-removal strategies, producing **1,692 electrical states** across the benchmark set.

The structural trajectories and electrical service consequences are compared without treating VELE as a physical resilience metric by itself.

## 6. Electrical validation layer

The island-aware DC workflow retains the available MATPOWER electrical information needed for active-power screening, including branch reactance, taps/phase shifts, generation and load. The workflow includes deterministic generator redispatch and a secondary surviving-load-shedding proxy when aggregate surviving generation cannot meet surviving demand.

Where positive `RATE_A` values are available, branch active-power loading relative to `RATE_A` is reported as a **DC active-power-to-RATE_A diagnostic proxy**. `RATE_A` is not enforced as a redispatch or optimization constraint in this study.

## 7. Implementation cross-checks

Two implementation checks are retained:

1. an independent PYPOWER-core cross-check for intact and representative outage states;
2. executable MATPOWER 8.1 / GNU Octave CI validation for all six intact systems.

Repeated clean MATPOWER CI executions agree with the independent NumPy DC implementation within `1e-12` degrees in bus angle and `1e-11` MW in branch active-power flow.

## 8. Statistical interpretation

The study uses case-wise rank correlations, case-resampling intervals, finite-benchmark permutation/FDR diagnostics, event ROC-AUC where event counts are adequate, ranking overlap, sensitivity analyses and explicit disagreement cases.

These analyses describe the finite benchmark evidence. They are not presented as population-level guarantees.

## 9. Runtime/scalability

Runtime measurements cover individual VELE evaluation, structural screening trajectories, candidate selection, DC screening and hybrid structural-electrical screening. Reported absolute timings are hardware/software dependent and are interpreted accordingly.

## 10. Reproducibility boundary

The live `main` branch is intentionally a compact reviewer-facing validation/provenance layer. The complete public computational submission snapshot is preserved in the GitHub release `v1.0.0-submission`.

For exact navigation, see:

- `QUICKSTART.md`
- `docs/REPRODUCIBILITY.md`
- `docs/FROZEN_RESULTS.md`
- `docs/DATA_SOURCE_MANIFEST.md`
