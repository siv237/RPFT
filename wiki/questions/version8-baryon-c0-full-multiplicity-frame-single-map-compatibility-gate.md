# Совместимость полного multiplicity-кадра с одиночной картой c0

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Полный изотропный пакет трёх комплексных коннекторов имеет матрицу
Коссаковского `I3`, Choi/Kraus rank `3` и минимальную среду размерности `3`.
Одна карта имеет ковариацию `z z*`, ранг `1` и одномерную среду. Эти ранги
не меняются при Kraus-изометриях, поэтому процессы операторно неравны.

На центральном срезе различие теряется: ограничение зависит только от
`Tr C`, и скорость одиночной карты можно умножить на три. Явный проектор
`P_eR` различает полные процессы. Rank-one редукция требует выбрать чистое
состояние среды в `CP2` или `RP2`, возвращая исходный недостающий селектор.

## Связи

- [[version8-baryon-c0-extended-endpoint-bimodule-weight-origin-gate]]
- [[version8-baryon-c0-old-new-gauge-covariant-connector-classification-gate]]
- [[version8-minimal-covariant-stinespring-carrier-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate.py`
- `s2t/results/s2t_v8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate_results.json`