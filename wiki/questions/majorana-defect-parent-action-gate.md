# Majorana Defect Parent Action Gate

> Status: working
> Research status: topology closes winding conditionally; dynamical defect generation remains open
> Type: question
> Updated: 2026-08-06

## Question

Does the existing S2T action force the class-D Majorana defect whose kernel gives the rank-23 complement?

## Positive Result

For square-root meridian flux pi and a nonzero charge-two pairing field, finite energy requires

    integral(d arg Phi - 2 a)=0,

so the pairing phase winds once. The odd mod-two index is therefore fixed rather than fitted. The existing local kernel, core gluing, R24 embedding and tubular restriction remain consistent.

## Dynamical Obstruction

Topology does not force Phi to condense. For the minimal potential

    V=m_Phi^2 |Phi|^2 + lambda_Phi |Phi|^4,

nonnegative m_Phi^2 gives Phi=0 and no gapped defect. Condensation requires a negative Hessian or an independently derived attractive gap equation.

The smooth ambient Z2 line is trivial on the core meridian. Its square root has holonomy -1 and cannot extend through the core. A local parent theory therefore needs a dynamical Z4/U1 root connection or an explicit disorder sector.

## Verdict

The implication pi-flux plus nonzero pairing implies unit winding is closed. The implication S2T action implies pi-flux and nonzero pairing is not closed. Adding them manually creates a new model version.

## Evidence

- s2t_majorana_defect_parent_action_gate_audit.py
- s2t_majorana_defect_parent_action_gate_results.json
- majorana_defect_parent_action_gate.tex