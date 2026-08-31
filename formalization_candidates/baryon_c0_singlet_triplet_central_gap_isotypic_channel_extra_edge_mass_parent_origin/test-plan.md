# Test plan

1. Verify the predecessor's `next_gate` token.
2. Construct the three exact Hermitian edge blocks.
3. Compute their physical half-traces symbolically.
4. Verify the unweighted coefficient vector `(2,3,3)`.
5. Exhibit two positive central traces with non-proportional vectors.
6. Compute the exact gauge-index matrix, determinant, and rank.
7. Solve the gauge reconstruction of the unweighted vector.
8. Verify pairwise inequivalence of the three representations.
9. Reject every SymPy `Float`.