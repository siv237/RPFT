# Спектральный гессиан матричной функции: литература 2026

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Формула Далецкого--Крейна выражает производную матричной функции через
разделённые разности на спектре самосопряжённой матрицы. Для следа
`Tr f(Phi)` это даёт точный конечномерный гессиан без конечных разностей и
без усечения теплового ряда.

## Project Use

В [[version7-weak-aligned-cycle-competition-gate]] применена функция
`f_t(x)=exp(-t x²)`. Формула вычисляет одновременно диагональные и смешанные
вариации полного 21-мерного оператора и отделяет down- и weak-блоки.

## Boundary

Численный спектральный проход подтверждает знак на заданном диапазоне, но
не заменяет самостоятельную аналитическую теорему о знаке при всех `t>0`.
Поэтому вывод дополнительно сверяется с малой и большой асимптотиками и
маркируется как вычислительный no-go автономного Gaussian.

## Links

- [[version7-weak-aligned-cycle-competition-gate]]
- [[product-a6-spectral-action-literature-2026]]

## Source Notes

- V. Noferini, “A Daleckii–Krein Formula for the Fréchet Derivative of a
  Generalized Matrix Function”, SIAM J. Matrix Anal. Appl. 38 (2017).
- D. V. Vassilevich, “Heat Kernel Expansion: User's Manual”,
  arXiv:hep-th/0306138.