# Поиск микроскопического interaction-Hamiltonian для Тома VIII

> Status: working
> Type: synthesis
> Updated: 2026-08-29

## Summary

Сильнейший найденный кандидат не требует произвольного продолжения
Stinespring-изометрии. Уже выведенные двенадцать самосопряжённых
cross-arrow операторов можно напрямую связать с вакуумом минимальной
тринадцатимерной среды одним самосопряжённым «звёздным» взаимодействием.
В пределе слабых частых столкновений оно возвращает проектный
GKSL-генератор. Это настоящий мост от замкнутой unitary-микродинамики к
безразмерной непрерывной полугруппе, но ещё не уникальный физический
Hamiltonian часов.

## Minimal candidate

Пусть

```text
K_env = C|0> direct_sum span{|a> : a=1,...,12}
```

и `D_a=D_a*` — уже проверенный cross-arrow базис. Минимальный линейный
кандидат имеет вид

```text
H_int = sum_a g_a D_a tensor (|a><0| + |0><a|).
```

Он самосопряжён. При совместном ортогональном преобразовании операторов
`D_a` и меток среды сумма базисно-независима. Если среда несёт уже
выведенное dual cross-представление, то взаимодействие gauge-инвариантно.

Для одного короткого столкновения берётся

```text
U_h = exp(-i sqrt(h) H_int),
```

а среда готовится в `|0>`. Тогда

```text
K_0(h) = I - h G_g/2 + O(h^2),
K_a(h) = -i sqrt(h) g_a D_a + O(h^(3/2)),
G_g = sum_a g_a^2 D_a^2,
```

и редуцированная карта удовлетворяет

```text
Phi_h(X) = X + h L_g(X) + O(h^2),
L_g(X) = sum_a g_a^2 (D_a X D_a - {D_a^2,X}/2).
```

При повторении со свежими ancilla получается уже найденный collision-limit.
Это стандартный механизм repeated interactions, но здесь его системные
операторы и минимальный carrier не вставлены извне: они взяты из
cross-arrow геометрии Тома VIII.

## What this closes

- Предъявлен явный самосопряжённый system--environment Hamiltonian, а не
  произвольный логарифм Kraus-карты.
- Объяснена размерность среды `1+12=13`: одна vacuum-линия и полный
  cross-arrow модуль.
- GKSL-генератор возникает как слабый предел unitary столкновений.
- Ковариантность реализуется на уровне полного system--environment
  взаимодействия.
- Свобода `U(252)` произвольного unitary-продолжения больше не нужна для
  построения конкретной микродинамики.

## What remains open

1. **Не точный конечный шаг.** Экспонента `exp(-i sqrt(h)H_int)` совпадает с
   проектным каналом `K_0=sqrt(I-hG)`, `K_a=sqrt(h)D_a` только в касательной
   при `h=0`; высшие порядки в общем случае различны.
2. **Не уникальный Hamiltonian.** Можно добавлять допустимые блоки внутри
   jump-сектора или выбирать другую микроскопическую реализацию с тем же
   Lindblad-пределом.
3. **Остаётся матрица связей.** Точный последующий kill-test показал, что
   `QLYR` и `XLdR` являются двумя эквивалентными gauge-копиями. Полный
   вещественный коммутант имеет размерность `8`; каждый его вещественный
   элемент даёт самосопряжённый interaction-Hamiltonian. Генератор видит
   симметричную rate-метрику `C^T C` из четырёхмерного подпространства.
   Поэтому допустимы не только две диагональные скорости, но и межсемейное
   смешивание.
4. **Остаётся масштаб времени.** Замена `H_int -> g H_int` эквивалентна
   перенормировке макроскопического времени через `g^2 h`.
5. **Свежая среда не выведена.** Бесконечная цепь подготовленных ancilla или
   её Fock-предел остаётся физическим ресурсом модели.
6. **Автономные часы требуют ресурса.** Литература по автономным квантовым
   часам связывает устойчивое тиканье с неравновесностью и производством
   энтропии; один стационарный канал не поставляет этот ресурс.

## Kill test for the next gate

Следующий гейт имеет смысл только как проверка конкретного утверждения:

> Является ли звёздный `H_int` единственным interaction-Hamiltonian в классе
> самосопряжённых, Real-чётных, gauge-инвариантных операторов, линейных по
> `D_a`, не содержащих jump--jump блока и использующих минимальный carrier?

Полученный честный результат оказался слабее ожидаемой единственности:
`QLYR` и `XLdR` эквивалентны, поэтому вещественная матрица
interaction-связей имеет восемь параметров, а индуцированная симметричная
rate-метрика — четыре. Положительная часть результата остаётся
существенной: это микроскопическая реализация динамики, но не полное
физическое замыкание.

## Literature comparison

- Attal--Pautrat выводят квантовый шум и master-equation как непрерывный
  предел повторных Hamiltonian-взаимодействий; любой Lindblad-генератор
  допускает такую аппроксимацию.
- Attal--Joye показывают критический режим `lambda^2 tau=1`, в котором
  repeated-interaction модель даёт общий Lindblad-генератор, и обратное
  построение модели для заданного генератора.
- Tempel--Aspuru-Guzik строят Feynman-clock для открытых систем через
  ансамбль неэрмитовых history-Hamiltonian и stochastic unraveling. Это
  полезная история-состояний, но не заменяет единственный самосопряжённый
  system--bath Hamiltonian проекта.
- Erker et al. показывают на автономных часах, что рабочее тиканье требует
  неравновесного ресурса и имеет термодинамическую цену.

## Links

- [[version8-canonical-autonomous-clock-unitary-extension-no-go-gate]] —
  почему Kraus-карта не выбирает полный unitary.
- [[version8-microscopic-repeated-interaction-hamiltonian-gate]] — точный
  kill-test кандидата: восьмимерный interaction-коммутант и четырёхмерный
  коммутант симметричных rate-метрик.
- [[version8-trace-dual-cross-interaction-selector-gate]] — следующий
  условный шаг: полевой суперслед выбирает `I_12/3`, если среда является
  метрически двойственным cross-модулем.
- [[version8-minimal-covariant-stinespring-carrier-gate]] — минимальная
  среда и двенадцать `D_a`.
- [[version8-intrinsic-noise-clock-dilation-gate]] — существующий
  collision-limit.
- [[intrinsic-time-and-repeated-interaction-literature-2026]] — первичная
  литература по пределу повторных взаимодействий.
- [[relational-modular-internal-time-literature-2026]] — отличие
  реляционного и модульного времени.

## Source Notes

- `s2t/gates/version8_minimal_covariant_stinespring_carrier_gate.tex`
- `s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex`
- `s2t/gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex`
- `s2t/gates/version6_clock_controlled_energy_conserving_quench_gate.tex`
- S. Attal, Y. Pautrat, “From repeated to continuous quantum interactions”,
  Annales Henri Poincare 7 (2006), 59--104; arXiv:math-ph/0311002.
- S. Attal, A. Joye, “Weak coupling and continuous limits for repeated
  quantum interactions”, Journal of Statistical Physics 126 (2007),
  1241--1283; arXiv:math-ph/0501012.
- D. G. Tempel, A. Aspuru-Guzik, “Feynman's Clock for open quantum
  systems”, arXiv:1406.5631.
- P. Erker et al., “Autonomous quantum clocks: does thermodynamics limit
  our ability to measure time?”, Physical Review X 7 (2017), 031022;
  arXiv:1609.06704.