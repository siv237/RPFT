# Hypothesis Batch Pruner Gate

> Status: working
> Research status: completed; no new closed physical prediction
> Type: question
> Updated: 2026-08-07

## Question

Do the ten proposed APS, conformal, orbifold, Chern--Simons,
inverse-susceptibility, `B-L`, nonuniform-saddle, torsion-splitting,
two-loop and projection-weight hypotheses survive a uniform rerun in the
frozen Tome II conventions?

## Reproduced Results

- The APS mass-shift route fails both the frozen eta menu and the blockwise
  vectorlike reality gate. The value `5/24` applies only to `eta=-1/4`; the
  `eta=+1/4` branch gives `-1/24`.
- Gravitational gauge reduction leaves the Majorana rank at `24`.
- The proposed diagonal orbifold matrix has determinant `-1`; the corrected
  `Z2/Z4` construction passes only the representation-direction gate.
- The proposed Chern--Simons integrand is a three-form, not a five-form.
- The six-channel `pi^-4` identity, anomaly-free `B-L` root content and
  reduced nonuniform GL saddle are retained as exact or conditional lemmas,
  not physical closures.

## New Precision Pruners

- `I_rho(beta)=I_rho(-beta)=I_rho(1-beta)` exactly, so the declared circle
  determinant cannot split conjugate GL orientations.
- At `rho=1`, `I_1(1/2)=0.0074697796100663`, while
  `2 I_1(1/4)=0.0074837289794912`; the earlier rounded value is corrected.
- Solving `(alpha/pi)^2 X=alpha/3` gives
  `X=pi^2/(3 alpha)=450.8303668617`. The strict rejection is circularity,
  because the coefficient imports the train anchor `alpha`.
- `12 pi/7=5.3855874062` misses the required projection weight
  `5.4027533072` by `0.317725%`.

## Unregistered Claim

The statement that an axial difference shift vanishes identically was not
registered as a theorem because no operator formula was supplied. Existing
axis audits prove a residual projective orbit and a free two-family relative
angle, not an identically zero shift operator.

## Verdict

The batch retains four exact or conditional constructive lemmas and adds
three precision pruners. It does not change
`N_closed_physical=0`. Kinetic mixing is a future normalization-sensitive
second gate, not a second sector already passed.

## Evidence

- `s2t/audits/s2t_hypothesis_batch_pruner_audit.py`
- `s2t/results/s2t_hypothesis_batch_pruner_results.json`
- `s2t/gates/hypothesis_batch_pruner_gate.tex`
- [[bl-nonuniform-pairing-working-package-2026-08-07]]
- [[eta-phase-mass-gate]]
- [[conformal-majorana-rank-gate]]
- [[anomaly-free-holonomy-projection]]
- [[six-channel-inverse-susceptibility-gate]]
- [[nonuniform-pairing-saddle-gate]]