# Радиальные уравнения и устойчивость дефектов типа Скирма

> Status: working
> Type: source
> Updated: 2026-08-20

## Summary

Кластер первичных источников задаёт корректную границу нового результата:
радиальный анзац сводит нелинейный функционал к краевой задаче, а
четырёхпроизводный член способен поддерживать минимизаторы в фиксированных
топологических классах. Однако устойчивость внутри сферически-симметричного
сектора не является доказательством устойчивости относительно произвольных
возмущений.

## Sources

- J. A. Ponciano, L. N. Epele, H. Fanchiotti, C. A. Garcia Canal,
  *Approximate solutions for the skyrmion*, `arXiv:hep-ph/0106150` —
  нелинейное радиальное уравнение Эйлера--Лагранжа, граничные асимптотики и
  сравнение численного решения с аналитическими приближениями.
- Sergiy Koshkin, *Gauge theory of Faddeev-Skyrme functionals*,
  `arXiv:0907.0899` — существование конечной энергии минимизаторов в
  топологических классах для симметрических однородных пространств и
  калибровочное представление вариационной задачи.
- Sergiy Koshkin, *Homogeneous spaces and Faddeev-Skyrme models*,
  `arXiv:math-ph/0608042` — функциональные пространства, обобщённый
  гомотопический тип и область применимости теорем о минимизаторах.
- Lukasz Bratek, *Skyrmion on a three-cylinder*, `arXiv:0712.1510` —
  явное исследование второй вариации радиального сферически-симметричного
  сектора; полезно именно как пример ограниченной, а не полной устойчивости.

## Project Use

Литература не доказывает устойчивость конкретного проекторного дефекта
Тома VI. Она обосновывает метод: сначала вывести точный радиальный
функционал и решить его краевую задачу, затем отдельно исследовать гессиан
в радиальном и нерадиальных секторах.

## Links

- [[version6-bosonic-defect-full-euler-lagrange-stability-gate]]
- [[bosonic-defect-parent-scale-and-portal-literature-2026]]
- [[spatial-projective-defect-energy-literature-2026]]
- [[composite-projector-connection-literature-2026]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_full_euler_lagrange_stability_gate.tex`
- `s2t/results/s2t_v6_bosonic_defect_full_euler_lagrange_stability_gate_results.json`