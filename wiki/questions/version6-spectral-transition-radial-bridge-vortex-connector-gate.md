# Том VI: прямой коннектор семейного вихря со слабым дублетом

> Status: working
> Type: question
> Updated: 2026-08-21

## Краткий вывод

Среди уже установленных полей нет прямой эквивариантной стрелки от
семейного вихря к Хиггсу. Для группы
`SO(3)_fam x SU(2)_L x U(1)_Y` пространства интертвинеров
`B_fam -> H`, `Q -> H`, `T -> H` имеют размерность ноль.

## Что видит существующий квадрат

Эквивариантные стрелки семейной цепи сведены к `X=rho V`, `Y=Phi I3`.
Правое ребро пропорционально семейной единице. Поэтому смешанный след
видит только радиальную амплитуду `T |H|^2`, а бесследовая форма `Q`
исчезает.

## Почему `M300` не скрывает произвольную стрелку

`M300(C)` является окружающей алгеброй эндоморфизмов и носителем следа,
а не координатной алгеброй в определяющем представлении. Одна
принадлежность матрицы `M300` не означает принадлежность физическому
комплексу одноформ.

## Сохранившаяся зацепка

Смешанный модуль `Y_rho=E_rho tensor Lambda_ch` существует и имеет
комплексную размерность `12`. Но он является аффинным пространством
связностей: остаются две вещественные относительные координаты между
рёбрами `u,d,e`. В полном моритовском углу неоднозначность составляет не
менее пяти комплексных направлений. Каноническая ненулевая секция не
выбрана.

## Следующий гейт

Нужно проверить двухшаговую композицию уже существующих семейной и
хиггсовской одноформ. Только если её кривизна автоматически даст
`Tr(Q^2) H^dagger H` с фиксированными знаком и коэффициентом, непрямой
коннектор будет выведен без расширения модели.

Последующий аудит закрыл и этот путь: градуированное произведение
сокращает смешанный оператор, junk-идеал удаляет форму `Q`, а моритова
кривизна остаётся аддитивной. См.
[[version6-spectral-transition-morita-two-step-connector-gate]].

## Links

- [[version6-spectral-transition-rank-change-localization-gate]]
- [[version6-bosonic-defect-field-identification-gate]]
- [[version5-commuting-square-readout-gate]]
- [[version5-h15-physical-oneform-bimodule-gate]]
- [[version5-physical-corner-connection-classification-gate]]
- [[version5-m300-coordinate-algebra-wellposedness-gate]]
- [[spectral-transition-primitive-literature-2026]]
- [[version6-spectral-transition-morita-two-step-connector-gate]]

## Source Notes

- `s2t/gates/version6_spectral_transition_radial_bridge_vortex_connector_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_radial_bridge_vortex_connector_gate.py`
- `s2t/results/s2t_v6_spectral_transition_radial_bridge_vortex_connector_gate_results.json`
- T. Krajewski, *Classification of Finite Spectral Triples* (1998).
- M. Paschke, A. Sitarz, *Discrete Spectral Triples and Their
  Symmetries* (1998).