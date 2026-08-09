# Finite Gap Source Audit

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

Which concrete mechanism can still explain the small absorption-route gap

```text
N_need - 10 = 0.0099700224
```

without adding a fitted coefficient or a new broad sector?

## Plain-Language Result

The gap is probably not a hidden large physical tower. Most obvious bookkeeping routes either change the rank too much, leave a dangerous scalar half-determinant, or only affect local terms. The still-live possibilities are narrower: the physical transverse quotient definition, coexact-projector variation, Hilbert/basis transport, and a pre-fixed local/finite subtraction convention. If those fail, `pi^-4` should be downgraded from theorem to structural compression.

## Source Audit Table

| Candidate | Evidence In Project | Can Explain Tiny Gap? | Risk | Verdict |
|---|---|---:|---|---|
| `det'` zero-mode convention | `kappa-cas-one-over-24` says zero modes are essential; `det'` removes the true `(0,0)` mode. | maybe | mostly integer/log-scale shifts, not naturally `0.009970` | keep as part of same-scheme check, not enough alone |
| Hodge measure/Jacobian | `current-status` says standard FP may leave scalar half-power until Hodge Jacobian, `det'`, and gauge volume are combined. | maybe | if it leaves scalar half-power, rank becomes effectively `5`, not `10.009970` | required check, but dangerous not automatically helpful |
| Gauge-volume normalization | `Gamma_zero/gauge` handles gauge volume and removed scalar zero mode. | maybe | likely fixes powers/zero modes, not finite coexact tail | required same-scheme component, not enough alone |
| Scalar ghost half-power leakage | Standard covariant FP gives `Gamma = 1/2 log det' Delta_1,coex - 1/2 log det' Delta0`. | no as rescue | changes effective rank from `10` to `5`; relative error `1.53e-3` | downgrade trigger unless removed/cancelled |
| Local heat-kernel counterterm | Local counterterms are recognized in formal `Gamma_M+gh`. | limited | cannot remove nonlocal finite Bessel/winding tail unless convention fixed before fit | allowed only as pre-fixed scheme, not ad hoc rescue |
| Coexact projector variation | Listed as remaining full-operator block; affects what counts as physical coexact sector. | yes | may be nonlocal/scheme-sensitive; not yet computed | best live C6-rescue component |
| Hilbert/basis transport | Existing skeleton says fixed-metric Gram trace is not final if Hilbert metric and orthonormal basis move. | yes | no canonical transport/basis convention selected yet | best live normalization component |
| Ricci/curvature block | Required remaining operator block. | weak/maybe | likely ordinary operator contribution, not pure bookkeeping gap | must compute, but not primary gap explanation |
| Principal + connection cancellation | Already assembled and verified. | no | nonzero for all `55`; no internal cancellation | ruled out as cheap rescue |
| New paired Dirac/spin sector | Naive Maxwell--ghost--Dirac pairing rejected. | unlikely | wrong spectrum or unnatural prefactors | fallback only with new mandatory symmetry |
| Holonomy/Z2 quotient | Explains carrier, parity, `pi` branch, and rank scene. | limited | already baked into `RP3` quotient; not a new gap source | background structure, not sufficient |

## Current Decision

The most promising next proof target is not a new sector. It is the same-scheme reduced determinant:

```text
Gamma_phys[g]
  = 1/2 log det' Delta_1,coex[g]
    + Gamma_zero/gauge[g]
    + Gamma_projector[g]
    + Gamma_Hilbert/basis[g]
    + Gamma_local.fixed[g]
```

The scalar ghost/exact sector must either be removed by defining the physical transverse quotient, or be proven to cancel in the same normalization. If it remains as a nonzero scalar half-determinant, the rank-10 absorption route is not a theorem.

## Next Computation-Facing Steps

1. **Projector block:** derive the second variation of the coexact projector in the same `n=1/n=3` quotient-normalized basis.
2. **Hilbert/basis block:** choose a canonical basis-transport convention and compute the Gram/Hilbert correction to `C11`.
3. **Scalar-FP verdict:** decide whether the project uses the physical transverse quotient as definition, or keeps standard covariant FP and must cancel the scalar half-power.
4. **Local scheme lock:** state which finite local counterterms are fixed before fitting; forbid post-hoc counterterms aimed at `0.0099700224`.
5. **Downgrade gate:** if no same-scheme source produces the gap, mark `pi^-4` as structural compression while preserving `S_geo`, `m_tau`, and the Higgs EFT bridge.

## Links

- [[projector-hilbert-rescue-sprint]] — next computation-facing sprint for the best live rescue components.
- [[finite-spectral-residue-gap]] — parent question page for the gap.
- [[coexact-tower-delta]] — coexact tower and absorption route.
- [[kappa-cas-one-over-24]] — determinant and zero-mode proof risk.
- [[s2t-closure-roadmap]] — C6/C11 roadmap.
- [[current-status-and-next-vectors]] — global status and next vectors.

## Source Notes

- Source paths: `s2t_determinant_casmix_results.json`, `s2t_c6_ghost_exact_isolation_results.json`, `s2t_c6_closure_matrix_results.json`, `s2t_c6_l21_delta2_second_hilbert_formula_results.json`, `wiki/questions/kappa-cas-one-over-24.md`, `wiki/syntheses/current-status-and-next-vectors.md`, `wiki/syntheses/s2t-closure-roadmap.md`.