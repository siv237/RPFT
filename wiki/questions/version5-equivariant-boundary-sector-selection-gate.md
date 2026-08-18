# Эквивариантная граница и выбор сектора

> Status: working
> Type: question
> Updated: 2026-08-18

## Summary

Spin-cover bridge строго определяет хопфову линию после выбора
сферически-эквивариантного ежа, но текущий глобальный фон не заставляет
такой ёж существовать.

В проекте имеется явный постоянный проектор `P0` с нулевой производной и
нулевым зарядом. Для исторического носителя `RP3 x S1` выполнено `pi2=0`,
а `H2(-;Z)=Z2` имеет только кручение. Любой такой класс ограничивается
тривиально на локальную сферу, поскольку `H2(S2;Z)=Z` не имеет кручения.
У позднего `S4` вторая группа когомологий вообще нулевая.

Существующие функционалы также не выбирают материю: тождественная петля
имеет действие `0`, тогда как минимум сектора 15 равен `1/7`. Точный
вакуумный отклик дефекта положителен и измеряет его цену, а не
неустойчивость нулевого вакуума.

## Verdict

- Форма выбранного эквивариантного дефекта: **строго определена**.
- Однородный нулевой сектор: **допустим**.
- Топологическое принуждение ненулевого сектора: **не получено**.
- Динамическая неустойчивость нуля: **не получена**.
- Ветка линий и накрытий: **остановлена до нового родительского критерия**.

## Reopening Criterion

Требуется отрицательная мода полного гессиана нулевого сектора, глобальная
аномалия полной меры либо независимое доказательство отсутствия постоянной
секции.

## Links

- [[version5-spin-cover-defect-sphere-bridge-gate]]
- [[version5-global-carrier-forced-nontrivial-sector-gate]]
- [[version5-toeplitz-parent-action-variational-gap-gate]]
- [[version5-closure-deficit-induced-vacuum-response-gate]]
- [[zero-prompt-inevitability-gate]]
- [[global-defect-sector-neutrality-literature-2026]]
- [[transition-primitive]]

## Source Notes

- `s2t/gates/version5_equivariant_boundary_sector_selection_gate.tex`
- `s2t/audits/s2t_v5_equivariant_boundary_sector_selection_gate.py`
- `s2t/results/s2t_v5_equivariant_boundary_sector_selection_gate_results.json`