# Нечётный фон оператора Дирака и кубическая проекция

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Конечная градуировка разделяет кубические формы. Канонический следовой
тензор имеет опору `140 TTG+28 GGG`, то есть чётную конечную матричную
чётность. Для любого нечётного фона `D` выполнено
`Tr(D_odd S_even)=0`, поэтому он не может воспроизвести ненулевой множитель
всего `d_abc`.

На физическом инцидентном фоне полный точный перебор дал дополнительную
опору `130 TTT+35 TGG` и строгий ноль в каналах `TTG,GGG`.

## Пространственно-временная граница

Настоящая суперсвязность восстанавливает общую нечётность степенью форм:
калибровочная связность является матрично чётной одноформой, а поле
переноса --- матрично нечётной нуль-формой. Кубические `TTG/GGG`-вершины
нормы кривизны содержат `dA` или `dPhi` и исчезают на постоянном
нулеимпульсном срезе. Они не равны статическому оператору `lambda_3 W3`.

## Вердикт

Локальная беспроизводная суперкривизностная ветвь закрыта. Следующий
допустимый тест --- явное производное либо нелокальное шеститочечное ядро;
новый постоянный коэффициент при `W3` вводить нельзя.

## Связи

- [[version8-baryon-spacetime-supercurvature-cubic-projection-admission-gate]]
- [[superconnection-odd-endomorphism-parent-literature-2026]]
- [[shifted-supercurvature-cubic-shape-literature-2026]]
- [[version8-baryon-connected-three-body-kernel-admission-gate]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex`
- `s2t/audits/s2t_v8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.py`
- `s2t/results/s2t_v8_baryon_noncentral_odd_dirac_background_projection_no_go_gate_results.json`