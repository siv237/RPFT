# EW QCD Threshold Closure

> Status: draft
> Type: question
> Updated: 2026-07-09

## Question

Can the electroweak and QCD closure rows be derived from an explicit threshold spectrum with physical masses and admissible logarithmic phases, rather than from small residual logs or post-hoc scale choices?

## Why It Matters

EW/QCD threshold closure is marked open in [[s2t-closure-roadmap]]. Treating small-log checks as proof would blur the boundary between exact spectral closure and adjustable threshold fitting.

## Current Evidence

- The current wiki records no dedicated threshold solver for EW/QCD closure.
- Existing S2T audit rows strongly support `S_vac`, `m_tau`, and Higgs EFT bridge, but they do not close the threshold spectrum.
- The sector-attribution audits show that phase branches and subleading spectral loads can separate, which is useful for designing a threshold model but not sufficient for closure.

## Needed Closure Test

- Build a threshold solver that takes candidate masses, charges, beta-function coefficients, and matching scales as explicit inputs.
- Solve the logarithmic system and reject solutions that require unphysical masses or hidden fitted constants.
- Compare one-loop and two-loop RG variants so the closure claim is not an artifact of a single approximation.

## 2026-08-04 Blind Fermi-Constant Postdiction

The independently constructed `v_S2T=245.993409261 GeV` predicts at tree level

```text
G_F^S2T=1/(sqrt(2) v_S2T^2)=1.1685251368e-5 GeV^-2.
```

The PDG control value is `1.1663788(6)e-5 GeV^-2`. The relative excess is `1.84017e-3`, or about `0.184%`. This is a genuine blind postdiction because `G_F` was explicitly excluded from the construction of `v_S2T`.

The result does not yet reject every possible completion because the model has not derived its finite electroweak matching or renormalization scheme. It does reject the zero-matching identification of `v_S2T` with the physical charged-current scale. The required factors are

```text
G_F matching: 0.998163209,
v matching:   1.000919663.
```

A universal rescaling fixed by `G_F` changes the current one-loop values only to `M_W=79.9965 GeV` and `M_Z=90.4151 GeV`; it does not close those residuals. Therefore the next admissible calculation must derive non-universal gauge and threshold matching from a frozen spectrum and test all four observables together.

## 2026-08-04 Representation-Cone Gate

The required inverse-coupling correction has normalized direction `(16.91,1,11.01)` in `(Y,SU2,SU3)`. Complete-generation KK replicas fail because they carry far too much `SU(2)`. A split diagnostic ray `U+2D+H` gives `(17,1,12)` and is directionally close, but it was inferred from the target and is not evidence by itself.

The frozen modulus supplies only `|log rho|/(2pi)=0.0453994` per geometric splitting unit. The required magnitude needs a coherent regulated tower rather than one threshold. The next gate is therefore precise: derive an anomaly-free parent representation and a holonomy projection that creates the split, then compute the finite KK sum without fitting.

See [[kk-representation-cone-gate]].

## 2026-08-04 Anomaly-Free Projection Candidate

The split direction can be embedded in the vectorlike parent `(10+10bar)+2(5+5bar)+5_H`. Combining the `RP3` parity `diag(1,1,1,-1,-1)`, the order-four hypercharge element `exp(i3piY)` and conjugate flat characters retains exactly one `U`, two `D` and one Higgs doublet while shifting `Q,L,E` and the colored triplet.

This passes the anomaly and zero-mode-content gates. It does not yet pass the physical threshold gate: the character assignment and the regulated determinant magnitude remain open. See [[anomaly-free-holonomy-projection]].

## 2026-08-04 Projected Determinant Verdict

The finite determinant of the shifted `Q,L,E,T_H` partners fails independently of normalization: with a common `RP3` spectrum its color/weak correction ratio is always `9/20`, far below the required `11.014`. The formerly proposed ordinary running of periodic `U+2D+H` is also closed below by the correct-sign two-loop audit.

See [[projected-kk-determinant-gate]].

## 2026-08-04 Geometric Split-Scale Candidate

The existing invariants `Vol(RP3)=pi^2` and `||e1||^2=1/pi` define the zero-parameter action `S_split=pi^2+1/(2pi)`. It gives the scale `3.9674e10 GeV`, but the formerly reported gauge improvement used a sign-reversed RG correction and did not preserve `alpha_em`.

The action remains a conditional defect saddle, not a gauge prediction. See [[geometric-split-mass-action]].

## 2026-08-04 Two-Loop Sign Correction

Correct downward running adds `+(Delta b/2pi) log(Lambda/M)` to inverse couplings. The legacy shortcut used the opposite sign and changed `alpha_em^-1` from `137.0360` to `132.2454`. Preserving `alpha_em` in the coupled two-loop boundary problem gives `M_W=82.0226 GeV`, `M_Z=92.0616 GeV`, `sin2=0.206203` and `alpha_s=0.080177`. The missing mechanism must therefore be a finite threshold of different sign or a genuinely independent UV normalization. See [[two-loop-split-stress-test]].

## 2026-08-04 Finite Threshold Cone Verdict

The corrected target shift is `(0.3680,-0.3680,-2.4592)`. The declared `XY/H3/Sigma8/Sigma3` threshold cone contains it only algebraically: the least extreme exact below-scale solution needs logarithms `(0,34.68,116.05,41.62)`, while the entire available interval is `29.92`. Restricting all masses to `M_Z...Lambda_S2T` makes the system infeasible and leaves a best-case relative residual of `50.7%`. See [[finite-threshold-sign-cone]].

## Links

- [[tome2-s2t-spectral-closure]] — Tome II source defining this as a II.B task.

- [[s2t-closure-roadmap]] — marks this row as open.
- [[numerical-audits]] — current audit source layer.
- [[spectral-correlational-source]] — broader object that any successful closure should constrain.

## Source Notes

- Source paths: `tome2_s2t_spectral_closure.tex`, `s2t_tome2_results.json`, future threshold-audit script/results.