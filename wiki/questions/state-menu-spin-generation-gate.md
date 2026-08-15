# State Menu Spin Generation Gate

> Status: count three passes conditionally; equivalence of generations fails on the bare geometry
> Updated: 2026-08-04

## Reference Selector

- `RP3=L(2,1)` bounds the oriented disk bundle over `S2` with Euler number `2`.
- The filling is spin and has `H1=0`, so it induces one distinguished boundary spin structure.
- `D2` selects the bounding/antiperiodic spin structure on `S1`.
- Their product choice gives one factorwise bounding reference among the four spin structures of `K`.

Therefore exactly three nonreference spin sectors remain.

## Abstract S3

After choosing the reference, spin labels form `F2^2`. The three nonzero vectors are one orbit of

```text
GL(2,2) ~= S3.
```

So an abstract generation-triplet symmetry is available.

## Geometric Obstruction

The integral group is `pi1(K)=Z2 x Z`. Its automorphisms must preserve the unique torsion subgroup. The induced mod-two action has order two, not six, and splits the three nonzero labels into orbits of sizes `1+2`.

Thus bare geometry supplies the count three but not three equivalent generations.

The two `RP3` spin structures also have opposite Dirac eta invariants `+/-1/4`, while the two `S1` structures differ by zero-mode/gap behavior, so the four product sectors are spectrally distinguishable.

## Verdict

The generation count is no longer arbitrary once standard factor fillings define the reference sector. However, a genuine family triplet requires an emergent `S3` action from the `SU(5)` fiber or transition algebra.

The stronger menu-level resolution is developed in [[state-menu-affine-triplet-gate]]: the full affine group is `S4`, and its permutation representation canonically splits as `1+3` without selecting a reference point.

## Evidence

- `s2t/audits/s2t_spin_generation_selector_audit.py`
- `s2t/results/s2t_spin_generation_selector_results.json`
- `s2t/gates/state_menu_spin_generation_gate.tex`
- Primary spectral check: Christian Bär, *The Dirac operator on space forms of positive curvature*; for `RP3`, the two spin structures have eta invariants `+/-1/4`.