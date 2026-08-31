# Селектор относительной скорости семейного синглета и триплета

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Представление `1+3` имеет двумерное пространство invariant covariance:
`C=gamma_1 P1+gamma_3 P3`. Семейная симметрия оставляет произвольное
отношение `r=gamma_3/gamma_1>0`.

Два точных положительных свидетеля показывают неединственность. Равная
скорость на стрелку даёт `rho=I4/4` и `r=1`; равная полная интенсивность
двух неприводимых секторов даёт `rho=P1/2+P3/6` и `r=1/3`. KMS фиксирует
только forward/backward ratio внутри каждого сектора, а примитивность
зависит от support, не от положительного `r`.

Полный `M4` с уникальным следом несовместим с grading
`diag(-,+,+,+)`; максимальная чётная алгебра равна `M1+M3` и сохраняет
центральный trace-вес. Итоговый selector ledger: `0/6`.

## Связи

- [[version8-baryon-c0-grading-compatible-family-triplet-endpoint-extension-gate]]
- [[version8-canonical-noise-frame-common-trace-gate]]
- [[version8-noise-isotropy-symmetry-admission-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate.py`
- `s2t/results/s2t_v8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate_results.json`