# Version IV: spectral-action/Gibbs equivalence gate

> Status: working
> Research status: exact equivalence closed negatively; operator dictionary corrected
> Type: question
> Updated: 2026-08-11

## Problem

The Gibbs completion selects the Gaussian state and round `S4`, but Tome IV
still had to prove whether it is the same functional as Postulate 2 of the
primary TOE document.

## Search for solution

- Visually checked page 2 of `s2t/17705966/TOE.pdf`.
- Confirmed the literal formula `S[Chat]=Tr f(Chat/Lambda^2)` followed by a
  claimed Seeley-DeWitt expansion.
- Tested trace-class behaviour for a standard cutoff with `f(0)>0`.
- Reconstructed the unbounded generator from the correlation operator.
- Compared composition laws of trace spectral actions and Gibbs free energy.

## First obstruction

For an infinite-rank compact positive operator, correlation eigenvalues
approach zero. If `f(0)` is nonzero, then eigenvalues of `f(Chat/Lambda^2)`
approach `f(0)`, so the operator is not trace class.

For `f(u)=exp(-u)` on unit-volume `S4`, partial traces grow from about
`1.7e3` at shell 10 to `3.77e6` at shell 80. The raw TOE formula therefore
cannot be the conventional spectral action with an ordinary cutoff.

## Corrected dictionary

The unbounded generator is recovered exactly:

```text
H_C = -log(Chat)/tau = Delta.
```

The standard EFT spectral action must therefore be

```text
S_EFT[Chat] = Tr f(-log(Chat)/(tau Lambda^2))
            = Tr f(Delta/Lambda^2).
```

This is the functional that admits the Seeley-DeWitt expansion.

## Equivalence no-go

Every scalar trace functional is additive on direct sums. Gibbs free energy
is not:

```text
F(C1 direct-sum C2) = -log(Tr C1 + Tr C2)/tau.
```

For `Z1=2`, `Z2=3`, the direct-sum free energy is `-log 5`, while the sum of
free energies is `-log 6`. Therefore no scalar `f` can make
`Tr f(Chat)` identical to `-log Tr Chat/tau` on all operators.

## Result

One Gaussian correlation operator has two compatible but inequivalent
readings:

```text
local EFT dynamics:       Tr f(-log C/(tau Lambda^2)),
global carrier selection: -log Tr C/tau.
```

They should be applied sequentially rather than added with a new arbitrary
relative coefficient.

## Expected result

Formalize the two-stage parent principle: first minimize the normalized
state free energy over carriers, then derive local observed dynamics from
the corrected logarithmic-generator spectral action on the selected
carrier.

## Compliance check

- The primary PDF formula was visually verified.
- Divergence and additivity arguments are operator-level, not fitted
  numerics.
- Exact equivalence is rejected rather than asserted.
- The fundamental Gaussian correlation operator is retained.

## Links

- [[version4-gibbs-free-energy-carrier-gate]]
- [[version4-s4-s2xs2-correlation-purity-gate]]
- [[version4-toe-native-s4-carrier-candidate-gate]]
- [[version4-observed-reconstruction-roadmap]]
- [[toe]]

## Sources

- `s2t/17705966/TOE.pdf`, page 2
- `s2t/gates/version4_spectral_gibbs_equivalence_gate.tex`
- `s2t/audits/s2t_v4_spectral_gibbs_equivalence_gate.py`
- `s2t/results/s2t_v4_spectral_gibbs_equivalence_gate_results.json`