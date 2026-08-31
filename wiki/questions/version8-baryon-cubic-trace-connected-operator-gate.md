# Кубический следовой связный оператор трёх копий

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

После канонического центрирования полный 42-мерный кадр остаётся
невырожденным и задаёт тот же двойной коммутатор. Симметричный тензор
`d_abc=Tr(Fhat_a{Fhat_b,Fhat_c})/2` имеет `168` ненулевых неупорядоченных
компонент: `140 TTG` и `28 GGG`.

Поднятие индексов обратной следовой метрикой даёт ненулевой
самосопряжённый и перестановочно-инвариантный оператор
`W3=d^abc Fhat_a tensor Fhat_b tensor Fhat_c`. Все его одночастичные
частичные следы равны нулю, поэтому это настоящий связный трёхкопийный
носитель.

## Граница

Оператор каноничен алгебраически, но член `lambda_3 W3` отсутствует в
текущем квадратичном родительском действии. Не выведены `lambda_3`, знак,
пространственное продолжение и полное ядро Фаддеева. Чистой компоненты
`TTT` нет: связный канал обязательно содержит калибровочное направление.

## Связи

- [[version8-baryon-connected-three-body-kernel-admission-gate]]
- [[version8-full-noise-trace-frame-metric-gate]]
- [[version8-full-noise-42-jump-gksl-fixed-algebra-gate]]
- [[baryon-six-point-faddeev-literature-2026]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_baryon_cubic_trace_connected_operator_gate.tex`
- `s2t/audits/s2t_v8_baryon_cubic_trace_connected_operator_gate.py`
- `s2t/results/s2t_v8_baryon_cubic_trace_connected_operator_gate_results.json`