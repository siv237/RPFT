# Version VII: Hodge-родитель градуировки рёбер

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Точный селектор `6 из 11` получил единый полевой Hodge-родитель. Фиксированный
нильпотентный дифференциал выводит знаковую градуировку своим отображением
момента, а одна норма суммарного момента одновременно создаёт отрицательные
квадратичные моды шести целевых рёбер, положительную щель пяти нежелательных
и положительную квартичную стабилизацию.

Это строгий положительный результат на пространстве полей. Физическое
Real-бимодульное вложение и семейные ориентации ещё открыты.

## Derived Background

На двух копиях одиннадцатимерного пространства стрелок введён фиксированный
дифференциал

$$
\delta_E=\begin{pmatrix}0&P_*\\I-P_*&0\end{pmatrix},
\qquad \delta_E^2=0.
$$

Он не является новым динамическим полем и удовлетворяет

$$
[\delta_E,\delta_E^\dagger]
=-\operatorname{diag}(\Gamma_E,-\Gamma_E).
$$

Таким образом, `Gamma_E` больше не вставляется как независимый сдвиг.

## One Hodge Action

Для динамической диагональной стрелки `Z=diag(z_e)` действие равно

$$
\mathcal S_\mu
=\frac12\operatorname{Tr}
\left([d_Z,d_Z^\dagger]+\mu^2[\delta_E,\delta_E^\dagger]\right)^2
-5\mu^4.
$$

Оно точно редуцируется к

$$
\sum_{e\in E_*}(|z_e|^2-\mu^2)^2
+\sum_{e\notin E_*}(|z_e|^4+2\mu^2|z_e|^2).
$$

Следовательно, в минимуме все шесть целевых рёбер имеют модуль `mu`, а
пять нежелательных равны нулю.

## Hessian Status

- нуль: `(12,0,10)` на одном поколении;
- минимум: `(0,6,16)`;
- семейный нуль: `(108,0,90)`;
- семейный минимум: `(0,54,144)`;
- семейное вакуумное многообразие: `mu U(3)^6`.

Нулевые моды минимума являются фазовыми и семейно-унитарными ориентациями,
а не нестабильностями роста нежелательных рёбер.

## Remaining Gap

Нужно вывести два ортогональных цвета стрелок из одной конечной
Real-бимодульной суперсвязности, проверить первый порядок, кинетическую
метрику и gauge-quotient. Масштаб `mu` и относительные элементы `U(3)^6`
пока не определены.

## Links

- [[version7-rooted-cycle-isotypic-edge-projector-gate]]
- [[version7-chiral-hodge-index-instability-gate]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[version7-rank-change-parent-program]]
- [[quiver-spectral-action-nonbacktracking-cycle-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[live-formulas-gates-version7-24]]

## Source Notes

- `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex`
- `s2t/audits/s2t_v7_edge_grading_hodge_superconnection_parent_gate.py`
- `s2t/results/s2t_v7_edge_grading_hodge_superconnection_parent_gate_results.json`