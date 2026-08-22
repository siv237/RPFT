# Том VI: флоке-устойчивость двухузлового компакттона

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, является ли точный компактон при `kappa=2pi` устойчивым
локализованным состоянием, а не только тонко настроенной периодической
орбитой с нулевой утечкой.

## Search for solution

Вычислена полная вещественная производная четырёхшаговой возвратной карты
на периодических решётках `N=8,12,16`. Отделены фазовые и слабые
симметрийные касательные, измерено ненормальное переходное усиление и
выполнен 80-шаговый тест конечных случайных возмущений на 256 узлах.

## Expected result

Локальный тест считался пройденным, если полная и симметрийно
редуцированная монодромии не имеют мультипликаторов с модулем выше единицы
за численным допуском, а малые возмущения сохраняют ядро.

## Compliance check

- остаток четырёхшаговой орбиты: `2.61e-15`;
- спектральный радиус для `N=8,12,16`: не выше `1+1.1e-9`;
- расширяющих мультипликаторов при допуске `1e-5`: ноль;
- после удаления четырёх независимых симметрийных касательных
  редуцированный радиус равен `1.000000000901`;
- в редуцированном секторе остаются 128 нейтральных мультипликаторов;
- максимальное проверенное переходное усиление равно `11.83923`, но
  экспоненциальный рост не обнаружен;
- при `delta<=0.05` после 80 шагов в ядре остаётся более `0.995` нормы;
- для фиксированного случайного направления срыв начинается между
  `delta=0.06` и `0.07`;
- ветвь `2pi` проходит численный локальный флоке-тест, но полная
  нелинейная и асимптотическая устойчивость не доказаны.

## Следующий гейт

[[version6-spectral-transition-discrete-compacton-physical-scale-map-gate]]
проверит, фиксируют ли прежние масштабы S2T физический шаг решётки, размер
двухузлового ядра и квазиэнергию фазы `±i`.

## Последующая коррекция

[[version6-spectral-transition-discrete-compacton-dynamical-capture-gate]]
переинтерпретировал нейтральные направления: локальная устойчивость
относится к непрерывному компакттонному многообразию, а не к единственному
изолированному endpoint.

## Links

- [[version6-spectral-transition-discrete-compacton-existence-gate]]
- [[version6-spectral-transition-discrete-composite-higgs-spatial-binding-gate]]
- [[nonlinear-quantum-walk-discrete-dirac-literature-2026]]
- [[version5-transition-primitive-scientific-language-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_discrete_compacton_stability_quantization_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_discrete_compacton_stability_quantization_gate.py`
- `s2t/results/s2t_v6_spectral_transition_discrete_compacton_stability_quantization_gate_results.json`