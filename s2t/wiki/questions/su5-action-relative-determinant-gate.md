# SU5 Action and Relative Determinant Gate

## Gate I: canonical action

A single SU(5) trace gives `kY=5/3`, `sin2(thetaW)=3/8`, and equal adjoint
subgroup indices `(5,5,5)`. Gauge actions use Dynkin indices rather than raw
representation dimensions.

For one mixed `(3,2)_{5/6}` block the indices are `(5/2,3/2,1)`; for the
charge-conjugate pair they are `(5,3,2)`. These are not the rank data
`(6,6/24)` used by the atlas selector.

Functions of the torsion involution and `ad(Y)^2` cannot distinguish the
unbroken `C,W,Y` blocks. Explicit block projectors reintroduce independent
sector weights.

## Gate II: relative determinant

Only `X/Xbar` change between trivial and torsion-twisted branches, so every
minimal adjoint relative determinant lies on the ray

`Delta alpha_inverse = A_rel (5,3,2)`.

The required gauge repair is `(0.3680,-0.3680,-2.4592)`. The positive ray has
100% relative residual. Even allowing an arbitrary overall sign leaves a
96.3% relative L2 residual.

## Verdict

The rank selector remains an economical spectral-address encoding, and the
relative determinant remains a finite scheme-safe topology response. Neither
is a derivation of the current low-energy gauge observables.

## Evidence

- `s2t_su5_rank_action_gate_audit.py`
- `s2t_su5_rank_action_gate_results.json`
- `s2t_su5_adjoint_relative_determinant_audit.py`
- `s2t_su5_adjoint_relative_determinant_results.json`
- `su5_action_relative_determinant_gate.tex`