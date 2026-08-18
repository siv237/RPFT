# Version V twisted family automorphism gate

> Status: mature
> Type: question
> Updated: 2026-08-16

## Problem

Does the current finite algebra
`R_0 direct_sum M3(R)_G direct_sum C_2` admit a coefficient-free canonical
twist capable of supplying the orientation missing from the ordinary
spectral action?

## Automorphism classification

The three simple real star ideals have dimensions `1`, `9`, `2` and are
pairwise nonisomorphic. Every automorphism must therefore fix all three
primitive central idempotents. There is no exchange automorphism between
the current summands.

The remaining star automorphisms are:

- identity on `R`;
- inner orthogonal conjugations on `M3(R)`;
- identity or complex conjugation on `C`.

A particular noncentral orthogonal conjugation is a continuous gauge-basis
choice, not a canonically selected orientation. After excluding such a new
selector, only identity and complex conjugation remain as discrete classes.

## Radial witness

On `X=rho I3`, `Phi=r` real, the remaining discrete classes act trivially.
They therefore cannot replace

`6(rho^2+r^2)^2`

by the required

`(rho^2-r^2)^2`.

At `rho=r=1` the two values are respectively `24` and `0`.

## Literature boundary

Known grand-symmetry and minimal twists use a flip between isomorphic
represented copies. The current algebra contains no such pair. This closes
only the coefficient-free twist of the current algebra, not twisted spectral
geometry after algebra enlargement.

## Reopening menu

Duplicating exactly one of `R`, `M3(R)` or `C` gives four simple summands and
remains inside the frozen Version V budget. Doubling the whole algebra gives
six and exceeds it. No selective duplication yet has a representation,
real structure or twisted first-order proof.

## Verdict

- simple-ideal automorphism classification: pass;
- exchange twist of the current algebra: absent;
- canonical radial sign repair: fail;
- coefficient-free current-algebra twist: closed;
- selective minimal doubling: not decided;
- physical closure: not passed.

The completed [[version5-minimal-twist-doubling-budget-gate]] selects the
real-scalar duplication for one explicit twisted-KO6 representation test.

## Links

- [[version5-oriented-height-hodge-ko6-gate]]
- [[version5-minimal-twist-doubling-budget-gate]]
- [[version5-nonordinary-architecture-fork-gate]]
- [[pati-salam-twisted-connector-threshold-gate]]
- [[version5-finite-geometry-complexity-bound-gate]]

## Source Notes

- `s2t/gates/version5_twisted_family_automorphism_gate.tex`
- `s2t/audits/s2t_v5_twisted_family_automorphism_gate.py`
- `s2t/results/s2t_v5_twisted_family_automorphism_gate_results.json`
- Grand-symmetry exchange twist: `arXiv:1503.03861`, `arXiv:1411.1320`.
- Real/minimal twists: `arXiv:1601.00219`, `arXiv:2010.15367`.
- Review of finite minimal twists: `arXiv:2301.08346`.