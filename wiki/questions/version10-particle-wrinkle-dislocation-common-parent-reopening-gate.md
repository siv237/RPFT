> Status: working
> Type: question
> Updated: 2026-09-02

# Общий родитель частицы-морщинки и частицы-дислокации

## Вопрос

Являются ли топологическая дислокация и локализованная энергетическая
морщинка двумя следствиями уже существующего общего родителя?

## Результат

Противоречия нет. Дефектный представитель имеет индекс `-15`, проектор
коядра ранга `15` и дефицит `1/7`. Условный профиль
`E(L)=L+1/L` имеет минимум `L*=1`, энергию `2` и кривизну `2`.

Однако унаследованный гессиан равен `diag(2,0)`: его ранг/ядро `1/1`, а
смешанный блок отсутствует. Нулевыми остаются морфизм локализации класса в
ядре морщинки и отображение энергии профиля в спектральный полюс. Поэтому
совместность закрыта `8/8`, а происхождение общего родителя — `0/3`.

## Следующий вопрос

Проверить кандидаты на смешанный оператор между проекторным полем,
тёплицевым дефектом, клеточным комплексом и спектральным полюсом:
`version10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate`.

## Связи

- [[particle-wrinkle-dislocation-formula-intuition-2026]]
- [[version5-topological-closure-deficit-gate]]
- [[version5-local-defect-transfer-operator-gate]]
- [[version6-projective-order-parameter-field-spectrum-gate]]
- [[version6-spatial-projective-defect-energy-spectrum-gate]]
- Гейт: `s2t/gates/version10_particle_wrinkle_dislocation_common_parent_reopening_gate.tex`.
- Аудит: `s2t/audits/s2t_v10_particle_wrinkle_dislocation_common_parent_reopening_gate.py`.
- Результат: `s2t/results/s2t_v10_particle_wrinkle_dislocation_common_parent_reopening_gate_results.json`.