# Version VII: совместный гессиан singlet-вакуума и виртуального цикла

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Gauge-Casimir проектор запускает четыре бесцветных ребра и оставляет два
цветных циклических моста массивными. Их виртуальный детерминант создаёт
отрицательную нелинейную связь между двумя бесцветными коннекторами. Нужно
проверить совместный потенциал в singlet-вакууме, не закрывает ли
determinant-поправка тяжёлую цветную щель и сохраняется ли положительность
полного физического гессиана.

## Search for Solution

Следует подставить Hodge-вакуум четырёх gauge-синглетов в тяжёлый блок
`K(pq)`, канонически нормировать поля и вычислить:

1. условие `Delta(pq)>0` на всём вакуумном многообразии;
2. радиальные и фазовые смешанные производные `3 log Delta`;
3. совместный гессиан четырёх singlet-блоков;
4. изменение масс двух виртуальных цветных мостов;
5. зависимость результата от ещё не выведенного отношения
   `kappa mu^2/(M_a M_b)`;
6. семейный подъём и gauge-quotient.

## Expected Result

Положительный проход требует открытой области безразмерного отношения, в
которой singlet-вакуум остаётся поперечно устойчивым и `Delta>0`, причём
само отношение выводится из одного спектрального действия. Если
устойчивость зависит от свободного порога или достигается только при
закрытии цветной щели, совместное динамическое замыкание остаётся условным.

## Result

На симметричной ветви `r=s=sqrt(u)` стационарность требует

`gamma=2(u-1)(1-a u^2)/(a u)`.

Точные радиальные собственные значения равны

`lambda_parallel=8[1-a u^2(2u-1)]/(1-a u^2)` и
`lambda_perp=8(2u-1)`.

Поэтому существует непустая открытая локально устойчивая область
`a u^2(2u-1)<1`, которая автоматически лежит внутри тяжёлой цветной щели
`a u^2<1`. Однако конечномерный логарифм уходит к минус бесконечности при
закрытии щели, четыре singlet-фазы остаются нулевыми, а параметры `a` и
`gamma` не выведены. Получен условный локальный проход, но не глобальный
физический вакуум.

## Subsequent Correction

[[version7-full-product-a6-cycle-coefficient-gate]] раскрыл слабые
интертвинеры и показал, что использованная здесь up-пара имеет `kappa=0`,
поскольку полный цикл содержит `H_tilde^dagger H=0`. Поэтому эта глава
сохраняется как корректный условный анализ абстрактного двухполевого
determinant-блока, но больше не является физическим гессианом исходного
полного product-оператора. Ненулевая связь переносится на down-пару и
должна конкурировать со слабой дублетной парой.

Следующий тест — вывести отношение `a,gamma` из одного спектрального
профиля: [[version7-common-spectral-profile-singlet-virtual-ratio-gate]].

## Links

- [[version7-color-preserving-quadratic-selector-origin-gate]]
- [[version7-virtual-colored-bridge-schur-complement-gate]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version7-common-spectral-profile-singlet-virtual-ratio-gate]]
- [[version7-full-product-a6-cycle-coefficient-gate]]

## Source Notes

- `s2t/gates/version7_color_preserving_quadratic_selector_origin_gate.tex`
- `s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex`
- `s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex`
- `s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex`
- `s2t/results/s2t_v7_singlet_vacuum_virtual_cycle_combined_hessian_gate_results.json`