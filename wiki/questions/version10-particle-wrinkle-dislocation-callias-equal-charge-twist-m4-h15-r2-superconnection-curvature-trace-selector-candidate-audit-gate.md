# Аудит trace-селекторов superconnection curvature

> Status: working
> Type: question
> Updated: 2026-09-03

## Summary

Точный endpoint trace единственно требует весов `(1,-1)`, поэтому не может
быть положительным на полном прямосуммарном пространстве кривизны.
Положительный exact-route возможен условно только после выделения
relative-curvature блока.

## Key Points

- Endpoint channel map имеет rank `2` и Gram `diag(72,64)`.
- Ordinary trace с весами `(1,1)` даёт `T-B`; supertrace `(1,-1)` даёт
  `Q=T+B`, но является неопределённым.
- Relative projector `1/2[[1,-1],[-1,1]]` идемпотентен, имеет rank `1` и
  положительно полуопределённую Gram form.
- Его inherited rank в текущем represented calculus равен `0`.
- Аудит двенадцати механизмов даёт `0/12`; represented junk quotient и
  length-two relative block получают `5/6`, проваливая только inheritance.

## Open Question

Порождает ли существующий mapping-cone differential нужный relative block
как класс представленной кривизны modulo junk?

## Links

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-superconnection-mixed-curvature-parent-origin-gate]] — точный graded-curvature source.
- [[version7-real-linking-superconnection-assembly-gate]] — прежняя граница полного квадрата и length-two блока.
- [[current-status-and-next-vectors]] — текущий исследовательский фронтир.

## Source Notes

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_curvature_trace_selector_candidate_audit_gate_results.json`