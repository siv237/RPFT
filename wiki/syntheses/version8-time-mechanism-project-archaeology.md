# Археология механизмов времени для автономной шумовой цепи

> Status: mature
> Type: synthesis
> Updated: 2026-08-30

## Итог

Проект уже замкнул кинематическую и локально-наблюдаемую части автономного
времени: построены свежие 43-мерные вспомогательные системы, индексно
сбалансированный локальный конвейер, конечные часы истории и совместный
предел часов со слабым столкновительным процессом. Не замкнута размерная
часть: формула `Gamma=chi^2 E_C/hbar` получена, но ни `E_C`, ни `chi` не
выводятся текущим родителем.

## Задача

Проверить, не была ли автономная поставка среды или физическое время уже
решена на более раннем уровне, и определить, какие формулы можно перенести
без смены их смысла.

## Поиск решения

| Ранняя ветвь | Точная формула | Что действительно решено | Почему недостаточно отдельно |
|---|---|---|---|
| Внутренний lapse Тома V | `d tau=N(q) dt` | Отношение внутреннего и внешнего темпа; `N=1/4` даёт задержку в четыре раза | Уже предполагает внешнее `t`; не создаёт такты, устойчивость или резервуар |
| Резонанс `C4` | `1,i,-1,-i,1` | Четырёхтактная фазовая задержка без уменьшения локальной скорости | Считает фазу по модулю четыре; не хранит абсолютный номер шага и не обновляет среду |
| Оператор числа/Тёплица | `N e_n=n e_n`, `[N,U^k]=kU^k` | Абсолютный целый счётчик и канонический сдвиг между тактами | Носитель `ell2(Z)` сам по себе не является цепью квантовых ancilla и не задаёт их vacuum-состояние |
| Модулярное время | `sigma_s(A)=rho^(is) A rho^(-is)` | Внутренний обратимый поток и ориентация стрелок | Сохраняет породившее его состояние и не создаёт диссипативный GKSL-перенос |
| Четырёхуровневые часы | `[W,H_S+H_C]=0` | Строгий тест автономности и энергетических кратностей | Невырожденная лестница имеет потолок `2/3`; часы испытывают обратную реакцию и не являются свежей средой |
| Дискретный compacton | `E Delta t=pi hbar/2`, `a/Delta t=c` | Условное произведение `EL=pi hbar c` | Остаётся масштабная орбита `(a,Delta t,E)->(lambda a,lambda Delta t,E/lambda)` |
| Page--Wootters--Stinespring | `rho_n=Phi^n(rho_0)` | Условные срезы часов точно возвращают последовательность канала | Конструкция уже предполагает отдельную среду на каждом такте; полный clock-unitary не каноничен |
| Полный collision-предел | `Phi_(u/n)^n -> exp(u L_42)` | Непрерывное безразмерное течение и микроскопический star-Hamiltonian | Источник fresh ancilla и длительность такта остаются внешними |

## Переиспользуемая конструкция

Ранний Toeplitz-блок даёт правильный кинематический каркас для следующего
гейта. Пусть

`K_cell=C43`, `K_chain=otimes_(n in Z) K_cell`

относительно опорного vacuum-вектора `|0>^(otimes Z)`. Обозначим сдвиг
ячеек через `S_chain`, а collision-unitary системы с нулевой ячейкой через
`U_col`. Один автономный дискретный такт имеет кандидат

`V=(I_system tensor S_chain) U_col^(0)`.

Если входная цепь является произведением vacuum-ячеек, то после `n` тактов
система должна точно иметь состояние `Phi^n(rho_0)`: использованная ячейка
уходит по сдвигу, а к системе приходит следующая свежая ячейка. Оператор
числа маркирует положение фронта и различает первый и произвольный `n`-й
такт.

## Граница автономности

Нужно различать два уровня.

1. **Кинематически автономный конвейер:** один фиксированный глобальный
   унитарий действует повторно на заранее приготовленной бесконечной
   vacuum-цепи. Этот уровень теперь имеет все необходимые проектные детали
   и является следующим конструктивным гейтом.
2. **Сильная физическая автономность:** сам parent выводит цепь, её
   опорное состояние, локальную энергию, сдвиг, отсутствие начальных
   корреляций и ресурс поддержания. Этот уровень ранними формулами не закрыт.

Конечная среда не может бесконечно оставаться свежей без возврата,
сброса или истощения. Поэтому строгий маршрут должен сразу использовать
бесконечную цепь, Fock-дилатацию либо сформулировать конечновременное окно.

## Результаты продолжения после конвейера

