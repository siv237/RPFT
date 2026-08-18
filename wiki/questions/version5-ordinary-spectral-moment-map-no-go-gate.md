# Version V ordinary spectral moment-map no-go

> Status: mature
> Type: question
> Updated: 2026-08-15

## Problem

Can an ordinary spectral functional depending only on `Spec(D^2)` derive the
oriented three-node quiver potential `Tr(XXdagger-YdaggerY)^2`?

## Exact result

For the odd three-node operator, write

`M=(X,Ydagger)`, `A=XXdagger`, `B=YdaggerY`.

Then `MMdagger=A+B`, so every ordinary functional `Tr f(D^2)` depends on
the two arrows only through the sum `A+B` (up to the fixed zero-mode term).
The family

`A_t=tS`, `B_t=(1-t)S`

has identical spectrum and identical spectral moments for all `t`, while

`Tr(A_t-B_t)^2=(2t-1)^2 Tr(S^2)`

varies. Therefore the oriented moment-map norm cannot be reconstructed from
ordinary spectral data on the full configuration space.

At quartic order the mismatch is explicit:

- `Tr D^4 = 2 Tr(A+B)^2`, with a positive mixed term;
- `Tr(A-B)^2` has the required negative mixed term.

The unprojected supertrace does not rescue the construction: positive even
powers cancel between the two gradings, while a general heat supertrace
retains index/zero-mode data rather than a varying moment-map potential.

## Scope boundary

Closed by this theorem:

- ordinary `Tr f(D^2)` and functions of its spectral moments;
- determinant functionals using only singular values;
- an unprojected graded supertrace.

Not decided:

- node-relative or conditionally projected curvature;
- an auxiliary moment-map field;
- twisted or derived calculi and BV/BFV structures;
- relative modular or explicitly nonlocal boundary functionals.

These are genuinely new architectures because they add orientation-sensitive
data. They may be tested, but may not be presented as consequences of the
ordinary one-trace spectral action alone.

## Verdict

- spectral-blindness theorem: pass;
- positive-cross quartic corollary: pass;
- supertrace rescue: fail;
- ordinary one-trace origin of the quiver moment map: closed;
- physical closure: not passed.

The completed [[version5-nonordinary-architecture-fork-gate]] selects the
oriented height--Hodge construction for one full-KO6 kill-test.

## Links

- [[version5-family-algebra-rectangle-gate]]
- [[version5-nonordinary-architecture-fork-gate]]
- [[version4-family-defect-ko6-quiver-embedding-gate]]
- [[version4-family-defect-quiver-moment-map-gate]]
- [[version5-project-literature-novelty-gate]]

## Source Notes

- `s2t/gates/version5_ordinary_spectral_moment_map_no_go.tex`
- `s2t/audits/s2t_v5_ordinary_spectral_moment_map_no_go.py`
- `s2t/results/s2t_v5_ordinary_spectral_moment_map_no_go_results.json`
- Chamseddine--Connes spectral action, `arXiv:hep-th/9606001`.
- Quiver moment-map background, `arXiv:0807.4734`.
- McKean--Singer/index background, `arXiv:2307.11061`.