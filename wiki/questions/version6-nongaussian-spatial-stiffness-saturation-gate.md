# Version VI: пространственная жёсткость и однородное насыщение

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Квадратичные, скирмовские и любые другие локальные производные члены не
устраняют долину

`R=diag(1,0,0)`, `B=diag(1,C)`, `C in M2(R)`.

Для постоянных `R` и `B` все пространственные производные равны нулю, а
локальное мостовое действие уже обращается в нуль. Поэтому четырёхмерный
уход по `C` сохраняется точно.

## Main Result

Дискретная пространственная жёсткость удаляет неоднородные нулевые моды,
но оставляет четыре глобальные постоянные моды `M2(R)`. Следовательно,
она не делает однородный интеграл коэрцитивным.

Баланс Деррика `aL+b/L` остаётся содержательным: он способен удерживать
размер уже возникшего топологического дефекта. Но это второй этап, а не
механизм выбора проекторной фазы.

## Status Boundary

Пространственная жёсткость как механизм рождения фазы закрыта.
Скирмовский сектор как механизм стабилизации уже созданной частицы
остаётся условно открытым после вывода коэффициентов.

## Next Test

Тест выполнен в
[[version6-modular-dual-weight-bridge-coercivity-gate]]. Коммутант несёт
`R^T=R`, КМС-норма не поднимает ядро, а каноническая относительная
энтропия слишком сильно стабилизирует изотропный вакуум.

## Links

- [[version6-common-intensive-free-energy-normalization-gate]]
- [[version6-modular-dual-weight-bridge-coercivity-gate]]
- [[spatial-stiffness-bulk-phase-literature-2026]]
- [[version5-spatial-extension-derrick-balance-gate]]
- [[version5-superconnection-skyrme-coefficient-gate]]
- [[version5-projector-superconnection-common-scale-gate]]
- [[version5-fermionic-determinant-induced-skyrme-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_nongaussian_spatial_stiffness_saturation_gate.tex`
- `s2t/audits/s2t_v6_nongaussian_spatial_stiffness_saturation_gate.py`
- `s2t/results/s2t_v6_nongaussian_spatial_stiffness_saturation_gate_results.json`