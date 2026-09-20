#!/usr/bin/env python3
"""Independent NumPy DC power-flow reference for MATPOWER case files.

This script parses MATPOWER .m case matrices directly and solves the standard
DC equations without importing MATPOWER or PYPOWER. It is used only for the
executable MATPOWER 8.1 / GNU Octave cross-validation workflow.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

CASES = [14, 30, 39, 57, 118, 300]


def _matrix(text: str, name: str) -> np.ndarray:
    match = re.search(rf"mpc\.{name}\s*=\s*\[(.*?)\];", text, re.S)
    if not match:
        raise ValueError(f"Missing mpc.{name}")
    rows = []
    for raw in match.group(1).split(";"):
        cleaned = "\n".join(line.split("%")[0] for line in raw.splitlines()).strip()
        if cleaned:
            rows.append([float(x) for x in cleaned.replace("\n", " ").split()])
    if not rows or len({len(r) for r in rows}) != 1:
        raise ValueError(f"Invalid/non-rectangular mpc.{name}")
    return np.asarray(rows, dtype=float)


def _scalar(text: str, name: str) -> float:
    match = re.search(rf"mpc\.{name}\s*=\s*([^;]+);", text)
    if not match:
        raise ValueError(f"Missing mpc.{name}")
    return float(match.group(1).strip())


def parse_case(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    return _scalar(text, "baseMVA"), _matrix(text, "bus"), _matrix(text, "gen"), _matrix(text, "branch")


def solve_dcpf(base_mva: float, bus: np.ndarray, gen: np.ndarray, branch: np.ndarray):
    # MATPOWER columns (zero-based here):
    # bus: BUS_I=0, BUS_TYPE=1, PD=2, GS=4, VA=8
    # gen: GEN_BUS=0, PG=1, GEN_STATUS=7
    # branch: F_BUS=0, T_BUS=1, BR_X=3, TAP=8, SHIFT=9, BR_STATUS=10
    ids = bus[:, 0].astype(int)
    idx = {int(b): i for i, b in enumerate(ids)}
    nb = len(ids)
    nl = branch.shape[0]

    f = np.asarray([idx[int(v)] for v in branch[:, 0]], dtype=int)
    t = np.asarray([idx[int(v)] for v in branch[:, 1]], dtype=int)
    status = branch[:, 10].astype(float)
    x = branch[:, 3].astype(float)
    if np.any((status > 0) & np.isclose(x, 0.0)):
        raise ValueError("In-service zero-reactance branch encountered")

    tap = np.ones(nl, dtype=float)
    nonzero_tap = ~np.isclose(branch[:, 8], 0.0)
    tap[nonzero_tap] = branch[nonzero_tap, 8]
    b = status / x / tap
    shift = np.deg2rad(branch[:, 9])
    pfinj = b * (-shift)

    bf = np.zeros((nl, nb), dtype=float)
    rows = np.arange(nl)
    bf[rows, f] = b
    bf[rows, t] = -b

    bbus = np.zeros((nb, nb), dtype=float)
    pbusinj = np.zeros(nb, dtype=float)
    for k in range(nl):
        bbus[f[k], :] += bf[k, :]
        bbus[t[k], :] -= bf[k, :]
        pbusinj[f[k]] += pfinj[k]
        pbusinj[t[k]] -= pfinj[k]

    pbus = -bus[:, 2] / base_mva - pbusinj - bus[:, 4] / base_mva
    online = gen[:, 7] > 0
    for row in gen[online]:
        pbus[idx[int(row[0])]] += row[1] / base_mva

    refs = ids[bus[:, 1].astype(int) == 3]
    if len(refs) != 1:
        raise ValueError(f"Expected one reference bus, got {refs.tolist()}")
    ref = idx[int(refs[0])]
    nonref = np.asarray([i for i in range(nb) if i != ref], dtype=int)

    va0 = np.deg2rad(bus[:, 8])
    va = va0.copy()
    rhs = pbus[nonref] - bbus[np.ix_(nonref, [ref])].ravel() * va0[ref]
    va[nonref] = np.linalg.solve(bbus[np.ix_(nonref, nonref)], rhs)

    pf = (bf @ va + pfinj) * base_mva
    pt = -pf
    return np.rad2deg(va), pf, pt


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matpower-data", required=True, type=Path, help="MATPOWER 8.1 data directory containing case*.m")
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    bus_rows = []
    branch_rows = []
    for n in CASES:
        case = f"case{n}"
        path = args.matpower_data / f"{case}.m"
        if not path.exists():
            raise FileNotFoundError(path)
        base, bus, gen, branch = parse_case(path)
        va_deg, pf, pt = solve_dcpf(base, bus, gen, branch)
        for i, bus_id in enumerate(bus[:, 0].astype(int)):
            bus_rows.append((case, int(bus_id), float(va_deg[i])))
        for k in range(branch.shape[0]):
            branch_rows.append((case, k + 1, int(branch[k, 0]), int(branch[k, 1]), float(pf[k]), float(pt[k])))

    pd.DataFrame(bus_rows, columns=["case", "bus_id", "Va_deg_python"]).to_csv(
        args.output / "python_bus_angles.csv", index=False
    )
    pd.DataFrame(branch_rows, columns=["case", "branch_id", "fbus", "tbus", "Pf_MW_python", "Pt_MW_python"]).to_csv(
        args.output / "python_branch_flows.csv", index=False
    )
    print(f"Wrote Python DC reference for {len(CASES)} MATPOWER cases to {args.output}")


if __name__ == "__main__":
    main()
