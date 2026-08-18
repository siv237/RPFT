# Version V minimal twist doubling budget gate

> Status: working
> Type: question
> Updated: 2026-08-16

## Problem

Which single summand may be duplicated to create a genuine flip while
remaining inside the four-summand Version V budget and avoiding unnecessary
new gauge structure?

## KO6 support audit

For the particle/conjugate vertices

`(0,0)+, (G,0)-, (G,2)+, (0,0)-, (0,G)+, (2,G)-`,

the left/right label occurrences are:

| Summand | Plus | Minus |
|---|---:|---:|
| `R0` | 3 | 3 |
| `M3(R)_G` | 2 | 2 |
| `C2` | 1 | 1 |

Each selective duplication therefore has provisional support on both
chiralities without adding fermionic dimensions.

## Incidence and cost

- Duplicating `R0` touches both `X` and `Y` and adds no continuous gauge
  generators.
- Duplicating `M3(R)_G` touches both arrows but adds three generators before
  diagonal reduction.
- Duplicating `C2` touches only `Y` and adds one generator.
- Doubling the complete algebra produces six simple summands and violates
  the frozen budget.

## Selected branch

The lexicographic rules select

`R0,+ direct_sum R0,- direct_sum M3(R)_G direct_sum C2`

with the flip exchanging the two real scalar copies. Selection applies only
to one explicit representation test.

It remains unknown whether both copies act faithfully, whether the flip is
compatible with `J`, grading and twisted order conditions, and whether the
radial quartic acquires the required negative mixed sign.

## Verdict

- exhaustive selective menu: pass;
- full algebra doubling: rejected by budget;
- complex duplication: deferred by one-arrow coverage;
- matrix duplication: eligible but higher gauge cost;
- real scalar duplication: selected for one kill-test;
- twisted parent action and physical closure: not passed.

The completed [[version5-real-scalar-flip-twisted-ko6-gate]] passes as a
faithful real twisted geometry but fails dynamically: its ordinary spectral
quartic still has the Gram-sum sign.

## Links

- [[version5-twisted-family-automorphism-gate]]
- [[version5-real-scalar-flip-twisted-ko6-gate]]
- [[version5-finite-geometry-complexity-bound-gate]]
- [[version5-oriented-height-hodge-ko6-gate]]
- [[pati-salam-twisted-connector-threshold-gate]]

## Source Notes

- `s2t/gates/version5_minimal_twist_doubling_budget_gate.tex`
- `s2t/audits/s2t_v5_minimal_twist_doubling_budget_gate.py`
- `s2t/results/s2t_v5_minimal_twist_doubling_budget_gate_results.json`
- Minimal and real twists: `arXiv:1601.00219`, `arXiv:2010.15367`.
- Finite minimal-twist review: `arXiv:2301.08346`.