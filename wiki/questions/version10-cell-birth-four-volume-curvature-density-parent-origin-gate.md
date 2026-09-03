# Родитель объёмной плотности кривизны

> Status: working
> Type: question
> Updated: 2026-09-01

## Вопрос

Может ли собственная кривизна четырёхмерной ячейки выбрать её абсолютную
длину и тем самым закрыть геометрический масштаб Тома X?

## Результат

Для изотропной ячейки

$$
v=\ell^4,\qquad R=\frac{12}{\ell^2},\qquad
vR=12\ell^2,\qquad vR^2=144.
$$

Квадрат кривизны безмасштабен. Конкуренция объёмного и эйнштейновского
членов допускает положительный условный родитель

$$
\mathcal P_R(q)=Aq^2-Bq+\frac{B^2}{4A}
=A\left(q-\frac{B}{2A}\right)^2,\qquad q=\ell^2,
$$

с минимумом $q_*=B/(2A)$ и гессианом $2A>0$. Однако преобразование

$$
(q,A,B)\mapsto(s^2q,A/s^4,B/s^2)
$$

сохраняет функционал. Карта ограничений имеет ранг/ядро `2/1`, а её ядро
порождается вектором `(-2,-1,1)`. Поэтому масштаб перенесён в отношение
коэффициентов, но не выведен физически.

## Статус

- архитектура: `8/8`;
- условное происхождение: `3/3`;
- происхождение коэффициентов кривизны: `0/1`;
- абсолютный масштаб ячейки: `0/1`;
- ProofDSL: `18/18`, общий реестр `81/791`.

Следующий вопрос — может ли какой-либо внутренний механизм независимо
вывести коэффициенты $A$ и $B$ или их размерное отношение.

## Связи

- Предшественник: [[version10-cell-birth-four-volume-topological-quantum-candidate-audit-gate]].
- Формулы: [[global-formula-atlas]].
- Реестр статусов: [[global-theorem-and-no-go-ledger]].
- Исходники: `s2t/gates/version10_cell_birth_four_volume_curvature_density_parent_origin_gate.tex`, `s2t/audits/s2t_v10_cell_birth_four_volume_curvature_density_parent_origin_gate.py`, `s2t/results/s2t_v10_cell_birth_four_volume_curvature_density_parent_origin_gate_results.json`.