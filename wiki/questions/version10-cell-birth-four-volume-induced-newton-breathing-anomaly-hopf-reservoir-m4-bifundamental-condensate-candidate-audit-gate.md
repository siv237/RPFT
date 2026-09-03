# Аудит кандидатов бифундаментального M4-конденсата

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Какой внутренний механизм может породить отрицательную квадратичную моду
для резервуарно-хопфовского cross-поля и стабилизировать её без целевой
подстановки?

## Результат

Одиннадцать кандидатов проверены по шести критериям. Матрица имеет ранг
`6`, максимальная оценка `5/6`, полных проходов нет: `0/11`. Ни один
кандидат не совмещает правильный тип, унаследованность и отрицательную
квадратичную моду.

Клеточная incidence-карта унаследована, но даёт положительный лапласиан со
спектром `(0,2)`. Ручная смена знака создаёт `(-2,0)`, однако не имеет
родительского происхождения. Профиль Каллиаса и Higgs-портал условно дают
нужный знак, но не унаследованы на минимальном общем носителе.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-hopf-reservoir-intertwiner-m4-cross-generator-parent-origin-gate]]
- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-hopf-reservoir-intertwiner-common-carrier-admission-gate]]
- [[version10-particle-wrinkle-dislocation-callias-profile-common-carrier-admission-gate]]