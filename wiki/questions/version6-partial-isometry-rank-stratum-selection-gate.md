# Version VI: селекция ранговых страт частичных изометрий

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Нулевые страты самосогласованного моста имеют размерности `4, 5, 3` для
рангов `1, 2, 3`. Энтропия выбирает ранг 3, а обычная низкотемпературная
мера Морса--Ботта выбирает ранг 2. Real-транспонирование сохраняет ранг.

Редуцированные состояния рангов 1 и 2 имеют орбиты
`Gr(1,3)=RP2` и `Gr(2,3)=RP2`; топология дефекта их не различает.

## Reopened Mechanism

Археология Тома IV дала точную identity

`||B_ia B_jb-B_ib B_ja||^2 = 4 e2(B^T B)`.

После нормировки самим состоянием она превращается в
`4 e2(R)=2(1-Tr(R^2))`. Одна копия такого члена эквивалентна
коэффициенту чистоты `2>log(4)` и на уровне потенциала создаёт
полноранговую одноосную фазу с приблизительным спектром
`(0.95393,0.02303,0.02303)`. Её орбита равна `RP2`.

## Status Boundary

Точный ранг один при конечной энтропии не выбирается: член
`epsilon log epsilon` удерживает минимум внутри пространства состояний.
Это не мешает дефектной фазе, потому что для `RP2` достаточно расщепления
`1+2`.

Внешний квадрат пока не выведен из текущего обменного родителя. Нельзя
переносить double-path формулу из Pati--Salam-графа без построения обеих
композиций и их относительного знака в текущем Real-соответствии.

## Next Test

Построить `version6_exchange_bridge_exterior_square_parent_gate` и
проверить происхождение нормированного `B wedge B` без нового поля,
коэффициента и ручного проектора.

Тест выполнен в
[[version6-exchange-bridge-exterior-square-parent-gate]]. Обычная
двухузловая суперсвязность внешний квадрат не содержит. Канонический
exterior-carrier даёт `2e2(R)`, тогда как полный самосогласованный переход
требует `m_crit=3.026145...`. Сырой тензорный канал `4e2(R)` проходит, но
его дополнительный множитель два ещё не выведен.

## Links

- [[version6-self-consistent-state-bridge-purification-gate]]
- [[partial-isometry-morse-bott-rank-selection-literature-2026]]
- [[version6-real-qutrit-purification-transition-gate]]
- [[version4-pati-salam-rank-selector-archaeology-gate]]
- [[version5-rank-one-tangent-junk-gate]]
- [[version5-equivariant-boundary-sector-selection-gate]]
- [[version6-matter-birth-program]]
- [[version6-exchange-bridge-exterior-square-parent-gate]]

## Source Notes

- `s2t/gates/version6_partial_isometry_rank_stratum_selection_gate.tex`
- `s2t/audits/s2t_v6_partial_isometry_rank_stratum_selection_gate.py`
- `s2t/results/s2t_v6_partial_isometry_rank_stratum_selection_gate_results.json`