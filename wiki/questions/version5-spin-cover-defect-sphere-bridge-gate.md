# Спин-накрытие и сфера проекторного дефекта

> Status: working
> Type: question
> Updated: 2026-08-18

## Summary

Пространственная сфера направлений имеет вид `SO(3)/SO(2)=S2`, а
пространство неориентированных проекторных осей — `SO(3)/O(2)=RP2`.
Включение стабилизаторов задаёт каноническую карту `q(n)=[n]`.

Это единственная `SO(3)`-эквивариантная карта `S2 -> RP2`. Она имеет два
глобальных подъёма `n` и `-n` степеней `+1/-1`. Их спинорные собственные
линии являются хопфовой парой `L/L*` с `c1=+1/-1`; коэффициентный проектор
ранга 15 даёт классы `+15/-15`.

Тем самым spin-cover bridge для уже выбранного вращательно-эквивариантного
проекторного ежа закрыт без нового семейного дублета. Уточнена роль
моритовой градуировки: она согласует два знака с `E/E*`, а величина класса
приходит от степени ежа.

## Open Boundary

Единственность ежа внутри эквивариантного сектора не доказывает, что
однородный вакуум обязан создать точечный центр и проколотую сферу.
Граничное условие ежа пока является условием сектора, а не следствием
родительского действия. Поэтому безусловное существование материи ещё не
доказано.

## Links

- [[version5-global-carrier-forced-nontrivial-sector-gate]]
- [[version5-projective-hedgehog-point-defect-gate]]
- [[version5-hopf-line-morita-orientation-functor-gate]]
- [[version5-topological-closure-deficit-gate]]
- [[projective-hedgehog-spin-cover-literature-2026]]
- [[transition-primitive]]

## Source Notes

- `s2t/gates/version5_spin_cover_defect_sphere_bridge_gate.tex`
- `s2t/audits/s2t_v5_spin_cover_defect_sphere_bridge_gate.py`
- `s2t/results/s2t_v5_spin_cover_defect_sphere_bridge_gate_results.json`