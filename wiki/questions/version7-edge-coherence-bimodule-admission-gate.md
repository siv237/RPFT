# Version VII: бимодульный допуск цепи когерентности

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Абстрактная спектральная цепь `1 -> 6 -> 3` не вкладывается в
неизменённый физический фермионный носитель со строгим первым порядком.

## Exact Result

Для алгебры `C + H + M3(C)` единственный одномерный неприводимый бимодуль
имеет координаты `(C,C)`. Шестимерный неприводимый бимодуль имеет тип
`(H,M3)` или `(M3,H)`. Эти типы не имеют общей левой или правой
координаты, поэтому ребро `1 -> 6` нарушает первый порядок.

В фактически принятом носителе существуют четыре размерностных кандидата

$$
\{e_R,X_R\}\longrightarrow Q_L\longrightarrow\{u_R,d_R\},
$$

но во всех четырёх первое ребро запрещено, а второе разрешено.
Real-сопряжение препятствие не снимает.

## Interpretation

Шестимерный средний узел найденного спектрального родителя является
пространством коэффициентов шести стрелок, а не шестимерным фермионным
мультиплетом. Трёхмерный конечный узел является пространством внешних
миноров, а не кварковым модулем.

Приводимая same-column цепь формально возможна, но требует добавить один
левый слабый дублет и два правых синглета ещё до аномального завершения.
Первый порядок также не связывает два её ребра требуемой
поляризационной формулой.

## Verdict

Спектральный родитель остаётся точным комплексом полей, но его строгая
фермионная реализация на неизменённом носителе закрыта. Следующая
проверяемая возможность — вспомогательный BV/BRST или mapping-cone
комплекс, не добавляющий физических фермионов.

## Subsequent Intuition Search

[[version7-auxiliary-carrier-project-intuition-search]] уточнил маршрут.
Стандартный BV/BRST уже закрыт проектом как источник нового классического
потенциала, а mapping cone не требуется, пока работает полный спектральный
след. Основной кандидат — Quillen-суперсвязность или градуированное
соответствие на пространстве стрелок. Ориентированный оператор является
кривым комплексом с `d_B^2=Lambda^2 B` и становится настоящим комплексом
ровно в ранга-один вакууме.

[[version7-edge-coherence-field-space-superconnection-gate]] подтвердил
это чтение: ассоциированный полевой носитель ковариантен, имеет
положительную метрику `3 I_12` и не требует новых физических вершин.

## Links

- [[version7-edge-coherence-spectral-parent-gate]]
- [[version7-edge-coherence-formula-intuition-map]]
- [[version7-auxiliary-carrier-project-intuition-search]]
- [[field-space-superconnection-bv-mapping-cone-literature-2026]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[mixed-connector-krajewski-leptoquark-literature-2026]]
- [[version7-rank-change-parent-program]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_edge_coherence_bimodule_admission_gate.tex`
- `s2t/audits/s2t_v7_edge_coherence_bimodule_admission_gate.py`
- `s2t/results/s2t_v7_edge_coherence_bimodule_admission_gate_results.json`