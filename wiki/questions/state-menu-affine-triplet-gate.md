# State Menu Affine Triplet Gate

> Status: positive canonical `1+3` family-space construction; hierarchy open
> Updated: 2026-08-04

## Core Shift

If the four spin structures are treated as an abstract affine menu rather than literal geometric sectors, their intrinsic relabeling group is

```text
AGL(2,2) = F2^2 semidirect GL(2,2) ~= S4.
```

## Canonical Decomposition

The four-dimensional permutation representation decomposes as

```text
C4 = 1_uniform + 3_sum-zero.
```

The projectors are

```text
P1 = J/4,
P3 = I - J/4.
```

The commutant of the full affine action is exactly `span{I,J}`, so every invariant transition operator preserves this split.

Examples:

- complete-graph Laplacian `L=4I-J` has spectrum `(0,4,4,4)`;
- rank-one singlet mass `M=J` has spectrum `(0,0,0,4)` and leaves a canonical rank-three kernel.

## SU5 Combination

Tensoring the triplet with one anomaly-free `10+bar5` package gives three identical anomaly-free generations:

```text
H_matter = im(P3) tensor (10+bar5).
```

This derives the family count from a representation split rather than selecting three individual spin structures.

## Caveat

Full affine `S4` is a symmetry of the abstract menu, not of the bare geometry `K`. Treating it as physical is the new III.0 principle.

Exact symmetry also makes the generations degenerate. The next gate must project the previously derived geometric `1+2` subgroup breaking onto the triplet and test whether it produces a fixed family splitting without a free Yukawa matrix.

This projection is completed in [[state-menu-family-rank-one-gate]] and yields the canonical leading spectrum `(0,0,1)`.

## Evidence

- `s2t/audits/s2t_affine_spin_menu_triplet_audit.py`
- `s2t/results/s2t_affine_spin_menu_triplet_results.json`
- `s2t/gates/state_menu_affine_triplet_gate.tex`