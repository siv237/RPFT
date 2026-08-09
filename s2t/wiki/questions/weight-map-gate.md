# Weight Map Gate

> Status: C0/C1 failed; C2 lookup passes but parent-measure gate failed
> Date: 2026-08-07

## Question

Can one preregistered positive weight map reproduce the charged-lepton seed
`pi^2+2pi+2/3` and neutrino stiffness `23+pi^-1` without sector-labelled
readouts?

## Reference-Metric Correction

A weight map has meaning only relative to one frozen base inner product.
Therefore `C0 const=1 with canonical norms` and `C0 const=1 with raw norms`
are not two constant-weight rules: the latter changes the reference metric.

With the canonical component metric:

- `C0` gives tau `8/3` and neutrino `24`, so both targets fail.
- `C1`, using degree and quantized period, gives tau `8/3` and neutrino
  `23+pi^-1`; only the neutrino sector passes.
- The proposed rule `degree zero -> raw` is not genuinely `C1`, because raw
  zero-form norms depend on the manifold factor. It already belongs to `C2`.

## C2 Result

The factor/degree cells

- `(RP3,0) -> pi^2`;
- `(S1,0) -> 2pi`;
- `(finite internal,0) -> 1`;
- `(integral S1,1) -> pi^-1`

reproduce both aggregate norms exactly. This is a valid geometric lookup
table and does not explicitly use the labels `lepton` or `neutrino`.

It is not yet a two-sector prediction. The table contains the required
relative normalizations but is not derived as the Hessian, symplectic form or
measure of one action.

## Covariance Gate

Under a field redefinition, the metric and observable vertices must transform
together. A list of norms without this transformation law is coordinate
dependent. The current `C2` proposal supplies no covariant stiffness/coupling
map and therefore fails the operator gate.

## Logical Scope

The audit establishes that simple universal `C0-C1` rules fail and that the
common measure is not presently derived. It does **not** prove:

- that no deeper parent action can derive the `C2` metric;
- that the measure, CP, vacuum-selection and threshold gaps are logically
  independent;
- that the one-principle hypothesis is permanently false.

The correct status is `C2 lookup pass; action fail`, with zero new closed
physical predictions.

## Reopening Condition

Derive the `C2` cells from one preregistered local, boundary or global action,
include field-redefinition covariance, and predict an independent EM or rotor
quantity with no new weights.

## Evidence

- `s2t_weight_map_gate_audit.py`
- `s2t_weight_map_gate_results.json`
- `weight_map_gate.tex`
- [[tiered-parent-action-p1-gate]]
- [[kinematics-dynamics-pairing-diagnosis-2026-08-07]]