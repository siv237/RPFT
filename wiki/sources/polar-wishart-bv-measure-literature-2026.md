# Полярные, Wishart- и BV-меры

> Status: working
> Type: source
> Updated: 2026-08-19

## Summary

Полярное или сингулярное разложение матрицы не меняет исходный интеграл:
орбитальный объём возвращается как якобиан сингулярных значений. Для
вещественных индуцированных состояний Wishart-якобиан создаёт степень
детерминанта, определяемую размерностями матрицы очищения. BV-формализм
организует калибровочную редукцию и квантовые детерминанты, но не разрешает
произвольно менять классический потенциал физических мод.

## Primary Sources

- P. J. Forrester, *Matrix Polar Decomposition and Generalisations of the
  Blaschke--Petkantschin Formula in Integral Geometry*,
  `arXiv:1701.04505`.
- A. S. Cattaneo, P. Mnev, N. Reshetikhin, *Perturbative Quantum Gauge
  Theories on Manifolds with Boundary*, `arXiv:1507.01221`.
- C. Elliott, O. Gwilliam, *Higher Deformation Quantization for
  Kapustin--Witten Theories*, `arXiv:2108.13392` — обзор классического
  BV-комплекса как описания производного критического локуса.
- J. M. Ball, A. Majumdar, *Nematic liquid crystals: from Maier--Saupe to
  a continuum theory*, Mol. Cryst. Liq. Cryst. 525 (2010) — пример
  сингулярного потенциала, выведенного из микроскопической энтропии, а не
  назначенного как калибровочный якобиан.

## Project Consequence

Полярный якобиан не лечит расходимость `dt/t`. Индуцированный
`-nu log det R` является осмысленным контрольным семейством, но стандартные
целочисленные Wishart-коэффициенты не попадают в найденное проектом окно
`0 < nu < 17/168`. Возможное дробное происхождение требует отдельного
относительного детерминантного вывода.

## Links

- [[version6-polar-bv-rank-loss-barrier-gate]]
- [[background-field-one-loop-determinant-literature-2026]]
- [[version6-state-weighted-bridge-nonperturbative-saturation-gate]]

## Source Notes

- Литературная проверка выполнена 2026-08-19.