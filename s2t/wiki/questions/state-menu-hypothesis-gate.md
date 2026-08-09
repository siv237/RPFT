# State Menu Hypothesis Gate

> Status: passes as an abelian kinematic skeleton; fails as a standalone particle theory
> Updated: 2026-08-04

## Hypothesis

Interpret `K=RP3 x S1` as a menu/configuration space of global quantum gluing and phase sectors rather than as literal compact space.

## Exact Structure

- `pi1(K)=Z2 x Z`.
- Flat `U(1)` moduli are `{+1,-1} x U(1)`: two disjoint circles.
- Spin structures form a torsor over `H1(K,Z2)=Z2 x Z2`: four choices.
- If spin structures are included as menu components, the enlarged menu is eight circles.
- Stable loop labels are `(epsilon,n) in Z2 x Z`.

## Positive Gate

The reinterpretation is mathematically coherent and naturally supplies:

- a torsion/parity label;
- an integer winding label;
- continuous phase position;
- global spin-sector choices.

## No-Go

`pi1(K)` is abelian. Every finite-dimensional unitary representation splits into one-dimensional characters. Therefore base-loop holonomy alone cannot produce irreducible `SU(2)` doublets or `SU(3)` triplets.

The natural component counts are `2`, `4`, and `8`, not a canonical `3`; topology also supplies no mass or transition operator.

## Verdict

The hypothesis survives as an abelian kinematic classification of global sectors. It fails as a complete particle theory.

The next admissible gate is a single nonabelian fiber/groupoid over the two-circle menu. It must generate both an `SU(2)` doublet and an `SU(3)` triplet without independent sector choices.

This follow-up gate is now completed positively in [[state-menu-su5-fiber-gate]] using a minimal `SU(5)` fiber and the existing order-two torsion holonomy.

## Evidence

- `s2t_state_menu_hypothesis_audit.py`
- `s2t_state_menu_hypothesis_results.json`
- `state_menu_hypothesis_gate.tex`
