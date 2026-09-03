# Универсальное покрытие как граф рождения

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Семиузловой причинный путь канонически реализуется как шар радиуса три в
универсальном покрытии хопфовского цикла `C3`. Покрытие равно `Z`, проекция
задаётся `p(n)=n mod 3`, а высота `h(n)=n` возрастает на единицу вдоль
каждого ориентированного ребра. Получена точная дискретная история рождения,
но не физическое время или абсолютная длина.

## Key Points

- Проекции вершин и рёбер образуют цепной морфизм
  `B_C3 p1 = p0 B_cover`.
- На внутренних вершинах точно выполнено переплетение операторов соседства.
- Сдвиг на три является преобразованием деков; семиузловой путь — конечное
  окно бесконечной прямой, а не отдельный выбранный граф.
- `B_cover^T h=1`: каждое ориентированное ребро повышает высоту рождения на
  единицу.
- Рост шара равен `(1,3,5,7)`, а будущая полупрямая добавляет одну вершину
  за шаг.
- Сдвиг `h→h+c` не наблюдается; размерная карта остаётся `8/1` после
  `v_g=c`.
- Физический граф, абсолютная метрика и часы рождения имеют статус `0/3`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-cell-complex-edge-length-common-parent-origin-gate]] — незакрытая длина ребра.
- [[version10-cell-birth-four-volume-nonequilibrium-bath-local-causal-propagation-kernel-cell-complex-typed-embedding-gate]] — исходный семиузловой путь.
- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-two-reservoir-affinity-hopf-cycle-typed-origin-gate]] — хопфовский цикл основания.
- [[current-status-and-next-vectors]] — общий фронтир Тома X.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding.py`