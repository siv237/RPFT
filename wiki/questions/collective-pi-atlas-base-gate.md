# Collective Pi Atlas Base Gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Retrospective Test

Eleven existing atlas formulas were evaluated with a common base `x in [2,4]`
and equal-weight RMS logarithmic error. The score at `pi` is `0.01827893`; the
best grid base is `3.16422` with score `0.01587965`.

`pi` lies in the best `2.27%` of the scanned interval, but it is not unique:
`sqrt(10)` and `22/7` both score slightly better. Leave-one-out optima remain
between `3.15535` and `3.17735`, so the common-base effect is collective rather
than caused by one claim.

## Verdict

The atlas has nontrivial shared-base compression near `3.16`, but the test is
retrospective and does not identify `pi` as the physical base. A prospective
test remains blocked until an operator selector assigns a previously hidden
observable to a frozen formula without using its measured value.

## Evidence

- `s2t/audits/s2t_collective_pi_atlas_base_audit.py`
- `s2t/results/s2t_collective_pi_atlas_base_results.json`
- `s2t/gates/collective_pi_atlas_base_gate.tex`