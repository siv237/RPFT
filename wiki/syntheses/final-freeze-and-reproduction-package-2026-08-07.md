# Final Freeze and Reproduction Package — 2026-08-07

> Status: mature
> Type: synthesis
> Updated: 2026-08-15

## Summary

The II.A/II.B scientific status was frozen on 2026-08-07 at
`R_sci=4/10` and `N_closed_physical=0` pending independent computational
reproduction and mathematical replication. The repository reorganization of
2026-08-15 changed file locations but did not upgrade this scientific status.

## Package Layout

- `s2t/docs/final_freeze_reproduction_protocol.tex` — human-readable freeze protocol.
- `s2t/reproduction_package/FREEZE_MANIFEST.json` — current integrity manifest.
- `s2t/reproduction_package/REPRODUCTION_PROTOCOL.md` — independence and blind-handling rules.
- `s2t/reproduction_package/specification/` — frozen statements, allowed inputs and failure criteria.
- `s2t/reproduction_package/submission/` — location for an independent submission.

## Status Boundary

The package exposes mathematical modules M1--M6. Physical observables are
excluded from the sealed reproduction payload. Passing the package can raise
the external reproducibility status, but cannot by itself create a closed
physical prediction.

## Links

- [[global-falsification-closure-audit]] — why the physical closure count is zero.
- [[theorem-status-ledger-2026-08-04]] — proved, conditional and failed claims.
- [[version4-tome-conclusion]] — later project-wide status boundary.