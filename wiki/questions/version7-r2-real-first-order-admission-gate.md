# Version VII: Real/первопорядковый допуск R2

> Status: mature
> Type: question
> Updated: 2026-08-26

## Summary

Графово минимальный `R2=(3,2)_(7/6)` не проходит строгое условие первого
порядка стандартной конечной геометрии.

## Exact Obstruction

Для ребра `H_(ij) -> H_(kl)` двойной коммутатор содержит множитель
`(a_i-a_k) D (b_j-b_l)`. Ненулевое ребро допустимо только в той же строке
или том же столбце диаграммы Краевского.

Существующие рёбра меняют одну координату и проходят. Каждое отсутствующее
ребро между кварковым и лептонным секторами меняет обе координаты:

- `L_L-u_R`: `(H,C) -> (C,M3)`;
- `L_L-d_R`: `(H,C) -> (C,M3)`;
- `Q_L-e_R`: `(H,M3) -> (C,C)`.

Real-сопряжение только меняет координаты местами и препятствие сохраняет.

## Verdict

Неизменённый строгий родитель закрыт раньше спектрального действия.
Проверять потенциал и цветовой вакуум пока нечего: допустимого `D_F`-блока
`R2` нет.

Следующая развилка обязана явно изменить алгебру/представление, добавить
вершины либо перейти к скрученному или обобщённому условию первого порядка.

## Subsequent Result

[[version7-r2-minimal-architecture-branch-gate]] закрыл простую автоморфную
скрутку и оставил две ветви: нелинейный `A_(2)` без новых фермионов либо
строгий шестикромочный цикл минимум с двумя зеркальными вершинами.

## Links

- [[version7-minimal-h15-mixed-connector-admission-gate]]
- [[version7-r2-minimal-architecture-branch-gate]]
- [[version4-order-one-krajewski-square-gate]]
- [[mixed-connector-krajewski-leptoquark-literature-2026]]
- [[version7-rank-change-parent-program]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_r2_real_first_order_admission_gate.tex`
- `s2t/audits/s2t_v7_r2_real_first_order_admission_gate.py`
- `s2t/results/s2t_v7_r2_real_first_order_admission_gate_results.json`