# Version VI: составная проекторная связность

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Из самого поля порядка выведена коэффициент-свободная составная связность

`A_Q=[Q,dQ]/Delta^2`.

Она удаляет дальнюю энергетическую расходимость проекторного ежа и
допускает гладкий конечный пробный профиль.

## Positive Result

- для `Q=q(P-I3/3)` имеем `A_Q=(q/Delta)^2[P,dP]`;
- при `q -> Delta` ковариантная производная удаляет вращение директора;
- профиль `q=Delta r^2/(r^2+R^2)` делает `Q` и `A_Q` гладкими в ядре;
- плотности `|DQ|^2`, `|F|^2` и `V` убывают как `r^-6`, `r^-4`, `r^-4`;
- все три пространственных интеграла конечны;
- положительный curvature-член способен предотвратить коллапс размера.

## Gauge Boundary

Связность правильно преобразуется на двух направлениях `SO(3)/O(2)`, но
не получает неоднородного члена стабилизатора `O(2)`. Поэтому это
составная косетная связность, а не три новых независимых gauge-бозона.

Spin-cover Тома V даёт недостающую хопфову линию `L/L*` на граничной
сфере и классы `+15/-15`, но её гладкое продолжение через ядро по-прежнему
упирается в ранговый no-go `20x15`.

## Next Test — completed

Тест выполнен в [[version6-composite-connection-callias-fredholm-gate]].
Векторная масса фредгольмова, но имеет индекс ноль. Spin-cover масса даёт
индекс один на линию и пятнадцать после коэффициентного умножения, однако
её finite-carrier оператор не выведен.

## Links

- [[version6-spatial-projective-defect-energy-spectrum-gate]]
- [[composite-projector-connection-literature-2026]]
- [[version5-hopf-pair-odd-core-extension-gate]]
- [[version5-spatial-so3-superconnection-parent-trace-gate]]
- [[version5-spin-cover-defect-sphere-bridge-gate]]
- [[version6-matter-birth-program]]
- [[version6-composite-connection-callias-fredholm-gate]]

## Source Notes

- `s2t/gates/version6_gauged_projective_spin_cover_parent_gate.tex`
- `s2t/audits/s2t_v6_gauged_projective_spin_cover_parent_gate.py`
- `s2t/results/s2t_v6_gauged_projective_spin_cover_parent_gate_results.json`