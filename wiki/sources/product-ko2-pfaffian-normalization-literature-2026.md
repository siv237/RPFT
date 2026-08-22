# Произведение KO2, пфаффиан и нормировка свободной энергии

> Status: working
> Type: source
> Updated: 2026-08-19

## Summary

Признанная литература подтверждает три разных утверждения, которые нельзя
сливать в одно:

1. KO-степени вещественных спектральных троек складываются при корректно
   построенном произведении.
2. Произведение четырёхмерной KO4-геометрии с конечной KO6-геометрией
   имеет суммарную степень два и допускает физический киральный пфаффиан.
3. Детерминант Фугледе--Кадисона использует нормированный след, но обычный
   березинский фермионный интеграл даёт ненормированный пфаффиан.

Поэтому product-KO2 не выводит автоматически дробный показатель
`(1/N) log Pf`.

## Primary Sources

- L. Dąbrowski, G. Dossena, *Product of real spectral triples*,
  `arXiv:1011.4456` — конструкция произведения и сложение KO-степеней.
- A. Connes, *Noncommutative Geometry and the Standard Model with
  Neutrino Mixing*, `hep-th/0608226` — внутренняя KO6-геометрия и
  четырёхмерное произведение суммарной степени `2 mod 8`.
- J. W. Barrett, *Fermion integrals for finite spectral triples*,
  `arXiv:2403.18428` — determinant/Pfaffian формулы и зависимость
  ненулевого интеграла от KO-степени.
- P. de la Harpe, *The Fuglede--Kadison determinant, theme and
  variations*, `arXiv:1107.1059` — определение
  `log Delta_tau(A)=tau(log|A|)` для нормированного следа.

## Project Consequence

Предыдущие отношения `15/300=1/20` и `15/210=1/14` являются корректными
для интенсивного нормированного логарифма пфаффиана. Они не являются
результатом стандартного конечномерного фермионного интеграла. Обычный
пфаффиан пятнадцатикратного семейного блока несёт показатель `15`, а
умножение квадратичной формы на `1/300` не меняет его зависимость от
семейного состояния.

## Links

- [[version6-product-ko2-family-pfaffian-operator-gate]]
- [[version6-fractional-determinant-measure-origin-gate]]
- [[normalized-pfaffian-fuglede-kadison-literature-2026]]
- [[version3-orbit-measure-pfaffian-gate]]

## Source Notes

- Литературная проверка выполнена 2026-08-19 по первичным публикациям.