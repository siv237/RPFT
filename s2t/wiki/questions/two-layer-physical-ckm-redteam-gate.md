# Two-Layer Physical CKM Red-Team Gate

## Correction

The physical CKM test is built from the squared-mass operators

`H_u = M_u M_u^dagger`, `H_d = M_d M_d^dagger`,

not only from the auxiliary commutator of the Hermitian texture matrices. For
the scaled two-layer ansatz the exact invariant is

`Tr([H_u,H_d]^3) = 192 i p^2 q (2p^2-15)(q^2-15)(q^2+1) sin(Phi)`.

It is nonzero at the blind weights `p=1`, `q=2`, but it has the additional
degeneracy zeros `p^2=15/2` and `q^2=15` required by the squared-mass
spectrum.

## Independent Controls

- exact symbolic derivation agrees with the closed formula;
- the Jarlskog determinant identity is satisfied numerically;
- eigendecomposition of `H_f` and direct SVD of `M_f` agree;
- common diagonal rephasing leaves absolute mixing and `J` invariant;
- `Phi -> -Phi` preserves absolute mixing and reverses the sign of `J`;
- 25 deterministic random parameter points reproduce the exact invariant.

## Blind Verdict

At the inherited flux and blind weights the texture predicts large,
nonhierarchical mixing angles and `J approximately 0.051`. The physical CKM
texture therefore fails even though the CP mechanism itself is nonzero.

Allowing a common fitted odd-edge weight does not repair the hierarchy: it
keeps the first two mixing angles nearly equal. Unequal odd-edge metrics are
necessary and must be derived before data comparison.

## Grading Verdict

The chain is grading-odd while the chord is grading-even. The present ansatz
is not yet an odd Quillen superconnection on the unchanged three-state
grading. The next admissible construction is a bipartite lift or a separately
derived even curvature layer.

## Evidence

- `s2t_two_layer_physical_ckm_redteam_audit.py`
- `s2t_two_layer_physical_ckm_redteam_results.json`
- `two_layer_physical_ckm_redteam_gate.tex`
