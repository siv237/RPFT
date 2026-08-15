# Version IV One-Kernel Sign Trilemma Gate

> Status: working
> Type: question
> Updated: 2026-08-15

## Summary

Tests whether identifying the fundamental correlation operator with the
Gaussian bare action as one heat operator can fix the carrier and its
ordering.

## Result

If `C = e^(-sigma^2 H) = e^(-H/Lambda^2)` is the same heat operator, then
exactly `Lambda sigma = 1` for the whole spectrum, closing the
cutoff-correlation identity without observable input. However, for
`Z_M = Tr C_M` the bare action `S_bare = Z_M` and the Gibbs free energy
`F_Gibbs = -sigma^-2 log Z_M` have opposite sign derivatives, so their
minima on any two unequal carriers are always opposite. At
`t = 0.106734039959646...`, scalar traces give `Z_S4 = 1.6196427172` and
`Z_22 = 1.4562989251`: the bare winner is `S^2 x S^2`, the Gibbs winner
`S^4` (with a Dirac-trace counterpart in the gate).

## Links

- [[version4-toe-native-s4-carrier-candidate-gate]] — S4 carrier candidate.
- [[version4-spectral-gibbs-equivalence-gate]] — equivalence gate context.

## Source Notes

- Gate: `s2t/gates/version4_one_kernel_sign_trilemma_gate.tex`.
