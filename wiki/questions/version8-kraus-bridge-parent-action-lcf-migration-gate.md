# Точная LCF-проверка parent-action Kraus-моста

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Положительная полевая форма Kraus-моста подтверждена точно. Она сохраняет
две сигнатуры Тома VII при любом неотрицательном весе, но в классическом
вакууме все полезависимые Kraus-веса равны нулю. Масса флуктуации не
является скоростью шума.

## Problem

Заменить scan шести весов символическим доказательством совместимости и
строго отделить положительный гессиан от ненулевого запуска процесса.

## Search for solution

- Для каждого из 12 cross-направлений вычислен точный коэффициент `7/36`;
  восемь внутренних контролей дают ноль.
- SymPy-гессиан сопоставлен с `7 I_12/18`.
- Исходная и вакуумная формы восстановлены как точные диагональные матрицы.
- Введён символический вес `lambda_bridge>=0` и проверены знаки каждой
  диагональной моды.
- Отдельно проверены энергия, градиент и вектор весов `z_a^2` при `z=0`.

## Expected result

Добавка должна быть совместима со старым качественным переходом, но не
должна создавать работающий канал без ковариации или среды.

## Compliance check

- `E_bridge=(7/36) sum z_a^2`.
- `Hess E_bridge=7 I_12/18`; 27-мерная сигнатура `(0,15,12)`.
- Для всех `lambda_bridge>=0`: origin `(7,0,20)`, vacuum `(0,0,27)`.
- При `z=0`: энергия, градиент и все Kraus-веса равны нулю.
- При внешних `c_Q,c_X>0`: скорость `7(c_Q+c_X)/6`.
- Гауссовский пробный коэффициент `35/96` точен, но его общий масштаб не
  выведен.

## Links

- [[version8-kraus-bridge-parent-action-hessian-gate]]
- [[version8-gauge-twirl-kraus-lcf-migration-gate]]
- [[version8-cross-arrow-covariance-origin-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version8_kraus_bridge_parent_action_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_kraus_bridge_parent_action_lcf_migration_gate.py`
- `s2t/results/s2t_v8_kraus_bridge_parent_action_lcf_migration_gate_results.json`
- `s2t/proofdsl/examples/version8_kraus_parent_hessian.py`