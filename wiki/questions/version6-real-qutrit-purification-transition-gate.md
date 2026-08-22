# Version VI: энтропийно-ориентационный переход

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Линейный Gibbs-функционал проекта не способен спонтанно породить вакуум
`RP2`: симметричный Hamiltonian оставляет `I3/3`, а несимметричный заранее
вставляет ось. Минимальный нелинейный контроль
`Tr(R log R)-kappa(Tr(R^2)-1/3)` имеет точный переход первого рода при
`kappa=log(4)`.

## Main Result

- при переходе сосуществуют спектры `(1/3,1/3,1/3)` и
  `(2/3,1/6,1/6)`;
- одноосный спектр уже создаёт орбиту `SO(3)/O(2)=RP2`;
- полная очистка до ранга один не требуется;
- текущий родитель не выводит отрицательный член чистоты, его знак или
  коэффициент;
- `1/7` является откликом уже выбранного дефекта и не может быть назначено
  коэффициентом перехода.

## Next Test

Интегрировать обменный Real-мост при общем семейном состоянии и проверить,
возникает ли из его флуктуаций отрицательное взаимодействие `-Tr(R^2)` с
фиксированной нормировкой.

## Links

- [[version6-rp2-geometric-phase-derivation-gate]]
- [[rp2-vacuum-manifold-and-nematic-transition-literature-2026]]
- [[version6-exchange-bridge-minimal-parent-gate]]
- [[version4-variational-family-state-gate]]
- [[version4-gibbs-free-energy-carrier-gate]]

## Source Notes

- `s2t/gates/version6_real_qutrit_purification_transition_gate.tex`
- `s2t/audits/s2t_v6_real_qutrit_purification_transition_gate.py`
- `s2t/results/s2t_v6_real_qutrit_purification_transition_gate_results.json`