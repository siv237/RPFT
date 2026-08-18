# Version V real selector-leaf KO6 gate

> Status: working
> Type: question
> Updated: 2026-08-15

## Question

Can a pendant `M3(R)` node constrain the arbitrary family matrix on an
existing Krajewski square?

## Exact result

No. First-order equations decompose by Dirac block. The leaf changes its own
block `D_AE` but does not enter the equation for the cycle block `D_AB`.
The family freedom on that edge remains nine-dimensional before and after
adding the leaf.

The leaf placements themselves pass the row/column rule and can be completed
under the real structure. The failure is their selector function.

## Important correction

If `M3(R)` is promoted from passive family multiplicity to a common algebra
coordinate of two adjacent rectangle nodes, Schur commutation reduces the
edge commutant from dimension nine to one:

`End_M3(R)(R3) = R I3`.

This is a four-node active-family rectangle, not a five-node selector leaf.
It was not tested by the earlier square gate, which assumed passive family
multiplicity.

## Verdict

- selector-leaf geometry: closed;
- graph enumeration: retained;
- active-family rectangle: admitted for one gate;
- parent architecture and physical closure: not passed.

## Next gate

[[version5-family-algebra-rectangle-gate]] constructs the minimal particle
block and closes its ordinary spectral dynamics: the family commutant becomes
scalar, but the global vacuum has zero triplet connectors and leaves the
family gauge sector unbroken.

## Links

- [[version5-finite-geometry-complexity-bound-gate]]
- [[version4-order-one-krajewski-square-gate]]
- [[version4-family-defect-ko6-quiver-embedding-gate]]

## Source Notes

- `s2t/gates/version5_real_selector_leaf_ko6_gate.tex`
- `s2t/audits/s2t_v5_real_selector_leaf_ko6_gate.py`
- `s2t/results/s2t_v5_real_selector_leaf_ko6_gate_results.json`
- Blockwise Krajewski structure: `arXiv:hep-th/9701081` and
  `arXiv:2207.04466`.