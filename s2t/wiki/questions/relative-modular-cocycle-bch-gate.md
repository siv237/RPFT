# Relative Modular Cocycle BCH Gate

> Status: working
> Type: question
> Updated: 2026-08-06

## Summary

The direct finite-dimensional relative modular cocycle is an exact
rephasing no-go for CKM CP violation. The first BCH commutator creates CP
only when its backreaction is sector-asymmetric, but the canonical
coefficient overshoots the physical Jarlskog scale and the asymmetry is not
yet derived.

## Results

- Tested 24 frozen oriented Wilson sector pairs.
- Verified zero base Jarlskog invariant in every pair.
- Tested 72 direct-cocycle evolutions at three modular times.
- Found maximum Jarlskog change `2.1e-17`, as required by rephasing invariance.
- Tested the canonical Hermitian operator `Q=(i/2)[H_u,H_d]`.
- Symmetric two-sided backreaction gives zero CP in all 24 cases.
- One-sided backreaction gives nonzero CP in all 48 cases.
- The smallest absolute J is `0.0012085`, at least 38.7 times the post-blind CKM control.

## Interpretation

The missing mechanism is not the direct Connes cocycle. It is a derived
chiral or charge asymmetry controlling how the relative modular commutator
backreacts on the two sectors. A free suppression coefficient would merely
replace the old selector by a new fit.

## Next Gate

Derive the one-sided or unequal coupling of `Q` from a finite algebra,
real structure and parent action. Freeze its coefficient before CKM data,
then require the same construction to pass a fermion mass-hierarchy test.

## Links

- [[wilson-modular-state-readout-gate]] — source Hamiltonians and CP no-go.
- [[chiral-doubled-triplet-yukawa-gate]] — finite-operator consistency and selector gap.
- [[two-layer-physical-ckm-redteam-gate]] — physical CKM control.
- [[observed-world-coverage-gate]] — empirical closure requirements.

## Source Notes

- s2t_relative_modular_cocycle_bch_audit.py
- s2t_relative_modular_cocycle_bch_results.json
- relative_modular_cocycle_bch_gate.tex