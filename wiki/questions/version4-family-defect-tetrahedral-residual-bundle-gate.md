# Version IV family-defect tetrahedral residual-bundle gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Question

Is the `Z3` transition used by the cubic-root family frame an additional discrete input, or does it already follow from the projector-selected tetrahedral carrier?

## Construction

- The four projector axes form a regular tetrahedron in the standard real triplet.
- Their symmetric traceless rank-three tensor is a canonical spin-three field.
- Its proper rotational stabilizer is `A4`.
- Selecting one projector leaves `Stab_A4(P_a)={1,C_a,+,C_a,-}=Z3`.

## Result

The cubic denominator is intrinsic. All four projector stabilizers have order three and contain exactly the two winding-oriented cycles. The commutator subgroup of `A4` has order four, so its abelianization is `Z3`. Each order-three `SO(3)` holonomy lifts to an order-six element of `SU(2)`.

## Literature cross-check

- `arXiv:2607.12366` constructs finite-tension order-three vortices in a renormalizable `SO(3) -> A4` spin-three Higgs theory.
- `arXiv:0910.4392` analyzes spin-three `SO(3)` scalar potentials with tetrahedral vacua.
- `arXiv:1307.4793` confirms that an Abelian charge-`n` condensate leaves `Zn`; therefore the existing charge-two `B-L` field can leave only `Z2`, not the required `Z3`.

## Remaining fork

- Global `A4` retains distinguishable family axes but produces no gauge bundle.
- Gauged `A4` produces residual `Z3` flux, but the four axes are gauge-related unless boundary framing or additional matter makes their relative orientation observable.

The next parent gate must derive a gauged or boundary-framed tetrahedral carrier together with the nonzero ordinary charge-two defect condensate.

## Files

- `s2t/gates/version4_family_defect_tetrahedral_residual_bundle_gate.tex`
- `s2t/audits/s2t_v4_family_defect_tetrahedral_residual_bundle_gate.py`
- `s2t/results/s2t_v4_family_defect_tetrahedral_residual_bundle_gate_results.json`