# Repository submission/review freeze — 3 November 2026

**Status:** final review-scoped public software/data/visual evidence snapshot `v2.1.0-review-freeze` prepared for the AUT Journal of Electrical Engineering submission. **This is not a journal submission or claim of acceptance.**

## Immutable evidence lineage

1. `v1.0.0-submission` — historical original six-system MATPOWER/DC study and reproducibility archive, retained unchanged.
2. `v2.0.0` — original source-rated PGLib-OPF v23.07 cut-bound software/data release with 536 intact/physical-outage records and 13 independently certified connected stressed IEEE118 positive-cut events, retained unchanged. Four connected events have unchanged VELE yet cut bounds of ≥60.29, ≥49.29, ≥15.10 and ≥13.49 MW.
3. `v2.1.0-review-freeze` — final public review package containing the above tracked scripts/results plus four source-traceable SVG visuals, final reviewer navigation, correct unpublished-manuscript citation metadata, release hashes and additional verification. **No new electrical experiment is represented.**

## Scientific and interpretation restrictions

- The eccentricity-based VELE invariant was published in 2025, not introduced in the unpublished manuscript.
- The physical-capacity cut inequality and maximum-flow computations are established necessary-condition tools, not new mathematical algorithms or globally optimal AC OPF.
- The historical 269/784 nonresponse result is a **DC redistribution** statement; it does not by itself certify unavoidable curtailment.
- The separate source-rated PGLib cohort has two network topologies, each under typical and API operating conditions (four conditions, not four independent systems).
- **A zero cut lower bound is inconclusive**, not proof that all demand can be served. Historical nonconverged AC candidate rankings must not be described as validated AC-security AUROCs.
- Original MATPOWER or PGLib cases are not relicensed; benchmark and code terms are distinguished in `THIRD_PARTY_LICENSES.md`.

## Reviewer and manuscript boundary

The public GitHub release must not contain the unpublished manuscript, journal cover letter, personal author declarations or private anonymized review evidence ZIP. The identified/editor-facing manuscript may cite the historical `v2.0.0` core scientific release; the final reproducibility snapshot is `v2.1.0-review-freeze`. The anonymous manuscript must not reveal this author-identifying URL unless the editor authorizes it.

All final journal-specific declarations, author approval, signed forms and explicit final submission authorization remain independent of this repository freeze.

## No-changes-until-review policy

After the final tag is verified:

- **No commits to `main`, release replacement, undocumented scientific re-analysis, visual alteration, new research result or documentation change during initial review.**
- Keep `v1.0.0-submission`, `v2.0.0` and `v2.1.0-review-freeze` tags and original assets intact.
- Make subsequent changes only after an editor/referee request or a verified security/integrity defect, with a documented new release and explicit change log. Do not force-push or rewrite frozen history.
- GitHub repository administrative branch-protection is an optional additional account-owner control; the policy above is a documented procedural freeze and is **not** itself a technical branch lock.

The existence of a public repository does not mean the manuscript itself has been published.
