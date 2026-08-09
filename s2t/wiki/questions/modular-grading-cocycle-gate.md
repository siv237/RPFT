# Modular Grading and CP Cocycle Gate

## Result

The modular spectrum selects the three-level chain `A3` and, up to an overall
sign, its unique grading

`Gamma = diag(1,-1,1)`.

Both chain edges are grading-odd. Since `A3` is a tree, its first edge
cohomology is trivial: all edge phases are removable by vertex rephasing and
cannot produce physical CP violation.

## Minimal Cycle Obstruction

Adding the direct `0 <-> 2` chord creates one gauge-invariant flux `Phi` and
an auxiliary CP-odd invariant proportional to `sin(Phi)`. The chord commutes
with `Gamma`, however, and is grading-even. A triangle is not bipartite, so
all three of its edges cannot be the odd part of one Dirac operator.

The result is therefore structural rather than phenomenological:

- the `A3` tree explains why the original common connection has zero CP;
- a cycle is necessary for a physical flux;
- the minimal triangle cannot be an entirely odd graded Dirac graph;
- reopening requires an enlarged graded space or a separate even curvature
  layer derived from a parent action.

## Next Gate

Classify minimal bipartite lifts, beginning with a four-cycle `C4`, that reduce
to three observable family modes without introducing fitted continuous
coefficients.

## Evidence

- `s2t_modular_grading_cocycle_audit.py`
- `s2t_modular_grading_cocycle_results.json`
- `modular_grading_cocycle_gate.tex`
