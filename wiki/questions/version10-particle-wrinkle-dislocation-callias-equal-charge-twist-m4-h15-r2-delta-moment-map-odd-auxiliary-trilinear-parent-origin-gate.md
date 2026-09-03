# Родитель Delta moment-map odd auxiliary trilinear

> Status: working
> Type: question
> Updated: 2026-09-03

## Summary

Нейтральный `Delta`-фон фиксирует точный оператор `Q=6Y`, но каноническое
отображение момента на ортогональной сумме `A_Sigma ⊕ Sigma` аддитивно и
имеет нулевой смешанный блок.

## Key Points

- Нормированная инвариантная метрика кратности имеет вид
  `K(kappa)=[[1,kappa],[kappa,1]]`; параметр `kappa` остаётся свободным.
- Унаследованная прямая сумма задаёт `kappa=0`, тогда как target требует
  `kappa=1`.
- При `kappa=1/2` метрика невырождена, но cross-блок равен только `Q/2`.
- При `kappa=1` полный trace carrier имеет rank/nullity `8/8`: независимая
  auxiliary-комбинация теряет норму.
- Поэтому moment map фиксирует направление `Q`, но не создаёт физический
  parent смешанного билинейного члена.

## Open Question

Может ли смешанная компонента кривизны суперк связности породить `Q` без
свободной multiplicity metric и без вырождения auxiliary-поля?

## Links

- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-odd-auxiliary-cross-bilinear-candidate-audit-gate]] — предыдущий аудит кандидатов.
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-delta-stabilizer-moment-map-curvature-parent-origin-gate]] — происхождение направления `Q`.
- [[current-status-and-next-vectors]] — текущий исследовательский фронтир.

## Source Notes

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate_results.json`