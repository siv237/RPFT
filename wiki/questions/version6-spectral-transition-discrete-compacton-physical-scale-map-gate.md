# Том VI: физическая шкала двухузлового компакттона

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, превращают ли точные числа `kappa=2pi`, фаза `±i` и опора на
двух узлах компактон в предсказание физического размера и массы.

## Search for solution

Составлен ранг размерных условий для шага `a`, времени `delta_t` и энергии
`E`; проверены масштаб объединения S2T, прежнее планковское сопоставление и
общий масштаб суперсвязности. Отдельно сопоставлены компактонное условие
`kappa=2pi` и непрерывное масштабирование `kappa=g*a`.

## Expected result

Абсолютная шкала считалась выведенной только при наличии дополнительного
родительского уравнения, устраняющего одновременное преобразование
`(a,delta_t,E)->(lambda*a,lambda*delta_t,E/lambda)`.

## Compliance check

- две размерные связи имеют ранг два для трёх переменных;
- остаётся одно непрерывное масштабное направление;
- условно выводится `E*L=pi*hbar*c` и `L/lambda_C=pi`;
- подстановка `a=alpha*hbar*c/Lambda_S2T` сохраняет произвольный `alpha`;
- квазиэнергия определена по модулю `2pi` и требует временного шага;
- прежнее планковское сопоставление уже признано неконтролируемым;
- общий масштаб суперсвязности и скрытая иерархия в проекте отсутствуют;
- при фиксированном `g` компактон не переживает предел `a->0`, поскольку
  сохранение `kappa=2pi` требует `g=2pi/a->infinity`;
- абсолютные размер и масса не предсказаны, R5 не закрыт.

## Следующий гейт

[[version6-spectral-transition-discrete-compacton-dynamical-capture-gate]]
проверит, захватывается ли открытое множество начальных пакетов в точную
двухузловую орбиту.

## Links

- [[version6-spectral-transition-discrete-compacton-stability-quantization-gate]]
- [[version6-single-thread-scale-hierarchy-branch-decision-gate]]
- [[version5-projector-superconnection-common-scale-gate]]
- [[version4-absolute-scale-eft-validity-gate]]
- [[nonlinear-quantum-walk-discrete-dirac-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_compacton_physical_scale_map_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_compacton_physical_scale_map_gate_results.json`