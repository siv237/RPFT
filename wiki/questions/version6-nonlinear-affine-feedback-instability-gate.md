# Version VI: нелинейная аффинная обратная связь

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Найден первый коэффициент-свободный механизм, который не содержит
заранее выбранной оси, но усиливает любую малую семейную анизотропию:

`P(R)=R^2/Tr(R^2)`.

## Positive Result

- карта `SO(3)`-эквивариантна;
- `I3/3` является точным fixed point;
- traceless-возмущение усиливается вдвое за шаг;
- непрерывный поток `dR=R^2-Tr(R^2)R` имеет скорость роста `1/3`;
- случайная флуктуация сама выбирает ось в `RP2`.

## Saturation Failure

Состояние сосуществования
`(0.9121666,0.0439167,0.0439167)` после одного шага превращается в
`(0.9953854,0.0023073,0.0023073)`. Итерации быстро сходятся к чистому
проектору. Поэтому карта запускает упорядочение, но не удерживает
полноранговый мир-кристалл.

## Quantum Boundary

Нарушение выпуклой линейности равно `0.272165527...`; один фиксированный
CPTP-канал такую карту реализовать не может. Нужны постселекция, несколько
копий, feedback или выведенный mean-field предел.

Проект уже имеет внешний квадрат и tensor-square carrier, поэтому открыт
тест линейной двухкопийной дилатации, а не ручного введения нелинейной
квантовой механики.

## Next Test — completed

Двухкопийный тест выполнен в
[[version6-two-copy-affine-dilation-gate]]. SWAP-чтение виртуального
состояния точно, но один детерминированный линейный канал нормированную
квадратную карту не реализует. Поэтому квадратный feedback остаётся
эффективным/условным механизмом, а не автономной микродинамикой.

## Links

- [[version6-existing-multiplicity-resonant-sink-gate]]
- [[state-squaring-virtual-distillation-literature-2026]]
- [[version6-exchange-bridge-exterior-square-parent-gate]]
- [[version6-two-copy-affine-dilation-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_nonlinear_affine_feedback_instability_gate.tex`
- `s2t/audits/s2t_v6_nonlinear_affine_feedback_instability_gate.py`
- `s2t/results/s2t_v6_nonlinear_affine_feedback_instability_gate_results.json`