# Аудит спектральной плотности и масштаба памяти ванны

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Содержит ли текущий корпус профиль спектральной плотности, который
одновременно выбирает форму корреляции и независимый абсолютный масштаб
памяти неравновесной ванны?

## Результат

Десять кандидатов проверены по шести условиям: положительность,
нормировка, конечная память, KMS-совместимость, выбор существующим родителем
и некруговое разрушение масштабной орбиты.

Матрица `10x6` имеет ранг `6`, но полных проходов нет. Стандартные
аналитические профили достигают не более `4/6`, поскольку их форма не
выводится. Наблюдаемое время релаксации получает `5/6`, но является внешним
круговым якорем.

Точные времена для допустимых профилей различны: `1`, `sqrt(pi)/2`, `1/2`
и `1/2` в единицах `omega_UV^-1`. Восемь кандидатов относятся к форме,
два — к масштабу; происхождение обеих компонент равно `0/2`.

## Статус

- кандидаты: `10/10`;
- критериальный ранг: `6/6`;
- полные проходы: `0/10`;
- происхождение формы и абсолютной памяти: `0/2`.

## Источники

- `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate.tex`
- `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate.py`
- `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate_results.json`

## Связи

- [[version10-cell-birth-four-volume-nonequilibrium-bath-correlation-time-parent-origin-gate]]
- [[version9-endpoint-creation-kms-logdet-reservoir-spectral-density-parent-origin-gate]]
- [[version8-correlation-kernel-short-time-rate-selector-gate]]