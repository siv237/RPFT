# Version VI: самосогласованное очищение состояния мостом

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Состояние связано с мостом формулами

- `R_R=B^T B/Tr(B^T B)`;
- `R_L=B B^T/Tr(B^T B)`.

Самосогласованное действие точно восстанавливает скалярный мост и растёт
квартично на бесконечности. Прежняя долина при фиксированном чистом `R`
исчезает: чистота `R` требует `rank B=1`, поэтому для
`B=diag(1,C)` обязательно `C=0`.

## Main Result

Нулевое множество нового действия состоит из всех ненулевых частичных
изометрий рангов 1, 2 и 3. Интеграл становится конечным без добавленного
барьера, однако ранг один не выбирается.

После включения канонической энтропии значения на стратах равны
`0`, `-log 2`, `-log 3`. Глобальный минимум имеет ранг 3,
`B in O(3)` и `R=I3/3`.

Таким образом, устранение расходимости прошло, а рождение проекторной
фазы — нет.

## Status Boundary

Прежний коэффициент `-45/16` был получен интегрированием `B` при
независимом фиксированном `R`. После отождествления `R=R(B)` этот
детерминант нельзя переносить без нового фонового расчёта одного поля.

## Next Test

Проверить, выбирают ли топология, Real-структура или естественная мера
рангово-один страту среди частичных изометрий рангов 1, 2 и 3. Ручное
условие `rank B=1` запрещено.

Тест выполнен в
[[version6-partial-isometry-rank-stratum-selection-gate]]: энтропия
выбирает ранг 3, плоская мера Морса--Ботта — ранг 2, а топология не
различает ранги 1 и 2. Зато архивный double-path внешний квадрат создаёт
полноранговую одноосную `RP2`-фазу на уровне потенциала; открыт вывод этого
члена из текущего родителя.

## Links

- [[version6-modular-dual-weight-bridge-coercivity-gate]]
- [[purification-induced-state-rank-strata-literature-2026]]
- [[version6-real-qutrit-purification-transition-gate]]
- [[version6-exchange-bridge-induced-alignment-gate]]
- [[version6-bridge-fluctuation-determinant-purity-gate]]
- [[version6-matter-birth-program]]
- [[version6-partial-isometry-rank-stratum-selection-gate]]

## Source Notes

- `s2t/gates/version6_self_consistent_state_bridge_purification_gate.tex`
- `s2t/audits/s2t_v6_self_consistent_state_bridge_purification_gate.py`
- `s2t/results/s2t_v6_self_consistent_state_bridge_purification_gate_results.json`