# Version V family-algebra rectangle gate

> Status: working
> Type: question
> Updated: 2026-08-15

## Construction

Promoting family `M3(R)` from multiplicity to an algebra coordinate gives
the structured off-diagonal block

`M=(y I3,w;v^T,z)` in block notation,

with two scalar edges and two family-triplet connectors. The arbitrary
family matrix is eliminated and a genuine loop-orientation term appears in
`Tr D4`.

## Exact vacuum result

The ordinary potential satisfies

`V = 2 lambda Tr(M Mdagger - r2 I4)^2 + constant`.

Its global minima require `M Mdagger=r2 I4`. The upper-left block is a
scalar matrix plus the rank-one matrix `w wdagger`, forcing `w=0`.
The remaining equations then force `v=0` and `|y|=|z|=r`.

At normalized parameters the Hessian spectrum is

`0 x3, 16 x4, 48`.

The three flat directions obey `v=-w` and have positive quartic rise
`4 t4`, so they do not condense.

## Verdict

- active-family order-one rectangle: pass;
- scalar family commutant: pass;
- loop-sensitive quartic: pass;
- family-triplet condensation: fail;
- family gauge breaking: fail;
- standard finite-geometry route inside the frozen budget: closed.

## Next gate

Before comparing new categories, the ordinary spectral obstruction is made
global in [[version5-ordinary-spectral-moment-map-no-go-gate]]. That theorem
closes every functional of `Spec(D^2)`, not only this rectangle potential.
The following `version5_nonordinary_architecture_fork_gate` must compare
relative curvature, twisted calculus, auxiliary moment-map and nonlocal
boundary architectures as explicitly new categories.

## Links

- [[version5-real-selector-leaf-ko6-gate]]
- [[version5-ordinary-spectral-moment-map-no-go-gate]]
- [[version4-family-defect-ko6-quiver-embedding-gate]]
- [[version4-family-defect-quiver-moment-map-gate]]

## Source Notes

- `s2t/gates/version5_family_algebra_rectangle_gate.tex`
- `s2t/audits/s2t_v5_family_algebra_rectangle_gate.py`
- `s2t/results/s2t_v5_family_algebra_rectangle_gate_results.json`