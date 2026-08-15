# Version IV: exact Pati–Salam first-order kernel

> Status: strong conditional pass
> Updated: 2026-08-13

## Variable space

The real KO6-compatible Dirac space has dimension `272`:

- arbitrary complex `Y`: `128` real;
- symmetric complex `M_R`: `72` real;
- symmetric complex `M_L`: `72` real.

## Full Pati–Salam algebra

The exact double-commutator kernel has real dimension `8`:

```text
Y = A_(2x2) tensor I4
M_R = M_L = 0
```

Thus the full first-order condition enforces quark–lepton unification and
removes Majorana channels.

## Embedded Standard Model algebra

The exact kernel has real dimension `32`:

- `16` real parameters in
  `Y=A_lepton tensor P_lepton + A_quark tensor P_quark`;
- `16` real parameters in one symmetric right-Majorana channel equivalent
  to a complex `Delta=(2_R,4_4)` seed;
- `M_L=0`.

The analytic bases vanish on every `40^2` or `24^2` algebra-basis pair, and
their subspaces coincide with the numerical kernels. Four embedding
conventions preserve the dimensions and representation content.

## Interpretation

This matches the structural seeds of the literature composite branch, but
does not yet derive the nonlinear fluctuated fields. The next gate is the
explicit generalized inner fluctuation, including its quadratic `A_(2)`
term.

## Sources

- Chamseddine, Connes and van Suijlekom, arXiv:1304.8050.
- Chamseddine, Connes and van Suijlekom, arXiv:1507.08161.
- `version4_pati_salam_first_order_kernel_gate.tex`
- `s2t_v4_pati_salam_first_order_kernel.py`