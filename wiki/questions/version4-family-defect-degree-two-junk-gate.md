# Version IV family-defect represented degree-two junk gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Question

Does the ordinary Connes two-form quotient of the explicit 18-dimensional KO6 geometry contain the six-dimensional middle `Sym3(R)` curvature required for `mu=XX^T-|Phi|^2 I`?

## Computation

The audit constructs represented one-forms, represented two-forms and `d(ker pi_1)` from the full 12-element real algebra basis. On four generic full-rank backgrounds the complexified ranks are stable:

- represented one-forms: `20`;
- represented two-forms: `20`;
- degree-two junk: `9`;
- quotient: `11`.

The implementation reproduces the existing three-point control in which the length-two endpoint matrix unit is junk.

## Verdict

On the particle half, the middle `M3` image and its junk image both have rank `9`; the quotient middle rank is zero. The full KO6 quotient retains only one central complex direction on the conjugate chain and no traceless-symmetric direction. Therefore neither `Sym3,0(R)` nor the full `Sym3(R)` auxiliary module survives.

At radial `X=rho I` backgrounds the calculus rank jumps because commutators degenerate. This singular-locus enlargement cannot derive an off-shell shape-locking potential.

## Remaining path

The ordinary degree-two route is closed. The only current route is an imaginary Hubbard–Stratonovich representation derived from the KO6 fermionic determinant/Pfaffian measure. Otherwise the project needs a modified differential calculus or a new finite carrier.

## Files

- `s2t/gates/version4_family_defect_degree_two_junk_gate.tex`
- `s2t/audits/s2t_v4_family_defect_degree_two_junk_gate.py`
- `s2t/results/s2t_v4_family_defect_degree_two_junk_gate_results.json`