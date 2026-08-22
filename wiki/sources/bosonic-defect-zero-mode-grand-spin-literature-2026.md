# Нулевые моды и полный угловой момент солитона

> Status: working
> Type: source
> Updated: 2026-08-20

## Summary

Первичная литература связывает нулевые моды солитона с непрерывными
симметриями и показывает, что для ежа переносные и вращательные направления
следует классифицировать по диагональному полному моменту. Она также
предупреждает, что нулевая мода, пороговый резонанс и нормируемая
коллективная координата требуют разных проверок.

## Sources

- Hiroyuki Hata, Toru Kikuchi, *Relativistic Collective Coordinate System
  of Solitons and Spinning Skyrmion*, `arXiv:1008.3605` — коллективные
  координаты должны вводиться так, чтобы их уравнения движения следовали
  из полного полевого уравнения; нулевые моды связаны с направлениями
  симметрии солитона.
- B. Moussallam, *Casimir Energy in the Skyrme Model*,
  `arXiv:hep-ph/9211229` — в скалярном спектре ежа выделяются три
  переносные и три вращательные нулевые моды.
- H. Walliser, G. Holzwarth, *The Casimir energy of skyrmions in the
  2+1-dimensional O(3)-model*, `arXiv:hep-ph/9907492` — частично-волновое
  разложение помещает переносную нулевую моду ежа в канал момента один и
  отделяет её от связанных состояний и рассеятельного спектра.

## Project Use

Для составного дефекта Тома VI литература оправдывает классификацию по
диагональному полному моменту, но не переносит готовый спектр из модели
Скирма. Нулевой закон `L^-4` получается из собственной проекторной
тождественности `D_QQ=0` и кривизного члена проекта.

## Links

- [[version6-bosonic-defect-canonical-continuum-stability-gate]]
- [[version6-bosonic-defect-nonradial-stability-gate]]
- [[bosonic-defect-collective-quantization-literature-2026]]
- [[bosonic-defect-radial-stability-literature-2026]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_canonical_continuum_stability_gate.tex`
- `s2t/results/s2t_v6_bosonic_defect_canonical_continuum_stability_gate_results.json`