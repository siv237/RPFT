# Version IV: explicit Pati–Salam finite Dirac block

> Status: working
> Research status: representation/KO6 target pass; spectral-triple gate open
> Type: question
> Updated: 2026-08-13

## Hilbert module

For one generation:

- `V_R=(2_R,1_L,4_4)`, complex dimension `8`;
- `V_L=(1_R,2_L,4_4)`, complex dimension `8`;
- particle dimension `16`;
- KO6 particle–antiparticle dimension `32`.

The grading is `diag(+I8,-I8,-I8,+I8)`, while reality exchanges particles
and antiparticles and anticommutes with the grading.

## Dirac channels

- `Y: V_L -> V_R`, `64` complex components,
  `(2_R,2_L,1+15_4)`;
- symmetric `M_R`, `36` complex components,
  `(3_R,1_L,10_4)+(1_R,1_L,6_4)`;
- symmetric `M_L`, `36` complex components,
  `(1_R,3_L,10_4)+(1_R,1_L,6_4)`.

The constructed `32 x 32` matrix passes self-adjointness, odd grading,
reality and `J Gamma=-Gamma J` numerically at machine precision.

## Composite restriction

The first-order Standard Model branch uses `phi`, `Delta` and traceless
`Sigma_4`. Its complexification has `27` complex coordinates; if the
physical adjoint condition is Hermitian, it has `39` real degrees. Both are
strictly smaller than the `200` real components of general `Y+M_R`. The
Majorana formula is explicitly symmetric.

## Remaining gate

Implement the full algebra and opposite-algebra matrices on all 32 states
and compute the exact first-order double-commutator kernel for both the full
Pati–Salam algebra and the embedded Standard Model subalgebra.

## Sources

- Chamseddine, Connes and van Suijlekom, arXiv:1507.08161, equations
  (21)–(23) and (27).
- Chamseddine, Connes and van Suijlekom, arXiv:1304.8050.
- `s2t/gates/version4_pati_salam_finite_dirac_block_gate.tex`
- `s2t/audits/s2t_v4_pati_salam_finite_dirac_block.py`