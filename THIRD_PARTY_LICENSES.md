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