| Проверка | Результат |
|---|---|
| Родитель вакуумной цепи | `H_Lambda=sum_m(I-|0><0|_m)`, единственный вакуум, щель `1` |
| Локальное происхождение одностороннего сдвига | запрещено: `ind_GNVW(S_43)=43` |
| Встречный поток | `43*(1/43)=1`, точная двухслойная схема перестановок |
| Один статический гамильтониан на минимальном носителе | запрещён числами намотки `(-1,+1)` |
| Часы истории | точное выполнение двух слоёв за `pi/2`, без возврата часов |
| Конечная глобальная точность | `epsilon<=2LA exp(-cd)`, достаточно `d>=c^(-1)log(2AL/delta)` |
| Локальный непрерывный предел | `C_u/n+nA exp(-cd)`, логарифмическое расписание `d_n` |
| Абсолютная секунда | не выведена из-за общей масштабной орбиты |
| Размерный мост | `Gamma=chi^2E_C/hbar`, `Gamma/Omega=chi^2` |
| Внутренние кандидаты на `E_C` | шесть классов проверены, ни один не прошёл |
| Смешанный резонансный родитель | `[H_0,G]=0`, полный `L_42` возвращается, но `E_C` и `chi` свободны |

## Текущий ожидаемый результат

Последняя осмысленная проверка временной ветви выполнена. Минимальный
смешанный родитель сохраняет полную энергию и возвращает `L_42`, однако
общая масштабная орбита и свобода `chi` сохраняются. Аффинная кратность три
не поставляет каноническую карту в 42-мерный шумовой носитель. Временной
спринт на текущем родительском действии закрыт; следующий фронт — точные
материалы барионного сектора.

## Проверка соответствия

- Проверены ранние ветви Томов IV--VIII и их страницы вики.
- Lapse, фазовый `C4`, модулярный поток, абсолютный счётчик и физическая
  калибровка разведены по типам.
- Toeplitz `N/U` действительно переиспользован как адресный конвейер для
  `C43`-ячеек.
- Вакуум, локальный перенос, часы и локальный непрерывный предел разведены
  по отдельным формулам и статусам.
- Проверены шесть внутренних кандидатов на энергию часов; переименование
  безразмерной щели в энергию запрещено.
- Найдена одна новая зацепка в старом слое: энергосохраняющий резонанс
  `[W,H_S+H_C]=0` и аффинная кратность три. Они задают последний
  ограниченный тест, но пока не являются размерным якорем.
- Полная формульная цепь вынесена в
  [[version8-time-formula-intuition-map]].

## Links

- [[version5-self-consistent-internal-time-horizon-gate]]
- [[version5-order-four-resonant-loop-transport-gate]]
- [[version5-real-toeplitz-unbounded-parent-cycle-gate]]
- [[version6-single-thread-c4-suspension-parent-gate]]
- [[version6-clock-controlled-energy-conserving-quench-gate]]
- [[version6-projective-quench-parent-dynamics-gate]]
- [[version6-spectral-transition-discrete-compacton-physical-scale-map-gate]]
- [[version8-page-wootters-stinespring-history-gate]]
- [[version8-full-noise-repeated-interaction-hamiltonian-gate]]
- [[version8-full-noise-physical-time-scale-no-go-gate]]
- [[version8-full-noise-toeplitz-ancilla-chain-dilation-gate]]
- [[version8-vacuum-chain-parent-state-and-local-hamiltonian-origin-gate]]
- [[version8-index-balanced-ancilla-conveyor-gate]]
- [[version8-static-local-hamiltonian-embedding-or-no-go-gate]]
- [[version8-clock-augmented-static-hamiltonian-conveyor-gate]]
- [[version8-bounded-strength-autonomous-clock-thermodynamic-limit-gate]]
- [[version8-local-observable-clocked-qms-limit-and-time-anchor-gate]]
- [[version8-typed-clock-energy-to-noise-rate-anchor-gate]]
- [[version8-clock-energy-anchor-candidate-audit-gate]]
- [[version8-minimal-mixed-clock-collision-parent-gate]]
- [[version6-existing-multiplicity-resonant-sink-gate]]
- [[version8-time-formula-intuition-map]]

## Source Notes

- `s2t/gates/version5_self_consistent_internal_time_horizon_gate.tex`
- `s2t/gates/version5_real_toeplitz_unbounded_parent_cycle_gate.tex`
- `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex`
- `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex`
- `s2t/gates/version8_page_wootters_stinespring_history_gate.tex`
- `s2t/gates/version8_full_noise_repeated_interaction_hamiltonian_gate.tex`
- `s2t/gates/version8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate.tex`
- `s2t/gates/version8_index_balanced_ancilla_conveyor_gate.tex`
- `s2t/gates/version8_static_local_hamiltonian_embedding_or_no_go_gate.tex`
- `s2t/gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex`
- `s2t/gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex`
- `s2t/gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex`
- `s2t/gates/version8_typed_clock_energy_to_noise_rate_anchor_gate.tex`
- `s2t/gates/version8_clock_energy_anchor_candidate_audit_gate.tex`
- `s2t/gates/version8_minimal_mixed_clock_collision_parent_gate.tex`
- `s2t/gates/version6_existing_multiplicity_resonant_sink_gate.tex`