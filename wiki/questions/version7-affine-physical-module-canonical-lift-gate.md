# Version VII: канонический аффинно-хиральный подъём

> Status: working
> Type: question
> Updated: 2026-08-26

## Summary

Исходный носитель Тома VII размерности `144` над `C` дважды учитывал
семейный слой. `E_aff` уже является динамическим аффинным модулем, тогда как
`E_rho` — касательное пространство после выбора конкретного rank-one
проектора `rho`. Фиксированное `E_rho` не инвариантно под полным `S4`.

Минимальная исправленная типизация:

`Psi in E_aff tensor Lambda_ch`, `dim_C Psi = 36`.

## Equivariance Audit

- инвариантное подпространство `E_aff` одномерно и порождается коизометрией
  `V`;
- любая инвариантная линейная свёртка имеет ядро размерности `11`;
- такая свёртка исходного поля уничтожила бы `132` комплексных направления;
- орбитальная оболочка фиксированного `E_rho` имеет размерность `8`, а не
  исходные `4`.

## Canonical Lift

Исправленное поле включается без свёртки:

`Hom(C4,V3) tensor Hom(HL,HR) -> Hom(C4 tensor HL, V3 tensor HR)`.

Физический левый ранг равен `3*8=24`, правый — `3*7=21`. Поднятый
Hodge-функционал имеет отрицательный нулевой гессиан и минимум `1/15`.

Явный свидетель `Z*=V tensor Y*` имеет:

- ранг `21`;
- полное ядро `11 = 8 + 3`;
- `8` опорных равномерных направлений;
- `3` физических ядерных линии — по одной на поколение.

## Boundary

Это исправляет общий носитель, но не завершает физику. Открыты полный
Real/junk/BRST-BV гессиан, классификация нефакторизованных минимумов,
относительные амплитуды `u,d,e` и пространственная динамика.

## Later Result

[[version7-corrected-vacuum-relative-edge-hessian-gate]] показал, что
минимум поперечно устойчив, но образует `U(3)^3`: `27` точных нулевых мод,
из которых не менее `18` являются относительными даже после общего
семейного факторирования.

## Links

- [[version7-rank-change-parent-program]]
- [[version7-chiral-hodge-index-instability-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[version5-rank-one-tangent-junk-gate]]
- [[version5-affine-ko6-reference-corner-gate]]
- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]
- [[version7-corrected-vacuum-relative-edge-hessian-gate]]

## Source Notes

- `s2t/gates/version7_affine_physical_module_canonical_lift_gate.tex`
- `s2t/audits/s2t_v7_affine_physical_module_canonical_lift_gate.py`
- `s2t/results/s2t_v7_affine_physical_module_canonical_lift_gate_results.json`