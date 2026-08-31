# Комплексы пространства полей, суперсвязности, BV и mapping cone

> Status: working
> Type: source
> Updated: 2026-08-29

## Summary

Литературная граница следующего шага: градуированный вспомогательный
носитель может быть суперсвязностью или соответствием без превращения его
волокон в физические фермионы. Стандартный BV/BRST-комплекс, напротив,
организует калибровочную редукцию и сам по себе не является источником
нового классического потенциала. Relative/mapping-cone геометрия требует
явных идеала или граничных данных и не возникает только из совпадения
размерностей.

## Primary Sources

- D. Quillen, *Superconnections and the Chern character*, Topology 24
  (1985), DOI `10.1016/0040-9383(85)90047-3`: суперсвязность допускает
  нечётную эндоморфную часть; её квадрат является кривизной.
- M. Harada, G. Wilkin, *Morse theory of the moment map for
  representations of quivers*, `arXiv:0807.4734`: квадрат нормы
  отображения момента на пространстве представлений колчана задаёт
  естественный Morse-функционал.
- H. Nakajima, *Instantons on ALE spaces, quiver varieties, and Kac--Moody
  algebras*, Duke Mathematical Journal 76 (1994), 365--416: колчанные
  многообразия строятся редукцией пространства представлений по
  произведению групп вершин; циклические данные переживают древесную
  калибровочную фиксацию.
- G. Roepstorff, *Superconnections and Matter*,
  `arXiv:hep-th/9801040`: поле Хиггса рассматривается как часть
  суперсвязности на внешней алгебре, а действие строится из кривизны.
- B. Mesland, *Unbounded Bivariant K-Theory and Correspondences in
  Noncommutative Geometry*, `arXiv:0904.4383`: оператор и связность на
  модуле являются данными морфизма спектральных геометрий, а не
  дополнительными координатными фермионными вершинами.
- I. Forsyth, M. Goffeng, B. Mesland, A. Rennie,
  *Boundaries, spectral triples and K-homology*,
  `arXiv:1607.07143`: relative spectral triple задаётся относительно
  идеала и граничной структуры.
- M. Grigoriev, *Parent formulation at the Lagrangian level*,
  `arXiv:1012.1903`: parent/BV-расширения вводят поля и анти-поля в
  мастер-действии, сохраняя контролируемую связь с исходной системой.
- K. Fredenhagen, K. Rejzner, *Batalin--Vilkovisky formalism in the
  functional approach to classical field theory*,
  `arXiv:1101.5112`: BV описывает гомологическую калибровочную редукцию
  и наблюдаемые.

## Project Cross-Check

Проект уже получил пять разграничивающих результатов.

1. `version3_fluctuated_product_bv_complex_gate.tex`: BRST/BV правильно
   считает gauge, Goldstone и ghost степени свободы после того, как
   физическое действие уже задано.
2. `version4_pati_salam_bv_multiplicity_fork_gate.tex`: контрактные
   gauge-fixing пары не добавляют новый determinant-потенциал и не меняют
   классический stationary locus.
3. `version6_polar_bv_rank_loss_barrier_gate.tex`: FP/BV-якобиан
   переписывает меру, но не создаёт требуемый классический барьер.
4. `version4_pati_salam_junk_mapping_cone_gate.tex`: mapping-cone
   производная может выделить endpoint-кривизну, однако standard junk
   quotient способен, наоборот, удалить этот путь.
5. `version5_graded_correspondence_superconnection_gate.tex`:
   дополнительная цепь допустима как операторное содержание
   градуированного соответствия, хотя не следует из одной координатной
   алгебры.

## Consequence for Tome VII

Цепь `1 -> 6 -> 3` не следует называть BV-комплексом: ориентированный
оператор `d_B` вне вакуума имеет

$$
d_B^2=\Lambda^2B\ne0.
$$

Это кривой градуированный комплекс, кривизна которого измеряет нарушение
условия ранга один. В вакууме `Lambda^2 B=0`, и он становится настоящим
комплексом.

Наиболее консервативное чтение — Quillen-суперсвязность или
градуированное соответствие на ассоциированном пространстве стрелок.
Mapping cone остаётся возможной относительной интерпретацией, но для
полученного потенциала не нужен: полный спектральный след уже содержит
детерминант. Стандартный BV/BRST следует подключать позже, только если
возникнет реальная калибровочная избыточность.

## Project Outcome

[[version7-edge-coherence-field-space-superconnection-gate]] подтвердил
основной литературный маршрут. Цепь реализована как ассоциированный
градуированный пучок с индуцированными связностями; полный `U(3)` каналов
не получает физического статуса, а конечная следовая метрика поля `B`
положительна. Открытым остаётся не носитель, а конкуренция всех
одиннадцати разрешённых рёбер.

[[version7-edge-coherence-full-graph-competition-gate]] закрыл эту
конкуренцию отрицательно для текущего действия: целевая опора имеет ранг
два, а внешние рёбра не входят в суперсвязность. Это не опровергает
литературный носитель; оно ограничивает конкретное физическое применение.

[[version7-edge-grading-hodge-superconnection-parent-gate]] вернул
положительный полевой результат уже на полном пространстве стрелок.
Фиксированный нильпотентный фоновый цвет выводит знаковую градуировку, а
норма одного отображения момента одновременно запускает шесть целевых
блоков и стабилизирует их квартикой. Открыта не математическая норма, а её
конечное Real-бимодульное физическое вложение.

[[version7-real-arrow-bimodule-forest-quotient-gate]] дал точную границу
этого вложения. Два цвета являются одним Real-эквивариантным колчанным
суперсвязностным объектом на модуле стрелок. Но поскольку фоновый оператор
бимодульно линеен, его стандартный модуль внутренних одноформ равен нулю:
это соответствие пространства полей, а не новая почти-коммутативная
фермионная тройка. Колчанный quotient также должен учитывать замороженные
рёбра `H15`; они превращают лес новых рёбер в граф с одной циклической
`U(3)`-голономией.

## Повторное использование в Томе VIII

Новый [[version8-gauge-closed-noise-parent-hessian-gate]] показал, что
старый полевой срез и новый noise-module не совпадают. Поэтому прежняя
суперсвязностная конструкция снова становится актуальной, но уже в более
полной форме: endpoint gauge-связности, полный arrow-модуль и BV/BRST
касательный комплекс должны быть собраны до отображения флуктуаций в
операторы QMS. Подробная формульная карта дана в
[[version8-unified-field-space-project-intuition-search]].

## Links

- [[version7-auxiliary-carrier-project-intuition-search]]
- [[version7-edge-coherence-bimodule-admission-gate]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[version7-edge-coherence-full-graph-competition-gate]]
- [[version7-edge-grading-hodge-superconnection-parent-gate]]
- [[version7-real-arrow-bimodule-forest-quotient-gate]]
- [[version7-edge-coherence-spectral-parent-gate]]
- [[exterior-power-superconnection-parent-literature-2026]]
- [[superconnection-odd-endomorphism-parent-literature-2026]]
- [[pati-salam-junk-mapping-cone-gate]]
- [[version5-graded-correspondence-superconnection-gate]]

## Source Notes

- `s2t/gates/version3_fluctuated_product_bv_complex_gate.tex`
- `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex`
- `s2t/gates/version4_pati_salam_junk_mapping_cone_gate.tex`
- `s2t/gates/version5_graded_correspondence_superconnection_gate.tex`
- `s2t/gates/version6_polar_bv_rank_loss_barrier_gate.tex`