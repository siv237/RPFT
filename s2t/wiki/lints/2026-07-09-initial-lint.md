# Initial Wiki Lint

> Status: working
> Type: lint
> Updated: 2026-07-09

## Summary

Initial structure is coherent but shallow. The wiki now has navigation, concept pages, source stubs, a synthesis layer, and a first tracked research question. It still needs source-level ingestion of the main TeX papers and JSON audit files.

## Findings

- No orphan problem yet: all initial pages are linked through `wiki/index.md`.
- Most pages are based on `RESEARCH_CATALOG.md` and filename-level inspection, not full source extraction.
- The concept [[spectral-correlational-source]] is central but still underdefined.
- JSON audit files are listed but not yet interpreted.
- `RPFT-main/` is too large for a single page and should be ingested branch by branch.

## Recommended Next Ingests

1. `toe_ugsm_unified_shadow_paper.tex`
2. `toe_ugsm_shadow_audit_report.tex`
3. `tome2_s2t_spectral_closure.tex`
4. `spectral_bridge_results.json` and related audit files
5. `RPFT-main/rigorous/00_main.md` plus `RPFT-main/rigorous/README.md`

## Links

- [[project-overview]]
- [[toe-ugsm-unified-shadow-paper]]
- [[numerical-audits]]