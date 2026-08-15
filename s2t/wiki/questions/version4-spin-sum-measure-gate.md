# Version IV: spin-sum measure gate

> Status: closed negatively for the current parent action
> Updated: 2026-08-11

## Problem

The fermion relative determinant ranks the antiperiodic `S1` branch below
the periodic branch. This becomes a physical selection only if the parent
partition function actually sums over spin structures with fixed relative
weights.

## Search for solution

- Inspected the almost-commutative Hilbert space and BV complex.
- Checked whether any field maps one spinor bundle into another.
- Tested whether the `H^1(K,Z2)=Z2^2` torsor itself forces equal weights.
- Compared the result with the legacy RPFT choice of periodic spatial
  boundary conditions.

The current theory defines `L2(K,S_s) tensor H8` for one fixed spin
structure. It contains no spin-transition field, direct-sum groupoid
Hilbert space, `Z2` topological gauge sector, spin-TQFT weight, or
cobordism prescription.

## Expected result

If a canonical spin-sum measure were present, the scheme-independent
determinant inequality would promote the antiperiodic branch from a ranking
to a dynamic selection.

## Compliance check

The operator ledger instead gives four separate fixed-background theories.
Equal counting weights would be unique only after postulating the full spin
torsor translation symmetry as a physical symmetry; that postulate is not
derived by the current algebra or BV complex.

## Verdict

The strict result is

```text
Gamma_AP < Gamma_P                 proved relative ranking
beta_S1 = 1/2 dynamically chosen  not derived
```

The legacy claim that a spatial circle forces periodic fermions is also too
strong. A spatial circle admits both spin structures; antiperiodicity is
specifically thermal only when the circle is Euclidean time. Periodicity may
still be frozen as a model input.

## Next options

1. Freeze periodic or antiperiodic `S1` spin structure as explicit
   background input and continue the zeta calculation.
2. Build a new `Z2`/spin-TQFT measure and repeat anomaly, reality, and
   determinant gates.

The possible use of the same branch ratio as a mass-scale selector has now
been tested in [[version4-spin-branch-mass-stationarity-gate]]. Its
derivative has one sign for every positive `chi R`, so no nonzero stationary
scale exists.

## Links

- [[holonomy-and-dirac-sectors]]
- [[version4-observed-reconstruction-roadmap]]
- [[version4-corrected-zero-mode-pfaffian-gate]]
- [[version4-spin-branch-mass-stationarity-gate]]

## Sources

- `version4_spin_structure_relative_determinant_gate.tex`
- `version4_spin_sum_measure_gate.tex`
- `s2t_v4_spin_sum_measure_gate_results.json`
- legacy conflict: `RPFT-main/rigorous/CRITIQUE.md` and
  `RPFT-main/rigorous/30_qed_one_loop_proof.md`