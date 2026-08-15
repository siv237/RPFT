# Anomaly-Free Holonomy Projection

> Status: working
> Research status: constructive candidate
> Type: question
> Updated: 2026-08-04

## Parent Content

Use the vectorlike `SU(5)` parent

```text
(10+10bar) + 2(5+5bar) + 5_H.
```

The fermionic cubic anomaly vanishes pairwise. Any surviving `U` and `D` modes are vectorlike, so the projected low-energy sector is also anomaly-free.

## Two Geometric Holonomies

In the fundamental representation define

```text
h=exp(i 3 pi Y)=diag(-1,-1,-1,-i,-i),
P5=h^2=diag(+1,+1,+1,-1,-1).
```

`h` has order four and determinant one. Interpret `P5` as the `RP3` `Z2` holonomy and `h` as the quarter branch on `S1`. Assign conjugate flat characters `+1` to `10+10bar`, `-1` to both `5+5bar` copies and `-i` to `5_H`.

## Zero-Mode Table

The total phase is `P5 * i^(6Y) * flat_character`. A periodic zero mode requires total phase `+1`.

```text
U:   +1   survives,
Q:   -i   projected,
E:   -1   projected,
D:   +1   survives twice,
L:   +i   projected,
H:   +1   survives,
T_H: +i   projected.
```

The surviving content is exactly one vectorlike `U`, two vectorlike `D` fields and one complex Higgs doublet. Its beta direction is `(17/6,1/6,2)`.

## Status

The inverse hint now has an anomaly-free parent and a concrete `Z2/Z4` projection using structures already present in the model. The projected partners have fixed circle shifts: quarter branches for `Q`, `L` and `T_H`, and a half branch for `E`.

The character assignment must still follow from S2T sector attribution rather than being selected for this result. The finite `RP3 x S1` determinant difference between periodic survivors and shifted partners must also produce the required magnitude.

## Determinant Follow-Up

The common-spectrum determinant has now been computed and fails directionally. The shifted partner tower has fixed color/weak ratio `9/20`, whereas the gauge scorecard requires about `11.014`. See [[projected-kk-determinant-gate]]. The surviving possibility is intermediate-scale running of the periodic split sector, not the finite shifted-partner determinant alone.