# Version VII: ранга-один конденсат когерентности стрелок

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Построен минимальный потенциал, который без фиксированной оси запускает
когерентность разрешённых стрелок и выбирает матрицу ранга один.

## Exact Result

Для `B in M_2x3(C)` и прямого минус перекрёстного тензора `W` рассмотрено

$$
S_{coh}(B)=(Tr(BB^*)-3)^2+\|W(B)\|^2,
\qquad \|W(B)\|^2=4\det(BB^*).
$$

Нули имеют точный вид

$$
B_*=\sqrt3\,u v^*,
$$

то есть `rank B=1`. Нуль поля имеет двенадцать отрицательных мод. У
ненулевого минимума полный вещественный гессиан содержит семь касательных
нулей и пять положительных собственных значений `24`.

Индуцированное копийное состояние `BB*/Tr(BB*)` является чистым проектором,
поэтому модулярная высота возникает после конденсации, а не вставляется как
готовая `sigma_x`.

## Boundary

Это пока потенциал уровня конфигураций. В текущем родителе не показана одна
Real-градуированная суперсвязность, чья единая норма кривизны одновременно
даёт радиальный квадрат и норму внешнего квадрата с нужной относительной
метрикой.

## Verdict

Задача рождения ранга-один когерентности закрыта условно на уровне
потенциала. Родительское происхождение действия остаётся открытым.

## Subsequent Result

[[version7-edge-coherence-spectral-parent-gate]] устранил ручную сумму
слагаемых. Полные следы одного трёхузлового нечётного оператора дают
радиальный квадрат и положительный детерминант с фиксированным
коэффициентом `5/3`. Родительский вопрос закрыт на градуированном
спектральном уровне; строгая бимодульная реализация остаётся открытой.

## Links

- [[version7-universal-incidence-parent-admissibility-gate]]
- [[version7-modular-copy-projector-origin-gate]]
- [[version7-edge-coherence-formula-intuition-map]]
- [[version7-edge-coherence-spectral-parent-gate]]
- [[kernel-grassmannian-quiver-stability-literature-2026]]
- [[version7-rank-change-parent-program]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex`
- `s2t/audits/s2t_v7_edge_coherence_rank_one_condensate_gate.py`
- `s2t/results/s2t_v7_edge_coherence_rank_one_condensate_gate_results.json`