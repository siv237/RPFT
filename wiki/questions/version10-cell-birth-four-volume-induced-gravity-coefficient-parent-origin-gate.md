# Сквозной ток и условно индуцированные коэффициенты гравитации

> Status: working
> Type: question
> Updated: 2026-09-01

## Вопрос

Может ли ранняя хопфовская картина сквозного потока объяснить ненулевую
геометрию вакуума и одновременно вывести абсолютные коэффициенты
кривизненного родителя?

## Результат

Для стационарного канала

$$
\dot N=J_{\rm in}-J_{\rm out}=0,
\qquad
\Theta=J_{\rm in}+J_{\rm out}=2J>0.
$$

При неравновесной силе $F>0$ производство энтропии равно $\sigma=FJ$.
Положительный родитель

$$
\mathcal P_{\rm flow}(x)
=\frac{\lambda}{4}\left(x^2-\frac{g\sigma}{\lambda}\right)^2
$$

имеет устойчивые ветви

$$
x_*^2=\frac{g\sigma}{\lambda},
\qquad
\mathcal P_{\rm flow}''(x_*)=2g\sigma>0.
$$

При $J=0$ остаётся только четвертичный родитель и ненулевая ветвь исчезает.
Тем самым математически реализована интуиция геометрии, поддерживаемой
прохождением потока.

Однако условно индуцированные коэффициенты
`A=alpha m²`, `B=beta m`, где `m=x_*²`, по-прежнему выбирают только
`q m=beta/(2alpha)`. Карта отношений имеет ранг/ядро `2/1`: совместный
масштаб тока и геометрии остаётся свободным.

## Статус

- архитектура сквозного тока: `9/9`;
- условное происхождение нарушенной геометрии: `4/4`;
- физическое происхождение силы и тока: `0/1`;
- абсолютный гравитационный масштаб: `0/1`;
- ProofDSL: `20/20`, общий реестр `83/829`.

Следующий вопрос — выводятся ли сила $F$, ток $J$ и сопротивление канала из
существующих хопфовского носителя, КМС-динамики и родительского функционала.

## Связи

- Ранняя интуиция: [[early-light-mobius-resonator-hypothesis]].
- Предшественник: [[version10-cell-birth-four-volume-curvature-coefficient-origin-candidate-audit-gate]].
- Формулы: [[global-formula-atlas]].
- Реестр статусов: [[global-theorem-and-no-go-ledger]].
- Исходники: `s2t/gates/version10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate.tex`, `s2t/audits/s2t_v10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate.py`, `s2t/results/s2t_v10_cell_birth_four_volume_induced_gravity_coefficient_parent_origin_gate_results.json`.