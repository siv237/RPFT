# Version IV family-defect relative/auxiliary moment gate

## Question

Can the required middle-node square be obtained canonically from mapping-cone curvature or an auxiliary field without changing the kinetic trace normalization?

## Negative routes

- The canonical mapping-cone norm of `(d+d†)^2` selects the endpoint composition and equals `2 |Phi|^2 Tr(XX^T)`; it has no pure quartics.
- The required `mu=XX^T-|Phi|^2 I` is symmetric, while the strict `SO(3)` adjoint is skew-symmetric, so its adjoint projection vanishes.
- Therefore the square is neither the previous Pati–Salam mapping-cone mechanism nor an ordinary `SO(3)` D-term.

## Sign correction

The self-adjoint part `Sym3(R)` gives the exact algebraic identity

`tau3(mu^2) = sup_K [2 tau3(K mu)-tau3(K^2)]`.

But `K=mu` is a strict maximum: the six Hessian eigenvalues are `-2/3`. A positive real Euclidean auxiliary instead gives `-tau3(mu^2)`, the wrong sign. The correct positive quartic can be represented only with an imaginary Hubbard–Stratonovich coupling and complex saddle `K=-i mu`.

Moreover `Sym3(R)=1+5` under `SO(3)`, so invariant metrics have two weights. Symmetry alone does not derive the normalized matrix trace.

## Remaining gate

Compute the represented degree-two quotient. If `Sym3(R)` does not survive, derive the imaginary HS contour and its determinant/Pfaffian measure from the KO6 fermionic integral. Until then there is no classical parent-action pass.

## Files

- `version4_family_defect_relative_auxiliary_moment_gate.tex`
- `s2t_v4_family_defect_relative_auxiliary_moment_gate.py`
- `s2t_v4_family_defect_relative_auxiliary_moment_gate_results.json`