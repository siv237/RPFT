# Off-shell auxiliary copy, Mathai--Quillen and suspension literature

> Status: working
> Type: source
> Updated: 2026-09-03

## Summary

Primary literature separates three mechanisms that look similar at the level
of a doubled formula but have different physical meaning. A Quillen
superconnection or a mapping cone supplies grading and relative geometry; it
does not by itself introduce an independently integrated bosonic field. An
off-shell chiral multiplet does contain a non-propagating bosonic field in the
same gauge representation as its scalar. The Mathai--Quillen construction
contains an independent bosonic fiber coordinate with a positive Gaussian
metric, but only as part of a full cohomological multiplet and a Thom-section
localization mechanism.

## Primary Sources

- D. Quillen, *Superconnections and the Chern Character*, Topology 24
  (1985), DOI `10.1016/0040-9383(85)90047-3`. A superconnection is an odd
  operator on a graded bundle; its curvature is its square and its canonical
  characteristic expression uses the supertrace.
- G. Roepstorff, *Superconnections and the Higgs Field*,
  `arXiv:hep-th/9801040`. The Higgs is an odd endomorphism of a superbundle,
  and the curvature decomposes as `D^2 + {D,L} + L^2`. The construction
  explicitly enlarges the graded bundle when the original Clifford module
  has no scalar slot.
- S. P. Martin, *A Supersymmetry Primer*, `arXiv:hep-ph/9709356`. A chiral
  multiplet contains non-propagating complex auxiliary fields `F_i`;
  eliminating them gives the non-negative scalar potential
  `V=W_i W_i^*`. Functional integration over the quadratic `F_i` has the
  same effect.
- W. Beenakker, T. van den Broek, W. D. van Suijlekom,
  *Supersymmetry and noncommutative geometry. Part I*,
  `arXiv:1409.5982`. Supersymmetry of an almost-commutative model requires
  complete building blocks and tightly related interaction coefficients;
  eligible examples are sparse. An isolated auxiliary field is not enough.
- The same authors, *Part III: The noncommutative supersymmetric Standard
  Model*, `arXiv:1409.5984`. Even the correct particle content and formal
  interactions do not guarantee that the standard spectral action is
  supersymmetric.
- V. Mathai, D. Quillen, *Superconnections, Thom Classes, and Equivariant
  Differential Forms*, Topology 25 (1986), 85--110; exposition:
  S. Wu, *Mathai--Quillen Formalism*, `arXiv:hep-th/0505003`. The Thom form
  has a Gaussian fiber factor. For a section `s` the exponent contains
  `1/2 (s,s)`, its covariant derivative and curvature terms; the resulting
  form localizes on `s^{-1}(0)`.
- M. Blau, *The Mathai--Quillen Formalism and Topological Field Theory*,
  `arXiv:hep-th/9203026`. The Gaussian Thom representative becomes a
  cohomological field theory only together with its odd fields and
  nilpotent symmetry.
- I. Forsyth, M. Goffeng, B. Mesland, A. Rennie,
  *Boundaries, spectral triples and K-homology*, `arXiv:1607.07143`.
  Relative spectral triples require an ideal and boundary data; doubling by
  a Clifford normal is a boundary construction, not automatically a new
  matter degree of freedom.
- A. Rennie, D. Robertson, A. Sims, *The Cuntz--Pimsner extension and
  mapping cone exact sequences*, `arXiv:1605.08593`. Suspension and mapping
  cone appear as exact-triangle/K-theory machinery at the level of unbounded
  cycles.

## Consequences for Tome X

The missing eight-dimensional copy can be produced conditionally in two
honest ways, but both enlarge the parent architecture.

1. **Off-shell chiral route.** If `Sigma` belongs to a chiral multiplet,
   its auxiliary `F_Sigma` is an independent bosonic coordinate in the same
   representation and has no kinetic term. A source
   `s_Q(Sigma)=Q Sigma` can arise from a quadratic superpotential only if
   holomorphy, gauge invariance and the full fermionic partner sector pass.
2. **Mathai--Quillen route.** Take an associated bundle `E_Sigma` and the
   section `s_Q(Sigma)=Q Sigma`. The Thom multiplet supplies a bosonic fiber
   field `H_Sigma` with the bundle metric and the same transition law, plus
   an odd partner. Gaussian elimination localizes on `s_Q=0`. Omitting the
   odd partner and nilpotent differential reduces this to a manually added
   Hubbard--Stratonovich field and loses the claimed origin.
3. **Pure suspension route.** It canonically supplies a parity-shifted copy
   and an odd swap operator, but the literature supports reading this first
   as stabilization or characteristic-class data. A separate action and
   measure are needed before the copy becomes a physical auxiliary field.
4. **Mapping-cone route.** It is justified only after the current program
   identifies an actual ideal, boundary map or cylinder variable whose
   boundary operator is the desired relative edge.

The subsequent full-quartet audit sharpened the Mathai--Quillen route.
The minimal field content is not the pair `(chi,H)` alone but the quartet
`(Sigma,psi,chi,H)`. Its odd determinant cancels the square root of the
localized bosonic determinant conditionally. The current parent has the
carrier grading but no inherited Grassmann coordinates `psi,chi`, so the
literary analogy does not by itself close physical origin.

The subsequent statistics audit isolates the missing datum further.
Existing physical fermions already demonstrate that Grassmann variables
and Berezin integration are available in the wider theory, but they do not
become Thom ghosts automatically. The equation `delta Sigma=psi_Sigma`
requires a translation-type gauge generator on the Sigma field space.
Thus the remaining Mathai--Quillen route is specifically a rank-eight
shift-BRST parent-origin problem, not a generic shortage of fermions.

The shift-origin calculation closes that route for the current parent.
The effective `Sigma` Hessian has nullity two, not eight; ordinary gauge
transformations have zero translational tangent at `Sigma=0`. A doubled
Stückelberg carrier realizes the desired BRST complex only conditionally
and introduces a new pure-gauge copy. The literature analogy therefore
supports the conditional architecture but not physical inheritance.

## Links

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-superconnection-suspension-auxiliary-copy-parent-origin-gate]] —
  bare-suspension discriminator и условная Thom-достройка.
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-mathai-quillen-thom-multiplet-common-parent-origin-gate]] —
  полный quartet, determinant cancellation и field-statistics no-go.
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-mathai-quillen-odd-pair-statistics-candidate-audit-gate]] —
  odd-pair candidate audit and shift-symmetry discriminator.
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-mathai-quillen-shift-symmetry-parent-origin-gate]] —
  strict shift-origin no-go and conditional Stückelberg completion.
- [[version10-relative-hodge-auxiliary-edge-project-intuition-search]]
- [[field-space-superconnection-bv-mapping-cone-literature-2026]]
- [[quillen-mckean-singer-common-trace-no-go-literature-2026]]
- [[version7-auxiliary-carrier-project-intuition-search]]
- [[current-status-and-next-vectors]]

## Source Notes

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate.tex`
- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate.tex`
- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate.tex`