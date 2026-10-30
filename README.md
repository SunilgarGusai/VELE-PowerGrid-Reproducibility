# VELE power-grid vulnerability research — corrected, source-traceable evidence

This repository accompanies a modest **structural observability and electrical-consequence validation** study. The vertex eccentricity labeled energy (VELE) is a published unweighted spectral graph diagnostic, **not** a power-flow model, OPF solver, reinforcement optimizer, protection algorithm or general reliability score.

## Current Version 2 working evidence

The peer-review-oriented [certified-cut module](certified_cut_v2/README.md) includes:
- Exact source-identified PGLib-OPF **v23.07** IEEE57/118 typical/API case manifests and SHA-256-checked upstream download utility;
- all **532 physical single-circuit outages plus four intact states** evaluated by a conservative, standard capacity-cut inequality;
- independently reproduced critical bus sets for **13 positively cut-certified connected** IEEE118 heavily loaded outages;
- **four rigorously certified zero-VELE cases**: branches 52 (at least 60.29 MW curtailed), 53 (49.29 MW), 55 (15.10 MW) and 173 (13.49 MW);
- scripts using two different maximum-flow/minimum-cut algorithms, archived case-level CSV and a dedicated GitHub Actions validation job.

The IEEE57/118 typical and API conditions are **four operating cases on two topologies**, not four independent grids. The MW values are necessary minimum-curtailment **lower bounds** under source-rated passive branch assumptions, not globally optimized AC OPF outputs. A zero cut bound is **unknown**, not verified safe.

## Original MATPOWER/DC work — retained as Version 1

The existing [v1.0.0-submission release](https://github.com/SunilgarGusai/VELE-PowerGrid-Reproducibility/releases/tag/v1.0.0-submission) preserves the earlier six IEEE/MATPOWER 8.1 structural/DC evidence, its 784 active physical-circuit outages, 558 bus-outage scenarios, archived structural heuristics, case outputs and executable MATPOWER/Octave validation. It has not been overwritten.

The verified historical **269/784** result means that for those original physical-circuit outages, the source-specified DC redistribution changed while both VELE and mean eccentricity were unchanged. This is evidence of a DC-flow **proxy mismatch**, not proof of necessary AC load shedding.

Historical documents under docs/ and stages/ remain identified as **Version 1** interpretations unless updated explicitly. They must not be used to turn candidate solver curtailment into proven physical risk.

## Essential correction to the original exploratory AC study

The preliminary nonlinear AC experiment saved primal-feasible candidate operating points. Of 157 candidate-positive curtailment labels, **91** came from unsuccessful/time-limited IPOPT terminations. Independent primal feasibility does not establish an optimizer-converged minimum; even a converged locally feasible solution would be an **upper bound** on globally minimal curtailment. Older candidate-defined AC event AUROCs are therefore **not validated security-event discrimination**.

The source-rated capacity-cut proof supplies **positive necessary lower bounds for 13 connected outages**, without relying on the AC optimizer. The graph-theoretic cut idea and the published 2025 VELE invariant are not claimed as newly invented.

## Reproduce Version 2

Install the Python packages in [certified_cut_v2/requirements.txt](certified_cut_v2/requirements.txt). In the certified_cut_v2 directory, run in order:

1. python fetch_pglib_v23_07_sources.py
2. python build_source_cut_bounds.py
3. python replay_cut_certificates_offline.py
4. python independent_explicit_cut_witnesses.py

The four benchmark source cases are downloaded by exact upstream tag and checked against their individual SHA-256 records. The benchmark files belong to PGLib's **CC BY 4.0 data** licence, not the repository's custom-code MIT licence. See [source provenance](certified_cut_v2/README.md).

## Publication and double-blind review

The revised prospective paper is **“Electrical Consequences Invisible to Eccentricity-Based Spectral Screening in Power-Grid Contingencies.”** The paper is being prepared for AUT Journal of Electrical Engineering; **no acceptance or publication is claimed**.

This GitHub URL is author-identifying. The blind-review manuscript should use its **anonymous source-complete supplementary ZIP** unless the journal explicitly authorizes an identifying repository citation during double-blind review. The identified paper may link to this repository and the **eventually tagged Version 2 release**. The present branch is a reviewed development candidate, not a final DOI-bearing data release.

## Existing repository assets

- [Historical frozen numerical results](docs/FROZEN_RESULTS.md)
- [Historical method protocol](docs/METHOD_PROTOCOL.md)
- [MATPOWER 8.1 source provenance](docs/DATA_SOURCE_MANIFEST.md)
- [Historical quickstart](QUICKSTART.md)
- [Third-party licences](THIRD_PARTY_LICENSES.md)
- [Version 2 source-case evidence](certified_cut_v2/README.md)
- [GitHub automated source-replay workflow](.github/workflows/certified-cut-v2.yml)
