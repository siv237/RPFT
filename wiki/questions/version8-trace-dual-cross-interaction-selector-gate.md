# Следово-двойственный селектор cross-взаимодействия

> Status: working
> Type: question
> Updated: 2026-08-30

## Summary

Конечный суперслед полевой суперсвязности задаёт на полном cross-модуле
`M_2x3(C)` точную вещественную метрику `K_B=3 I_12`. Если минимальная
jump-среда отождествляется с метрически двойственным модулем относительно
того же следа, то rate-метрика фиксируется как `R=K_B^-1=I_12/3`, а
каноническая связь — как `C_tr=I_12/sqrt(3)`. Это условный геометрический
селектор формы cross-скоростей, но не вывод физической единицы времени.

## Problem

После построения repeated-interaction Hamiltonian оставались восемь
вещественных параметров его gauge-допустимой связи и четыре параметра
симметричной rate-метрики `C^T C`, видимой редуцированным процессом.
Требовалось проверить, выбирает ли уже существующая полевая геометрия
каноническую точку этого конуса.

## Search for solution

- На 12 вещественных matrix-unit направлениях `B in M_2x3(C)` точно
  вычислена форма `Tr(delta D_B^(1) delta D_B^(2))=3 I_12`.
- Минимальная среда типизирована как двойственный модуль, что даёт
  coevaluation-связь `K_B^-1/2`.
- Проверено, что все квадратные связи с тем же скалярным Gram-оператором
  имеют вид `C=O/sqrt(3)` и отличаются лишь ортогональным кадром среды.
- Равенство коротковременного генератора `(1/3)L_cross` проверено на всех
  441 матричных единицах `M_21(C)`.
- Проверено сохранение ранее найденной полярной cross-оси.

## Expected result

Форма cross-rate метрики должна быть единственной с точностью до общего
масштаба времени, если принцип метрически двойственной среды принят явно.
Gauge-симметрия сама по себе не должна повышаться до этого принципа.

## Compliance check

- Полевая метрика: `3 I_12`, точно, без Float.
- Двойственная rate-метрика: `I_12/3`.
- Каноническая coupling-матрица: `I_12/sqrt(3)`.
- Полный real interaction-коммутант: `8`.
- Симметричный rate-коммутант: `4`.
- Проверенных matrix-unit: `441`.
- LCF-обязательств гейта: `9`.
- Общий реестр: `16` гейтов, `110` обязательств.
- Не выведены: общий масштаб времени, источник свежих ancilla, скорости
  linking/`SU(3)`/`SU(2)`/`U(1)` и сам принцип двойственной среды из одного
  родительского действия.

## Links

- [[version8-microscopic-repeated-interaction-hamiltonian-gate]] — исходная
  свобода coupling- и rate-метрик.
- [[version8-gauge-closed-field-space-superconnection-gate]] — полевая
  суперсвязность, чей след задаёт `K_B`.
- [[version8-cross-arrow-covariance-origin-gate]] — сохраняемая полярная ось.
- [[version8-lcf-proofdsl-architecture-gate]] — формальный реестр.
- [[version8-dynamic-physical-closure-redteam-gate]] — граница физического
  статуса.
- [[version8-metric-dual-environment-parent-action-origin-gate]] — точная
  проверка того, выводится ли Riesz-принцип из старого действия.

## Source Notes

- `s2t/gates/version8_trace_dual_cross_interaction_selector_gate.tex`
- `s2t/audits/s2t_v8_trace_dual_cross_interaction_selector_gate.py`
- `s2t/results/s2t_v8_trace_dual_cross_interaction_selector_gate_results.json`
- `s2t/proofdsl/examples/version8_trace_dual_cross_coupling.py`