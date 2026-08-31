# Производная кубическая вершина: шеститочечное ядро или остановка

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Результат внешнего отчёта независимо воспроизведён из текущего
42-мерного центрированного кадра. Полный перебор `13244` неубывающих троек
дал

- `supp d = 140 TTG + 28 GGG`, всего `168`;
- `supp C = 106 TTG + 10 GGG`, всего `116`;
- `supp d intersect supp C = empty`.

Коммутаторный тензор антисимметричен и имеет нулевую полную
симметризацию. Все допустимые производные вершины линейны по импульсу,
поэтому исчезают при `p=0`; при ненулевом импульсе они всё равно остаются
в цветовом секторе `C`, не содержащем `W3`.

## Вердикт

Производная локальная ветвь закрыта со статусом STOP. Продолжение возможно
только через нелокальное шеститочечное ядро с ненулевым статическим
значением либо через явное объявление коэффициента внешним масштабом.

## Связи

- [[external-baryon-attack-report-ba05]]
- [[version8-baryon-noncentral-odd-dirac-background-projection-no-go-gate]]
- [[version8-baryon-cubic-trace-connected-operator-gate]]
- [[baryon-six-point-faddeev-literature-2026]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_baryon_derivative_cubic_vertex_to_six_point_kernel_or_stop_gate.tex`
- `s2t/audits/s2t_v8_baryon_derivative_cubic_vertex_to_six_point_kernel_or_stop_gate.py`
- `s2t/results/s2t_v8_baryon_derivative_cubic_vertex_to_six_point_kernel_or_stop_gate_results.json`