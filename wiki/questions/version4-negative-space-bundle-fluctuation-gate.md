# Version IV: negative-space bundle and fluctuation gate

> Status: working
> Research status: forgotten bundle tested; full-field carrier action open
> Type: question
> Updated: 2026-08-11

## Question

Which old no-go results apply only to restricted assumptions, and which
variants requested in early files were never independently tested?

## Forgotten circle bundle

`H2(RP3;Z)=Z2` gives a nontrivial principal circle bundle modeled by

```text
P = (S3 x S1)/[(x,theta) ~ (-x,theta+pi)] ~= U(2).
```

Its scalar modes obey the exact coupled rule `ell+m` even, unlike the direct
product rule `ell` even with arbitrary `m`. This derives parity-momentum
locking rather than choosing projective and circle sectors independently.

The scalar correlation density nevertheless tends to minus infinity when
the base radius shrinks at fixed circle radius. The branch is therefore
closed as a standalone scalar vacuum, though its selection rule remains a
possible ingredient of a future action.

## Genuine omission

All recent `S4` carrier comparisons use a positive scalar heat state. The
complete parent ledger contains three scalars, a massive vector with ghosts,
and two Dirac pairs. Its signed one-loop determinant has never been compared
between `S4` and `S2 x S2` in one renormalization scheme.

This cannot be repaired by inserting the flat supertrace `67` into the
entropy calculation: a signed supertrace is not a positive density state.

## Other gaps

- Warped metrics remain unclassified, but are underdetermined until an
  action supplies the cross term and a finite parameter class.
- The general single-vertex no-go is explicitly unproved; only the minimal
  `Q_cycle` vertex failed.
- The old quark/Skyrmion lattice experiment was never run, but its action is
  phenomenologically postulated and does not close the parent theory.

## Next exact calculation

Compute the renormalized scalar-vector-ghost-Dirac fluctuation action on
fixed-volume `S4` and `S2 x S2`, freeze all local counterterms before the
comparison, and then test the joint geometry Hessian in the TOE 6.5
functional.

## Sources

- `s2t/gates/version4_negative_space_bundle_fluctuation_gate.tex`
- `s2t/audits/s2t_v4_negative_space_bundle_fluctuation_gate.py`
- `s2t/results/s2t_v4_negative_space_bundle_fluctuation_gate_results.json`
- `RPFT-main/ai-promts/First-principles-00-variational.md`
- `s2t/gates/canonical_measure_vertex_localization_gate.tex`