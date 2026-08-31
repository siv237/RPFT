# Parent-origin портала радиуса стрелочной когерентности

> Status: working
> Type: question
> Updated: 2026-08-31

## Problem

Может ли единый операторный parent породить портал
`lambda Tr(BB*)`, превращающий уже выведенный rank-one конденсат в источник
центральной singlet--triplet щели?

## Search for solution

- Центральное направление продолжено на coherence-chain `1->6->3`.
- Из бесследовости найден единственный средний вес `q=0`.
- Точно вычислены моменты общего оператора
  `X=D_B+lambda Qhat` до четвёртой степени.
- Проверены чётный inherited-parent, условный кубический момент, Real-полуслед
  и тип представления трёхмерного чётного угла.

## Expected result

Успех требовал ненулевого линейного портала из уже принятого действия и
канонического отождествления coherence-угла с текущим семейным триплетом.

## Compliance check

- `Qhat=diag(-3/4,0_6,(1/4)I3)` единственно по `Tr Qhat=0`.
- `Tr(Qhat D_B²)=-5T/8`, где `T=Tr(BB*)`.
- `Tr X³=-15 lambda T/8-3 lambda³/8`; условный cubic-parent фиксирует
  отношение portal/self-cubic равным `5`.
- `Tr X²` и `Tr X⁴` чётны по `lambda`, поэтому inherited even-parent не
  создаёт источник.
- Coherence-угол имеет канальный тип `1+2` и коммутант размерности `2`,
  тогда как family-triplet неприводим и имеет коммутант размерности `1`.
- Алгебраическая форма закрыта `4/4`; parent-origin — `0/2`.

## Boundary

Размерностное совпадение `1+3` не является типизированным мостом. Для
физического портала ещё нужны family-intertwiner и происхождение ненулевого
коэффициента кубического момента.

## Links

- [[version8-baryon-c0-singlet-triplet-central-gap-existing-scalar-source-carrier-classification-gate]]
- [[version7-edge-coherence-spectral-parent-gate]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[kernel-grassmannian-quiver-stability-literature-2026]]
- [[superconnection-curvature-and-polar-strata-literature-2026]]
- [[global-theorem-and-no-go-ledger]]
- [[global-formula-atlas]]

## Source Notes

- `s2t/gates/version8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate.py`
- `s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate_results.json`
