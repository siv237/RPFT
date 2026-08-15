# Pati-Salam Associative-Node No-Go

> Status: closed literal-node route
> Type: question
> Updated: 2026-08-14

## Problem

The exterior-square chain had the correct determinant selector, but its
one-dimensional and color-six endpoints had only passed a coarse label test.
They still had to be representations of the actual associative algebra
`H_R direct_sum H_L direct_sum M4(C)`.

## Search for Solution

The exterior-square action was tested at three levels:

1. as a `GL(4)` group representation;
2. as the derived `gl(4)` Lie-algebra representation;
3. as a candidate unital complex-linear representation of `M4(C)`.

The project module ledger was then compared with the proposed node
dimensions.

## Result

- `Lambda2(AB)=Lambda2(A)Lambda2(B)` passes at `10^-14`.
- The derived map preserves Lie commutators at `10^-14`.
- The wedge edge is exactly `SU(2)_R x SU(4)` equivariant.
- `Lambda2` fails additivity and scalar linearity as a map on `M4(C)`.
- Its derivative fails associative multiplication and sends `I4` to `2 I6`.
- Every nontrivial `M4(C)` module has dimension divisible by four, so an
  irreducible color-six fermion node is unavailable.
- The color six remains valid as the scalar channel `(1_R,6_4)` inside the
  existing symmetric Majorana block.

## Verdict

The three-node construction is a valid equivariant superconnection carrier,
not a strict Krajewski finite triple over the unchanged Pati-Salam algebra.
The determinant mechanism survives, but it must be realized as a represented
universal two-form or curvature component on the existing 32-dimensional
Hilbert module after quotienting degree-two junk.

## Links

- [[pati-salam-three-node-parent-graph-gate]]
- [[pati-salam-wedge-channel-compatibility-gate]]
- [[pati-salam-rank-selector-archaeology]]
- [[project-success-tree-2026-08-11]]

## Source Notes

- `s2t/gates/version4_pati_salam_associative_node_no_go.tex`
- `s2t/audits/s2t_v4_pati_salam_associative_node_no_go.py`
- `s2t/results/s2t_v4_pati_salam_associative_node_no_go_results.json`
- T. Krajewski, arXiv:hep-th/9701081 and hep-th/9803199.
- A. H. Chamseddine and W. D. van Suijlekom, arXiv:1304.7583.
- A. H. Chamseddine, A. Connes and W. D. van Suijlekom, arXiv:1304.8050.