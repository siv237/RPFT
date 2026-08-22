# Version VI: энергосохраняющий четырёхтактный quench

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Минимальная автономная модель проверена при строгом условии
`[W,Hs+Hc]=0`. Энтропийная ёмкость четырёх состояний достаточна, но
невырожденная энергетическая лестница не может охладить qutrit до
кристаллической фазы.

## Exact Bound

Для

- `Hs = epsilon diag(0,1,1)`;
- `Hc = epsilon diag(0,1,2,3)`;
- исходного `I3/3`;
- произвольного чистого состояния часов

получено

`a_out <= [p0+max(p1,p0)+max(p2,p1)+max(p3,p2)]/3 <= 2/3`.

Требуемая фаза имеет `a*=0.9121665963...`, поэтому дефицит равен
`0.2454999296...`.

## Obstruction

Поперечный уровень qutrit имеет кратность два. Обе ортогональные
компоненты должны передать одинаковую энергию, но невырожденные часы имеют
только одну принимающую ground-clock моду на каждом разрыве. Унитарность
не позволяет сложить две ортогональные компоненты в одну моду.

Четыре характерных значения `1,i,-1,-i` различны, поэтому сами по себе не
дают необходимого энергетического вырождения.

## Reopening Conditions

- две существующие копии одного резонансного характера;
- второй резонансный канал;
- parent-derived неаддитивная энергия взаимодействия;
- выведенные начальные корреляции.

Расщеплять поперечный дублет запрещено: это разрушит точную `RP2`-орбиту.

## Next Test

Гейт [[version6-existing-multiplicity-resonant-sink-gate]] нашёл настоящую
кратность три в аффинном `P3`-углу. Минимальный невырожденный запрет
сохраняется, но полная аффинная архитектура переоткрыта; теперь требуется
нелинейный осеселективный перенос без готового `P`.

## Links

- [[version6-internal-entropy-transfer-cooling-gate]]
- [[thermal-operations-energy-degeneracy-literature-2026]]
- [[version5-transition-primitive-scientific-language-gate]]
- [[version6-matter-birth-program]]
- [[version6-existing-multiplicity-resonant-sink-gate]]

## Source Notes

- `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex`
- `s2t/audits/s2t_v6_clock_controlled_energy_conserving_quench_gate.py`
- `s2t/results/s2t_v6_clock_controlled_energy_conserving_quench_gate_results.json`