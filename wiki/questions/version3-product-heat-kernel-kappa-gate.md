# Version III Product Heat-Kernel Kappa Gate

> Status: kappa derived; finite B remains positive
> Date: 2026-08-10

## Derivation

For the flat product Dirac operator i gamma d + gamma5 Phi, the spin trace
of E squared gives equal coefficients for (d Phi)^2 and Phi^4 in the a4
heat-kernel coefficient.

In the previous convention this fixes kappa = 2.

## Corrected Spectrum

The physical scalar mass-squared matrix becomes diag(4,4,4) in units of
chi squared. Three real scalars contribute 48 to Str M^4, while two Dirac
pairs contribute -8.

The corrected finite coefficient is therefore

    B0 = 5/(8 pi^2) > 0.

The previous 23/(8 pi^2) value depended on the conditional kappa=1
normalization and is not robust.

## Remaining Gate

Compute gauge/ghost and nonzero KK contributions in the same heat-kernel or
zeta scheme. The quantum scale branch survives only if the total B is
positive.

## Evidence

- version3_product_heat_kernel_kappa_gate.tex
- s2t_v3_product_heat_kernel_kappa_audit.py
- s2t_v3_product_heat_kernel_kappa_results.json
- [[version3-finite-zero-mode-supertrace-gate]]