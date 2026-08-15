# Pati-Salam Junk and Mapping-Cone Gate

> Status: working
> Research status: conditional pass with ordinary-junk no-go
> Type: question
> Updated: 2026-08-14

## Problem

The projected-curvature recovery still selected the endpoint block and used
the canonical-looking normalization `c=1`. The task was to determine whether
both facts follow from one parent construction.

## Search for Solution

Three mechanisms were tested separately:

1. the represented universal differential calculus on the minimal
   three-node path;
2. the reflection/reality relation between the two Delta edges;
3. the unique reflection-odd graph-Laplacian mode of the path `P3`.

## Result

- The map `Delta -> Delta^T epsilon_2` is a Frobenius isometry. A single
  reflection/reality-invariant trace-Hodge metric fixes `|c|=1`, and endpoint
  rephasing fixes `c=1`.
- In the minimal `C^3` node calculus, represented one-forms have rank 4,
  represented two-forms rank 5 and degree-two junk rank 2.
- Both endpoint matrix units `E_02` and `E_20` lie in the junk. Standard junk
  therefore removes rather than selects the desired length-two path.
- The path Laplacian has a unique lowest reflection-odd mode. With endpoint
  gap normalization it is `h=(-1,0,1)`.
- The relative derivative `delta_h(F)=[h,F]/2` kills diagonal backtracking
  curvature and retains exactly the endpoint curvature.
- Consequently
  `||delta_h(D_Delta^2)||^2=4 det(Delta Delta^dagger)` at the now-derived
  normalization `c=1`.
- Three hundred random tests pass at `10^-12` or better.

## Verdict

The normalization and projector are no longer arbitrary inside a declared
relative mapping-cone geometry. However, the ordinary spectral curvature
norm remains rank-blind, and the ordinary junk quotient does not provide the
selector. The remaining parent-action question is why the physical bosonic
functional is the relative norm `||delta_h(F)||^2` rather than the full norm
`||F||^2`.

## Links

- [[pati-salam-projected-curvature-selector-gate]]
- [[pati-salam-twoform-a2-trilemma-gate]]
- [[pati-salam-rank-selector-archaeology]]
- [[project-success-tree-2026-08-11]]

## Source Notes

- `s2t/gates/version4_pati_salam_junk_mapping_cone_gate.tex`
- `s2t/audits/s2t_v4_pati_salam_junk_mapping_cone_gate.py`
- `s2t/results/s2t_v4_pati_salam_junk_mapping_cone_gate_results.json`
- T. Schuecker, arXiv:hep-th/9312186.
- G. Roepstorff, arXiv:hep-th/9801040.
- M. Requardt, arXiv:math-ph/0001026.