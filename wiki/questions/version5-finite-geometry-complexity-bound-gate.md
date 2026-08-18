# Version V finite-geometry complexity-bound gate

> Status: working
> Type: question
> Updated: 2026-08-15

## Result

The standard KO6 search is bounded by five algebra summands, matrix size
four, five particle nodes, six edges, Hilbert dimension 64 and cycle rank
one. The raw algebra menu contains at most 6,187 multisets.

Connected bipartite graph counts are `1,3,5` for three, four and five
vertices. The unique new five-node one-cycle graph is
`K2,3 minus one edge`, a square with a pendant leaf.

This is only a provisional graph selection. The leaf must still prove that
it constrains a cycle edge under the blockwise first-order condition.

## Follow-up

[[version5-real-selector-leaf-ko6-gate]] shows that it does not. The graph
enumeration remains correct, but the selector interpretation fails.

## Links

- [[version5-boundary-parent-trace-freeze-gate]]
- [[version4-order-one-krajewski-square-gate]]
- [[family-bipartite-c4-lift-gate]]

## Source Notes

- `s2t/gates/version5_finite_geometry_complexity_bound_gate.tex`
- `s2t/audits/s2t_v5_finite_geometry_complexity_bound_gate.py`
- `s2t/results/s2t_v5_finite_geometry_complexity_bound_gate_results.json`