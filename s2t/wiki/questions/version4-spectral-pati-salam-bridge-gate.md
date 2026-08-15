# Version IV: spectral Pati–Salam bridge gate

> Status: architecture candidate; fixed-scale test failed
> Updated: 2026-08-13

## Problem

The project’s low-rank, discrete and fixed-scale relations are the strongest
part of the model, while gauge/RG closure fails as a correlated cluster.
Test whether a spectral Pati–Salam layer can provide the missing structured
high-energy transmission without independent gauge thresholds.

## Preregistered test

- Keep the measured low-energy couplings and Standard Model running.
- Use the Pati–Salam matching `g3=g4`, `g2=gL`,
  `1/gY^2=1/gR^2+2/(3g4^2)`.
- Test the four scalar scenarios listed in arXiv:1507.08161.
- Fix `mR=1.0317137e13 GeV` from the project’s existing `g1=g2` crossing.
- Do not fit `mR` to gauge unification.

## Result

At the fixed project scale, the best relative spreads are:

- composite: `3.13%`;
- composite plus `(1,1,15)`: `2.92%`;
- fundamental: `2.63%`;
- left-right fundamental: `4.90%`.

No scenario passes a one-percent gate. If `mR` is freely optimized, exact
one-loop unification returns at `mR ~ 10^11–10^13 GeV`, reproducing the
published pattern. That is evidence that the bridge is viable, but not a
prediction of this project.

## Model improvement

Preserve the current low-energy finite geometry as an IR corner and test one
canonical Pati–Salam UV bridge. Before any new RG claim, the finite
Dirac/scalar sector must independently derive:

1. the Pati–Salam-breaking vacuum;
2. the scalar scenario;
3. the intermediate scale `mR`;
4. the threshold spectrum.

Only then may the gauge running be evaluated blind.

## Kill conditions

- No stable Pati–Salam-to-SM vacuum.
- `mR` determined only by requiring gauge unification.
- Scalar content added outside the finite-geometry menu.
- Independent threshold shifts introduced after viewing residuals.

## Sources

- Chamseddine, Connes, van Suijlekom, arXiv:1507.08161.
- Karimi Khozani, arXiv:1905.04533.
- Lee, arXiv:hep-ph/0611196.
- Hebecker and Westphal, arXiv:hep-th/0407014.
- `version4_spectral_pati_salam_bridge_gate.tex`
- `s2t_v4_spectral_pati_salam_bridge_gate.py`
- `s2t_v4_spectral_pati_salam_bridge_gate_results.json`