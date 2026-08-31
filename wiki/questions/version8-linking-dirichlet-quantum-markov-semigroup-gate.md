# Связывающая форма Дирихле и квантово-марковская полугруппа

> Status: mature
> Type: question
> Updated: 2026-08-28

## Summary

Физическая инцидентность `A0:C11 -> C10` канонически задаёт на endpoint-
алгебре `M11(C) direct_sum M10(C)` симметричную квантово-марковскую
полугруппу. Процесс переходов получен без нового коэффициента, но его
неподвижная алгебра имеет размерность 41 и не выбирает классические события.

## Key Points

- Linking-оператор имеет блоки `D_A=block(0,A0*;A0,0)`.
- Генератор `L=-ad(D_A)^2/2` сохраняет endpoint-алгебру, единицу и след.
- Перекрёстные члены `A0* Y A0` и `A0 X A0*` дают ненулевой перенос между
  source- и target-углами.
- Полная положительность следует из гауссового Schur-ядра в собственном
  базисе `D_A`; она также проверена численно на трёх временах.
- Матрица генератора имеет размер `221`, не имеет положительных собственных
  значений и имеет 41 нулевое направление.
- Вклад `36` в неподвижную алгебру создаётся шестикратным сингулярным
  значением `1`; ещё четыре направления дают простые значения и одно —
  индексное ядро.
- Получена некоммутативная динамика, но не каноническая максимальная
  коммутативная алгебра событий.

## Links

- [[version8-full-correlation-kernel-locality-reconstruction-gate]] —
  причина сохранять полную полугруппу, а не только её спектр.
- [[version7-incidence-transfer-markov-weight-gate]] — полярный UCP-перенос.
- [[version7-minimal-curvature-support-trace-gate]] — полный связывающий
  фактор на 21-мерной опоре.
- [[quantum-markov-dirichlet-fixed-algebra-literature-2026]] — внешний
  математический контекст.

## Source Notes

- `s2t/gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex`
- `s2t/audits/s2t_v8_linking_dirichlet_quantum_markov_semigroup_gate.py`
- `s2t/results/s2t_v8_linking_dirichlet_quantum_markov_semigroup_gate_results.json`