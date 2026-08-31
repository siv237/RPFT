# Гауссовская, гармоническая и тепловая ковариации

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Квадратичный оператор задаёт естественные кандидаты ковариации, но правило
зависит от физического чтения. Классическая гауссовская мера использует
обратный оператор, гармоническое основное состояние — обратный квадратный
корень вместе с кинетической метрикой, а тепловое ядро — экспоненту с
явным временем.

## Key Points

- Для классического квадратичного действия ковариация пропорциональна
  обратному гессиану; общий коэффициент действия меняет её масштаб.
- Квантовый гармонический вакуум дополнительно требует симплектической или
  кинетической нормировки и значения `hbar`.
- Тепловой оператор `exp(-tau H)` сохраняет полную операторную информацию,
  но зависит от выбранного `tau`.
- Все три правила наследуют собственные подпространства `H`, поэтому
  совпадение осей сильнее совпадения численных дисперсий.

## Links

- [[version8-cross-arrow-covariance-origin-gate]] — проектный тест.
- [[open-system-rate-and-covariant-dilation-literature-2026]] — различие
  между ковариацией и скоростью открытого процесса.
- [[full-heat-kernel-diffusion-geometry-reconstruction-2026]] — роль
  полного теплового ядра.

## Source Notes

- M. Lewin, P. T. Nam, N. Rougerie, “Classical field theory limit of
  many-body quantum Gibbs states in 2D and 3D”, Inventiones Mathematicae
  224 (2021), 315–444; arXiv:1810.08370.
- E. Alvarez, “Covariant techniques in Quantum Field Theory”,
  arXiv:2203.11292.
- P. Del Moral, E. Horton, “Quantum harmonic oscillators and Feynman–Kac
  path integrals for linear diffusive particles”, arXiv:2106.14592.