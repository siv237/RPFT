# Version IV: Pati–Salam representation-separation diagnostic

> Status: working
> Research status: necessary sensitivity passed; potential gate open
> Type: question
> Updated: 2026-08-13

## Target modes

- Required Goldstone: `(I_R,R4)=(1,10)`.
- Unwanted pseudo-Goldstone: `(I_R,R4)=(0,6)`.

## Sensitivity test

| Operator | Required | Unwanted | Difference |
|---|---:|---:|---:|
| Identity singlet | 1 | 1 | 0 |
| `SU(2)_R` Casimir | 2 | 0 | -2 |
| `SU(4)` Casimir | 9/2 | 5/2 | -2 |
| Combined Casimir | 13/2 | 5/2 | -4 |

The universal singlet is blind, while the Casimir invariants distinguish the
representations. This is not an adjoint-VEV mass matrix: an actual mass
splitting depends on the breaking direction and the full potential.

## First candidate

Target one Hermitian weak-singlet four-color diagonal block `1+15`:

- its trace component can participate in dimensional transmutation;
- the `10` and `6` sectors have different `SU(4)` Casimirs;
- the general fundamental field has the same `SU(4)` content but transforms
  as `(2_R,2_L,1+15_4)`;
- a weak-singlet `(1_R,1_L,15_4)` is present in the constrained composite
  branch, but its dynamical legitimacy remains open.

## Open gate

First construct one explicit project Pati–Salam finite block and derive the
composite restriction rather than imposing it. Then derive its full spectral
potential and explicitly compute the mass matrix for a high-scale adjoint VEV,
the full Hessian, Goldstone counting, colored scalar masses, fermion masses,
and the Coleman–Weinberg sign. Casimir sensitivity alone is not a vacuum
solution.

## Sources

- Chamseddine, Connes and van Suijlekom, arXiv:1304.8050.
- Kurkov and Lizzi, arXiv:1801.00260.
- Karimi Khozani, arXiv:1905.04533.
- `s2t/gates/version4_pati_salam_diagonal_connector_menu_gate.tex`
- `s2t/audits/s2t_v4_pati_salam_diagonal_connector_menu.py`