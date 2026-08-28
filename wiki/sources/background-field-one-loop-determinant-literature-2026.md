# Фоновый метод и однопетлевой детерминант

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

В фоновом методе гауссово интегрирование физических флуктуаций даёт
однопетлевую поправку `1/2 Tr log Hess`, дополненную ghost/BV-факторами при
наличии калибровочных направлений. Зависимость эффективного потенциала от
фонового состояния возникает только через зависимость гессиана и меры от
этого фона.

## Primary Sources

- S. Coleman, E. Weinberg, *Radiative Corrections as the Origin of
  Spontaneous Symmetry Breaking*, Phys. Rev. D 7 (1973), 1888.
- A. Codello, R. K. Jain, *On the covariant formalism of the effective
  field theory of gravity and its cosmological implications*,
  `arXiv:1505.03119` — функциональные детерминанты и нелокальное
  тепловое разложение.
- S. Dittmaier, S. Schuhmacher, M. Stahlhofen, *Integrating out heavy
  fields in the path integral using the background-field method*, Eur.
  Phys. J. C 81 (2021), 826.
- P. J. Forrester, *Matrix polar decomposition and generalisations of the
  Blaschke--Petkantschin formula in integral geometry*,
  `arXiv:1701.04505` — якобианы матричного полярного разложения.

## Project Consequence

Формула `1/2 log det' Hess` допустима как первый контроль, но проект обязан
отдельно вывести меру на матричных мостах, обработать орбитальные нулевые
моды и проверить непертурбативное насыщение. Отрицательный локальный
гессиан не равен доказанному конечному вакууму.

Для виртуальной цветной пары Тома VII первый четырёхмерный лёгкий оператор
пропорционален логарифмически расходящемуся интегралу с двумя тяжёлыми
пропагаторами. Поэтому коэффициент локальной вершины `|pq|²` обязан быть
записан как сумма loop-части и перенормированного контрчлена. Выбор общего
голого спектрального профиля сам по себе не задаёт конечную часть этого
контрчлена и масштаб согласования.

## Links

- [[version6-bridge-fluctuation-determinant-purity-gate]]
- [[version6-exchange-bridge-induced-alignment-gate]]
- [[version5-carrier-measure-freeze-gate]]
- [[version7-virtual-colored-bridge-schur-complement-gate]]
- [[version7-singlet-vacuum-virtual-cycle-combined-hessian-gate]]
- [[version7-common-spectral-profile-singlet-virtual-ratio-gate]]

## Source Notes

- Литературная проверка выполнена 2026-08-19; вывод для нового гейта
  уточнён 2026-08-28.