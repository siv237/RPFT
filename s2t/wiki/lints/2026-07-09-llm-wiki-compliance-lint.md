# LLM Wiki Compliance Lint

> Status: working
> Type: lint
> Updated: 2026-07-09

## Summary

The wiki now better matches the `llm-wiki.md` pattern: it has persistent synthesis pages, concrete source pages, tracked open questions, cross-links, and an append-only log. The main remaining weakness is that several TeX sources are still represented at filename or roadmap level rather than fully ingested.

## Checks

- Page format is consistent: non-log wiki pages include `Status`, `Type`, and `Updated` metadata.
- Obsidian links resolve across the wiki; no missing `double-bracket` targets were found in the validation pass.
- The numerical-audit page now contains extracted metrics instead of only listing JSON filenames.
- Major proof gaps are promoted from prose notes into tracked pages: [[neutrino-overlap-lemma]] and [[ew-qcd-threshold-closure]].
- The index now exposes core syntheses, concepts, source pages, open questions, and maintenance passes.

## Remaining Weaknesses

- `tome2_s2t_spectral_closure.tex` still needs full source-level ingest.
- `toe_ugsm_unified_shadow_paper.tex` remains the main bridge source but is still summarized at a high level.
- `RPFT-main/rigorous/` should be split into source pages for the strict derivations that support `K`, the `π` term, radius stabilization, and QED one-loop anchoring.
- The wiki has audit evidence but does not yet contain enough analytic derivation to close neutrino overlap or EW/QCD thresholds.

## Recommended Next Actions

1. Ingest `tome2_s2t_spectral_closure.tex` in detail.
2. Create source pages for the strict RPFT files named in [[s2t-closure-roadmap]].
3. Add a reproducible threshold-audit result file before changing EW/QCD status from open.
4. If a neutrino-overlap derivation appears, update [[neutrino-overlap-lemma]], [[holonomy-and-dirac-sectors]], and [[s2t-closure-roadmap]] in the same edit.

## Links

- [[s2t-closure-roadmap]]
- [[numerical-audits]]
- [[neutrino-overlap-lemma]]
- [[ew-qcd-threshold-closure]]