# State Menu Family Rank-One Gate

> Status: positive leading family texture; light-family masses and mixing open
> Updated: 2026-08-04

## Input

The affine spin menu gives the canonical family triplet `im(I-J/4)`. Bare geometry retains one nontrivial involution

```text
S:(p,q) -> (p,q+p).
```

On the triplet,

```text
Spec(S)=(-1,+1,+1).
```

## Rank-One Texture

The unique odd projector

```text
P_minus=(I-S)/2
```

has triplet spectrum

```text
(0,0,1).
```

Therefore a leading family mass/Yukawa operator proportional to `P_minus` gives one heavy family and two massless families, up to an overall scale and permutation.

If the same projector acts in the up and down sectors, the leading CKM matrix is the identity; small mixing requires subleading breaking.

## Limit

No second parameter-free operator currently splits the even two-dimensional family subspace. A generic `2x2` perturbation is forbidden as a hidden fit.

## Verdict

The state-menu branch now derives a qualitative flavor chain:

```text
4 spin states -> 1 + 3 families -> 2 light + 1 heavy.
```

It does not yet derive light-family masses, mass ratios, CKM angles or sector-dependent misalignment.

## Evidence

- `s2t_family_rank_one_breaking_audit.py`
- `s2t_family_rank_one_breaking_results.json`
- `state_menu_family_rank_one_gate.tex`
