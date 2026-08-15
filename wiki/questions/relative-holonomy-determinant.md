# Relative Holonomy Determinant

> Status: working
> Research status: first gate completed
> Type: question
> Updated: 2026-08-03

## Question

Can the program replace scheme-dependent absolute determinant residues with twisted/untwisted determinant ratios whose local heat-kernel terms cancel before comparison with observables?

## Observable

For a massive circle mode with `rho=R1 sqrt(lambda)` and holonomy `beta`, use

```text
I_rho(beta)=log[(cosh(2 pi rho)-cos(2 pi beta))/(cosh(2 pi rho)-1)].
```

The massive Maxwell--FP response is

```text
Delta Gamma_rel
 = 1/2 Delta logdet(Delta_1,coex)
 - 1/2 Delta logdet'(Delta_0,massive).
```

The true scalar zero mode is excluded from this first audit because its comparison requires an explicit gauge-volume and zero-mode measure.

## Results

- The ratio is rapidly convergent, periodic under `beta -> beta+1`, and symmetric under `beta -> 1-beta`.
- At `R1/R3=1`, `Delta Gamma_rel(1/4)=2.0752238855e-5` and `Delta Gamma_rel(1/2)=4.1504331779e-5`.
- Only `beta=0` and `beta=1/2` are symmetry stationary points. The existing quarter-holonomy is not selected by this determinant alone.
- The response decreases monotonically toward zero as `R1/R3` grows, so it does not independently stabilize a finite radius.
- The discrete nontrivial/trivial `Z2` flat-bundle winding ratio is also finite. Its massive Maxwell--FP value at unit radius ratio is `9.5763273455e-5`, but it is likewise monotone.

## Verdict

The relative determinant survives as a clean global response observable, not as a replacement formula for `alpha`. The next gate is a joint configuration functional containing geometry, relative spectral response, the derived zero-mode measure, and the defect/superconnection sector. Its stationary point must predict multiple blind observables without fitted coefficients.

## Reciprocal Completion

The existing primal/dual cycle structure suggests the coefficient-free completion

```text
F_beta(r)=Delta Gamma_rel(beta;r)+Delta Gamma_rel(beta;1/r).
```

In `x=log r`, this satisfies `F_beta(x)=F_beta(-x)`, so `r=1` is an exact stationary point. The dense numerical sweep gives positive curvature and a global grid minimum at `r=1` for every tested nontrivial phase branch.

For the topology-selected quarter sector:

```text
F_1/4(1)=4.1504477710e-5,
d2F_1/4/d(log r)^2|_1=5.9801278147e-3 > 0.
```

The discrete `RP3` flat-bundle completion also has its minimum at `r=1`, with curvature `2.2068743247e-2`.

This is the first post-C6 no-fit shape selection result. Its theorem gate is the ambient bridge: prove that the intrinsic `Qcycle` reciprocal involution pairs the full Maxwell--FP determinants at `r` and `1/r` with equal weights, and include the scalar zero-mode/gauge-volume measure.

## Ambient Bridge Audit

The bridge fails in the current field content.

- The `RP3 x S1` product spectra at `r` and `1/r` are not isospectral away from `r=1`.
- The single response is strongly asymmetric: at quarter holonomy, `G(1/2)=1.0080209509e-2`, while `G(2)=7.2966632735e-11`.
- The constant scalar circle determinant scales as `2 log(2 pi R1)` and changes by `4 log r` under inversion before gauge-volume bookkeeping.
- Ordinary Maxwell duality is a reformulation, not an additive inverse-radius determinant sector.
- `Qcycle` duality acts on the intrinsic `H0(gamma) direct_sum H1(gamma)` complex; no intertwiner to the ambient Maxwell--FP Hilbert space exists.

Revised verdict: the minimum of `G(r)+G(1/r)` is a true property of the imposed symmetrization, but it is not derived vacuum selection in Tome II.A. Reviving it requires a new mandatory winding sector, string-like T-duality, or an explicit ambient operator involution including the zero-mode measure.

## Sources

- `s2t/audits/s2t_relative_holonomy_determinant_audit.py`
- `s2t/results/s2t_relative_holonomy_determinant_results.json`
- `s2t/audits/s2t_dual_completed_relative_functional_audit.py`
- `s2t/results/s2t_dual_completed_relative_functional_results.json`
- `s2t/audits/s2t_ambient_reciprocal_duality_bridge_audit.py`
- `s2t/results/s2t_ambient_reciprocal_duality_bridge_results.json`
- `s2t/results/external_l21_spectrum_determinant_reproduction_results.json`
- `s2t/results/external_rp3xs1_winding_determinant_results.json`

## Links

- [[external-rp3xs1-winding-determinant-audit]]
- [[holonomy-and-dirac-sectors]]
- [[current-status-and-next-vectors]]