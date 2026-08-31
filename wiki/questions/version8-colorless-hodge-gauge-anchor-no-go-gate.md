# Бесцветный Hodge-вакуум и калибровочный якорь

> Status: mature
> Type: question
> Updated: 2026-08-28

## Summary

Финальный физически допустимый Hodge-вакуум Тома VII состоит из четырёх
представлений `(1,1)_0`. Его калибровочные индексы равны нулю, поэтому этот
сектор не может определить `f0` из калибровочной кинетики. Весь ненулевой
индекс полного рёберного носителя находится на семи заглушённых рёбрах.

## Key Points

- Активная опора: `L_L--Y_R`, `X_L--X_R`, `X_L--e_R`, `Y_L--Y_R`.
- На ней `(I1,I2,I3)=(0,0,0)`, хотя скалярный Hodge-потенциал ненулевой.
- Семь spectators несут полный индекс `(13,2,3/2)`.
- Подстановка полного индекса в квартику активного сектора смешала бы два
  разных следовых носителя и вручную выбрала относительную метрику.
- Ветвь общего gauge--spacetime следа закрыта в текущей архитектуре. Из трёх
  подготовительных примитивов остаётся проверить только второй независимый
  семейный тензор.

## Links

- [[version7-color-preserving-quadratic-selector-origin-gate]] — источник
  окончательной четырёхрёберной опоры.
- [[version7-full-gauge-weighted-edge-carrier-gate]] — полный физический
  подъём представлений и индексов.
- [[version7-common-gauge-f0-anchor-gate]] — условная формула калибровочного
  якоря и прежний trace-mismatch.
- [[version8-qlyr-ur-real-connector-lift-gate]] — закрытая ветвь коннектора.
- [[global-theorem-and-no-go-ledger]] — глобальный статус программы.

## Source Notes

- `s2t/gates/version8_colorless_hodge_gauge_anchor_no_go_gate.tex`
- `s2t/audits/s2t_v8_colorless_hodge_gauge_anchor_no_go_gate.py`
- `s2t/results/s2t_v8_colorless_hodge_gauge_anchor_no_go_gate_results.json`