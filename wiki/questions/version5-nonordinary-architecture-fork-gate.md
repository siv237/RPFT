# Version V nonordinary architecture fork

> Status: working
> Type: question
> Updated: 2026-08-15

## Problem

After ordinary `Spec(D^2)` was proved blind to the incoming/outgoing
decomposition, which genuinely orientation-sensitive architecture deserves
the next finite kill-test?

## Anti-circle ledger

The following current realizations remain closed:

- ordinary mapping-cone curvature selects only the endpoint product;
- real and standard BV auxiliaries have the wrong role or sign;
- the computed KO6 Gaussian/Pfaffian measure still depends on the Gram sum;
- the current boundary common trace does not exist.

Twisted spectral calculus and derived/BV--BFV geometry are genuine open
classes, but neither currently computes the project family moment map.
Relative modular functionals provide asymmetry, but their positive
information Hessian does not automatically supply the required quiver
difference.

## Selected minimal architecture

Reuse the existing integer height

`h=diag(-I3,0,I3)`

on the three-node chain. If `D=d+ddagger` and both forward arrows raise
height by one, then

`d=(D+[h,D])/2`.

The zero-height-node projector is not fitted independently:

`P_G=I-h^2=diag(0,I3,0)`.

Therefore

`S_hH=(1/3) Tr_H(P_G [d,ddagger]^2)`

is exactly

`tau3((XXdagger-YdaggerY)^2)`.

Global reversal `h -> -h` exchanges `d` and `ddagger` but leaves the action
unchanged. The selector `I-h^2` is the unique affine polynomial in `h^2`
that equals one on height zero and zero on heights `+/-1`.

## Why this is new

The failed mapping-cone action projected the even curvature
`(d+ddagger)^2` and retained an endpoint composition. The new candidate
uses the oriented Hodge commutator, which is already block diagonal, and
then selects its unique middle block. It changes the curvature primitive,
not merely its notation.

## Verdict

- exact oriented algebraic target: pass;
- coefficient-free height selector: pass;
- reuse of the existing family chain: pass;
- unique origin of height and trace in the full KO6 geometry: not passed;
- physical closure: not passed.

The selection applies only to the next kill-test. Twisted and derived
architectures are deferred, not disproved.

The completed [[version5-oriented-height-hodge-ko6-gate]] finds two
inequivalent admissible heights. The coherent orientation is therefore not
derived by the existing KO6 data, and the route closes at parent level.

## Links

- [[version5-ordinary-spectral-moment-map-no-go-gate]]
- [[version5-oriented-height-hodge-ko6-gate]]
- [[version4-family-defect-relative-auxiliary-moment-gate]]
- [[version4-family-defect-degree-two-junk-gate]]
- [[version5-foundational-relative-architecture-gate]]
- [[version5-project-literature-novelty-gate]]

## Source Notes

- `s2t/gates/version5_nonordinary_architecture_fork_gate.tex`
- `s2t/audits/s2t_v5_nonordinary_architecture_fork_gate.py`
- `s2t/results/s2t_v5_nonordinary_architecture_fork_gate_results.json`
- Twisted spectral triples: `arXiv:1411.1320`.
- Noncommutative derived Poisson reduction: `arXiv:2012.04451`.
- Derived symplectic reduction/BV--BFV: `arXiv:2106.06625`,
  `arXiv:1905.08047`.
- Noncommutative quiver moment maps: `arXiv:math/0502301`.