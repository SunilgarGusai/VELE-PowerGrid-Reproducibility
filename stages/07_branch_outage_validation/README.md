# Stage 07 — Physical-branch outage validation

This stage extends the primary single-bus analysis with a one-at-a-time outage screen of every active physical MATPOWER branch row in the six frozen benchmark systems.

## Scope

| Network | Active physical branch rows |
|---|---:|
| IEEE14 | 20 |
| IEEE30 | 41 |
| IEEE39 | 46 |
| IEEE57 | 80 |
| IEEE118 | 186 |
| IEEE300 | 411 |
| **Total** | **784** |

A physical branch row is removed while all buses, loads and generators remain unless the resulting topology separates them. The electrical layer retains individual branch rows, reactance, transformer data and branch status. The structural VELE layer is rebuilt as a **simple graph** from the surviving physical rows.

This is a transmission-branch **N-1 screening extension**, not a complete security-constrained N-1 assessment: it does not perform remedial OPF, protection simulation, generator-contingency analysis, AC voltage-security analysis or cascading-failure simulation.

## Why parallel circuits matter

A simple structural graph records only whether at least one active connection exists between two buses. Therefore, if one circuit of a parallel pair trips while another remains, the structural edge is unchanged even though the electrical network is different.

In the frozen study:

- 22 active branch rows belong to parallel pairs;
- all 22 single-circuit trips leave the simple structural topology unchanged;
- all 22 therefore have zero simple-graph VELE stress;
- all 22 nevertheless produce nonzero DC flow redistribution.

More broadly, 269/784 physical branch outages have numerically zero bounded VELE stress. This is a deliberate limitation result, not a failure hidden from the analysis, and it is one reason VELE is positioned as complementary structural screening rather than as a general critical-transmission-line index.

## Reviewer-facing outputs committed on `main`

The `outputs/` directory contains frozen summary tables:

- `branch_n1_network_summary.csv` — network-level counts, maxima and runtime;
- `branch_n1_vele_correlations.csv` — case-wise VELE/electrical rank associations;
- `branch_n1_vele_event_auc.csv` — eligible event-discrimination summaries;
- `branch_n1_redispatch_sensitivity_summary.csv` — sensitivity to the alternative deterministic redispatch rule.

Key invariants checked automatically by the Repository verification workflow are:

- 784 physical branch outages;
- 22 parallel/topology-unchanged branch rows;
- 114 residual structural-disconnection cases;
- 47 secondary surviving-load-shedding cases.

## Interpretation boundary

The branch extension strengthens the paper by adding a conventional transmission-component perturbation layer, but it does not make VELE an electrical line-criticality metric. Flow redistribution, service consequences and `RATE_A` active-power loading remain electrical quantities; VELE contains no branch reactance, MW transfer, rating or circuit-multiplicity information.

For the full methodological interpretation, see `../../docs/PHASE11_BRANCH_OUTAGE_REPORT.md`.

## Frozen submission snapshot

The complete manuscript-associated `v1.0.0-submission` release is intended to carry the full row-level branch-outage table, surviving branch-flow outputs, reproduction script and independent stage verifier in addition to the reviewer-facing summaries committed on `main`.
