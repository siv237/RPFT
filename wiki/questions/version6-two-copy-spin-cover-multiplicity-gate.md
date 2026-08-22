# Version VI: двухкопийная spin-cover кратность

> Status: mature
> Type: question
> Updated: 2026-08-19

## Summary

Последняя двухкопийная лазейка закрыта. Ни семейный tensor-square, ни
пара порядков `LR/RL`, ни тензорные произведения физического `H15`, ни
повтор rank-адресов атласа не дают каноническую равнозарядную
`C2_twist`, на которой полный Pauli-фактор коммутирует с gauge-алгеброй.

## Results

- `C3 tensor C3 = 1+3+5`, каждое слагаемое имеет кратность один;
- коммутант диагонального `SO(3)` трёхмерен и абелев, блока `M2` нет;
- пространство порядков `LR/RL` имеет только абелев коммутант
  `span{I,SWAP}`, а после статистического проектора каждый сектор
  одномерен;
- в `H15 tensor H15` отсутствуют `L_L,u_R`, в смешанном квадрате —
  `d_R`, поэтому полной копии `H15` нет;
- два rank-four слота `(16,4,4)/24` имеют Gram-матрицу ранга один: это
  повтор одного и того же `W+Y`-проектора;
- `X/Xbar` имеют одинаковый ранг шесть, но сопряжённые gauge-заряды и не
  образуют complex-linear дублет.

## Verdict

Spin-cover fermion-ветвь текущего конечного родителя закрыта. Сохраняются
бозонное поле `Q`, конечный составной дефект, хопфова линия и граничный
класс `+15/-15`. Для физических локализованных фермионов требуется новый
равнозарядный multiplicity-модуль либо явно новая `Spin^h`-архитектура.

## Links

- [[version6-spin-cover-carrier-parent-derivation-gate]]
- [[version6-naive-atlas-order-parameter-rank-bridge-gate]]
- [[two-copy-spin-cover-multiplicity-literature-2026]]
- [[version6-two-copy-affine-dilation-gate]]
- [[version6-exchange-bridge-exterior-square-parent-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_two_copy_spin_cover_multiplicity_gate.tex`
- `s2t/audits/s2t_v6_two_copy_spin_cover_multiplicity_gate.py`
- `s2t/results/s2t_v6_two_copy_spin_cover_multiplicity_gate_results.json`