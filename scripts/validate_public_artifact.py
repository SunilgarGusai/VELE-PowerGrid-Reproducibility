#!/usr/bin/env python3
"""Validate the reviewer-facing VELE repository artifact using only stdlib."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str) -> Path:
    p = ROOT / path
    if not p.exists():
        raise FileNotFoundError(f"Missing required artifact: {path}")
    return p


def validate_manifest() -> int:
    manifest = require("REPOSITORY_MANIFEST.csv")
    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise AssertionError("Repository manifest is empty")
    missing = [row["path"] for row in rows if not (ROOT / row["path"]).exists()]
    if missing:
        raise AssertionError("Manifest paths missing: " + ", ".join(missing))
    return len(rows)


def validate_branch_summary() -> None:
    path = require("stages/07_branch_outage_validation/outputs/branch_n1_network_summary.csv")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6
    assert sum(int(r["branches"]) for r in rows) == 784
    assert sum(int(r["parallel_rows"]) for r in rows) == 22
    assert sum(int(r["topology_unchanged_outages"]) for r in rows) == 22
    assert sum(int(r["disconnection_cases"]) for r in rows) == 114
    assert sum(int(r["secondary_shedding_cases"]) for r in rows) == 47


def validate_matpower_summary() -> None:
    path = require("validation/results/matpower_octave_crosscheck_summary.csv")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected = {
        "case14": (14, 20),
        "case30": (30, 41),
        "case39": (39, 46),
        "case57": (57, 80),
        "case118": (118, 186),
        "case300": (300, 411),
    }
    assert len(rows) == 6
    for row in rows:
        case = row["case"]
        assert case in expected
        assert (int(row["buses"]), int(row["branches"])) == expected[case]
        assert float(row["max_abs_angle_error_deg"]) <= 1e-8
        assert float(row["max_abs_pf_error_MW"]) <= 1e-8
        assert float(row["max_abs_pt_error_MW"]) <= 1e-8


def validate_presentation_assets() -> None:
    for path in (
        "docs/assets/repository-banner.svg",
        "docs/assets/vele-workflow.svg",
        "docs/assets/parallel-circuit-blindspot.svg",
        "docs/METHOD_PROTOCOL.md",
        "docs/FROZEN_RESULTS.md",
        "docs/REPRODUCIBILITY.md",
        "environment.yml",
        "config/study_scope.yml",
    ):
        require(path)


def main() -> None:
    count = validate_manifest()
    validate_branch_summary()
    validate_matpower_summary()
    validate_presentation_assets()
    print(f"PASS: reviewer-facing artifact validated; {count} manifest entries present")


if __name__ == "__main__":
    main()
