# Nonuniform Pairing Saddle Gate

> Status: working
> Research status: analytic saddle found conditionally
> Type: question
> Updated: 2026-08-06

## Question

Does the surviving nonuniform pairing branch exist automatically, and does geometry select a unique winding orientation?

## Results

- The root connection shifts the GL momentum lattice to `k_n=(2n+1)pi/L`.
- The two lowest branches are exactly degenerate: `n=0` and `n=-1`.
- A nonzero saddle exists only if `lambda v^2 > pi^2/L^2`.
- For unit RP3 with `L=pi`, the threshold is `lambda v^2>1`.
- Above threshold the radial Hessian is positive, while topology still does not fix the condensate amplitude or select one conjugate orientation.
- The transverse odd-winding index remains conditional on the condensate existing.

## Verdict

Geometry determines the half-shifted spectrum and threshold, but not whether condensation occurs. A parent-derived stiffness scale and an orientation-splitting mechanism are still required before the rank-one BdG result can be promoted.

## Evidence

- `s2t/audits/s2t_nonuniform_pairing_saddle_audit.py`
- `s2t/results/s2t_nonuniform_pairing_saddle_results.json`
- `s2t/gates/nonuniform_pairing_saddle_gate.tex`