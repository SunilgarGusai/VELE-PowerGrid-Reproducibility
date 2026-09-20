# Data source manifest

## Primary benchmark source

The study uses public MATPOWER benchmark cases from **MATPOWER 8.1**:

- case14
- case30
- case39
- case57
- case118
- case300

Official release: https://github.com/MATPOWER/matpower/releases/tag/8.1

Official release asset used by the executable validation workflow:

`matpower8.1.zip`

Published SHA-256 digest:

`7f13b1441669a64e312d14a60e564cd91977ff1676ff77d25538e94ff313dd56`

The GitHub Actions validation job checks this digest before executing MATPOWER.

## Data fields used

From the MATPOWER case definitions, the workflow uses the benchmark's published values for:

- buses and bus types;
- active/reactive demands;
- generator locations, active-power outputs and limits;
- branch endpoints;
- branch series reactance;
- transformer tap ratios;
- phase shifts;
- branch status;
- `RATE_A` values where positive and available.

No missing thermal ratings are fabricated. In the frozen paper, absolute `RATE_A` loading diagnostics are therefore used only for benchmark systems where positive ratings are actually supplied for the relevant branches.

## Structural representation

For VELE calculations, an active MATPOWER network is mapped to a simple undirected structural graph. Parallel physical circuits collapse to a single structural edge. Electrical validation retains physical branch rows individually.

This distinction is deliberate and is explicitly tested by the physical-branch outage extension: a single circuit outage in a parallel pair can leave the simple structural graph unchanged while still changing electrical flows.

## Third-party licensing

MATPOWER software is distributed under the 3-clause BSD license. MATPOWER's own license states that its distributed case files are not covered by that software license; benchmark-data provenance/permissions remain those of the upstream distribution and original sources. This repository does not relicense MATPOWER case data.
