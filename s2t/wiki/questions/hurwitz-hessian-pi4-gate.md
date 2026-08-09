# Hurwitz Hessian Pi4 Gate

## Direct Hessian

The identity `zeta(4,1/2)=pi^4/6` was already present in Tome II. It does not
directly produce `pi^-4`.

For `lambda_n(R)=((n+1/2)/R)^2`, `zeta(0,1/2)=0`, so the zeta-regularized
log-determinant has zero scale Hessian. The direct inverse-square spectral
functional has

`d2/d(log R)^2 Tr(A_R^-2) = 16 zeta(4,1/2) = 8 pi^4/3`.

Thus the direct Hessian carries positive `pi^4`, not inverse `pi^4`.

## Six-Channel Lead

There is an exact inverse-response identity:

`[6 zeta(4,1/2)]^-1 = pi^-4`.

A parent theory with six equal unit-normalized channels and a physical inverse
collective susceptibility would therefore generate the desired coefficient.
Existing raw rank-six structures do not yet pass the physical weighting gate:
the SU5 mixed block is weighted by generator indices rather than raw dimension,
and a conformal deformation is one direction rather than all six metric strains.

## Verdict

The proposed direct-Hessian explanation fails. The six-channel inverse
susceptibility is a sharp II.B candidate, not a closure of the current C6
Maxwell-ghost calculation.

## Evidence

- `s2t_hurwitz_hessian_pi4_audit.py`
- `s2t_hurwitz_hessian_pi4_results.json`
- `hurwitz_hessian_pi4_gate.tex`