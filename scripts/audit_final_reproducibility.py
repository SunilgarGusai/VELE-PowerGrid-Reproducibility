#!/usr/bin/env python3
"""Independent stdlib-only pre-submission gate for the exact public VELE repository tree.

Does not download source cases, run AC OPF, or modify input files.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "certified_cut_v2"


def rows(path):
    with (ROOT / path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def require_tree():
    tracked = {
        p.decode("utf-8")
        for p in subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
        if p
    }
    assert tracked, "No tracked files found"
    listed = rows("REPOSITORY_MANIFEST.csv")
    inventory = [r["path"] for r in listed]
    assert len(inventory) == len(set(inventory)), "Duplicate manifest path"
    assert set(inventory) == tracked, (
        "Missing from manifest: " + repr(sorted(tracked - set(inventory)))
        + "; stale manifest: " + repr(sorted(set(inventory) - tracked))
    )
    forbidden = (".docx", ".doc", ".tex", ".pdf", ".pptx", ".pwb", ".key", ".pem")
    for path in tracked:
        low = path.lower()
        assert not low.endswith(forbidden), ("Manuscript/secret file in public tree", path)
        assert not low.startswith(("submission/", "manuscript/", "private/", "dist/")), path
    return tracked


def require_document_links(tracked):
    broken = []
    for p in sorted(tracked):
        if not p.endswith(".md"):
            continue
        s = (ROOT / p).read_text(encoding="utf-8")
        refs = re.findall(r"\]\(([^)]+)\)|(?:src|href)=[\"']([^\"']+)[\"']", s)
        for a, b in refs:
            link = (a or b).strip()
            if not link or link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            link = link.split("#", 1)[0].split("?", 1)[0].strip()
            if not link or link.startswith(("data:", "<")):
                continue
            target = (ROOT / p).parent / link
            if not target.exists():
                broken.append((p, link))
    assert not broken, "Broken Markdown/HTML links: " + repr(broken)
    return True


def require_citation_licence():
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert "cff-version: 1.2.0" in cff
    assert "version: \"2.1.0\"" in cff
    assert "v2.1.0-review-freeze" in cff
    assert "preferred-citation:" not in cff, "Unpublished manuscript must not be a published-article citation"
    assert "not" in cff.lower() and "published" in cff.lower()
    licence = (ROOT / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")
    assert "CC BY 4.0" in licence and "MIT" in licence
    assert "v23.07" in licence
    src = json.loads((TABLE / "SOURCE_CASE_SHA256.json").read_text())
    assert len(src) == 4 and all(re.fullmatch("[a-f0-9]{64}", v) for v in src.values())


def require_evidence():
    source = rows("certified_cut_v2/PHASE18_ALL_PHYSICAL_OUTAGES_RIGOROUS_CUT_BOUNDS.csv")
    summary = rows("certified_cut_v2/PHASE18_CUT_BOUND_CASE_SUMMARY.csv")
    witness = rows("certified_cut_v2/PHASE18_EXPLICIT_13_CONNECTED_AC_CUT_CERTIFICATES.csv")
    state = rows("certified_cut_v2/PHASE18_IEEE118_API_CONNECTED_PROVABLE_SHEDDING.csv")
    assert len(source) == 536 and len(summary) == 4 and len(witness) == 13 and len(state) == 13
    counts = Counter(x["condition"] for x in source)
    assert counts == {"ieee57_typ": 81, "ieee57_api": 81, "ieee118_typ": 187, "ieee118_api": 187}, counts
    for name, n in counts.items():
        actual = [int(x["branch_id"]) for x in source if x["condition"] == name]
        assert sorted(actual) == list(range(n)), (name, "missing or duplicate branch ID")
    assert sum(int(x["all_branch_outages"]) for x in summary) == 532
    assert sum(int(x["cut_certified_positive_connected"]) for x in summary) == 13
    assert sum(int(x["cut_certified_positive_all"]) for x in summary) == 24
    heavy = next(x for x in summary if x["condition"] == "ieee118_api")
    assert int(heavy["all_branch_outages"]) == 186 and int(heavy["connected_branch_outages"]) == 177
    assert int(heavy["cut_certified_positive_all"]) == 17 and int(heavy["cut_certified_positive_connected"]) == 13
    zero = {int(x["branch_id"]): float(x["cut_certificate_minimum_shed_MW"])
            for x in witness if x["VELE_delta_zero"] == "True"}
    assert set(zero) == {52, 53, 55, 173}
    for k, rounded in {52: 60.29, 53: 49.29, 55: 15.10, 173: 13.49}.items():
        assert abs(zero[k] - rounded) < 0.005, (k, zero[k])
    lookup = {(x["condition"], int(x["branch_id"])): x for x in source}
    for x in witness:
        k = int(x["branch_id"])
        val = float(x["cut_certificate_minimum_shed_MW"])
        ref = lookup[("ieee118_api", k)]
        assert ref["connected"] == "True"
        assert abs(float(ref["mandatory_shed_lower_bound_MW"]) - val) < 1e-5
        assert val > 0
        assert abs(
            float(x["cut_positive_demand_MW"])
            - float(x["cut_generator_total_Pmax_MW"])
            - float(x["cut_remaining_branch_RATEA_sum_MVA"])
            - val
        ) < 1e-5
    dc = rows("stages/07_branch_outage_validation/outputs/branch_n1_network_summary.csv")
    assert len(dc) == 6 and sum(int(x["branches"]) for x in dc) == 784
    assert sum(int(x["topology_unchanged_outages"]) for x in dc) == 22
    return {"source_rated_states": len(source), "cut_positive_connected": len(witness),
            "source_rated_conditions": len(summary), "historical_MATPOWER_physical_outages": 784}


def require_graphics():
    assets = ROOT / "docs" / "assets" / "v2-figures"
    names = [
        "fig1-validation-design",
        "fig2-certificates-by-source-condition",
        "fig3-branch52-physical-cut",
        "fig4-thirteen-certified-cases",
    ]
    for name in names:
        path = assets / (name + ".svg")
        assert path.is_file(), path
        tree = ET.parse(path)
        assert tree.getroot().tag.endswith("svg")
        body = path.read_text(encoding="utf-8")
        assert "<text " in body and len(body) > 2000
    cut = (assets / "fig3-branch52-physical-cut.svg").read_text(encoding="utf-8")
    assert "60.29 MW" in cut and "2 × 89 MVA" in cut and "REMOVED 52" in cut
    return len(names)


def main():
    tracked = require_tree()
    require_document_links(tracked)
    require_citation_licence()
    evidence = require_evidence()
    evidence["tracked_files_manifested"] = len(tracked)
    evidence["versioned_public_scientific_figures"] = require_graphics()
    print("REVIEW_FREEZE_SOURCE_AUDIT_PASS " + json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    main()
