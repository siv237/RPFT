# Аудит космологической постоянной как якоря проводимости

> Status: working
> Type: question
> Updated: 2026-09-01

## Вопрос

Может ли космологическая постоянная независимо выбрать абсолютную
проводимость хопфовского цикла после установления связи
`kappa=Gamma_B=3 Delta_zeta Omega`?

## Результат

Для ветви геометрического роста точно получено

$$
H_B=\frac{\kappa}{3},
\qquad
\Lambda_{\rm growth}=\frac{\kappa^2}{3c^2},
\qquad
c\sqrt{3\Lambda_{\rm growth}}=\kappa.
$$

Последнее равенство совместимо с гипотезой геометрического масштаба, но
является обращением определения: `Lambda_growth` уже вычислена через
`kappa`. Аналогично радиус кривизны фиксирует только произведение
`kappa*ell_Lambda=3c`.

Семь вариантов космологического якоря проверены по шести условиям. Матрица
имеет ранг `5`, полных проходов `0/7`, максимум `4/6`. Внутренних кандидатов,
одновременно доступных и разрывающих масштабную орбиту, нет.

Относительная карта на
`(kappa,Gamma_B,Omega,H_B,Lambda)` имеет ранг/ядро `4/1` и уничтожает вектор
`(1,1,1,1,2)`. Независимо фиксированная положительная `Lambda` повысила бы
ранг до `5` и действительно дала бы `kappa=c*sqrt(3 Lambda)`, но её
физическое происхождение пока отсутствует.

## Статус

- покрытие аудита: `7/7`;
- происхождение кандидата: `0/7`;
- условный независимый якорь: `1/1`;
- физическое происхождение `Lambda`: `0/1`;
- абсолютная проводимость: `0/1`;
- ProofDSL: `17/17`, общий реестр `88/928`.

Следующий вопрос — может ли общий родитель сквозного потока вывести
космологическую постоянную независимо от уже выбранной проводимости.

## Связи

- Предшественник: [[version10-cell-birth-four-volume-hopf-cycle-conductance-common-parent-origin-gate]].
- Ранний аудит часов: [[version10-cell-birth-clock-energy-geometric-anchor-candidate-audit-gate]].
- Формулы: [[global-formula-atlas]].
- Реестр статусов: [[global-theorem-and-no-go-ledger]].
- Исходники: `s2t/gates/version10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate.tex`, `s2t/audits/s2t_v10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate.py`, `s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate_results.json`.