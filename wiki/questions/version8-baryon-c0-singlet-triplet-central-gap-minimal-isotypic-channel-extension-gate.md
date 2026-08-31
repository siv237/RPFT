# Минимальное изотипическое канальное расширение

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Можно ли физически добавить минимальный endpoint `Z_R=(C,C,R)`, чтобы
получить три одинаковых coherence-канала `(e,X,Z)` и условный Hodge-портал?

## Search for solution

- Перебран полный строгий первопорядковый граф до и после добавления `Z_R`.
- Вычислены локальные аномалии и изменение заряженного хирального индекса.
- Отделён формальный Real-образ от независимого физического Weyl-партнёра.
- Построено минимальное вектороподобное завершение `Z_L+Z_R`.
- Перебраны все новые первопорядково разрешённые рёбра.
- Проверены размер и ориентация массового ядра и его совместимость с
  channel-`SO(3)`.

## Expected result

Одновершинный проход требовал сокращения аномалий и сохранения старого
хирального индекса. Условный ремонт должен был пройти эти проверки без
ручного удаления разрешённых рёбер и выбора массового ядра.

## Compliance check

- Один `Z_R` создаёт три новых строгих ребра, из них два coherence-рёбра.
- Его аномалии равны `(A221,Agrav,A111)=(0,1,1)`.
- Заряженный индекс меняется с `-1` на `-2`; admission-ledger равен `4/7`.
- Минимальный безопасный ремонт — физическая пара `Z_L+Z_R`; она сохраняет
  аномалии, Witten-паритет и индекс, structural ledger `6/6`.
- Полный граф пары содержит `23` ребра, из которых `9` новые, `3` желаемые
  и `6` лишние.
- Масса `C3_R -> C2_L` имеет одномерное, но неканоническое ядро.
- Ненулевая масса при текущем тривиальном левом действии не является
  channel-`SO(3)`-интертвейнером.
- Selector+origin ledger: `0/6`.

## Boundary

Физический носитель условно существует только после вектороподобного
завершения. Единый parent пока не выбирает три из девяти рёбер, массовый
тензор, новый конденсат или diagonal family--channel lock.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-coherence-channel-triplet-promotion-bimodule-compatibility-gate]]
- [[version7-minimal-mirror-pair-real-anomaly-gate]]
- [[version7-four-vertex-vectorlike-selector-gate]]
- [[version7-edge-coherence-full-graph-competition-gate]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate_results.json`