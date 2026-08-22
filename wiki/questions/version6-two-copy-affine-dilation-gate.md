# Version VI: двухкопийная дилатация квадратной карты

> Status: mature
> Type: question
> Updated: 2026-08-19

## Summary

Tensor-square carrier действительно содержит точное SWAP-чтение
наблюдаемых виртуального состояния `R^2/Tr(R^2)`, но не превращает его в
выход одного детерминированного линейного канала.

## Positive Result

- `Tr[(O tensor I) SWAP (R tensor R)]=Tr(O R^2)`;
- `Tr[SWAP (R tensor R)]=Tr(R^2)`;
- численный остаток на ста состояниях ниже `4.5e-16`;
- существующие tensor/exterior carriers достаточны для многокопийного
  чтения нелинейных функционалов.

## No-Go Result

Для одноосного семейства `R(t)` вход `R(t) tensor R(t)` квадратичен по
`t`, поэтому выход фиксированного линейного канала также не выше второй
степени. Целевая компонента
`t^2/[t^2+(1-t)^2/2]` рациональна; на рабочей сетке лучший квадратичный
fit оставляет остаток `0.1451715...`.

Следовательно, virtual distillation не является автономным обновлением
состояния. Нужны постселекция, измерительный feedback, дополнительная
запись результата или выведенный mean-field предел.

## Consequence

Фазовый функционал `Tr(R log R)+beta[S_rad+2e2(R)]` сохраняется, поскольку
его внешний член был выведен независимо. Можно переходить к спектру полей
в уже доказанной ordered-фазе, не выдавая квадратную карту за физический
закон движения.

## Links

- [[version6-nonlinear-affine-feedback-instability-gate]]
- [[state-squaring-virtual-distillation-literature-2026]]
- [[version6-projective-order-parameter-field-spectrum-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_two_copy_affine_dilation_gate.tex`
- `s2t/audits/s2t_v6_two_copy_affine_dilation_gate.py`
- `s2t/results/s2t_v6_two_copy_affine_dilation_gate_results.json`