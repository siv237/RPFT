# SU5 Rank Selector Gate

## Decomposition

The torsion involution `diag(1,1,1,-1,-1)` gives

`24 = 8_C + 3_W + 1_Y + 6_X + 6_Xbar`,

with an exact even/odd split `12+12`.

## Strong coupling

The rank functional

`alpha_s(Q)=1/(rank(Q)+pi^2 rank(Q)/24)`

selects the mixed rank-six orbit and yields `1/(6+pi^2/4)`. It is the only
rank orbit entering the atlas rounding bin `0.1181 +/- 0.00005`.

## Weinberg angle

The rank reconstruction

`(r_C-r_W(r_X/24)/pi)/((24-r_W)+(r_W+r_Y)pi)`

with `(r_C,r_W,r_Y,r_X)=(8,3,1,6)` reproduces the atlas formula. Among 120
labelled block permutations, the physical assignment ranks first; the only
tie is `X <-> Xbar`. The next inequivalent value is `0.2226941`.

## Status

The coefficients are uniquely reconstructed from representation ranks, but
the functional forms were read from the atlas. This is a representation-
theoretic reconstruction, not a blind prediction. The next gate is a common
gauge-fixed action deriving both functionals and predicting a hidden third
quantity.

## Evidence

- `s2t_su5_rank_selector_audit.py`
- `s2t_su5_rank_selector_results.json`
- `su5_rank_selector_gate.tex`