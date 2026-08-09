# APS Orbifold Inflow Red-Team Gate

> Status: constructive reframing; parent action and physical coefficients open
> Date: 2026-08-06

## Exact Positives

- The arithmetic identity `1/4 + |zeta(-1)| = 1/3` is exact.
- The existing `Z2/Z4` SU(5) projection retains `U+2D+H` and exactly gives `(17/6,1/6,2)`.
- The six-channel half-shifted Gaussian inverse susceptibility is exactly `pi^-4`.
- A bulk--boundary--defect formulation is a legitimate new II.B search class.

## Red-Team Failures

- `diag(-1,-1,-1,+1,+1)` has determinant `-1`; the valid SU(5) parity is `diag(+1,+1,+1,-1,-1)`.
- The proposed Chern--Simons integrand is a three-form, not a five-form.
- Existing RP3 spin audits give eta invariants `+/-1/4`; `eta=-1/2` needs a different explicitly twisted or doubled operator.
- `zeta(-1)` is a regularized linear sum, not automatically the `det-prime` contribution to one relative mass operator.
- The RP3 torsion and S1 spin signs belong to independent generators of `Z2 x Z`.
- Assigning the torsion line to the muon but not the tau is an underived family selector.
- Gauge fixing is not automatically the subtraction of one vector from a 24-dimensional Majorana module.
- Anomaly inflow fixes anomalous variation or phase, not automatically the real finite `1/24` and `pi^-4` response coefficients.

## Existing Stronger Orbifold Result

The project already uses

```text
h=diag(-1,-1,-1,-i,-i),
P5=h^2=diag(+1,+1,+1,-1,-1)
```

plus multiplet flat characters in a vectorlike SU(5) parent. This closes the representation-direction gate but not the derivation of the character assignment, threshold sign, or absolute magnitude.

## Reopening Condition

Construct a correctly normalized five-dimensional CS/invertible bulk action, compute the anomaly polynomial of the full projected spectrum, derive the twisted APS family assignment, and show that one common boundary operator produces the mass, rank, tensor-response, and gauge-threshold terms without fitted coefficients.

## Evidence

- `s2t_aps_orbifold_inflow_redteam_audit.py`
- `s2t_aps_orbifold_inflow_redteam_results.json`
- `aps_orbifold_inflow_redteam_gate.tex`