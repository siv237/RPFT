# Pati-Salam Three-Node Parent Graph Gate

> Status: corrected to equivariant-carrier pass
> Type: question
> Updated: 2026-08-14

## Problem

The project had an exact rank-one repair
`4 det(Delta Delta^dagger)`, but its direct-minus-crossed relative sign had
not been derived from one admissible finite graph.

## Search for Solution

A three-node graded chain was tested:

`C -> C2 tensor C4 -> Lambda2(C2) tensor Lambda2(C4)`.

The first edge is `vec(Delta)`. The second is the polarization of the
exterior-square map. Their composition is `Lambda2 Delta`, so its squared
norm is exactly `det(Delta Delta^dagger)`.

## Result

For relative edge normalization `c`, the particle trace is

`Tr D^4 = (2+3c^4/8) rho^2 + (4c^2-c^4/2) det`.

The determinant coefficient is positive throughout `0<c^2<8`; therefore
the mechanism is robust rather than tied to one fitted coefficient. At the
canonical value `c=1`, the raw half-trace potential has:

- rank-one norm squared `14/19` and energy `-49/38`;
- rank-two equal-singular-value energy `-49/52`;
- Hessian spectrum `14 (1), 0 (9), 98/19 (6)`.

The KO6 doubled chain passes self-adjointness, grading and reality. Coarse
labels `(0,0)->(0,1)->(1,1)` make each fundamental edge change only one
label, but this is only a necessary combinatorial test.

## Associative-Algebra Correction

The endpoint modules do not exist over the unchanged Pati-Salam algebra.
`M4(C)` has fundamental module dimension four, and all its finite modules
have dimensions divisible by four; the `SU(4)` color six is a group/Lie
representation but not an associative `M4(C)` module. The construction is
therefore an equivariant superconnection carrier, not a strict Krajewski
finite triple.

## Remaining Gap

The trace identity and rank selector remain valid. The next gate must realize
the wedge component as a represented universal two-form or curvature block
inside the existing 32-dimensional Pati-Salam Hilbert module and determine
its survival after the degree-two junk quotient.

## Links

- [[pati-salam-rank-selector-archaeology]]
- [[pati-salam-wedge-channel-compatibility-gate]]
- [[project-success-tree-2026-08-11]]
- [[pati-salam-associative-node-no-go]]

## Source Notes

- `s2t/gates/version4_pati_salam_three_node_parent_graph_gate.tex`
- `s2t/audits/s2t_v4_pati_salam_three_node_parent_graph.py`
- `s2t/results/s2t_v4_pati_salam_three_node_parent_graph_results.json`
- T. Krajewski, arXiv:hep-th/9701081.
- T. Krajewski, arXiv:hep-th/9803199.
- A. H. Chamseddine and A. Connes, arXiv:hep-th/9606001.