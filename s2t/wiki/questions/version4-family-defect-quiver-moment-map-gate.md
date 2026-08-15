# Version IV family-defect quiver moment-map gate

## Question

Can the pairing norm-locking ratio `1:-2/3:1/9` arise from one finite curvature trace, and does the resulting normalized action retain a nonzero defect condensate?

## Quiver

- Use a frozen–gauged–frozen chain of three real family triplets.
- `X` is the left-to-middle bifundamental locking field.
- The right arrow is `A4`-equivariant. Since the real `A4` triplet commutant has dimension one, Schur's lemma fixes `Y=Phi I3`.
- The middle-node moment map is `mu=X X^T-|Phi|^2 I3`.

## Exact identity

With `tau3=Tr/3`,

`tau3(mu^2)=(|Phi|^2-tau3(X X^T))^2 + tau3((X X^T-tau3(X X^T)I)^2)`.

The central term has the exact coefficient ratio `1:-2/3:1/9`; the second term is a positive anisotropy penalty.

## Vacuum checks

- Zero-gradient Hessian: `(7+,4zero,0-)`.
- In the normalized unit-momentum radial defect model, the global condensed minimum has `rho=0.7432242844`, `r=0.2288718801`, and energy `0.5395181198`.
- The best normal branch has energy `0.5408201282`.
- The condensed radial Hessian is positive.

## Status

The coefficient ratio and normalized condensate pass in the explicit quiver action. The remaining gate is to embed the frozen/gauged nodes, `B-L` charge, Schur-restricted arrow and normalized middle-node trace into the actual finite KO6/superconnection geometry.

## Files

- `version4_family_defect_quiver_moment_map_gate.tex`
- `s2t_v4_family_defect_quiver_moment_map_gate.py`
- `s2t_v4_family_defect_quiver_moment_map_gate_results.json`