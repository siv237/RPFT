# Wilson Modular State Readout Gate

> Status: working
> Type: question
> Updated: 2026-08-06

## Summary

The minimal Wilson Gibbs-state class is robustly nonfactorizing, but
entanglement depends on an underived sign. Its modularly selected rank-three
readouts preserve commuting factor translations and do not produce CKM.
Restoring the oriented Hermitian Wilson generator gives full three-family
overlap but still zero CP.

## Results

- Tested three factor kernels, two Wilson signs and two axis representatives.
- The two axes are equivalent modulo residual symmetry.
- All 12 states are nonfactorizing and have positive mutual information.
- Positive-sign states are PPT-separable; negative-sign states are entangled.
- The canonical modular block algebra is M3 plus C, not pure M3.
- Pure triplet conditioning discards 18.1 to 31.7 percent of state probability.
- All 48 rank-three spectral readouts preserve factor commutativity.
- Real relative-axis states give one two-family rotation and zero Jarlskog.
- All 24 oriented Wilson sector pairs have full support but remain CP conserving.

## Interpretation

The missing object is more specific than an entangled observer state. The
up/down sectors require a relative modular cocycle that breaks their common
antiunitary symmetry. Its sign, inverse temperature, singlet energy and
relative phase must be derived from one parent action.

## Links

- [[observer-readout-fixed-point-gate]] — readout possibility and nonuniqueness.
- [[continuous-wilson-gap-action-gate]] — Wilson saddle and axis orbit.
- [[family-relative-orbit-ckm-gate]] — real two-family rotation.
- [[observed-world-coverage-gate]] — missing empirical closure.

## Source Notes

- s2t_wilson_modular_state_readout_audit.py
- s2t_wilson_modular_state_readout_results.json
- wilson_modular_state_readout_gate.tex