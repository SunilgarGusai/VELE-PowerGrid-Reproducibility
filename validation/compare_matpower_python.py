#!/usr/bin/env python3
"""Compare executable MATPOWER 8.1 results with independent NumPy DC results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--python-dir", required=True, type=Path)
    ap.add_argument("--matpower-dir", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--angle-tol", type=float, default=1e-8)
    ap.add_argument("--flow-tol", type=float, default=1e-8)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    pyb = pd.read_csv(args.python_dir / "python_bus_angles.csv")
    mpb = pd.read_csv(args.matpower_dir / "matpower_bus_angles.csv")
    pyr = pd.read_csv(args.python_dir / "python_branch_flows.csv")
    mpr = pd.read_csv(args.matpower_dir / "matpower_branch_flows.csv")

    b = pyb.merge(mpb, on=["case", "bus_id"], how="outer", validate="one_to_one", indicator=True)
    r = pyr.merge(mpr, on=["case", "branch_id", "fbus", "tbus"], how="outer", validate="one_to_one", indicator=True)
    if not (b["_merge"] == "both").all():
        raise SystemExit("Bus-key mismatch between Python and MATPOWER outputs")
    if not (r["_merge"] == "both").all():
        raise SystemExit("Branch-key mismatch between Python and MATPOWER outputs")

    b["abs_angle_error_deg"] = np.abs(b["Va_deg_python"] - b["Va_deg_matpower"])
    r["abs_pf_error_MW"] = np.abs(r["Pf_MW_python"] - r["Pf_MW_matpower"])
    r["abs_pt_error_MW"] = np.abs(r["Pt_MW_python"] - r["Pt_MW_matpower"])

    rows = []
    for case in sorted(b["case"].unique(), key=lambda x: int(x.replace("case", ""))):
        bb = b[b["case"] == case]
        rr = r[r["case"] == case]
        rows.append({
            "case": case,
            "buses": int(len(bb)),
            "branches": int(len(rr)),
            "max_abs_angle_error_deg": float(bb["abs_angle_error_deg"].max()),
            "max_abs_pf_error_MW": float(rr["abs_pf_error_MW"].max()),
            "max_abs_pt_error_MW": float(rr["abs_pt_error_MW"].max()),
        })

    summary = pd.DataFrame(rows)
    summary.to_csv(args.output / "matpower_octave_crosscheck_summary.csv", index=False)
    b.drop(columns=["_merge"]).to_csv(args.output / "bus_angle_comparison.csv", index=False)
    r.drop(columns=["_merge"]).to_csv(args.output / "branch_flow_comparison.csv", index=False)

    max_angle = float(summary["max_abs_angle_error_deg"].max())
    max_pf = float(summary["max_abs_pf_error_MW"].max())
    max_pt = float(summary["max_abs_pt_error_MW"].max())
    passed = max_angle <= args.angle_tol and max(max_pf, max_pt) <= args.flow_tol

    record = {
        "passed": bool(passed),
        "angle_tolerance_deg": args.angle_tol,
        "flow_tolerance_MW": args.flow_tol,
        "max_abs_angle_error_deg": max_angle,
        "max_abs_pf_error_MW": max_pf,
        "max_abs_pt_error_MW": max_pt,
        "cases": rows,
    }
    (args.output / "validation_result.json").write_text(json.dumps(record, indent=2) + "\n")

    report = [
        "# MATPOWER 8.1 / GNU Octave executable cross-check",
        "",
        f"**Status:** {'PASS' if passed else 'FAIL'}",
        "",
        f"- Maximum absolute bus-angle difference: `{max_angle:.6e}` deg",
        f"- Maximum absolute from-end branch-flow difference: `{max_pf:.6e}` MW",
        f"- Maximum absolute to-end branch-flow difference: `{max_pt:.6e}` MW",
        f"- Angle tolerance: `{args.angle_tol:.1e}` deg",
        f"- Flow tolerance: `{args.flow_tol:.1e}` MW",
        "",
        "| Case | buses | branches | max |Δθ| (deg) | max |ΔPf| (MW) | max |ΔPt| (MW) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        report.append(
            f"| {row['case']} | {row['buses']} | {row['branches']} | "
            f"{row['max_abs_angle_error_deg']:.3e} | {row['max_abs_pf_error_MW']:.3e} | {row['max_abs_pt_error_MW']:.3e} |"
        )
    report.append("")
    (args.output / "MATPOWER_OCTAVE_VALIDATION_REPORT.md").write_text("\n".join(report))
    print("\n".join(report))

    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
