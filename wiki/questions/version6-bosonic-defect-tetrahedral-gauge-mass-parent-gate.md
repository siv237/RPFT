# Version VI: тетраэдрическая масса семейной связности

> Status: working
> Type: question
> Updated: 2026-08-20

## Summary

Литературный тетраэдрический потенциал сведён к одной матричной кривизне

`mu_T,ij=T_ikl T_jkl-(v_T^2/3)delta_ij`.

Её следовая норма одновременно фиксирует ненулевую амплитуду и форму
`SO(3)/A4`. Проверены две реализации: независимое поле спина три и
составной тензор четырёхосного кадра.

## Independent Spin-Three Result

- размерность полного поля: `7`;
- `v_T^2=32/9` для канонического тетраэдра;
- гессиан имеет три калибровочных нуля и четыре положительных значения:
  `(512/405)^3`, `256/81`;
- двенадцать собственных вращений сохраняют вакуум;
- непрерывный стабилизатор отсутствует, дискретный равен `A4`;
- все три компоненты семейной связности получают положительную массу;
- нормированный след `H45` точно совпадает с `tau3`.

Ограничение: независимое семикомпонентное поле ещё не выведено текущим
конечным родителем.

## Composite Frame Result

Для `X=(n1,n2,n3,n4)` введена единая блочная кривизна

`diag(XX^T-4I/3, X^T X-4P3/3)`.

- полный гессиан имеет три вращательных нуля и девять положительных мод;
- `T(X)=sum_a x_a^3` точно воспроизводит тетраэдрический тензор;
- новых фундаментальных компонент нет;
- стабилизатор относительно одного левого gauge-`SO(3)` тривиален;
- `A4` существует только как совместная левая/right-`S4` или гранично
  фиксированная симметрия.

## Verdict

Математический родительский квадрат найден, но физические ветви нельзя
смешивать. Независимое поле даёт настоящую остаточную калибровочную `A4`,
составной кадр — более экономную диагональную `A4`. Следующий гейт должен
решить gauge/frame-развилку по уже принятым принципам проекта.

## Subsequent Result

[[version6-bosonic-defect-tetrahedral-gauge-frame-branch-decision-gate]]
закрыл развилку отрицательно для текущего носителя. Чистый составной
третий момент существует и имеет стабилизатор `A4`, но
`End(Kfam)=10V0+15V1+9V2` не содержит спина три. Упорядоченный кадр
полностью нарушает один левый `SO(3)`. Поэтому для сохранения дискретной
калибровочной голономии выбран следующий минимальный тест внешнего
носителя `Sym0^3(V3)`.

## Links

- [[version6-tetrahedral-parent-action-pre-gate-audit]]
- [[so3-a4-spin3-parent-action-literature-2026]]
- [[version6-bosonic-defect-family-connection-parent-identification-gate]]
- [[version4-family-defect-projector-supercurvature-gate]]
- [[version4-family-defect-gauge-family-locking-gate]]
- [[version5-commuting-square-readout-gate]]
- [[version6-matter-birth-program]]
- [[tetrahedratic-composite-order-literature-2026]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_tetrahedral_gauge_mass_parent_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_tetrahedral_gauge_mass_parent_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_tetrahedral_gauge_mass_parent_gate_results.json`