# Размерностная трансмутация и планковская самосогласованность

> Status: working
> Type: question
> Updated: 2026-09-01

## Вопрос

Могут ли унаследованные RG-данные и ранняя гипотеза планковских локальных
часов совместно выбрать масштабное семя `m` и абсолютную постоянную Ньютона?

## Результат

Ранний relative-`U(1)` сектор строго поставляет `b=2` и
`g²(mu_spec)=3/8`. Отсюда следуют точные отношения

`log(Lambda_L/mu_spec)=32 pi²/3`,

`log(m_DT/mu_spec²)=64 pi²/3`.

При положительном `b` это ультрафиолетовый полюс Ландау, а не
инфракрасная гравитационная щель. Кроме того, перенос RG-данных в текущий
ньютоновский носитель отсутствует.

Планковское условие `m g_N=1` вместе с
`16 pi beta_E m g_N=1` условно выбирает

`beta_E=1/(16 pi)`.

Размерная величина при этом сокращается. Общий положительный родитель имеет
гессиан `[[2,-1,0],[-1,2,-1],[0,-1,1]]`, ранг `3`, определитель `1` и
ведущие миноры `(2,3,1)`. Однако размерная карта на
`(m,mu_spec²,g_N)` имеет ранг/ядро `2/1` с ядром `(1,1,-1)`.

## Статус

- исторические RG-данные: `2/2`;
- типизированный перенос: `0/2`;
- условная архитектура: `10/10`;
- условное замыкание: `7/7`;
- выбор `beta_E`: условно `1/1`;
- физическое происхождение: `0/4`;
- абсолютные `m` и `G`: `0/2`;
- ProofDSL: `21/21`, общий реестр `94/1048`.

Следующий вопрос — может ли раннее «дыхание вакуума» быть реализовано как
один открытый родитель инжекции, следовой аномалии и энтропийного выхода.

## Связи

- Предшественник: [[version10-cell-birth-four-volume-induced-newton-scale-seed-candidate-audit-gate]].
- Археология: [[tome10-early-metaphor-scale-origin-archaeology-2026-09-01]].
- Ранний RG-запрет: [[version3-rg-anomaly-scale-setting-gate]].
- Формулы: [[global-formula-atlas]].
- Реестр: [[global-theorem-and-no-go-ledger]].
- Исходники: `s2t/gates/version10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate.tex`, `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate.py`, `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_dimensional_transmutation_beta_parent_origin_gate_results.json`.