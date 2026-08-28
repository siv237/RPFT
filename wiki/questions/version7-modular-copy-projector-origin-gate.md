# Version VII: модулярно-графовый проектор копий

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Максимальный бинарный граф всех первопорядковых рёбер условно даёт первый
нецентральный селектор пространства копий. Он выбирает не старую вершину, а
чётную/нечётную комбинации двух одинаковых бимодулей.

## Exact Result

Для обеих физических пар близнецов с тремя общими соседями

$$
qA_{\max}^2q=3\begin{pmatrix}1&1\\1&1\end{pmatrix},
\qquad
S=\frac13qA_{\max}^2q-q=\sigma_x.
$$

Проекторы `(q +/- S)/2` определяют копийную чётность без метки
«старая/новая». Модулярное состояние `rho_beta proportional exp(-beta S)`
делает прежнюю Hodge-орбиту неплоской:

$$
W_\beta(\theta)=\frac12(1-\tanh\beta\sin2\theta),
\qquad
W_\beta''(\pi/4)=2\tanh\beta>0.
$$

При `beta=1` машинный аудит получил минимум `0.1192029220`, максимум
`0.8807970780` и гессиан `1.52318830`.

## Boundary

Проектор не восстанавливает прежние шесть рёбер: полный граф имеет девять
орбит `S2 x S2`, а целевой набор не является их объединением. Кроме того,
сам принцип максимальной бинарной инцидентности с единичными весами ранее не
был выведен как часть общего родителя.

## Verdict

Получен условно положительный селектор чётности, снимающий непрерывный
`U(2)` ядер. Физическое замыкание не достигнуто. Следующий гейт должен
проверить, является ли максимальная первопорядковая инцидентность
каноническим оператором полного представленного носителя, а не новой ручной
матрицей.

## Subsequent Result

[[version7-universal-incidence-parent-admissibility-gate]] дал отрицательный
ответ. Базисно-независимая ковариация пространства всех разрешённых стрелок
скалярна; `sigma_x` требует когерентного столбца `(1,1)` и невыведенной
относительной фазы. Условная формула этого гейта сохраняется, но её
родительская предпосылка закрыта.

## Links

- [[version7-copy-selector-project-archaeology]]
- [[version7-affine-hodge-copy-selector-no-go-gate]]
- [[version7-four-vertex-vectorlike-selector-gate]]
- [[modular-state-graph-twin-selector-literature-2026]]
- [[version7-rank-change-parent-program]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]
- [[version7-universal-incidence-parent-admissibility-gate]]

## Source Notes

- `s2t/gates/version7_modular_copy_projector_origin_gate.tex`
- `s2t/audits/s2t_v7_modular_copy_projector_origin_gate.py`
- `s2t/results/s2t_v7_modular_copy_projector_origin_gate_results.json`