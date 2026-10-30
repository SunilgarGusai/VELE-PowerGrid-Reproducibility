# Third-party software and data

This repository's **custom analysis code** is licensed under the repository MIT License. Third-party software and benchmark data retain their original upstream terms.

## MATPOWER 8.1

The executable validation workflow downloads the official MATPOWER 8.1 release from the MATPOWER GitHub project.

- Project: https://github.com/MATPOWER/matpower
- Release: https://github.com/MATPOWER/matpower/releases/tag/8.1
- MATPOWER code license: 3-clause BSD

The MATPOWER 8.1 upstream license explicitly states that the **MATPOWER case files distributed with MATPOWER are not covered by the BSD software license**; case-data provenance/permissions remain those stated by the MATPOWER distribution and original sources. This repository therefore does not relicense those benchmark cases.

## GNU Octave

GNU Octave is installed only in the GitHub Actions validation runner and is not redistributed by this repository.

## Python dependencies

NumPy, pandas, SciPy, NetworkX, Matplotlib and other Python dependencies retain their respective upstream licenses. See `requirements.txt` for pinned versions used in the frozen computational environment.

## PGLib-OPF v23.07 source data used in certified_cut_v2

The Version 2 certificate module downloads exact IEEE57/IEEE118 typical and API-stressed input files from the pinned upstream [PGLib-OPF v23.07 release](https://github.com/power-grid-lib/pglib-opf/tree/v23.07). The download utility verifies each source file against its archived SHA-256 record. These source case files are **not** relicensed by this repository.

- PGLib-OPF **data**: Creative Commons Attribution 4.0 International (CC BY 4.0). Cite the original benchmark/project, upstream version, data licensors and the appropriate case provenance.
- PGLib-OPF **software**: upstream MIT licence (not a claim about the benchmark data).
- Upstream [v23.07 LICENSE](https://github.com/power-grid-lib/pglib-opf/blob/v23.07/LICENSE) explicitly distinguishes these software and data terms; individual case-header credits also apply.
- The custom `certified_cut_v2/*.py` scripts remain under this repository's MIT licence, with original upstream data terms retained.

No PGLib case data are stored in `certified_cut_v2/inputs/` in the source-controlled branch. Users obtain them separately through the hash-checking downloader.
