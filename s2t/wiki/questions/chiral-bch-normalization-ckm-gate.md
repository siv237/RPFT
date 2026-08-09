# Chiral BCH Normalization CKM Gate

> Status: working
> Type: question
> Updated: 2026-08-06

## Summary

Natural inverse dimensions from the finite algebra can suppress the
one-sided BCH commutator to the observed Jarlskog scale. This scalar success
does not extend to the full CKM matrix.

## Results

- Froze nine coefficients from dimensions 2, 3, 4, 6, 8, 12, 24 and 48.
- Generated 432 candidates before loading the CKM control.
- Found 52 candidates with J within a factor two of the control.
- The closest J ratio is 0.9888283.
- Exhausted all 36 generation permutations for every candidate.
- No candidate reproduces all three CKM angles within factor two.
- The best angle-log-RMS among J-compatible candidates is 1.7283.
- The best absolute-matrix Frobenius score is 0.8175.

## Mass Obstruction

Central shifts of either Hamiltonian preserve mixing and J but continuously
change eigenvalue ratios. Therefore the same construction cannot predict a
mass hierarchy until a parent action fixes central offsets and a positive
Yukawa readout.

## Next Gate

Derive unequal family-edge metrics or a noncentral Yukawa map from the
finite algebra. The mechanism must fix central offsets and all three mixing
angles before the Jarlskog match is counted.

## Links

- [[relative-modular-cocycle-bch-gate]] — source of the one-sided CP term.
- [[chiral-doubled-triplet-yukawa-gate]] — valid chiral container without a selector.
- [[two-layer-physical-ckm-redteam-gate]] — full physical CKM control.

## Source Notes

- s2t_chiral_bch_normalization_ckm_audit.py
- s2t_chiral_bch_normalization_ckm_results.json
- chiral_bch_normalization_ckm_gate.tex