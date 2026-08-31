# Общая следовая нормировка cross-carrier вложения

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

На разделённой алгебре `A_src direct_sum A_aux` общий нормированный
положительный след имеет веса `p,q>0`, `p+q=1`. Pullback-изометрия карты
`M_kappa` даёт `kappa=sqrt(p/q)`, но не выбирает отношение весов.

Точные следы `(p,q)=(1/2,1/2)` и `(4/5,1/5)` дают соответственно
`kappa=1` и `kappa=2`. Оба полностью положительны, нормированы и
калибровочно-инвариантны.

## Граница

Общий след может выбрать нормировку только после включения двух углов в
одну linking-алгебру с ненулевым off-diagonal bimodule. Такого моста для
барионного auxiliary carrier пока нет.

## Связи

- [[version8-baryon-c0-minimal-cross-carrier-morphism-architecture-gate]]
- [[version8-field-to-noise-chain-map-pullback-metric-gate]]
- [[version8-linking-dirichlet-quantum-markov-semigroup-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_common_trace_embedding_normalization_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_common_trace_embedding_normalization_gate.py`
- `s2t/results/s2t_v8_baryon_c0_common_trace_embedding_normalization_gate_results.json`