# B-L Root And Nonuniform Pairing Working Package

> Status: active conditional branch
> Type: synthesis
> Updated: 2026-08-07

The ten-hypothesis numerical rerun and its precision corrections are recorded
in [[hypothesis-batch-pruner-gate]].

The first explicit parent-action normalization test is
[[tiered-parent-action-p1-gate]]. It retains the neutrino graded metric but
shows that the proposed tier rule does not yet derive the raw charged-lepton
seed from the same measure.

## Summary

This page consolidates the verified `B-L` root-extension chain without
reopening the negatively closed routes. Within the explicitly tested minimal
menu, the only surviving constructive branch is

```text
U(1)_(B-L) + one N_c per generation + charge-minus-two pairing field
    -> nonuniform defect texture, conditional on lambda v^2 > 1.
```

This is uniqueness only inside the audited menu, not a theorem over all
possible extensions.

## Confirmed Results

- One left-handed sterile conjugate `N_c` per generation cancels all six
  continuous local `B-L` anomaly sums.
- `integral_y a_(B-L)=pi/2` gives sterile root holonomy `+i`.
- A charge-minus-two pairing field permits the invariant vertex
  `Phi_(B-L) N_c N_c` because `-2+1+1=0`.
- Root meridian flux `pi` plus a nonzero condensate fixes
  `|wind(Phi)|=1`; it does not force the condensate or select orientation.
- The reduced Ginzburg--Landau saddle has momenta
  `k_n=(2n+1)pi/L`, threshold `lambda v^2>pi^2/L^2`, and for `L=pi`
  the exact condition `lambda v^2>1`.
- The lowest branches `n=0` and `n=-1` are exactly degenerate and conjugate.

## Torsion Correction

The ambient torsion twist is not a complete homogeneous rescue. It makes the
pairing section parallel, but transfers the nontrivial sign to the scalar
Yukawa map. The surviving branch should therefore be described as a
nonuniform `B-L` defect texture. Calling it fully torsion-twisted requires a
derived torsion-odd Yukawa map, which the current action does not contain.

This supersession chain is documented in:

- [[bl-root-condensate-consistency-gate]]
- [[root-mass-condensate-trilemma-gate]]
- [[nonuniform-pairing-saddle-gate]]
- [[spectral-pairing-stiffness-gate]]

## Independent Exact Structures

Two exact formulas remain valid but must not be merged into one physical
derivation:

1. The ordinary-trace six-channel Gaussian model gives
   `Var(xbar)=1/[6 zeta(4,1/2)]=pi^-4`.
2. The independent anomaly-free `Z2/Z4` projection retains `U+2D+H` and
   gives the exact beta direction `(17/6,1/6,2)`.

No common operator, measure or parent action currently links these results.
The first is an inverse-susceptibility candidate; the second is a
representation projection with an underived threshold magnitude and a failed
ordinary intermediate-running sign.

Related pages:

- [[six-channel-inverse-susceptibility-gate]]
- [[anomaly-free-holonomy-projection]]
- [[finite-threshold-sign-cone]]

## Open Dynamics

The following quantities remain underived:

- `lambda v^2` and whether the condensation threshold is crossed;
- selection of one of the two conjugate orientations;
- the `B-L` breaking scale and Majorana Yukawa matrix;
- the boundary value and running normalization of abelian kinetic mixing;
- the BdG kernel and determinant on the selected lowest-action texture.

The nonzero mixed trace `sum Y(B-L)=8/3` per generation means kinetic mixing
is generally generated, but topology does not fix its normalization. It is a
future normalization-sensitive second gate, not a second sector already
passed.

## Parent-Action Follow-Up

The later proposed action using the torsion-twisted pairing bundle fails the
global bundle gate. The twist makes the pairing field parallel but leaves
the Majorana vertex torsion-odd. It also cancels the total pairing holonomy
to +1, so retaining the half-shifted spectrum double-counts the same sign.

The surviving branch is therefore still the ordinary charge-two nonuniform
texture with total holonomy -1. See
[[bl-defect-action-global-consistency-gate]].

The collaborator has now explicitly selected this ordinary branch A. This
settles the bundle choice, but not the full parent action: root Wilson-line
selection, radial core gluing, exact-one kernel minimality and the rank-24
canonical metric remain open in addition to the SSB sign.

## Closed Routes

Do not reopen without genuinely new dynamics:

1. `1/3=1/4+1/12` as a real `-alpha/3` mass derivation from APS phases.
2. Universal `eta_D=-1/2`.
3. `|zeta_R(-1)|=1/12` as the circle logarithmic determinant.
4. `23=24-1` from removing a conformal or gauge mode.
5. The three-dimensional Chern--Simons form as a five-dimensional bulk action.
6. A sterile root from minimal `SU(5)`, spin, or Nambu doubling.
7. A homogeneous ordinary charge-two condensate.
8. Torsion twisting as a simultaneous rescue of condensate and Yukawa vertex.
9. EW/QCD closure by ordinary split running or the minimal logarithmic threshold cone.
10. `23=k+1`, `k=22`, as a derived CS/WZW level.

## Promotion Gate

The branch advances only if one prior action fixes the pairing threshold,
orientation-odd term, `B-L` scale, kinetic-mixing normalization and BdG
operator before comparison with neutrino or gauge data.

## Evidence

- `bl_nonuniform_pairing_working_package.tex`
- `s2t_bl_root_extension_gate_results.json`
- `s2t_root_mass_condensate_trilemma_results.json`
- `s2t_nonuniform_pairing_saddle_results.json`
- `s2t_spectral_pairing_stiffness_gate_results.json`
- `s2t_six_channel_inverse_susceptibility_results.json`
- `s2t_anomaly_free_holonomy_projection_results.json`