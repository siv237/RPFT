# Том VI: динамический захват в компакттонное многообразие

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, возникает ли компактон из обычных локализованных начальных
состояний и является ли орбита с фазой `±i` единственным endpoint.

## Search for solution

Аналитически расширена двухузловая конструкция на независимые
сбалансированные векторы двух узлов. Затем выполнены сканы относительной
фазы, амплитудного и хирального дисбаланса, а также 36 проспективных
испытаний одноузловых, двухузловых и гауссовых случайных состояний.

## Expected result

Механизм рождения требовал открытой области захвата в один изолированный
локализованный endpoint, а не только сохранения специально приготовленной
орбиты.

## Compliance check

- при `kappa=2pi` существует непрерывное точное семейство `F²(Psi)=-Psi`;
- два сбалансированных внутренних вектора могут выбираться независимо;
- фазы `±i` являются лишь двумя одношаговыми собственными точками;
- все 16 проверенных относительных фаз остаются точными двухшаговыми
  компакттонами;
- амплитудный баланс `p=1/2` не восстанавливается из соседних значений;
- хиральный баланс `q=1/2` также не выбирается динамически;
- в 36 заранее заданных обычных испытаниях получено ноль захватов;
- прежняя локальная устойчивость относится к неединственному решёточному
  многообразию, а не к единственной частице;
- R2, R3 и единственность R4 не закрыты.

## Следующий гейт

[[version6-spectral-transition-compacton-c4-affine-selector-admissibility-gate]]
проверяет последнюю ретроспективную зацепку: могут ли характеры `C4` и
аффинный сток выделить `±i` без ручного проектора. После него итоговый
ledger перейдёт к замораживанию ветви.

## Links

- [[version6-spectral-transition-discrete-compacton-existence-gate]]
- [[version6-spectral-transition-discrete-compacton-stability-quantization-gate]]
- [[version6-spectral-transition-discrete-compacton-physical-scale-map-gate]]
- [[version6-spectral-transition-compacton-c4-affine-selector-admissibility-gate]]
- [[nonlinear-quantum-walk-discrete-dirac-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_compacton_dynamical_capture_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_compacton_dynamical_capture_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_compacton_dynamical_capture_gate_results.json`