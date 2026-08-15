# Holonomy and Dirac Sectors

> Status: working
> Type: concept
> Updated: 2026-08-11

## Summary

This page tracks the verification layer involving Dirac-type operators, spin-holonomy, gauge-holonomy, and enriched sectors. These sectors are important because they test whether the [[toe-ugsm-bridge]] survives beyond scalar or simplified models.

## Key Points

- Dirac-type tests probe whether spectral claims persist under richer operator structure.
- Spin-holonomy and gauge-holonomy tests probe compatibility with global phase and bundle-like information.
- Enriched sector maps are early operator-attribution tools for identifying which sector contributes which effect.

## Audit Signals

- Spin/holonomy sweep: `dirac_spin_holonomy_results.json` keeps `a0` and `a2` invariant across five twists with max relative errors `2.0624484157763978e-15` and `2.4634800521773637e-13`.
- Gauge doublet sweep: `gauge_holonomy_results.json` moves the phase branches `theta_+/pi: 1.0 → 2.0` and `theta_-/pi: 1.0 → 0.0` while keeping coefficient errors near `10^-13`.
- Sector attribution: `sector_attribution_results.json` assigns phase control to `beta` and subleading spectral load to `mu_heavy`, with separation ratio `1761167242253.6758`.
- These signals make holonomy a plausible source for the missing neutrino overlap factor, but they do not yet derive `\mathcal{N}_\nu^2 = \pi + \pi^{-1}`.

## 2026-08-03 Phase Versus Positive Metric Gate

The first dedicated neutrino-overlap audit sharpens the sector dictionary. A unitary holonomy `U=exp(i theta)` controls phases, but `theta+theta^{-1}` is not a gauge-periodic class function. Therefore the missing reciprocal factor cannot belong to the holonomy sector alone.

The surviving candidate is a separate positive determinant-one operator

```text
Q_cycle=diag(g,g^{-1}).
```

This strengthens the earlier sector-attribution result: phase control and positive spectral load/metric normalization must be represented by distinct operator components. A future common source must carry both structures and a rule coupling them in the Dirac insertion.

## Systolic Qcycle Construction

The positive sector can now be represented concretely. A shortest noncontractible projective geodesic `gamma=RP1` in unit round `RP3` has length `pi`. Its integral zero-form generator and unit-period one-form generator have reciprocal Hodge norms, producing

```text
Qcycle=diag(pi,pi^{-1}).
```

This operator is independent of holonomy-angle branches. The remaining interaction problem is a coupling between the ambient spinor sector and the intrinsic cycle complex. Thus the phase/metric separation is no longer only conceptual: one explicit positive metric operator is available.

## Quarter-Holonomy Defect Branch

The neutrino defect audit adds a discrete square-root layer. For the complement of a generator core in `L(2,1)`, the meridian satisfies `mu=2y`. The ambient torsion character has `chi_L(y)=-1`, while its complement square roots have `chi_S(y)=+/-i` and therefore `chi_S(mu)=-1`.

This is exactly the conjugate quarter-holonomy pair already present at `beta=1/4`. It supplies a pi-flux defect and forces odd winding in a charge-two Majorana pair channel, but its extension and boundary condition at the core remain open. The unitary phase sector, positive `Qcycle` metric and defect square-root line therefore have distinct roles.

The local core transition is now explicit. In Nambu space `G_1/4=diag(i,-i)` maps the Majorana zero basis at pair phase `theta` to the basis at `theta+pi`. It therefore does not contribute an extra coefficient holonomy. The coefficient line sees only the antiperiodic spin sign and ambient torsion sign; their product is `+1`, yielding one periodic real core mode. This closes core gluing inside the minimal defect model while leaving global action derivation open.

## Base-K spin-branch determinant update

For the two physical vectorlike Dirac pairs, the two `RP3` spin structures
have identical squared spectra: they exchange the signs of Dirac levels but
not their absolute values or multiplicities. Their eta phases cancel after
vectorlike pairing, so the real determinant modulus cannot select between
them.

Along `S1`, the finite relative determinant is scheme-independent and ranks
the antiperiodic branch below the periodic branch. At `chi R3=1` and
`R1/R3=1`, the two-pair difference is approximately `-1.94828035e-4`.
However, [[version4-spin-sum-measure-gate]] shows that the current parent
action fixes one spinor bundle and does not sum over spin structures. The
result is therefore a branch ranking, not a dynamic selection.

This also corrects an older RPFT overstatement: a spatial circle does not by
itself force periodic fermions. Both spin structures are allowed; periodicity
must be frozen as a model input unless a spin-sum or topological measure is
constructed.

## Links

- [[numerical-audits]] — source cluster for result files.
- [[ugsm]] — operator/spectral framework being stress-tested.
- [[spectral-correlational-source]] — candidate object strengthened or weakened by these tests.
- [[neutrino-overlap-lemma]] — focused open problem for the Dirac/holonomy overlap factor.
- [[version4-spin-sum-measure-gate]] — why the antiperiodic determinant ranking is not yet a dynamic spin selection.

## Source Notes

- Source paths: `dirac_unity_results.json`, `dirac_spin_holonomy_results.json`, `gauge_holonomy_results.json`, `enriched_sector_map_results.json`, `sector_attribution_results.json`, `spectral_bridge_results.json`.