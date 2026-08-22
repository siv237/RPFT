# Том VI: хиральное замыкание дискретной монеты

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, можно ли замкнуть сектор `L_L + e_R` без внешнего направления
Хиггса и свободного юкавского ребра.

## Search for solution

Сопоставлены две монеты. Внешний `H` воспроизводит обычный одномерный
юкавский интертвинер со свободной амплитудой. В новой ветви построен
составной дублет `H_eff = ell*conj(e)` непосредственно из состояния.

## Expected result

Успех требовал точной калибровочной ковариантности, сохранения нормы,
единственного устойчивого хирального endpoint и отсутствия свободной связи.

## Compliance check

- составной генератор самосопряжён и локален;
- норма и калибровочная ковариантность проходят с машинной точностью;
- внешний `H` остаётся старым юкавским ребром со свободным `y`;
- составной `H_eff` устраняет внешний выбор направления;
- точная карта населённости имеет инвариантные страты `p=0,1/2,1`;
- коэффициент `kappa` и физический масштаб не выведены;
- единственный endpoint и пространственная локализация не получены.

## Следующий гейт

[[version6-spectral-transition-discrete-composite-higgs-spatial-binding-gate]]
соединит составную хиральную монету с пространственным сдвигом.

## Links

- [[version6-spectral-transition-discrete-equivariant-coin-selector-gate]]
- [[version6-spectral-transition-discrete-nonlinear-parent-reopening-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[version5-holonomy-projector-defect-multiplicity-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_chiral_coin_closure_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_chiral_coin_closure_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_chiral_coin_closure_gate_results.json`