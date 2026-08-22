# Version VI: кинетика проекторной кристаллизации

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Фазовый переход классифицирован по признанной теории переходов первого
рода. Найденный статический функционал допускает как нуклеацию отдельных
`RP2`-доменов, так и взрывной спинодальный распад глубоко переохлаждённой
изотропной среды.

## Exact Landscape

- ordered-ветвь появляется при `beta_ord = 1.3417938971...`;
- равновесный переход происходит при `beta_c = 1.5426695409...`;
- седловой барьер при сосуществовании равен `0.0571783574...`;
- изотропная кривизна равна `9/2 - 3 beta/7`;
- точная изотропная спинодаль: `beta_sp = 21/2 = 10.5`.

Между `beta_c` и `beta_sp` гладкая изотропная среда уже не является
глобальным минимумом, но всё ещё локально устойчива. Она может долго
оставаться переохлаждённой.

## Kinetic Verdict

- мелкое переохлаждение: распад через зародыши Лангера;
- глубокое переохлаждение: отрицательная мода и спинодальный распад;
- разные области выбирают независимые оси в `RP2`;
- несогласованность доменов создаёт проекторные дефекты;
- обычный Kibble--Zurek напрямую неприменим, потому что переход первого
  рода; допустим гибрид с нуклеацией.

## Open Boundary

Статика не задаёт подвижность, шум, натяжение интерфейса и скорость quench.
Главное: всё ещё не выведен внутренний закон роста `beta`. Поэтому
``взрыв как потеря устойчивости самой среды'' теперь математически возможен,
но условен относительно внутреннего переноса энергии и энтропии.

## Next Test

Гейт [[version6-internal-entropy-transfer-cooling-gate]] показал, что
четырёхсостояний носитель энтропийно достаточен и замкнутая унитарная орбита
существует. Теперь требуется энергосохраняющий автономный гамильтониан,
который реализует этот перенос без внешнего управления.

## Links

- [[version6-tensor-square-relative-carrier-normalization-gate]]
- [[first-order-projective-crystallization-kinetics-literature-2026]]
- [[version6-projective-quench-parent-dynamics-gate]]
- [[version6-nongaussian-spatial-stiffness-saturation-gate]]
- [[version6-matter-birth-program]]
- [[version6-internal-entropy-transfer-cooling-gate]]

## Source Notes

- `s2t/gates/version6_modular_cooling_projective_transition_gate.tex`
- `s2t/audits/s2t_v6_modular_cooling_projective_transition_gate.py`
- `s2t/results/s2t_v6_modular_cooling_projective_transition_gate_results.json`