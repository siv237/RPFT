# Происхождение общей корреляции среды

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Однокопийный микроскопический родитель фиксирует диагональ ковариации
среды, но не её межкопийные элементы. Независимые ячейки дают `c=0`, одна
общая ячейка — `c=1`; обе конструкции имеют один и тот же одночастичный
генератор и сохраняют перестановочную и калибровочную ковариантность.

## Точная проверка

Для

`L_c(X)=-(1/2) sum_rs R_rs [F^(r),[F^(s),X]]`

одночастичное наблюдаемое видит только `R_11=1`. Двухчастичное наблюдаемое
различает среды; в минимальном символьном контроле квадрат разности равен
`8c^2`.

## Статус

- Выбор `c=1` из текущего родителя: запрещён.
- Строгая тензорная композиция условно выбирает `c=0`.
- Аксиома общей среды условно выбирает `c=1`.
- Барионная ветвь остановлена до появления межкопийного двухточечного ядра
  среды или общего родительского действия.

## Связи

- [[version8-baryon-three-particle-lift-normalization-gate]]
- [[version8-full-noise-repeated-interaction-hamiltonian-gate]]
- [[version8-minimal-mixed-clock-collision-parent-gate]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_baryon_common_environment_correlation_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_common_environment_correlation_origin_gate.py`
- `s2t/results/s2t_v8_baryon_common_environment_correlation_origin_gate_results.json`