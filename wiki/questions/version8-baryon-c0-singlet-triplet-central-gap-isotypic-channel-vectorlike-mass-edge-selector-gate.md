# Вектороподобный mass/edge-селектор изотипического канала

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Может ли один симметричный parent согласовать rank-one coherence-конденсат
с rank-two вектороподобной массой и одновременно выбрать физическое меню
рёбер?

## Search for solution

- Поля `B,M` помещены на общий правый изотипический триплет.
- Построен четырёхчленный неотрицательный функционал с условиями
  `rank(B)=1`, `MM*=I2` и `MB*=0`.
- Выведено проекторное тождество `B*B/3+M*M=I3`.
- Проверена точная ортогональная ковариантность.
- Вычислен полный гессиан на вещественном двенадцатимерном срезе.
- Возвращены шесть разрешённых, но пропущенных полей полного строгого графа.

## Expected result

Положительный проход должен был выровнять массовое ядро с coherence-линией
без фиксированного `SO(3)`-ломающего тензора. Полное закрытие дополнительно
требовало включить все девять новых рёбер и поднять конкурирующие моды.

## Compliance check

- Нулевое множество имеет `Tr(BB*)=3`, `rank(B)=1`, `MM*=I2`, `rank(M)=2`
  и `MB*=0`.
- Проекторы удовлетворяют `P_B+P_M=I3`; `ker(M)=im(P_B)`.
- Вещественный гессиан имеет спектр `0^4,8^5,24,26^2`, отрицательных мод нет.
- Два разных channel-проектора имеют одинаковую нулевую энергию.
- Aligned-shape ledger: `8/8`.
- Шесть пропущенных комплексных рёбер дают двенадцать плоских вещественных
  мод; полный срез имеет сигнатуру `(0,16,8)`.
- Full-graph selector ledger: `0/5`; parent-origin ledger: `0/4`.

## Boundary

Условный parent точно согласует ядро и конденсат, но его область определения
уже содержит скрытый projector на выбранные блоки. Абсолютное направление,
шесть конкурирующих рёбер и diagonal family--channel lock не выведены.

## Superseded carrier count

Последующий полнографовый аудит установил, что три из шести нежелательных
новых рёбер уже входят как компоненты полной матрицы `M`. Поэтому вне
`B+M` находятся три, а не шесть комплексных полей. Число дополнительных
плоских вещественных мод до стабилизации исправлено с `12` на `6`, а
сигнатура — с `(0,16,8)` на `(0,10,8)`. No-go абсолютного направления и
происхождения полного parent сохраняется.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-minimal-isotypic-channel-extension-gate]]
- [[version7-edge-coherence-rank-one-condensate-gate]]
- [[version7-edge-coherence-full-graph-competition-gate]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate_results.json`