# VELE Source-Rated Certified-Cut Reproducibility — Version 2.0.0

This is the immutable **public code/data/evidence release** for the research manuscript in preparation, “Electrical Consequences Invisible to Eccentricity-Based Spectral Screening in Power-Grid Contingencies.” It is **not** the unpublished manuscript or its submission package.

## Scientific scope

- Historical MATPOWER 8.1 six-system DC evidence: 784 original physical branch outages; 269 have nonzero DC redistribution but unchanged VELE and mean eccentricity. This is not a necessary-AC-curtailment claim.
- Separate pinned PGLib-OPF v23.07 IEEE57/118 typical and stressed case cohorts: 532 physical circuit outages and four intact states (536 source-rated cut calculations).
- Thirteen connected stressed IEEE118 outages possess independently checked, positive **necessary** curtailment lower bounds. Four of these have exactly unchanged VELE: circuit 52 (60.29 MW), 53 (49.29 MW), 55 (15.10 MW), and 173 (13.49 MW), reported as conservative lower bounds.
- A zero source-rated cut bound cannot establish power-system safety; original AC candidate-curtailment AUROCs are not validated global-optimality outcome labels.
- VELE is the previously published 2025 invariant; the cut inequality and maximum-flow algorithms are established mathematical tools.

## Reproduction and licensing

The source files are downloaded directly from the upstream PGLib **v23.07** tag with recorded SHA-256 checks and are *not* relicensed. PGLib benchmark data use **CC BY 4.0**, separately from MIT-licensed custom analysis code. Read `THIRD_PARTY_LICENSES.md` and `certified_cut_v2/README.md` before reproduction. Automated source replay runs all 536 bounds and two independent flow methods for 13 positive connected witnesses.

This release **does not include the unpublished manuscript PDF, manuscript source, cover letter, personal author declarations or reviewer-only supplements**. The historical `v1.0.0-submission` release remains unchanged.

The attachment `VELE_REPRODUCIBILITY_PUBLIC_v2.0.0.zip` contains the tracked public source tree, and `SHA256SUMS_PUBLIC_V2.txt` records its digest. The GitHub-generated source archives contain the same public, tagged repository tree.
