# B-L Defect Action Global Consistency Gate

> Status: proposed action fails before its dynamical kill-gate
> Date: 2026-08-07

## Question

Can one action simultaneously use sterile root holonomy i, a
torsion-twisted charge-minus-two pairing field, a scalar Majorana vertex and
a half-shifted nonuniform pairing spectrum?

## Bundle Obstruction

The sterile pair has holonomy i squared, hence -1.

For the ordinary charge-minus-two field:

- pairing holonomy is -1;
- the Majorana vertex has total holonomy +1;
- a global parallel nonzero condensate is impossible.

For the torsion-twisted field:

- torsion times charge holonomy is +1;
- a parallel condensate is allowed;
- the Majorana vertex has total holonomy -1 and is torsion-odd.

Thus the proposed action combines the two incompatible sides of the existing
root--mass--condensate trilemma.

## Spectrum Double Counting

The twisted pairing bundle has total holonomy +1. Its covariant spectrum is
integer shifted and contains a zero mode:

    k_n=2 pi n/L.

The half-shifted spectrum

    k_n=(2 pi n+pi)/L

belongs to the ordinary field with total holonomy -1. Using the torsion
cancellation and retaining the half shift counts the same sign twice.

Therefore the proposed twisted action does not derive the conjugate
n=0,-1 saddle pair or the threshold 1-lambda v^2. Those belong to the
ordinary nonuniform defect branch.

## Additional Failures

- A flat Maxwell action does not select the Wilson line pi/2.
- The negative pairing mass is inserted as m_phi^2=-lambda v^2.
- The tanh core profile and S_core coupling are not solved from the action.
- The external rank-24 module is not constructed by the displayed fields.
- Equal kernel/quotient weights remain a canonical metric choice.
- The trace coefficient 8/3 is not a second predicted observable; physical
  kinetic mixing also requires boundary data, couplings, thresholds and
  running.

## Verdict

The proposed action is not globally defined as written. The surviving branch
is the ordinary charge-two nonuniform defect texture with holonomy -1 and a
scalar Yukawa vertex. Its condensation, core profile, rank-24 embedding and
relative metric remain open.

## Branch A Follow-Up

The collaborator subsequently selected the ordinary branch A. This correctly
closes the bundle and half-shift consistency problem. Given a fixed root
Wilson sector and a broken-symmetry potential, the circle saddle and its
threshold follow.

The branch is still not closed merely by assuming SSB:

- the Maxwell term does not select Wilson holonomy pi/2;
- the circle plane wave does not derive the transverse tanh kink;
- a mod-two index fixes odd kernel parity, not automatically exactly one
  zero mode;
- the rank-24 module and the relative kernel/quotient metric remain external.

Thus A is the unique globally coherent minimal branch, but its rank-one
physical Hessian remains conditional.

## Evidence

- s2t_bl_defect_action_global_consistency_audit.py
- s2t_bl_defect_action_global_consistency_results.json
- bl_defect_action_global_consistency_gate.tex
- [[root-mass-condensate-trilemma-gate]]
- [[nonuniform-pairing-saddle-gate]]
- [[bl-nonuniform-pairing-working-package-2026-08-07]]