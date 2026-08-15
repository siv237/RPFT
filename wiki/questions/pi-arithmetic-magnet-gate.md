# Pi Arithmetic Magnet Gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Question

Does the rank-one tau formula provide evidence for a special role of `pi`, or
does the frozen grammar form a dense arithmetic net?

## Frozen grammar

`x^2 + n*x + p/q + c*alpha`, with `n=0..4`, reduced `|p|<=4`, `q<=6`, and
`c in {0, +/-1, +/-1/2, +/-1/3, +/-2/3}`.

## Exact results

- Observed tau-ratio error: `0.0006679209`.
- Coverage of the full grammar support at that tolerance: `9.25%`.
- Coverage in a width-2 window around the tau ratio: `13.02%`.
- Exact fraction of bases `x in [2,4]` beating or matching `pi`: `9.08%`.
- With complexity no greater than the claimed formula: `5.40%` of bases.
- Removing the `c*alpha` fine-adjustment reduces full-support coverage from
  `9.25%` to `1.07%`.

## Interpretation

The tau expression is genuinely the closest member of the frozen list, but
that rank does not include the look-elsewhere effect over target values, base
constants, grammar choices, or earlier search decisions. Constants `e` and
`sqrt(10)` both admit closer formulas inside the same grammar.

## Verdict

`pi` behaves as part of an arithmetic magnet rather than as a statistically
unique signal. This does not falsify the formula; it removes the numerical
coincidence as standalone physical evidence. A prospective operator-derived
prediction remains required.

## Evidence

- `s2t/audits/s2t_pi_arithmetic_magnet_audit.py`
- `s2t/results/s2t_pi_arithmetic_magnet_results.json`
- `s2t/gates/pi_arithmetic_magnet_gate.tex`