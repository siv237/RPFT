# Типизированное Callias–M4 вложение фермионного cross-оператора

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Можно ли вложить равнозарядный $M_4$ cross-оператор в каллиасов носитель
так, чтобы он сохранял пространственный Clifford action и все 15 каналов?

## Результат

Условно да. На `C²_spin ⊗ C²_twist ⊗ H15` полная $M_4$-алгебра имеет
ранг `16`, cross-изометрия --- ранг `30`, charge defect --- ранг `0`, а
determinant-кривизна усиливается до `-60`.

Физическое происхождение не закрыто: равномерный усилитель имеет условный
ранг `2` и Gram `15I₂`, тогда как унаследованная карта имеет ранг `0`.
Требуется родитель, выбирающий одинаковый coupling во всех 15 каналах.

## Источники

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate.tex`
- `s2t/audits/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate.py`
- `s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-hopf-reservoir-m4-fermionic-determinant-cross-bilinear-odd-statistics-candidate-audit-gate]]
- [[version10-particle-wrinkle-dislocation-callias-profile-common-carrier-admission-gate]]
- [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-hopf-reservoir-intertwiner-common-carrier-admission-gate]]