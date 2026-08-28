# Version VII: допуск универсального инцидентного родителя

> Status: mature
> Type: question
> Updated: 2026-08-27

## Summary

Максимальная бинарная смежность не выводится из текущего представления
базисно-независимо. Полученный ранее `sigma_x` скрыто предполагает
когерентное сложение двух независимых стрелок с одинаковой фазой.

## Exact Result

На изотипической кратности `W=C2` физическая алгебра действует единично и
сохраняет полный `U(2)`. Поэтому канонический эндоморфизм должен быть
скалярным.

Для одного общего соседа независимые стрелки дают

$$
|e_1\rangle\langle e_1|+|e_2\rangle\langle e_2|=I_2,
$$

а после трёх соседей — `3 I2`. Нецентральный член возникает только из

$$
|e_1+e_2\rangle\langle e_1+e_2|=I_2+\sigma_x,
$$

то есть после фиксации относительной фазы.

Твирлинг `sigma_x` по Pauli-группе и по конечной подгруппе `O(2)` даёт ноль,
а проектор нечётной линии превращается в `I2/2` с машинным остатком ноль.

## Verdict

Предыдущий модулярный расчёт остаётся корректной условной моделью, но его
предпосылка не выводится из текущего родителя. Маршрут универсальной
единичной инцидентности закрыт.

Недостающий объект теперь сформулирован точно: ранга-один ковариация или
конденсат когерентности в пространстве разрешённых стрелок. Он должен
возникнуть из одного инвариантного действия, а не из заранее выбранного
вектора `(1,1)`.

## Subsequent Result

[[version7-edge-coherence-rank-one-condensate-gate]] реализовал требуемую
ковариацию условно на уровне потенциала. Радиальная неустойчивость запускает
ненулевое поле, а внешний квадрат точно оставляет ранг один. Чистый
копийный проектор теперь является следствием минимума, но происхождение
самого потенциала из одного родителя ещё не доказано.

## Links

- [[version7-modular-copy-projector-origin-gate]]
- [[version7-affine-hodge-copy-selector-no-go-gate]]
- [[version7-copy-selector-project-archaeology]]
- [[modular-state-graph-twin-selector-literature-2026]]
- [[version7-rank-change-parent-program]]
- [[version7-edge-coherence-rank-one-condensate-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_universal_incidence_parent_admissibility_gate.tex`
- `s2t/audits/s2t_v7_universal_incidence_parent_admissibility_gate.py`
- `s2t/results/s2t_v7_universal_incidence_parent_admissibility_gate_results.json`