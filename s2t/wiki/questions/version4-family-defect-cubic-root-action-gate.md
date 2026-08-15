# Version IV family-defect cubic-root action gate

## Question

Can the connection selected in the family-defect holonomy gate be derived by varying one positive action, rather than imposed as a constitutive ansatz?

## Construction

- Use the projector curvature `Q(H)=H^2-H/sqrt(3)-I/4`.
- In a fixed nonzero unit-winding sector write `z=Phi/|Phi|=exp(i phi)`.
- Define the cubic-root frame `W=exp[(phi/3) Omega(H)]`.
- Its transition is `Z=exp[(2 pi nu/3) Omega(H)]`, with `Z^3=I`.
- Vary the common-trace action `S=int [L^-1 Tr Q(H)^2 + L Tr((D W)^T D W)]`.

## Result

Variation over the skew connection gives

`A_s=-partial_s W W^T=-(partial_s phi/3) Omega(H)`.

For every projector and both winding signs the integrated holonomy is the required three-cycle. The result is independent of the local phase profile. The connection Hessian is positive with six eigenvalues equal to two in the orthonormal skew basis.

## Evidence

- 16 projector/winding/profile cases checked.
- Maximum covariant-derivative residual: `5.53e-16`.
- Maximum `Z^3-I` residual: `5.04e-15`.
- Maximum holonomy residual: `3.68e-15`.
- Minimum connection Hessian eigenvalue: `2-5e-16`.

## Status

The constitutive-action gate passes inside the fixed condensed unit-winding sector. The remaining parent gap is to derive the nonzero condensate, the cubic-root bundle, and its embedding into the finite graded superconnection rather than assume them as boundary data.

## Files

- `version4_family_defect_cubic_root_action_gate.tex`
- `s2t_v4_family_defect_cubic_root_action_gate.py`
- `s2t_v4_family_defect_cubic_root_action_gate_results.json`