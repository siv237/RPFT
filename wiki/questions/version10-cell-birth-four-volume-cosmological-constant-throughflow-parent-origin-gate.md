# Родитель космологической постоянной из сквозного потока

> Status: working
> Type: question
> Updated: 2026-09-01

## Вопрос

Можно ли получить космологическую кривизну как динамический отклик на
производство энтропии хопфовского сквозного цикла, а не определять её через
уже известную скорость роста?

## Результат

Из ранее выведенных величин

$$
F_\circlearrowright=3\log2,
\qquad
\sigma_\circlearrowright=\kappa\log2
$$

строится условный отклик

$$
\Lambda_{\rm flow}
=\frac{3\sigma_\circlearrowright^2}{c^2F_\circlearrowright^2}
=\frac{\kappa^2}{3c^2}.
$$

Положительный родитель на нормированных переменных потока и кривизны имеет
гессиан ранга `2`, определитель `1` и единственный минимум. При
`kappa=0` одновременно исчезают производство энтропии и условная кривизна.
Это строго реализует образ геометрии, поддерживаемой прохождением потока.

Однако аффинность и энтропия унаследованы, а член связи
`curvature_response_coupling` отсутствует в прежнем родительском действии.
Поэтому механизм остаётся условным. Карта
`(kappa,sigma,Lambda)` имеет ранг/ядро `2/1` с масштабными весами
`(1,1,2)` и не фиксирует абсолютную величину.

## Статус

- архитектура: `10/10`;
- условное происхождение: `5/5`;
- унаследованные источники: `2/3`;
- происхождение связи кривизна–поток: `0/1`;
- физическое происхождение `Lambda`: `0/1`;
- абсолютный масштаб: `0/1`;
- ProofDSL: `20/20`, общий реестр `89/948`.

Следующий вопрос — может ли связь кривизна–поток следовать из
эйнштейновского геометрического отклика, а не вводиться отдельным квадратом.

## Связи

- Предшественник: [[version10-cell-birth-four-volume-cosmological-constant-conductance-anchor-candidate-audit-gate]].
- Сквозной вакуумный ток: [[version10-cell-birth-four-volume-induced-gravity-coefficient-parent-origin-gate]].
- Формулы: [[global-formula-atlas]].
- Реестр статусов: [[global-theorem-and-no-go-ledger]].
- Исходники: `s2t/gates/version10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate.tex`, `s2t/audits/s2t_v10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate.py`, `s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate_results.json`.