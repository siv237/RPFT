# Version VII: конкуренция weak-aligned циклических ветвей

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Полный product-след обнулил исходный up-цикл, но одновременно открыл
down-цветную пару `(QL-YR,XL-dR)` и слабую пару `(LL-XR,YL-eR)`. Нужно
проверить их совместный точный Gaussian-гессиан около четырёхрёберного
singlet-вакуума.

## Search for Solution

Собран полный 21-мерный одно-поколенческий конечный оператор и без усечения
вычислен

$$S_t(\Phi)=\operatorname{Tr}\exp(-t\Phi^2).$$

Гессиан получен формулой разделённых разностей Далецкого--Крейна на всех
20 вещественных тяжёлых компонентах. Down- и weak-блоки ортогональны. При
`t=1` down-блок положителен, но weak-блок имеет восемь отрицательных мод.
Логарифмический проход по 401 значению `10^-4 <= t <= 10^2` не нашёл ни
одного профиля с неотрицательным weak-блоком. Кроме того, семь корневых
производных точного Gaussian ненулевые: исходный singlet-фон нестационарен.

## Expected Result

Автономный точный Gaussian не проходит как общий родитель. Он действительно
содержит down-связь, но не сохраняет Hodge-вакуум и не стабилизирует слабого
конкурента. Добавление прежнего Hodge-потенциала с произвольным весом
запрещено как ручное сложение двух действий.

Следующий гейт — [[version7-exact-profile-hodge-cycle-unification-gate]].

## Compliance Check

- Полный носитель имеет размерность `21`, тяжёлый сектор — `20` над `R`.
- Два запуска дали одинаковый машинный результат.
- Down--weak смешивание гессиана равно нулю с точностью машины.
- Малый и большой `t` согласуются с отрицательными асимптотиками weak-моды.
- Статус: `exact Gaussian no-go; common functional still open`.

## Links

- [[version7-full-product-a6-cycle-coefficient-gate]]
- [[version7-color-preserving-quadratic-selector-origin-gate]]
- [[product-a6-spectral-action-literature-2026]]
- [[matrix-spectral-hessian-literature-2026]]
- [[version7-exact-profile-hodge-cycle-unification-gate]]

## Source Notes

- `s2t/gates/version7_weak_aligned_cycle_competition_gate.tex`
- `s2t/audits/s2t_v7_weak_aligned_cycle_competition_gate.py`
- `s2t/results/s2t_v7_weak_aligned_cycle_competition_gate_results.json`