# Version VII: хиральная Hodge-неустойчивость и одна ядерная линия

> Status: working
> Type: question
> Updated: 2026-08-26

## Summary

Формульная генеалогия выделила новый кандидат, отличный от закрытой чистой
нормы суперсвязности. Каноническая хиральная градуировка пакета
`H15 = H_L^8 + H_R^7` задаёт функционал

`S_ch(Y) = tr_norm([d_Y,d_Y*] - Gamma_15)^2`.

Нулевой оператор стационарен, но имеет 112 отрицательных вещественных
направлений. Квартет того же функционала ограничивает действие снизу.

## Exact Result

Через семь сингулярных чисел:

`S_ch(Y) = [1 + 2 sum_j (1-sigma_j^2)^2] / 15 >= 1/15`.

Минимумы являются коизометриями `Y Y* = I7`. Поэтому:

- `rank Y = 7`;
- `dim_C ker Y = 1`;
- минимальная нормированная энергия равна `1/15`;
- ядро не вставляется проектором, а следует из `8-7=1`.

## Physical Edge Witness

Разрешённые рёбра `u,d,e` достигают минимума конструктивно. Рёбра `u,d`
закрывают шесть компонент `Q_L`, ребро `e` закрывает заряженное направление
`L_L`, а ортогональная левая нейтринная линия остаётся ядром.

Это ещё не вывод нейтринной массы или частицы: установлен только хиральный
индекс минимального оператора.

## Open Boundary

Нужно вывести каноническую карту полного поля
`Phi in E_aff tensor Y_phys` в нечётный оператор `Y_Phi` на `H15`, не
выбирая функционал на аффинном множителе. Затем необходим полный
gauge/Real/junk/BRST-BV гессиан и аудит двух относительных свобод рёбер.

## Later Result

[[version7-affine-physical-module-canonical-lift-gate]] построил
трёхпоколенный подъём после удаления повторного множителя `E_rho`.
Однопоколенное ядро стало тремя физическими линиями в рангах `24 -> 21`.

## Links

- [[version7-rank-change-parent-program]]
- [[version7-full-physical-rank-field-hessian-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[version5-h15-neutrino-degree-split-gate]]
- [[version5-m300-hodge-curvature-hessian-gate]]
- [[version7-affine-physical-module-canonical-lift-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/gates/version7_chiral_hodge_index_instability_gate.tex`
- `s2t/audits/s2t_v7_chiral_hodge_index_instability_gate.py`
- `s2t/results/s2t_v7_chiral_hodge_index_instability_gate_results.json`