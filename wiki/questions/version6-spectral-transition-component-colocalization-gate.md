# Том VI: пространственная колокализация классов 12 и 3

> Status: working
> Type: question
> Updated: 2026-08-21

## Краткий вывод

Пространственная колокализация кваркового класса `12` и лептонного
класса `3` текущим родителем не выведена.

Глобальный KO6-класс требует сумму `12+3=15`, но индекс не является
энергией связывания и допускает пространственно разделённые центры.

## Проверенные механизмы

- В конечном операторе есть рёбра `u,d,e`, но нет кварк-лептонного
  ребра.
- Моритова кривизна раскладывается по столбцовым опорам `12+3`; смешанная
  норма равна нулю.
- Общий Хиггс не создаёт прямого коннектора. Торсионный перекрёстный член
  возникает только в запрещённом новом потенциале.
- Минимальный портал `Tr(Q^2) H†H` имеет нулевой коэффициент.
- Семейная связность действует как `A_fam tensor I15` и не различает
  взаимное положение компонент.
- Поле `Q` является нейтральным семейным квинтетом; уникальное
  фермионное сцепление с `H15` не выведено.

## Условный общий центр

Один Каллиасов профиль

`(n(x)·sigma) tensor (q12+q3)`

действительно локализовал бы обе компоненты на одном ядре. Но необходимый
spin-cover-носитель не следует из конечного родителя, а двухкопийная
лазейка уже закрыта. Поэтому это условный анзац, а не результат.

## Прямой тест расстояния

Для двух гауссовых плотностей текущая аддитивная энергия остаётся равной
`0.05037406996` при расстояниях `0, 0.5, 1, 2, 4`; численный разброс
`3.47e-17`.

Гипотетический член `-lambda ∫rho_q rho_l` дал бы минимум при совпадении
центров, но текущий коэффициент `lambda=0`.

## Последующее разрешение

Полный класс `15` нельзя продолжать называть одной частицей. Последующий
[[version6-spectral-transition-higgs-resolved-support-gate]] проверил
разложение после ненулевого направления Хиггса:

`15 -> 6_u + 6_d + 2_e + 1_nu`.

Разложение подтверждено точно. Ещё один гейт показал, что нормированная
нейтринная линия не продолжается через `H=0`, но её ненормированный
квадратичный носитель продолжается нулём.

## Links

- [[version6-spectral-transition-component-boundary-gate]]
- [[version6-spectral-transition-higgs-resolved-support-gate]]
- [[version6-spectral-transition-neutrino-line-parent-gate]]
- [[version6-spectral-transition-minimal-support-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[version5-h15-spectral-torsion-selector-gate]]
- [[version5-morita-linking-parent-gate]]
- [[version6-bosonic-defect-mass-portal-parent-gate]]
- [[version6-bosonic-defect-family-connection-parent-identification-gate]]
- [[version6-bosonic-defect-field-identification-gate]]
- [[version6-composite-connection-callias-fredholm-gate]]
- [[version6-spin-cover-carrier-parent-derivation-gate]]
- [[transition-primitive]]

## Source Notes

- `s2t/gates/version6_spectral_transition_component_colocalization_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_component_colocalization_gate.py`
- `s2t/results/s2t_v6_spectral_transition_component_colocalization_gate_results.json`
- C. Callias, *Axial Anomalies and Index Theorems on Open Spaces* (1978).
- R. Jackiw, C. Rebbi, *Solitons with Fermion Number 1/2* (1976).