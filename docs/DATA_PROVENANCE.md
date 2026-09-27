# Data provenance

The VELE study is built on public MATPOWER benchmark systems and preserves a clear distinction between third-party benchmark data and original analysis code/results.

## Benchmark source

The frozen source version is **MATPOWER 8.1**. The six cases used are:

- `case14`
- `case30`
- `case39`
- `case57`
- `case118`
- `case300`

The executable validation workflow downloads the official `matpower8.1.zip` release asset and verifies the published SHA-256 digest recorded in `docs/DATA_SOURCE_MANIFEST.md` before running MATPOWER.

## Fields retained for electrical analysis

The workflow uses published MATPOWER values for bus types, demand, generator placement/output/limits, branch endpoints, reactance, transformer tap ratios, phase shifts, branch status and positive `RATE_A` values where available.

Missing thermal ratings are **not fabricated**. Consequently, absolute `RATE_A` loading diagnostics are restricted to cases/branches for which the benchmark source provides usable positive values.

## Structural versus physical representation

The VELE structural layer uses a simple undirected graph. Parallel physical circuits therefore collapse to a single structural edge.

The electrical layer retains physical MATPOWER branch rows individually. This is essential for interpreting the branch-outage extension and the quantified parallel-circuit blind spot.

## Provenance boundary

This repository does not claim ownership of MATPOWER software or benchmark case data and does not relicense those third-party materials. Original analysis scripts, documentation and derived outputs are distinguished from upstream materials through:

- `THIRD_PARTY_LICENSES.md`
- `docs/DATA_SOURCE_MANIFEST.md`
- the repository `LICENSE`

For exact release-level provenance, use the frozen `v1.0.0-submission` archive and its published checksums.
