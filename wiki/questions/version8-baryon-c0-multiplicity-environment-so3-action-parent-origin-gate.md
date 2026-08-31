# Происхождение SO(3)-действия на multiplicity-среде

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Три текущие стрелки имеют матричную модель
`span(E_00,E_11,E_21) subset Hom(R2,R3)` и не образуют инвариантную
тройку. Двумерный source не несёт нетривиального вещественного
`SO(3)`-действия, а стандартное действие на target выводит четыре
инфинитезимальных образа за пределы текущего пространства.

Минимальное ковариантное замыкание требует добавить `E_10,E_20,E_01` и
равно всему шестимерному `Hom(R2,R3) = 3+3`. После этого family-Hom имеет
размерность два: `T_(u,v)=stack(u I3,v I3)`. Изометрия оставляет
`[u:v] in RP1`, поэтому расширение уменьшает, но не устраняет
неоднозначность карты `c0`. Parent-origin реестр равен `0/5`.

## Связи

- [[version8-baryon-c0-family-to-multiplicity-intertwiner-admission-gate]]
- [[version8-baryon-c0-extended-endpoint-bimodule-weight-origin-gate]]
- [[version6-bosonic-defect-family-connection-parent-identification-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate_results.json`