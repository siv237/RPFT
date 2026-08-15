# Blind Prediction Scorecard — 2026-08-04

> Status: working
> Research status: frozen comparison
> Type: synthesis
> Updated: 2026-08-15

> Controls: PDG 2024 values loaded only after the S2T rows were fixed

## Result

The comparison is neither uniformly successful nor empty. It separates into two clusters.

### Close cluster

- `m_tau=1776.8594 MeV` versus `1776.93(9) MeV`: `-0.78 sigma`.
- `M_H=125.0565 GeV` versus `125.20(11) GeV`: `-1.30 sigma`.
- `lambda_H=0.1292217` versus the tree proxy `M_H^2/(2v_F^2)=0.1292806`: `-0.26 sigma`.
- Conditional neutrino rows: `delta m21^2` is `-0.26 sigma`; `delta m32^2` is `+1.95 sigma` for normal ordering.

The neutrino rows have low evidential weight because their action-level completion is still conditional. The charged-lepton and scalar rows are the strongest surviving numerical pattern.

### Failed zero-matching cluster

- `G_F`: `+0.184%`.
- Tree/on-shell weak-angle proxy: `-2.70%`.
- `M_W`: `-0.555%`.
- `M_Z`: `-0.939%`.
- `alpha_s(M_Z)`: `-26.36%`.

Experimental pulls are shown only as diagnostics; theory matching uncertainties have not been computed.

## Sector Diagnosis

Fixing the weak scale from `G_F` requires `v_F/v_S2T=1.0009197`. After this correction, the remaining factors are still different:

```text
g2 required factor = 1.004659,
gZ required factor = 1.008549,
g3 required factor = 1.165296.
```

Therefore the missing contribution is not one universal scalar normalization. The weak sector needs representation-dependent gauge matching, while QCD needs a much larger change in running or boundary data. The natural next object is a derived KK/breaking-sector threshold spectrum with separate `SU(2)`, `U(1)` and `SU(3)` traces.

## Scientific Reading

The scalar quartic relation is surprisingly close even after replacing the model weak scale by the measured Fermi scale. This suggests that the scalar normalization may contain a useful structural relation. The failure pattern is concentrated instead in the transport from high-scale spectral boundary conditions to low-energy gauge couplings.

This diagnosis is falsifiable: a frozen threshold spectrum must simultaneously improve `G_F`, `sin^2 theta_W`, `M_W`, `M_Z` and `alpha_s`. If it only repairs one row, it is a fit rather than evidence.