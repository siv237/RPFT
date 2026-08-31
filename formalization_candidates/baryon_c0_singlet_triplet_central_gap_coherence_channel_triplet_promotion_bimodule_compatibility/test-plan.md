# Test plan

1. Verify that the predecessor names this gate.
2. Solve `[A,P_Y]=0` on a general complex `3x3` matrix.
3. Restrict to real skew matrices and compute the surviving Lie algebra.
4. Test every standard `so(3)` generator against `P_Y`.
5. Test standard `A4` generators against `P_Y`.
6. Verify the nontrivial action of the `Spin(3)` center on the `2+1` block.
7. Add one isotypic endpoint and recompute the commutant.
8. Verify the selected `1-6-3` chain and the full eight-dimensional edge
   carrier.
9. Reject every SymPy `Float`.