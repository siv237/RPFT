# Version VII: замыкание с одним калибровочным масштабом

> Status: mature
> Type: question
> Updated: 2026-08-27

## Problem

После no-go внутреннего масштаба проверить честный EFT-вариант: принять
ровно одну размерную калибровку и определить, замыкает ли она все массы,
длины, щели, взаимодействия и нелинейные энергии Hodge-родителя.

## Search for Solution

Введена единая эффективная плотность с общими коэффициентами `Z` и `kappa`
для всех одиннадцати рёбер. После канонической нормировки остаются

$$
v=\sqrt Z\mu,\qquad
\lambda_E=\frac{\kappa}{Z^2},\qquad
M_0^2=\lambda_Ev^2=\frac{\kappa\mu^2}{Z}.
$$

Полный гессиан вычислен в единицах единственного размерного масштаба `M0`.
Затем при фиксированном `M0` варьировалась эффективная квартика
`lambda_E`.

## Result

Получен частичный положительный результат:

- одна измеренная масса калибрует весь внутренний линейный спектр;
- шесть выбранных радиальных мод имеют массу `2 sqrt(2) M0`;
- десять компонент нежелательных рёбер имеют массу `2 M0`;
- предсказано безразмерное отношение `m_rad/m_gap=sqrt(2)`;
- отношение корреляционных длин равно `1/sqrt(2)`.

Полный EFT не замкнут. При одном и том же `M0` различные `lambda_E` дают
одинаковые массы, но разные вакуумные амплитуды, четырёхточечные вершины и
нелинейные натяжения. Пространственно-временной коэффициент кинетического
следа также ещё не выведен.

## Compliance Check

- нулевой спектр в единицах `M0²`: `-4` кратности 12 и `+4` кратности 10;
- вакуумный спектр: `0` кратности 6, `+4` кратности 10, `+8` кратности 6;
- три теста `lambda_E=1/4,1,4` сохраняют массы и изменяют взаимодействия;
- конечная кинетическая метрика `3 I12` положительна и общая;
- физическая тепловая нормировка кинетики остаётся открытой.

## Next Gate

[[version7-spacetime-kinetic-potential-ratio-admission-gate]] должен
проверить, выводится ли `lambda_E=kappa/Z²` из одного произведённого
пространственно-временного спектрального оператора.

## Links

- [[version7-hodge-level-background-attribution-gate]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[version7-spacetime-kinetic-potential-ratio-admission-gate]]
- [[version3-absolute-scale-no-go]]

## Source Notes

- `s2t/gates/version7_single_scale_calibration_closure_gate.tex`
- `s2t/audits/s2t_v7_single_scale_calibration_closure_gate.py`
- `s2t/results/s2t_v7_single_scale_calibration_closure_gate_results.json`