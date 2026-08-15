# Pati-Salam Tensor-Product Coefficient Gate

> Status: threshold saturation
> Type: question
> Updated: 2026-08-14

## Canonical Coefficient

For the graded product
`D_x=D1 tensor I + Gamma1 tensor D2`, anticommutation gives
`D_x^2=D1^2 tensor I + I tensor D2^2`. Hence the mixed contribution to
`(1/2)Tr(D_x^4)` is exactly `Tr(D1^2)Tr(D2^2)`.

Odd self-adjoint completions satisfy `Tr(D_i^2)=2||M_i||^2`, so the
canonical mixed coefficient is `c=4`. KO6 particle-conjugate doubling
followed by the physical half-trace leaves this value unchanged.

## Vacuum Consequence

At the rank-one background the portal coefficient gives `zeta=c/2`.
Strict phi stability requires `zeta>2`, equivalently `c>4`. Therefore the
canonical value only saturates the threshold: four phi modes are positive
and four remain zero.

## Multiplicity No-Go

Two identical copies would give `c=8`, but their copy commutant is
`M2(C)`. This violates the established one-copy irreducibility selector.
Identical multiplicity cannot be used as a coefficient enhancement.

## Remaining Branches

1. A non-identical auxiliary factor with scalar joint commutant.
2. A derived higher spectral moment followed by full radial restationarization.

If neither branch lifts the four zero modes without a new continuous input,
the tensor-product rescue is closed.

## Source Notes

- `version4_pati_salam_tensor_product_coefficient_gate.tex`
- `s2t_v4_pati_salam_tensor_product_coefficient_gate.py`
- `s2t_v4_pati_salam_tensor_product_coefficient_gate_results.json`
- arXiv:math-ph/9902029; arXiv:1011.4456.