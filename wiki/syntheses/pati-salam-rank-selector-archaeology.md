# Pati-Salam Rank-Selector Archaeology

> Status: working
> Type: synthesis
> Updated: 2026-08-14

## Summary

The project already contained the pieces of an exact repair for the composite
Pati-Salam vacuum. A direct and a crossed quadratic Delta path differ by the
antisymmetric `(1_R,6_4)` channel, and the squared norm of their raw
difference is exactly `4 det(Delta Delta^dagger)`. The same coefficient `4`
appears independently as the combined `SU(2)_R + SU(4)` Casimir gap between
the desired `(3,10)` and unwanted `(1,6)` sectors.

## Key Points

- `||H_direct-H_crossed||^2 = 4 det(Delta Delta^dagger)`.
- The difference is weak-antisymmetric and color-antisymmetric, hence belongs
  to `(1_R,6_4)`.
- In `V=-rho^2+tau^2+kappa det`, the six bad Hessian eigenvalues are
  `sqrt(2)(kappa-2)`.
- The project-derived value `kappa=4` changes the signature from `(1,9,6)` to
  `(7,9,0)` and removes the rank-two competing stationary branch.
- Existing precedents supply rank-one projectors, relative path signs,
  Krajewski-loop interference, Casimir gaps and decorated traces.
- The remaining gap is geometric: derive both paths and their relative sign
  from one admissible KO6 finite graph or superconnection.

## Compatibility Update

The follow-up KO6 audit passes. The wedge channel is a symmetric
right-Majorana block, its Jacobian has rank six at the rank-one vacuum, the
nine-dimensional gauge orbit and the radial direction lie in its kernel, and
the channel itself vanishes at the vacuum. The only remaining obstruction is
deriving the doubled path and relative sign from one parent graph.

## Parent-Graph Update

An exterior-square three-node chain supplies a minimal equivariant carrier.
Its two-step composition is `Lambda2 Delta`, and the ordinary raw spectral
trace contains a positive determinant coefficient throughout `0<c^2<8`.
At canonical normalization the rank-one Hessian is
`14 (1), 0 (9), 98/19 (6)`. A subsequent associative-module audit corrects
its status: the color-six endpoint is not an `M4(C)` module, so the literal
Krajewski-node route is closed. The surviving route is a represented
degree-two curvature channel on the existing Pati-Salam Hilbert module.

## Junk and Mapping-Cone Update

The projected-curvature mechanism is now sharper. The relative edge metric
is fixed by the Frobenius isometry and endpoint reflection/reality, so `c=1`
is not a fitted weight. The standard junk quotient does not retain the
endpoint path in the minimal node calculus. A canonical projector nevertheless
exists as the normalized commutator with the unique reflection-odd coordinate
of the three-node path. The remaining freedom is therefore the choice of a
relative mapping-cone action, not a coefficient or matrix projector.

## Relative Quotient and BV-Fork Update

The fixed-point quotient norm canonically reproduces
`4 det(Delta Delta^dagger)` on even curvature. Standard BV auxiliaries cannot
generate this classical term, and the carrier is absent from the old
fermionic module. The remaining choice is a physical vectorlike extension or
a non-propagating classical mapping-cone sector.

## Irreducible-Cycle Update

Connected-cycle irreducibility resolves the identical-copy ambiguity. One
copy has scalar commutant; `k` copies have commutant `M_k(C)`, so the
coefficient-free classical branch fixes `k=lambda_rel=1`. The full
Delta-plus-fixed-point-auxiliary Hessian has no negative modes and reduces by
Schur complement to the exact stable effective Hessian.

## KO6 and Full-Hessian Update

The relative chain has an exact KO6 completion, but an ordinary direct-sum
interpretation would make its 20 finite components physical fermions. More
importantly, the determinant selector stabilizes only Delta: the full project
phi tangent has eight negative modes and Sigma contributes fifteen flat
directions. The current full composite vacuum is therefore closed; only a
connected phi/Sigma interaction or a two-scale parent action remains open.

## Relative Parent-Action Update

The graph height generates a circle action whose trace-preserving conditional
expectation removes the block-diagonal fixed-point curvature. On the even
curvature space,
`||F-E_h(F)||^2=||[h,F]/2||^2=4 det(Delta Delta^dagger)`.
The remaining issue is the auxiliary status, multiplicity and overall trace
weight of this relative carrier in the full BV or relative-spectral model.

## BV Multiplicity-Fork Update

The carrier cannot be embedded in the standard Pati-Salam fermionic space,
and standard contractible BV auxiliaries cannot modify the classical vacuum.
The alternatives are a physical anomaly-safe vectorlike chain, which changes
running but misses the one-percent gate, or a non-propagating mapping-cone
sector whose one-copy multiplicity remains a parent axiom.

## Links

- [[pati-salam-composite-potential-hessian-gate]] — obstruction being repaired.
- [[pati-salam-generalized-inner-fluctuation-gate]] — source of the crossed path.
- [[version4-pati-salam-diagonal-connector-menu]] — independent Casimir-gap evidence.
- [[project-success-tree-2026-08-11]] — global status.
- [[pati-salam-wedge-channel-compatibility-gate]] — KO6 and Goldstone audit.
- [[pati-salam-three-node-parent-graph-gate]] — exterior-square parent graph and raw spectral selector.
- [[pati-salam-associative-node-no-go]] — closes the literal color-six node and redirects the selector to curvature/junk calculus.
- [[pati-salam-twoform-a2-trilemma-gate]] — closes the odd two-form, physical-seed direct-path and generic-seed predictive routes.
- [[pati-salam-projected-curvature-selector-gate]] — recovers the exact determinant from endpoint curvature on a valid `4bar -> 2_R -> 4` chain.
- [[pati-salam-junk-mapping-cone-gate]] — fixes `c=1`, closes the ordinary-junk explanation and derives the relative graph projector.
- [[pati-salam-relative-parent-action-gate]] — derives the fixed-point quotient action.
- [[pati-salam-bv-multiplicity-fork-gate]] — isolates the physical/classical architecture choice.
- [[pati-salam-irreducible-relative-cycle-gate]] — selects the one-copy classical branch and closes its auxiliary Hessian.
- [[pati-salam-ko6-phi-sigma-hessian-gate]] — passes algebraic KO6 compatibility but closes the current full composite vacuum.
- [[pati-salam-relative-parent-action-gate]] — derives the quotient action and localizes its remaining full-carrier normalization problem.
- [[pati-salam-bv-multiplicity-fork-gate]] — closes the standard-BV origin and isolates the physical/classical architecture choice.

## Source Notes

- `s2t/gates/version4_pati_salam_rank_selector_archaeology_gate.tex`
- `s2t/results/s2t_v4_pati_salam_rank_selector_archaeology_results.json`
- `s2t/gates/version4_common_updown_krajewski_loop_gate.tex`
- `s2t/gates/version4_relative_krajewski_star_gate.tex`
- `s2t/gates/version4_algebra_embedding_weighted_selector_gate.tex`