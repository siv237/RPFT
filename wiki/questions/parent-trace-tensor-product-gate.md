# Parent Trace Tensor Product Gate

> Status: working
> Research status: algebraic pass; action-level coefficient open
> Type: question
> Updated: 2026-08-04

## Parent Algebra

```text
H_parent = C4_menu tensor (10+bar5),
dim H_parent = 60,
A_parent = M60(C).
```

`M60(C)` has a unique normalized trace. The physical family-triplet projector has rank `45`, and its corner algebra is `M45(C)`, again with a unique normalized trace.

## Joint Results

- Heavy-family projector rank: `15` inside rank `45`.
- Conditional heavy-family weight: `15/45=1/3`.
- Per-generation normalized gauge indices: `(2,2,2)`.
- Three-family loop indices: `(6,6,6)`.
- Relative trace parameters: `0`.

The `1/3` here is not the old tau coefficient. It is the exact fraction of the rank-one heavy-family channel inside the physical three-family matter space.

## Verdict

One parent matrix trace consistently supports both SU5 gauge normalization and the family rank-one operator. Different effective measures are fixed reductions, not independent sector choices.

## Open Gate

Trace unity is not action unity. The next audit must construct the most general `SU5 x AGL(2,2)`-invariant action and determine whether the family-breaking term has a fixed coefficient or introduces a new continuous coupling.

## Evidence

- `s2t/audits/s2t_parent_trace_tensor_product_audit.py`
- `s2t/results/s2t_parent_trace_tensor_product_results.json`
- `s2t/gates/parent_trace_tensor_product_gate.tex`
