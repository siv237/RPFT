# S2T II.A/II.B External Reproduction Protocol

Freeze date: 2026-08-07

## Independence Rules

1. Do not use project audit scripts or copy their numerical tables.
2. Implement modules M1--M6 from `specification/statements.md` and `allowed_inputs.json`.
3. Commit the independent source-code hash and `submission/independent_results.json` before expected outputs are unsealed.
4. Evaluate every failure criterion in `specification/failure_criteria.json`.
5. Review the analytical derivations independently of the numerical implementation.

## Two Required Levels

- **Computational reproduction:** independent implementation matches the mathematical outputs within declared tolerances.
- **Mathematical replication:** independent review confirms operator domains, multiplicities, quotient projections, regularization choices, and logical no-go implications.

Both levels are required before the frozen score may move from `R_sci=4/10` to `5/10`.

## Blind Handling

Physical observables and train anchors are excluded from this package. The release distribution contains only the SHA-256 commitment to the canonical expected-results payload. The custodian reveals that payload after the independent submission is frozen.