# Version IV: Gibbs free-energy carrier gate

> Status: conditionally closed
> Updated: 2026-08-11

## Problem

The correlation-purity gate ordered `S4` above `S2 x S2` if the vacuum
maximizes correlation entropy, but the sign was not derived. The primary TOE
text calls the Gaussian kernel a minimum-action spectral state without
writing a normalized density-state functional.

## Search for solution

- Re-read the primary TOE discussion of the dynamic correlation operator and
  minimum-action Gaussian state.
- Normalized the compact heat operator to
  `rho_tau=exp(-tau Delta)/Z(tau)`.
- Reconstructed the canonical Gibbs functional
  `Phi=Tr(rho Delta)-S_vN(rho)/tau`.
- Used quantum relative entropy to prove the sign and unique minimum.
- Compared the resulting carrier free energies at equal four-volume.

## Exact sign identity

```text
Phi_tau[rho;M]-F_tau(M)
  = D(rho || rho_tau)/tau >= 0,
F_tau(M)=-log Z_M(tau)/tau.
```

Klein positivity fixes the entropy sign and makes the Gaussian state the
unique equilibrium minimum. After minimizing over states, carrier selection
is equivalent to maximizing `log Z_M(tau)`.

## Result

For unit-volume round `S4` and equal-radius `S2 x S2`,

```text
Delta log Z = log Z(S4)-log Z(S2 x S2) > 0.
```

At small `tau`,

```text
Delta log Z = [4 pi (sqrt(6)-2)/3] tau + O(tau^2).
```

The large-`tau` sign is also positive because `S4` has the lower first
spectral gap. A 3001-point audit on `1e-5 <= tau <= 2` finds no nonpositive
point. Therefore `F_tau(S4)<F_tau(S2 x S2)` throughout the audited profile.

## Expected result

Prove or reject equivalence between the original TOE spectral action
`Tr f(Chat/Lambda)` and the normalized-state Gibbs functional. If their
carrier extrema agree, the entropy-sign and pairwise carrier gates become a
literal TOE consequence rather than a completion.

## Compliance check

- The entropy sign is derived, not selected after observing the carrier
  ranking.
- The same unit-volume spectra and one `tau=sigma^2` were used.
- The result is explicitly conditional on the normalization
  `Chat -> rho=Chat/Tr Chat`.
- Absolute radius and global carrier-class uniqueness remain open.

## Links

- [[version4-s4-s2xs2-correlation-purity-gate]]
- [[version4-toe-native-s4-carrier-candidate-gate]]
- [[zero-prompt-toe-carrier-trace-2026-08-11]]
- [[version4-observed-reconstruction-roadmap]]
- [[toe]]

## Sources

- `s2t/17705966/TOE.pdf`
- `s2t/gates/version4_gibbs_free_energy_carrier_gate.tex`
- `s2t/audits/s2t_v4_gibbs_free_energy_carrier_gate.py`
- `s2t/results/s2t_v4_gibbs_free_energy_carrier_gate_results.json`