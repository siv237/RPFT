# Том VI: компонентные граничные циклы классов 12 и 3

> Status: working
> Type: question
> Updated: 2026-08-21

## Краткий вывод

Кварковая опора ранга `12` и лептонная опора ранга `3` являются
настоящими самостоятельными спектральными подциклами:

- имеют собственные тёплицевы индексы `-12/+12` и `-3/+3`;
- задают KO6-классы `12` и `3`;
- допускают явные Real-парные KO7-символы;
- сохраняют градуировку, Real-структуру и условие первого порядка
  текущего заряженного `H15`;
- имеют собственные неограниченные циклы `N,U`.

## Глобальное ограничение

Ни одна компонента в одиночку не является исходным вынужденным дефектом.
Полный ledger требует

`15 = 12 + 3`.

Только прямая сумма восстанавливает индексы `-15/+15` и вес `1/7`.
Следовательно, класс `15` составен, но его суммарная величина остаётся
глобально фиксированной.

## Связывание не найдено

Петлевое действие и конечноранговый вакуумный отклик строго аддитивны:

`4/35 + 1/35 = 1/7`.

Перекрёстный след между ортогональными проекторами равен нулю. Текущий
родитель не содержит расстояния между кварковым и лептонным ядрами и не
заставляет их иметь общий пространственный центр.

Поэтому «пакет поколения» пока означает обязательную сумму классов, но
не связанную частицу.

## Массовая граница

Общий скалярный перенос оставляет один свободный параметр `m`.
Независимые переносы компонент оставляют два параметра `m_q,m_l`.
Компонентные веса `4/35` и `1/35` не выбирают эти амплитуды, поэтому
ненулевые щели не выведены.

## Результат следующего гейта

[[version6-spectral-transition-component-colocalization-gate]] проверил
пространственный, хиггсовский, gauge-, моритовский и Каллиасов каналы.
Все выведенные действия остались аддитивными или рангово-слепыми.
Единственный общий Каллиасов профиль условно колокализовал бы компоненты,
но его spin-cover-носитель конечным родителем не выведен.

## Links

- [[version6-spectral-transition-minimal-support-gate]]
- [[version6-spectral-transition-component-colocalization-gate]]
- [[version5-one-seventh-toeplitz-boundary-map-gate]]
- [[version5-real-toeplitz-bott-comparison-map-gate]]
- [[version5-real-toeplitz-unbounded-parent-cycle-gate]]
- [[version5-toeplitz-parent-action-variational-gap-gate]]
- [[version5-topological-closure-deficit-gate]]
- [[version5-closure-deficit-induced-vacuum-response-gate]]
- [[transition-primitive]]
- [[spectral-transition-primitive-literature-2026]]

## Source Notes

- `s2t/gates/version6_spectral_transition_component_boundary_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_component_boundary_gate.py`
- `s2t/results/s2t_v6_spectral_transition_component_boundary_gate_results.json`
- T. Krajewski, arXiv:hep-th/9701081.
- M. F. Atiyah, *K-Theory and Reality* (1966).
- S. Baaj, P. Julg, *Théorie bivariante de Kasparov et opérateurs non
  bornés dans les modules hilbertiens* (1983).