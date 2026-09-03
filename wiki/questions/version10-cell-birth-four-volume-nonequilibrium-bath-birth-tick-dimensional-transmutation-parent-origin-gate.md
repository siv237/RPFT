# Родитель размерностной трансмутации такта рождения

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Унаследованная RG-пара создаёт точный относительный такт
`tau_DT c mu_spec=exp(-32 pi²/3)`, но не выбирает `mu_spec`. После фиксации
`c` остаётся одномерная масштабная орбита. Наивное отождествление
`mu_spec=Lambda43` дополнительно противоречит закрытому условию
`tau_birth c Lambda43=42`.

## Key Points

- При `b=2`, `g²=3/8` получаем `log(Lambda_L/mu_spec)=32 pi²/3`.
- Условный кандидат равен `tau_DT=exp(-32 pi²/3)/(c mu_spec)`.
- Строгий родитель имеет гессиан `I3`; это закрывает относительные связи,
  но не происхождение размерной единицы.
- Размерная карта имеет ранг/ядро `3/2`, после фиксации `c` — `4/1`, после
  независимого якоря `mu_spec` — `5/0`.
- При `mu_spec=Lambda43` несовместимые правые части равны
  `exp(-32 pi²/3)` и `42`; точный множитель рассогласования —
  `42 exp(32 pi²/3)`.
- Физическое происхождение RG-переноса, опорной шкалы, совместимости K43 и
  абсолютного такта остаётся `0/4`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-birth-tick-absolute-scale-candidate-audit-gate]] — выбор этого кандидата для углубления.
- [[version10-cell-birth-four-volume-induced-newton-dimensional-transmutation-beta-parent-origin-gate]] — источник унаследованных RG-данных.
- [[version10-cell-birth-four-volume-spectral-counting-measure-origin-gate]] — точное K43-условие.
- [[current-status-and-next-vectors]] — общий фронтир Тома X.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin.py`