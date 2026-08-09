# Finite Spectral Residue Gap

> Status: working
> Type: question
> Updated: 2026-07-15

## Question

Can the small gap

```text
N_need - 10 = 0.0099700224
```

in the `pi^-4` absorption route be derived as a finite same-scheme residue of determinant bookkeeping, or must `pi^-4` be downgraded to structural/phenomenological compression?

## Plain-Language Summary

The current best `pi^-4` route almost lands on the clean rank `10 = 1 + 9`, but not exactly. The missing piece is small enough to look like a normalization or finite determinant residue, yet large enough that it cannot be ignored in a theorem. The next search should therefore test bookkeeping sources, not invent a new sector.

## A--E Scan Result

- **A: `pi^-4` residue.** The strongest current interpretation is absorption: `pi^-4` summarizes a normalized coexact determinant residue rather than adding a separate `Delta_tower^coex` correction.
- **B: determinant bookkeeping.** The most promising hidden source is the same-scheme combination of `det'`, Hodge measure/Jacobian, gauge volume, zero-mode removal, scalar ghost handling, and local subtraction.
- **C: reciprocal/neutrino overlap.** `N_nu^2 = pi + pi^-1` remains a clean parallel test of reciprocal spectral normalization, but it does not directly close C6.
- **D: compact QED/tau shift.** The tau row suggests finite compact one-loop shifts can be structural; this is an analogy, not yet a shared theorem with `pi^-4`.
- **E: `Z2`/holonomy/quotient.** The quotient layer is already central and supplies the carrier/parity scene. It does not by itself cancel the C6 obstruction.

## Candidate Sources Of The Gap

| Candidate | Could Produce Scalar Gap? | Could Shift Rank/Power? | Current Verdict |
|---|---:|---:|---|
| `det'` zero-mode convention | yes | possibly | high-priority bookkeeping check |
| Hodge measure/Jacobian | yes | yes | high-priority same-scheme check |
| Gauge-volume normalization | yes | possibly | high-priority same-scheme check |
| Scalar ghost half-power leakage | yes | yes | dangerous: can destroy rank-10 route |
| Local heat-kernel counterterm | yes | no/limited | allowed only if fixed before fit |
| Coexact projector variation | yes | yes | promising C6 rescue component |
| Hilbert/basis transport | yes | yes | promising C6 rescue component |
| Ricci/curvature block | maybe | no/limited | required, but less likely to explain scheme gap alone |
| New paired Dirac sector | unlikely | yes | naive route failed; only revisit with new mandatory symmetry |
| Holonomy/Z2 parity | limited | yes | already explains carrier/parity, not enough alone |

## Working Hypothesis

The best non-phenomenological hypothesis is:

```text
pi^-4 is a finite normalized spectral residue class.
The visible rank is P02 = 10,
while N_need - 10 comes from same-scheme determinant normalization
or from projector/basis transport in the physical coexact quotient.
```

This hypothesis is testable. It fails if the remaining same-scheme terms cannot produce the needed finite scalar residue without introducing a fitted coefficient.

## Next Test

Build a focused gap audit that takes the existing `N_need` calculation and tests each candidate source above under one normalization convention:

1. fix the physical determinant functional;
2. fix `det'`, gauge-volume, and Hodge-Jacobian conventions;
3. compute or symbolically classify projector and Hilbert/basis transport contributions;
4. decide whether the residual is derived, forbidden, or scheme-dependent.

## Links

- [[finite-gap-source-audit]] — candidate-by-candidate verdict table for the possible sources of the gap.
- [[coexact-tower-delta]] — coexact tower and absorption route.
- [[kappa-cas-one-over-24]] — determinant-scheme risks around the `1/24` branch.
- [[neutrino-overlap-lemma]] — parallel reciprocal-normalization test.
- [[holonomy-and-dirac-sectors]] — holonomy layer and sector-attribution evidence.
- [[s2t-closure-roadmap]] — current C6/C11 roadmap.
- [[current-status-and-next-vectors]] — global status and promising vectors.

## Source Notes

- Source paths: `s2t_determinant_casmix_results.json`, `s2t_full_coexact_delta_results.json`, `s2t_c6_ghost_exact_isolation_results.json`, `s2t_c6_closure_matrix_results.json`, `wiki/questions/kappa-cas-one-over-24.md`, `wiki/syntheses/s2t-closure-roadmap.md`.
- This page records a controlled A--E scan requested on 2026-07-15; it is a question page, not a closure claim.