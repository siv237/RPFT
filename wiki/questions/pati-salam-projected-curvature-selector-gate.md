# Pati-Salam Projected Curvature Selector Gate

> Status: working
> Research status: conditional reopening
> Type: question
> Updated: 2026-08-14

## Problem

The literal color-six node, ordinary two-form identification and direct
physical-seed `A_(2)` route had failed. The remaining question was whether
the project already contained a valid-module curvature mechanism producing
the same determinant selector.

## Search for Solution

Three archived mechanisms were combined:

1. the minimal `(+,-,+)` superconnection carrier with orthogonal targets;
2. endpoint inclusion-exclusion projectors from the relative Krajewski star;
3. anomaly-safe vectorlike extensions made from fundamental modules.

This gives the chain `4bar -> 2_R -> 4`, with edges
`A=Delta` and `B=c Delta^T epsilon_2`.

## Result

- Every node is a valid fundamental or opposite module of the unchanged
  Pati-Salam algebra.
- The two-step path is the antisymmetric matrix
  `c Delta^T epsilon_2 Delta` in the color six.
- The full ordinary trace is rank-blind at `c=1`:
  `Tr D^4 = 4 rho^2`.
- The projected endpoint curvature satisfies exactly
  `||F_02||^2 = 4 c^2 det(Delta Delta^dagger)`.
- After KO6 doubling, the physical half-norm gives `4 det` at `c=1`.
- Rank-one stability only requires `c^2>1/2`, so the mechanism is robust.
- Three hundred random covariance/reality/trace tests pass at `10^-11` or
  better.

## Verdict

The archived project mechanisms contain the ingredients of a valid
projected-superconnection curvature selector. The result remains conditional.
The parent action must derive the endpoint projector and the relative metric
`c=1`; it must also decide whether the extra fundamental modules are physical
vectorlike states or auxiliary bosonic grades.

## Follow-Up Resolution

The next audit fixes `c=1` from the Frobenius isometry and endpoint
reflection/reality. It also shows that ordinary degree-two junk removes the
endpoint path in the minimal node calculus. The projector is instead derived
inside a relative mapping-cone geometry from the unique reflection-odd graph
coordinate `h=(-1,0,1)`. The remaining issue is the parent-action choice of
the relative curvature norm over the full rank-blind curvature norm.

## Links

- [[pati-salam-twoform-a2-trilemma-gate]]
- [[pati-salam-associative-node-no-go]]
- [[pati-salam-rank-selector-archaeology]]
- [[pati-salam-junk-mapping-cone-gate]]
- [[project-success-tree-2026-08-11]]

## Source Notes

- `s2t/gates/version4_pati_salam_projected_curvature_selector_gate.tex`
- `s2t/audits/s2t_v4_pati_salam_projected_curvature_selector.py`
- `s2t/results/s2t_v4_pati_salam_projected_curvature_selector_results.json`
- `s2t/audits/s2t_v4_three_node_superconnection_closure_gate.py`
- `s2t/gates/version4_relative_krajewski_star_gate.tex`
- `s2t/gates/version4_vectorlike_messenger_chain_gate.tex`
- H. Figueroa, J. M. Gracia-Bondia, F. Lizzi and J. C. Varilly,
  arXiv:hep-th/9701179.