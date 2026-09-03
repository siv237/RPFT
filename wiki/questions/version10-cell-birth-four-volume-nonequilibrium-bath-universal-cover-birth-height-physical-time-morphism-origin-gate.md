# Морфизм высоты покрытия в физическое время

> Status: working
> Type: question
> Updated: 2026-09-02

## Summary

Высота универсального покрытия допускает точное аффинное чтение
`t_n=t_0+n tau_birth`. Кобграница удаляет свободное начало `t_0` и оставляет
одинаковый тик на каждом ребре. Связи `tau_birth=hbar/E_C=ell_edge/c`
совместимы, но алгебраически зависимы и не выбирают абсолютный масштаб.

## Key Points

- Матрица аффинного чтения `({1},h)` имеет ранг `2`.
- Её реберная производная равна `({0},{1})` и имеет ранг/ядро `1/1`.
- Сдвиг начала времени не меняет интервалы; это координатная свобода.
- Родитель трёх часовых инвариантов имеет гессиан `I3`, однако размерная
  карта имеет только ранг/ядро `2/2`.
- После фиксации `c` остаётся масштабная мода
  `(tau,E,ell,c) -> (s tau,E/s,s ell,c)`.
- Физическое происхождение временного чтения и абсолютного тика остаётся
  `0/2`.

## Links

- [[version10-cell-birth-four-volume-nonequilibrium-bath-universal-cover-growth-graph-typed-embedding-gate]] — дискретная высота рождения.
- [[version10-cell-birth-four-volume-nonequilibrium-bath-cell-complex-edge-length-common-parent-origin-gate]] — общий родитель длины ребра.
- [[version10-cell-birth-clock-energy-common-parent-origin-gate]] — относительные часы рождения.
- [[current-status-and-next-vectors]] — общий фронтир Тома X.

## Source Notes

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate_results.json`
- `s2t/proofdsl/examples/version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin.py`