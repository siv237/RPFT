# Том VI: родительская нормировка жёсткостей Q и T

> Status: working
> Type: question
> Updated: 2026-08-20

## Краткий вывод

Один условный триплетный след фиксирует

`Z_Q=Z_T=1/3`, `Z_Q/Z_T=1`.

Нового относительного веса нет. Прежний профиль использовал для кинетики
`T` обычную тензорную норму вместо условной и завышал коэффициенты `A,B,C`
ровно втрое.

## Исправленный результат

- `A=C=128/243`, `B=160/243`, `G=2/27`;
- натяжение `1.5772484656...`;
- `b(0)=1.0851729254...`;
- `a'(0)=2.9597500000...`;
- радиальная щель `4.1439414612...`;
- отрицательных радиальных мод нет.

## Изменение статуса

Старые профиль и спектры остаются воспроизводимой условной ветвью, но
не являются канонической нормировкой родителя. Нерадиальный и полный
гессианы необходимо пересчитать на исправленном фоне.

Повторный нерадиальный расчёт выполнен в
[[version6-bosonic-defect-corrected-vortex-nonradial-stability-gate]].
Отрицательных мод на конечных сетках не найдено, однако восемь нижних
значений смягчаются к нулю и сходящийся положительный зазор отсутствует.

## Связи

- [[version6-bosonic-defect-q-tetrahedral-vortex-full-hessian-gate]]
- [[version6-bosonic-defect-corrected-vortex-nonradial-stability-gate]]
- [[version6-bosonic-defect-q-tetrahedral-coupled-defect-profile-gate]]
- [[version6-bosonic-defect-q-tetrahedral-vortex-radial-stability-gate]]
- [[hilbert-module-modular-corner-curvature-literature-2026]]
- [[q-tensor-elastic-normalization-literature-2026]]
- [[version6-matter-birth-program]]

## Исходные материалы

- `s2t/gates/version6_bosonic_defect_q_stiffness_parent_normalization_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_q_stiffness_parent_normalization_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_q_stiffness_parent_normalization_gate_results.json`