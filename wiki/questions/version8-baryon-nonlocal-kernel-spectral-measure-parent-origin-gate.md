# Родительское происхождение спектральной меры нелокального ядра

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Минимальный положительный родитель с одним вспомогательным полем даёт через
точное дополнение Шура

```text
K(z) = g²/(z+m²),
f_m(z) = m²/(z+m²).
```

Статическое условие фиксирует только `g²/m²=lambda_3`. Масштабирование
`m² -> q m²`, `g² -> q g²` сохраняет `K(0)`, но меняет наклон и всю форму
при ненулевом импульсе.

## Вердикт

Однополюсное ядро имеет корректный минимальный родитель, однако текущая
конечная геометрия не выбирает его спектральную массу. Родительское
происхождение конкретной меры закрыто со статусом NO-GO до появления
независимого якоря масштаба базы.

## Что не закрыто

- не доказано отсутствие любого возможного будущего геометрического якоря;
- не выбраны `m²`, `g²` и `lambda_3`;
- не выведен барионный полюс;
- не доказана достаточность одного спектрального атома.

## Связи

- [[version8-baryon-nonlocal-six-point-kernel-admission-gate]]
- [[version8-full-field-a4-dirac-lift-origin-gate]]
- [[baryon-six-point-faddeev-literature-2026]]
- [[global-theorem-and-no-go-ledger]]

## Исходники

- `s2t/gates/version8_baryon_nonlocal_kernel_spectral_measure_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_nonlocal_kernel_spectral_measure_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_nonlocal_kernel_spectral_measure_parent_origin_gate_results.json`