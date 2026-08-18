# Глобальный носитель и ненулевой сектор

> Status: working
> Type: question
> Updated: 2026-08-18

## Summary

Главное окружностное расслоение над `S2` с классом Черна `n` имеет полное
пространство `L(|n|,1)`; при `n=0` это `S2 x S1`. Поэтому полный носитель
`S3` строго принуждает `|c1|=1`, а `RP3` — `|c1|=2`. После умножения на
коэффициентный проектор ранга 15 хопфов носитель принуждал бы класс
`+15/-15` и исключал бы нулевой сектор.

Но текущая моритовская градуировка фиксирует только относительное правило
`E -> L`, `E* -> L*`. Оно совместимо и с тривиальной линией, поэтому само
не выбирает величину `c1`.

Точный оставшийся разрыв: проектный точечный дефект живёт первоначально в
`RP2`, а его ориентированный подъём к `S2` ещё не отождествлён с канонической
сферой пространственных спин-направлений `Spin(3)/Spin(2)`. Пока не доказано,
что физическая линия перехода является ассоциированной линией
`Spin(3) -> S2_defect`, нулевой сектор нельзя считать исключённым.

## Verdict

- Теорема `S3 carrier => |c1|=1`: **закрыта**.
- Следствие `|c1|=1 => coefficient class +/-15`: **закрыто**.
- Физическое отождествление носителя: **открыто**.
- Ненулевой сектор в версии V: **условно принуждён, но ещё не выведен**.

## Subsequent Resolution

[[version5-spin-cover-defect-sphere-bridge-gate]] впоследствии закрыл
отождествление для единственного `SO(3)`-эквивариантного ежа: карта
`n -> [n]` имеет два подъёма степеней `+1/-1` и даёт хопфову пару.
Открытым осталось не строение линии выбранного дефекта, а вывод самого
точечного центра и его граничного условия из однородного вакуума.

## Links

- [[version5-eta-wzw-real-pair-phase-gate]]
- [[version5-hopf-fell-line-transition-lift-gate]]
- [[version5-hopf-line-morita-orientation-functor-gate]]
- [[version5-projective-hedgehog-point-defect-gate]]
- [[version5-spatial-so3-superconnection-parent-trace-gate]]
- [[version5-topological-closure-deficit-gate]]
- [[global-circle-carrier-sector-literature-2026]]
- [[transition-primitive]]
- [[version5-spin-cover-defect-sphere-bridge-gate]]

## Source Notes

- `s2t/gates/version5_global_carrier_forced_nontrivial_sector_gate.tex`
- `s2t/audits/s2t_v5_global_carrier_forced_nontrivial_sector_gate.py`
- `s2t/results/s2t_v5_global_carrier_forced_nontrivial_sector_gate_results.json`