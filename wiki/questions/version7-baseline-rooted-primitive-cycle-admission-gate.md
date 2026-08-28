# Version VII: базисно-укоренённый примитивный цикл

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Старый фон `H15` действительно выделяет ровно один примитивный
шестирёберный цикл полного графа. Это первый положительный селектор порядка
прохождения рёбер после рангового no-go. Однако он выбирает только четыре
новых циклических ребра, не создаёт две вектороподобные массы и имеет
нулевой квадратичный гессиан в начале расширения.

Статус: положительный относительный наблюдаемый, но ещё не единое
родительское действие.

## Exact Result

Обычный шестой след содержит 305 мономов. Среди них 14 простых циклов,
каждый с кратностью 12. Небэктрекинговый оператор Хашимото удаляет все
возвратные мономы, но оставляет те же 14 циклов:

$$
\operatorname{Tr}H(x)^6
=12\sum_{\mathcal C\in\mathfrak C_6}\prod_{e\in\mathcal C}x_e.
$$

После укоренения на старых рёбрах `Q_L--u_R` и `L_L--e_R` остаётся одно
слово:

$$
\mathcal R_6
=12x_{Q_Lu_R}x_{u_RX_L}x_{X_Le_R}
x_{e_RL_L}x_{L_LY_R}x_{Y_RQ_L}.
$$

Оно совпадает с целевым смешанным циклом и не содержит нежелательных новых
рёбер.

## Canonicity Boundary

Без фона полный типизированный граф имеет группу близнецовых обменов порядка
4. Опора исходного `H15` уменьшает её стабилизатор до единицы. Поэтому
укоренение не требует ручных проекторов `old/new`, но остаётся относительным
к уже существующему ненулевому `D_H15`.

## Remaining Dynamical Gap

- цикл содержит четыре желаемых новых ребра;
- массы `X_L--X_R` и `Y_L--Y_R` в него не входят;
- хорда `X_L--Y_R` не получает положительной щели;
- после фиксации двух старых рёбер наблюдаемый имеет четвёртую степень по
  новым полям, поэтому его гессиан в нуле равен нулю;
- остальные разрешённые рёбра также не подавлены.

Следующий гейт должен проверить, выводит ли циклический отклик один
квадратичный проектор рёбер с правильными знаками без новых коэффициентов.

## Links

- [[version7-post-rank-one-cycle-parent-intuition-search]]
- [[version7-edge-coherence-full-graph-competition-gate]]
- [[quiver-spectral-action-nonbacktracking-cycle-literature-2026]]
- [[version7-four-vertex-vectorlike-selector-gate]]
- [[version7-rank-change-parent-program]]
- [[global-theorem-and-no-go-ledger]]
- [[live-formulas-gates-version7-22]]

## Source Notes

- `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex`
- `s2t/audits/s2t_v7_baseline_rooted_primitive_cycle_admission_gate.py`
- `s2t/results/s2t_v7_baseline_rooted_primitive_cycle_admission_gate_results.json`