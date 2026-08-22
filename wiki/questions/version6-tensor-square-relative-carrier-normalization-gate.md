# Version VI: tensor-square carrier и термическое переоткрытие

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Тензорный квадрат полной Real-пары не создаёт недостающий множитель два.
Same-orientation секторы дают суммарно `2e2(R)`, mixed-сектор после
нормировки является константой, а физический half-trace сокращает Real-
удвоение.

Raw antisymmetrizer `I-swap` равен `2P_-`; его коэффициент `4e2` является
ненормированным двойным счётом по сравнению с ортогональным проектором.

## Main Discovery

Усиление оператора не требуется, если вернуть температуру:

`F_beta(R)=Tr(R log R)+beta[S_rad(R)+2e2(R)]`.

Канонический внешний квадрат создаёт переход первого рода при

`beta_c = 1.5426695409...`.

В точке сосуществования упорядоченная фаза имеет спектр
`(0.9121666,0.0439167,0.0439167)` и орбиту `RP2`. При охлаждении система
переходит от изотропной среды к проекторным доменам.

## Casimir Clue

Левый и правый векторные `SO(3)`-казимиры дают `2+2=4`, точно совпадая с
raw coefficient. Но соответствующий лапласиан не выведен из текущего
`M35`/exchange parent и пока является только подсказкой.

## Status Boundary

В проекте существует `rho_beta=exp(-beta h_F)/Z`, но:

- абсолютное `beta` не вычислено;
- `h_F` скалярно на семейных триплетах;
- собственный модулярный поток не меняет состояние и его температуру;
- динамика пересечения `beta_c` ещё не выведена.

## Next Test

Следующий гейт [[version6-modular-cooling-projective-transition-gate]]
классифицировал нуклеационный и спинодальный режимы. Теперь требуется
вывести перенос энергии и энтропии, который заставляет внутреннее `beta`
пересечь найденные пороги без внешнего времени.

## Links

- [[version6-exchange-bridge-exterior-square-parent-gate]]
- [[tensor-square-exchange-thermal-transition-literature-2026]]
- [[version6-projective-quench-parent-dynamics-gate]]
- [[version5-modular-commutant-parent-correspondence-gate]]
- [[version6-real-qutrit-purification-transition-gate]]
- [[version6-matter-birth-program]]
- [[version6-modular-cooling-projective-transition-gate]]

## Source Notes

- `s2t/gates/version6_tensor_square_relative_carrier_normalization_gate.tex`
- `s2t/audits/s2t_v6_tensor_square_relative_carrier_normalization_gate.py`
- `s2t/results/s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json`
