# Родитель тахионного знака клеточной incidence-моды

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Может ли унаследованная клеточная граница получить отрицательную
квадратичную моду без ручной замены положительного лапласиана на его минус?

## Результат

Нет в устойчивом бозонном секторе. Обращение ориентации `B -> -B` не меняет
`BBᵀ`, положительные реберные веса сохраняют его неотрицательность, а
дополнение Шура положительного родителя остаётся положительным.

Сверхкритическое смешивание создаёт отрицательную эффективную моду только
тогда, когда полный квадратичный родитель уже неустойчив. Первый условный
некруговой знак даёт фермионный детерминант:
`d²[-2 sqrt(1+x²)]/dx²|₀ = -2`. Но его носитель и связь с относительной
клеточной модой пока не унаследованы. Аудит: `0/12`, максимум `5/6`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-hopf-reservoir-m4-bifundamental-condensate-candidate-audit-gate]]
- [[version10-particle-wrinkle-dislocation-callias-profile-common-carrier-admission-gate]]
- [[version10-cell-birth-four-volume-nonequilibrium-bath-local-causal-propagation-kernel-cell-complex-typed-embedding-gate]]