# Stage 7 / Phase 11 — Physical-branch outage validation

This stage extends the manuscript's primary 558 single-bus outage study with a complete physical-branch outage screen over every active MATPOWER branch row in IEEE14/30/39/57/118/300.

## Scope

- 784 active physical branch rows are tripped one at a time.
- All buses, loads, and generators remain unless separated by the outage topology.
- The electrical layer retains physical branch multiplicity and original MATPOWER parameters.
- The structural layer is rebuilt as a simple graph from surviving branch rows.
- Therefore, tripping one circuit from a parallel pair can leave the structural edge unchanged.
- The experiment is a branch N-1 screening extension, not a full security-constrained N-1 assessment with remedial OPF, protection, or generator contingencies.

## Headline results

- 784 physical branch outages.
- 114 produce residual structural disconnection.
- 47 produce secondary surviving-load shedding under the frozen adequacy proxy.
- 22 outages are single-circuit trips in parallel pairs; all have exactly zero simple-graph VELE stress but nonzero DC flow redistribution.
- 269/784 branch outages have numerically zero bounded VELE stress because the eccentricity-sensitive structural intensity is unchanged.
- VELE-flow Spearman correlation is supported after finite-benchmark FDR adjustment on IEEE118 (rho=0.286633, q=0.0012) and IEEE300 (rho=0.255257, q=0.0012), but the six-network median is only about 0.110.
- Eligible branch-outage VELE ROC-AUC values include IEEE118 residual disconnection 0.844947, IEEE300 residual disconnection 0.877451, and IEEE300 secondary shedding 0.838302.
- IEEE39 is an explicit counterexample: VELE AUC is 0.384 for residual disconnection and 0.520 for RATE_A active-power exceedance.
- Alternative redispatch leaves secondary-shedding event counts unchanged on all six systems, while IEEE39 RATE_A exceedance cases change from 18 to 45.

## Interpretation

The extension strengthens the manuscript by adding a conventional transmission-component perturbation layer, but it does not turn VELE into a universal critical-line index. Its strongest branch-outage results again occur for larger-system disconnection/service consequences, while parallel circuits and many electrically important redistributions are invisible when the simple graph's eccentricity profile is unchanged. This reinforces the manuscript's central positioning of VELE as a complementary topology-only diagnostic rather than a substitute for electrical contingency analysis.
