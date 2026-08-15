# State Menu SU5 Fiber Gate

> Status: working
> Research status: positive group/representation gate; generations and masses open
> Type: question
> Updated: 2026-08-04

## Question

Can one minimal nonabelian fiber over the two-circle state menu produce both color and weak multiplets without separate sector choices?

## Minimality

The Standard Model gauge group has rank four. In the compact simple rank-four census, `SU(5)` has the smallest Lie-algebra dimension:

- `SU(5)`: 24
- `SO(8)`: 28
- `SO(9)`, `Sp(8)`: 36
- `F4`: 52

## Z2 Holonomy

Use the existing torsion branch as

```text
P = diag(1,1,1,-1,-1) in SU(5).
```

It satisfies `P^2=I`, `det P=1`, and

```text
C_SU5(P)=S(U3 x U2)=(SU3 x SU2 x U1)/Z6.
```

The unbroken algebra has dimension `12=8+3+1`; the other 12 generators are broken.

## One Generation

The anomaly-free chiral package

```text
10 + bar5
```

branches into exactly `Q,u_c,e_c,d_c,L` with the standard hypercharges. All checked gauge and mixed anomalies vanish.

The same `P` makes both weak doublets `Q,L` odd and every weak singlet even. This is a genuine shared parity rule, not separate sector assignment.

## Remaining No-Go

There are four spin structures. The tempting count `4-1=3` is not yet a generation theorem because spin structures form a torsor with no canonical zero. A prior invariant must select the excluded reference sector.

The construction also does not derive the choice `10+bar5`, Yukawa matrices, symmetry-breaking scales or masses.

## Verdict

This gate is positive: one minimal `SU(5)` fiber plus the existing `Z2` branch produces the SM gauge subgroup, one anomaly-free generation and a unified doublet/singlet parity split.

Next gate: find a geometric invariant of the four spin structures that selects one reference sector and leaves three equivalent sectors without using the observed generation count.

The follow-up [[state-menu-spin-generation-gate]] finds a factorwise bounding reference and hence exactly three nonreference sectors, but bare geometric automorphisms split them into `1+2`; full generation equivalence remains open.

## Evidence

- `s2t/audits/s2t_state_menu_su5_fiber_audit.py`
- `s2t/results/s2t_state_menu_su5_fiber_results.json`
- `s2t/gates/state_menu_su5_fiber_gate.tex`