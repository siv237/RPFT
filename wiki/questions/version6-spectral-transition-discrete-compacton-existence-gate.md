# Том VI: точный двухузловой компактон

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверена последняя лазейка безмассовой составной монеты: точное решение
конечной опоры, не использующее экспоненциальный хвост.

## Search for solution

Сначала доказан одноузловой запрет условным сдвигом. Затем решено условие
полного разворота двух граничных потоков для сбалансированной хиральной
пары на двух соседних узлах.

## Expected result

Успех требовал точного отсутствия утечки и возврата профиля после шага с
общей фазой без внешнего потенциала и массового угла.

## Compliance check

- ненулевой одноузловой стационарный профиль невозможен;
- точный двухузловой compacton существует;
- условие существования: `kappa=2(2m+1)pi`;
- минимальная положительная ветвь: `2pi`;
- собственная фаза: `±i`, фазовый период четыре;
- первые три ветви имеют остаток и утечку ниже `1e-15`;
- точная ветвь сохраняет всю норму на двух узлах после 100 шагов;
- расстройка создаёт утечку `sin²(pi*epsilon/2)`;
- устойчивость, физический шаг и наблюдаемая карта ещё не выведены.

## Следующий гейт

[[version6-spectral-transition-discrete-compacton-stability-quantization-gate]]
вычислит монодромию четырёхшаговой орбиты и отделит физические возмущения.

## Последующая коррекция

[[version6-spectral-transition-discrete-compacton-dynamical-capture-gate]]
показал, что собственные состояния `±i` не исчерпывают решения:
произвольная пара сбалансированных внутренних векторов образует
непрерывное семейство точных двухшаговых компакттонов `F²=-1`.

## Links

- [[version6-spectral-transition-discrete-composite-higgs-spatial-binding-gate]]
- [[version6-spectral-transition-discrete-chiral-coin-closure-gate]]
- [[nonlinear-quantum-walk-discrete-dirac-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_compacton_existence_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_compacton_existence_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_compacton_existence_gate_results.json`