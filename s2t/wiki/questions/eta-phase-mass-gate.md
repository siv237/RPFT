# Eta Phase to Real Mass Gate

> Status: closed negatively for the minimal vectorlike Dirac realization
> Date: 2026-08-06

## Question

Can the RP3 eta phase and the circle value `|zeta(-1)|` combine into the real charged-lepton correction `-alpha/3`?

## Blockwise Result

For every product eigenvalue,

```text
(m+iE)(m-iE)=m^2+E^2 > 0.
```

Thus the physical vectorlike charged-lepton determinant has a real block contribution `log(m^2+E^2)`. Its mass derivative is `2m/(m^2+E^2)` and contains no eta term. A deliberately asymmetric three-dimensional spectrum gives zero product phase for periodic and antiperiodic branches to machine precision.

## Functional Mismatch

At `rho=1`, the half-shifted Euclidean circle determinant ratio is

```text
I_1(1/2)=0.0074697796...
```

not `|zeta_R(-1)|=1/12`. The first is a mass-dependent logarithmic determinant; the second is a Casimir-regularized linear mode sum.

## Verdict

The arithmetic identity `1/3=1/4+1/12` does not produce a real mass shift in the minimal Gaussian/vectorlike operator class. The topological interpretation remains valid for determinant phases and global anomaly bookkeeping, but the tau formula still depends on the real QED winding self-energy and its unresolved projection normalization.

## Reopening Condition

Derive a complex chiral Yukawa phase, a CP-odd/topological-sector interference mechanism and a fixed coupling that converts the phase into a real linear mass response equal to `alpha/3` before loading tau data.

## Evidence

- `s2t_eta_phase_mass_gate_audit.py`
- `s2t_eta_phase_mass_gate_results.json`
- `eta_phase_mass_gate.tex`