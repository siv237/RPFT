# Version VI: пространственная энергия проекторных дефектов

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Три топологических сектора `RP2` резко различаются энергетически. Ни
линейный, ни глобальный точечный сектор сами по себе не дают частицы.

## Results

- минимальная `Z2`-дисклинация имеет энергию на единицу длины
  `2 pi kappa Delta^2 (1/2)^2 log(L/xi)`;
- точечный ёж имеет энергию
  `8 pi kappa Delta^2 (L-xi)` и линейно расходится;
- релаксация ядра не устраняет дальнюю расходимость ежа;
- spin-cover по-прежнему назначает двум ориентациям классы `+15/-15`;
- хопфова текстура постоянна на бесконечности, но при одном `E2`
  коллапсирует;
- положительные `E2+E4` дают `L*=sqrt(B/A)` и конечную энергию;
- проект пока не выводит отношение `A/B`;
- гладкий gauged-ёж имеет конечную BPS-энергию и индекс Каллиаса один, но
  пространственная `SO(3)`-динамика не выведена из родителя.

## Interpretation

Лучший ungauged-кандидат — хопфова текстура. Лучший прямой кандидат на
Real-пару `+15/-15` — калибровочно завершённый точечный ёж. Оба маршрута
пока условны, но теперь точно известно, какого элемента не хватает
каждому.

## Next Test — completed

Тест выполнен в [[version6-gauged-projective-spin-cover-parent-gate]]. Из
самого `Q` построена составная связность, устраняющая инфракрасную
расходимость. Она не является полным локальным `SO(3)`-полем: отсутствует
стабилизаторный компонент и гладкое spin-cover продолжение ядра.

## Links

- [[version6-projective-order-parameter-field-spectrum-gate]]
- [[spatial-projective-defect-energy-literature-2026]]
- [[version5-projective-hedgehog-point-defect-gate]]
- [[version5-hopf-twisted-defect-superconnection-energy-index-gate]]
- [[version5-spatial-so3-superconnection-parent-trace-gate]]
- [[version5-spatial-extension-derrick-balance-gate]]
- [[version6-matter-birth-program]]
- [[version6-gauged-projective-spin-cover-parent-gate]]

## Source Notes

- `s2t/gates/version6_spatial_projective_defect_energy_spectrum_gate.tex`
- `s2t/audits/s2t_v6_spatial_projective_defect_energy_spectrum_gate.py`
- `s2t/results/s2t_v6_spatial_projective_defect_energy_spectrum_gate_results.json`