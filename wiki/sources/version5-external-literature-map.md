# Version V external literature map

> Status: working
> Type: source
> Updated: 2026-08-17

## Фермионное спектральное действие и оператор Вайнберга

- S. Weinberg, DOI `10.1103/PhysRevLett.43.1566` — исходный оператор
  размерности пять, нарушающий лептонное число на две единицы.
- M. Sakellariadou, A. Sitarz, `arXiv:1903.09149` — нескалярное
  фермионное спектральное действие может породить хиггс-квадратичный
  майорановский член в 15-мерной геометрии без правого нейтрино; функция
  отсечения и её моменты остаются дополнительными данными. Формула
  содержит `Y_e Y_e^dagger`, масштаб отсечения и вакуумное значение Хиггса;
  классификация нескалярных функций оставлена открытой, а смешивание
  требует дополнительной недиагональной семейной части оператора `tau`.
- C. I. Low, `arXiv:hep-ph/0305243` — циклическая семейная симметрия
  ограничивает матрицы до циркулянтного класса, но не фиксирует полный
  спектр масс и смешиваний.

## Резонансные петли и связанные состояния в непрерывном спектре

- `arXiv:2309.01501` — экспериментальная и теоретическая граница между
  резонансами Фано и связанными состояниями в непрерывном спектре при
  интерференционном слиянии резонансов.
- `arXiv:1410.2846` — квантовые графы с петлями и полубесконечными рёбрами;
  локализованные состояния появляются при специальных спектральных и
  связующих условиях.

## Самогравитирующие поля и внутреннее время

- `arXiv:gr-qc/0404014` — стационарные и эволюционные решения системы
  Шрёдингера--Ньютона; масштаб решения связан с нормой, поэтому отдельный
  радиус требует фиксированной нормировки.
- `arXiv:1708.05674` — историческая идея геона как света, удерживаемого
  собственной гравитацией, и границы асимптотически плоских
  электровакуумных реализаций.
- `arXiv:1408.5906` — гладкие периодические геоноподобные решения в
  антидеситтеровском пространстве используют удерживающую глобальную
  геометрию и не являются готовой моделью изолированной элементарной
  частицы.

Проектный вывод зафиксирован в
[[version5-self-consistent-internal-time-horizon-gate]]: коэффициент хода
времени является допустимым ингредиентом, но не заменяет потенциал
дефекта, обратную реакцию и проверку открытого обмена.

## Summary

The Version V literature audit finds strong independent precedents for
nearly every individual ingredient in the three surviving architecture
classes. The admissible novelty target is therefore not an ingredient but a
single coefficient-free conjunction derived from one parent architecture.

## Carrier-first cluster

Already known:

- Gibbs variational principles and quantum-relative-entropy formulations;
- information geometry of density-state families;
- spectral action and heat-kernel metric variation;
- one-loop partition functions on compact positive-curvature saddles;
- renormalization and local counterterms.

Project-specific open conjunction: jointly vary a normalized state and
carrier derived from one correlation operator, obtain the fluctuation action
from the same Hessian, fix finite topology weights before comparison and pass
a physical joint Hessian.

## Boundary-source cluster

Already known:

- spontaneous `SO(3) -> A4` breaking;
- Wilson-line flavour breaking and Hosotani dynamics;
- finite-tension order-three `A4` vortices;
- fixed-charge path integrals and rotor EFT;
- topological Majorana defect modes.

Project-specific open conjunction: one boundary Hilbert space and trace must
simultaneously derive the odd fixed-charge sector, charge-two condensate,
physical tetrahedral family axis, exact-one Majorana kernel and an
SM-sensitive second normalization sector.

## Finite-geometry cluster

Already known:

- spectral Pati--Salam models and generalized inner fluctuations;
- their one-loop unification scenarios and vacuum difficulties;
- Connes forms, junk quotients and Krajewski diagrams;
- torsion-induced four-fermion channels and auxiliary-field rewrites.

Project-specific open conjunction: a bounded classification theorem for a
new finite geometry that derives the required relative sign and a full-rank
physical Hessian before phenomenology.

The ordinary spectral subroute is now closed more generally by
[[version5-ordinary-spectral-moment-map-no-go-gate]]: the spectrum of the odd
Dirac operator retains the middle-node sum `A+B` but not its oriented
decomposition into `A-B`. This is a project theorem, not a claim that all
noncommutative or symplectic architectures are incompatible.

## Anti-circle rule

Every new Tome V gate must distinguish:

1. known external ingredient;
2. already tested project implementation;
3. exact new theorem being attempted;
4. stop rule preventing a closed implementation from being renamed.

## Relative/functorial cluster

The foundational rereading adds a fourth, supporting literature cluster:

- unbounded KK-correspondences as morphisms between spectral triples;
- relative spectral triples for boundaries and ideals;
- BV-BFV cutting and gluing;
- determinant/Pfaffian lines and functorial anomaly theories;
- relative modular operators and cocycle derivatives.

These are established ingredients. The project-specific target is only the
concrete RPFT/UGSM/TOE reduction triangle and its closed-loop cocycle defect.

## Post-no-go orientation fork

The literature check following the ordinary spectral blindness theorem
separates four claims that must not be conflated:

- twisted spectral triples can generate linked scalar and vector
  fluctuations, but do not yet compute the project family moment map;
- derived Poisson and BV--BFV constructions provide symplectic reduction
  languages, but no finite KO6 project realization;
- relative-entropy Hessians provide positive information metrics, not an
  automatic incoming-minus-outgoing selector;
- quiver moment maps natively encode oriented arrows.

The project-specific candidate selected in
[[version5-nonordinary-architecture-fork-gate]] is cheaper: recover the
oriented differential using the existing integer height and select the
zero-height Hodge block with `I-h^2`. Its full KO6 origin remains to be
tested.

That test is now complete in [[version5-oriented-height-hodge-ko6-gate]].
The standard KO6 constraints admit both a coherent-chain height producing
`A-B` and a middle-sink height producing `A+B`. This matches the literature
boundary: quiver moment maps are defined after an orientation is supplied,
and height functions used to orient quivers are fixed combinatorial input.
The existing finite spectral triple does not derive that extra choice.

The first twisted precheck is also complete in
[[version5-twisted-family-automorphism-gate]]. The grand-symmetry and
minimal-twist mechanisms rely on flips between isomorphic represented
copies. Since the current `R direct_sum M3(R) direct_sum C` summands are
pairwise nonisomorphic, no such exchange exists. Only a selectively doubled
four-summand algebra remains inside the frozen complexity budget.

The bounded comparison in [[version5-minimal-twist-doubling-budget-gate]]
then tests all three selective duplications. Real-scalar and family-matrix
copies touch both quiver arrows, while complex duplication touches only the
outgoing arrow. The real-scalar flip is frozen for one representation test
because it adds no continuous gauge generators; this is a project triage
decision, not a literature novelty claim.

The explicit construction in
[[version5-real-scalar-flip-twisted-ko6-gate]] then passes faithfulness,
order zero and the real twisted first-order condition of the literature.
Its twisted one-forms nevertheless preserve the nearest-neighbour odd graph,
so an ordinary spectral trace remains blind to the oriented Gram
decomposition. The remaining question is no longer the twist itself but the
existence of a positive, canonically normalized twisted trace or modular
weight.

That final finite twisted-measure test is closed by
[[version5-flip-twisted-trace-positivity-gate]]. Unlike positive q-traces
implemented by a modular operator in established examples, a trace twisted
by the outer flip of two orthogonal central idempotents must annihilate both
idempotents. The explicit representation also has unequal flipped ranks
`6` and `3`, excluding an invertible positive intertwining weight. A type-III
replacement would therefore be a new parent architecture rather than a
completion of the finite twist.

The minimal derived test is now complete in
[[version5-derived-moment-map-minimal-data-gate]]. The doubled-quiver
preprojective relation exactly reproduces `XX^T-Y^T Y`, but the standard
orientation-change isomorphism uses a minus sign on the formal reverse
arrow and is not compatible with representing that arrow by the Hilbert
adjoint. Moreover the symmetric real relation pairs trivially with
`so(3)`; its standard Hamiltonian interpretation requires a `u(3)` or
`gl(3)` enlargement. Koszul/BRST resolution is therefore conditional on an
already supplied moment relation rather than an origin of it from the
current KO6 data.

The Version V ledger is frozen in
[[version5-parent-architecture-status-freeze-gate]]. None of the three
preregistered architecture classes reaches a common parent functional,
positive all-sector measure, physical BV/BRST Hessian or two-sector trace
normalization. This is an internal exhaustion theorem for the declared
finite positive KO6 menu, not a universal no-go for modular, type-III or
complex symplectic parent theories.

Последующее модулярное возобновление программы получило единый носитель
следа, но выявило новое различие в
[[version5-m300-coordinate-algebra-wellposedness-gate]]. Классификация
конечных вещественных спектральных троек рассматривает гильбертово
пространство как левый--правый бимодуль над заданной координатной алгеброй;
алгебра всех операторов на этом пространстве не становится координатной
автоматически. В определяющем представлении `M300(C)` коммутант скалярен,
поэтому верное противоположное действие не удовлетворяет условию нулевого
порядка. Кроме того, нескалярный `D` порождает все `90000` матричных
направлений одноформ. Результат о едином следе `M300` сохраняется, а полное
исчисление требует меньшей явно представленной координатной алгебры.

Обратный проектный поиск в
[[version5-affine-ko6-reference-corner-gate]] восстановил точный бимодуль
`(4→3→3)×15×2=300`. Стандарт-модельная литература трактует три поколения
как кратности одних и тех же бимодулей конечной алгебры, а не как три
координатные матричные копии. Поэтому следующий приоритет --- оставить
`C+H+M3(C)` координатной алгеброй, а семейную цепь искать в коммутанте её
представления как градуированное соответствие. Это избегает наивного
увеличения `M3 tensor M3 -> M9`, но ещё требует отдельного доказательства
дифференциального исчисления и действия Ходжа.

Проверка [[version5-sm-family-commutant-calculus-gate]] уточнила эту
границу. Если `A_SM` действует как `I_fam tensor pi_SM`, а семейный оператор
лежит в коммутанте, то
`[D,pi(a)]=I_fam tensor [D_SM,pi_SM(a)]`. Следовательно, обычные одноформы
не зависят от семейной цепи. Прямая сумма распадается по центральным
идемпотентам, а тензорное произведение семейного и цветового матричных
блоков создаёт `M9(C)`. Поэтому литературно естественная следующая ветвь ---
неограниченное градуированное соответствие со собственной связностью в
смысле программы Межланда, а не ещё одна обычная конечная спектральная
тройка. Это остаётся направлением проверки, а не установленным физическим
замыканием.

Следующий аудит [[version5-graded-correspondence-superconnection-gate]]
проверил эту ветвь в точном конечномерном виде. Теория неограниченных
соответствий действительно допускает модуль с собственной связностью и
оператором, а калибровочная теория факторизованной спектральной геометрии
разделяет связности и эндоморфизмы модуля. Но стандартный квадрат нечётного
эндоморфизма даёт `XX*+Y*Y`, а односторонняя кривизна `d^2` --- составной
путь `YX`. Поэтому проектная разность `XX*-Y*Y` остаётся эрмитовым
отображением момента, то есть дополнительным гамильтоновым обогащением.
Калибровка всех эндоморфизмов кратностного модуля создаёт большую новую
группу; при сохранении только группы Стандартной модели вращательные нули
не являются БРСТ-точными. Старый тетраэдрический тензор теперь становится
приоритетным дискретным механизмом их снятия.

Обратный аудит [[version5-commuting-square-readout-gate]] затем обнаружил,
что пространство полей было задано слишком широко. Теория условных
ожиданий и коммутирующих квадратов естественно описывает несколько
согласованных подалгебр одного операторного носителя. На проектном носителе
`H20 tensor H15` канонические частичные следы образуют такой квадрат, а
`S4/A4`-эквивариантность оставляет только `X=rho V` и `Y=Phi I3`.
Следовательно, три семейных вращательных нуля не нужно динамически снимать:
они отсутствуют в исходном эквивариантном пространстве полей. Литературная
роль здесь ограничена языком условных ожиданий; размерности, ортогональность
кривизн и восстановление старого препятствия являются внутренними
результатами проекта.

Перекрёстный аудит
[[version5-relative-bimodule-curvature-cross-audit-2026-08-16]] отделил
ещё не проверенную конструкцию от двух уже закрытых родственников.
Отображающий конус действует на обычную чётную кривизну и в семейной цепи
оставляет только крайний составной путь. Обычный фактор форм Конна удаляет
матричный средний блок. Иная литературная конструкция — двусторонняя
связность на бимодуле и кривизна дифференцируемого гильбертова модуля
относительно спектральной тройки. Она допускается как следующий гейт только
при явных левом и правом правилах Лейбница, отсутствии нового переставления
или веса и совместимости с уже построенным коммутирующим квадратом.

Гейт [[version5-state-corner-curvature-readout-gate]] затем использовал
более ранний внутренний словарь производных мер. Компрессия в существенный
угол `A -> rho A rho` является вполне положительной угловой картой; для
эквивариантной кривизны `mu I3` она даёт `mu rho`. Нормированный след угла
сохраняет `mu^2`, а полный след даёт фиксированную ранговую кратность
`1/3`. Поэтому двусторонняя связность больше не нужна для переноса этой
скалярной кривизны и остаётся только задачей динамики внедиагонального
модуля.

Гейт [[version5-morita-linking-parent-gate]] реализовал эту оставшуюся
задачу на уровне родительского контейнера. Равенство
`C300=M20x15(C)` превращает общий носитель в стандартный бимодуль Мориты, а
его связывающая алгебра равна `M35(C)`. Блочное умножение фиксирует правое
правило связности и кривизну `R(xi)=F_F xi-xi F_O` без независимого
переставления. При этом `M35` не объявляется физической координатной
алгеброй: калибровка всего контейнера дала бы запрещённую `U(35)`.

Классификация
[[version5-physical-corner-connection-classification-gate]] проверила, даёт
ли физическое ограничение углов операторную теорему для юкавских связей.
Для полного `M20-M15`-бимодуля неоднозначность связности скалярна, но после
ограничения наблюдаемого угла до блоков `6+2+3+3+1` коммутант имеет
комплексную размерность пять. Точная алгебра Стандартной модели является
подалгеброй этого блочного чтения, поэтому её коммутант не меньше. Это
совпадает с литературным статусом конечного оператора Дирака: геометрия
задаёт допустимую структуру юкавских блоков, но их значения входят как
данные оператора.

Последний динамический тест
[[version5-centered-connection-potential-gate]] использовал стандартный
инвариантный подход к пространству орбит и квадратам отображения момента.
Пять физически различимых блоков дают пять независимых квадратичных
инвариантов и пятнадцать квартичных произведений. Ограничение только одним
следом не восстанавливает единственность: положительная норма выбирает
нулевую связность, радиальный потенциал имеет семь нулевых мод, а
выравнивающий функционал --- три. Ненулевой центральный уровень
отображения момента сам содержит четыре относительных параметра.

Обратный аудит
[[version5-connection-calculus-reopening-audit-2026-08-16]] выявил
существенное ограничение этой классификации. В теории связностей разность
двух связностей является модульным отображением со значениями в одноформах,
а не просто эндоморфизмом исходного модуля. Литература по неограниченному
произведению Каспарова также разделяет связностную и эндоморфную части
внутренней флуктуации. Поэтому коммутант `C^5` классифицирует
нуль-форменный сектор, но не полный физический модуль связностей.

Новая работа о спектральном кручении внутренней геометрии Стандартной
модели, `arXiv:2511.08159`, усиливает этот вывод: первая и вторая
степени дифференциального исчисления несут разную информацию, обычные
одноформы слепы к части конечного оператора, а модификация второй степени
восстанавливает нетривиальный функционал кручения. Работа не выводит
юкавские матрицы, поскольку принимает их как вход, но даёт актуальный
аппарат для следующего проектного теста.

Гейт [[version5-h15-physical-oneform-bimodule-gate]] применяет это
различение к заряженному пакету `H15`. Общая теория проективных модулей
гарантирует существование грассмановой связности, но не её единственность:
пространство связностей аффинно над одноформенными модульными картами.
Конечная спектральная геометрия Стандартной модели фиксирует допустимые
блоки, тогда как коэффициенты Юкавы входят в конечный оператор Дирака.
Проектный результат состоит в более узком утверждении: после правильной
типизации три неэквивалентных ребра дают диагональный коммутант `C^3` и две
относительные вещественные свободы после удаления общего направления.

[[version5-h15-spectral-torsion-selector-gate]] проверяет последнюю
возможность внутреннего выбора. Ограничение формул спектрального кручения на
`H15` содержит как собственные, так и смешанный `u-d` инвариант и потому
имеет полный ранг по двум относительным юкавским координатам. Но работа
`arXiv:2511.08159` решает обратную задачу: для уже заданного конечного
оператора Дирака подбираются алгебраические данные, воспроизводящие
спектральный функционал. Обычное исчисление совпадения не даёт, а успешная
модификация использует дополнительный неэрмитов идемпотент второй степени.
Поэтому уникальность восстановительной связности нельзя переносить на
уникальность исходных коэффициентов Юкавы.

## Дефектный перенос и дираковский предел

[[version5-defect-transport-reframing-gate]] использует литературу не как
подтверждение буквальной модели вакуума, а для фиксации четырёх отдельных
математических мостов.

Геометрическая теория дефектов описывает дислокации кручением
римановой--картановой геометрии, а дисклинации --- кривизной
(`arXiv:cond-mat/0407469`, `arXiv:0909.4068`). Этот результат оправдывает
проверку словаря «дефект --- кручение --- голономия», но не позволяет
отождествить спектральное кручение конечной геометрии с механическим
кручением среды без явной карты между исчислениями.

Локальные однородные унитарные квантовые блуждания и клеточные автоматы
могут иметь уравнение Дирака в непрерывном пределе (`arXiv:1307.3524`,
`arXiv:1212.2839`). Поэтому проектный оператор переноса должен проверяться
по унитарности, локальности, общему предельному световому конусу и
дираковскому разложению, а не по одному сходству решёточной картины.

Индексные теоремы связывают топологический класс вихря или линейного
дефекта с устойчивой майорановской нулевой модой (`arXiv:0911.2558`,
`arXiv:1003.4814`). Это поддерживает уже условный проектный результат о
дефектном ядре, но не выводит спаривающий конденсат и не доказывает
нейтринную интерпретацию.

Квантовые блуждания способны моделировать стандартные нейтринные
осцилляции (`arXiv:1607.00529`). Для проекта это только проверка
достаточности языка переноса: физическим выводом результат станет лишь при
независимом происхождении внутренних каналов, фаз и щелей.

[[version5-local-defect-transfer-operator-gate]] выполнил этот тест в
минимальной одномерной модели. Получен тот же класс однородной причинной
унитарной эволюции, который используется в литературе для дираковского
предела. Проектное добавление состоит в бимодульной классификации:
ковариантный перенос скалярен на полном `M20x15(C)`, поэтому внутренняя
матрица размерности 300 не создаёт свободных амплитуд. Однако
ориентационный дублет оставляет один массовый модуль `m`, как и в известном
клеточно-автоматном построении. Таким образом, литература подтверждает
дисперсию и предел, но не предоставляет отсутствующий механизм выбора
массы.

Следующий
[[version5-rank-one-tetrahedral-transfer-reflection-gate]] отделил
голономную фазу от массовой поляризации. Это согласуется с литературой по
хиральным квантовым блужданиям (`arXiv:1303.1199`, `arXiv:1502.02592`), где
оператор хиральной симметрии является дополнительной структурой шага, а не
следует из одного спектра фаз. В проектной геометрии поперечная комплексная
структура и фаза `2pi/3` каноничны, но отражения образуют трёхциклическую
орбиту без выделенного элемента. Поэтому семейная голономия сохраняется
как граничная фаза, но исключается как самостоятельный источник массы.

[[version5-massless-holonomy-defect-index-gate]] затем использовал
стандартный спектральный факт для оператора Дирака с плоским скручиванием:
фазы голономии сдвигают целочисленные импульсы. Для `C3` получены ветви
`0,±1/3` и одна инвариантная нулевая мода. Сверка с теорией спектров
плоско скрученных операторов (`arXiv:math/0312004`) подтверждает форму
спектра, но проект отдельно фиксирует важную границу: граничное ядро имеет
нулевой Fredholm-индекс и не является локализованной дефектной модой.

## Научный язык первичных переходов

[[version5-transition-primitive-scientific-language-gate]] объединяет пять
существующих инструментов, не объявляя ни один из них готовой теорией
материи.

- Гильбертовы `C*`-бимодули образуют стрелки между алгебрами и составляются
  внутренним тензорным произведением (`arXiv:math-ph/0506024`). Это точно
  совпадает с проектным соответствием `M20x15(C)`.
- Категориальная квантовая механика трактует системы как объекты, процессы
  как морфизмы и предоставляет диаграммную композиционную грамматику
  (`arXiv:quant-ph/0402130`). Она не выбирает конкретную динамику.
- Группоидные алгебры являются алгебрами путей и переходов; их связь с
  матричной механикой и голономной некоммутативной геометрией изложена в
  `arXiv:math/0601054`.
- Обратимые квантовые клеточные автоматы строят глобальный дискретный шаг
  из локальных унитарных правил с конечной скоростью распространения
  (`arXiv:quant-ph/0405174`).
- Индекс квантовых блужданий и автоматов измеряет чистый поток квантовой
  информации и классифицирует компоненты локально обратимой динамики
  (`arXiv:0910.3675`).
- Последовательный рост причинных множеств является отдельным языком
  первичности событий (`arXiv:gr-qc/9904062`), но отложен до прохождения
  более дешёвого нелинейного теста на уже построенном носителе Мориты.

Проектная новизна здесь не в этих известных инструментах, а в проверяемой
связке: переходный бимодуль, локальный унитарный шаг, четырёхтактные
характеры и индексный дефект должны быть выведены из одного правила без
ручного профиля массы.

## Нелинейное самопорождение дефекта

[[version5-self-generated-transition-defect-gate]] проверяет следующий
слой после выбора языка.

- Самосогласованные неоднородные конденсаты и кинковые кристаллы существуют
  в моделях Гросса--Невё (`arXiv:0806.2659`).
- Знакопеременный дираковский массовый фон локализует нулевую моду по
  механизму Джакива--Ребби (DOI `10.1103/PhysRevD.13.3398`).
- Нелинейные квантовые блуждания имеют контролируемый непрерывный предел в
  виде нелинейного уравнения Дирака (`arXiv:1902.02017`).
- Локально взаимодействующие фермионные клеточные автоматы способны иметь
  связанные состояния (`arXiv:2304.14687`).

Проектный тест не объявляет эти механизмы новыми. Он впервые выводит
профиль из предъявленного локального функционала и затем проверяет его на
полном носителе Мориты, где возникает новая внутренняя кратность `300`.

## Голономно-хиггсовское сокращение кратности

[[version5-holonomy-projector-defect-multiplicity-gate]] сопоставляет
проектный голономный проектор с известной структурой оператора Вайнберга.
Сам оператор размерности пять содержит два лептонных и два хиггсовских
дублета (DOI `10.1103/PhysRevLett.43.1566`); в 15-состоянийной
почти коммутативной геометрии хиггс-квадратичный майорановский член может
возникать на следующем порядке фермионного спектрального действия
(`arXiv:1903.09149`).

Проектное уточнение состоит в ранговом журнале. Голономия фиксирует
семейную линию, но постоянный проектор на нейтрино внутри слабого дублета
запрещён коммутантом `M2(C)`. Ненулевое поле Хиггса даёт ковариантное
направление ранга один. Поэтому одиночная линия принадлежит совместному
голономно-хиггсовскому чтению, а не одной топологии.

## Точечные дефекты и спинорный подъём

[[version5-projective-hedgehog-point-defect-gate]] переносит проверку из
одного пространственного измерения в три.

- Классификация пространственно меняющихся гамильтонианов связывает
  топологию точечных дефектов с защищёнными нулевыми модами
  (`arXiv:1006.0690`).
- Индекс Каллиаса определяется классами Черна собственных расслоений
  асимптотической массовой матрицы (`arXiv:hep-th/0011081`,
  `arXiv:hep-th/0311215`).
- Глобальный монопольный ёж имеет расходящуюся дальнюю энергию, тогда как
  калибровочное поле способно экранировать угловой градиент
  (`arXiv:gr-qc/0307074`).
- Минимальное электрослабое вакуумное пространство имеет тип `S3` и не
  содержит топологически устойчивой монопольной `pi2`
  (`arXiv:1610.05623`).

Проектный результат различает два представления одного ежа: масса
`3P-I3` имеет нулевой класс Черна, а спинорная масса `n.sigma` — единичный.
Следовательно, точечная топология проекторной оси должна быть дополнена
ориентированным двойным подъёмом.

## Primary anchors

- Chamseddine--Connes, `arXiv:hep-th/9606001`.
- van Suijlekom, `arXiv:1104.5199`.
- Moriya, `arXiv:2002.04253`.
- Juhl, `arXiv:1411.7851`.
- Anninos et al., `arXiv:2505.11330`.
- Chamseddine--Connes--van Suijlekom, `arXiv:1304.8050`, `1507.08161`.
- Karimi Khozani, `arXiv:1905.04533`.
- Berger--Grossman, `arXiv:0910.4392`.
- Seidl, `arXiv:0811.3775`.
- Hosotani, `arXiv:hep-ph/0504272`.
- Abe et al., `arXiv:2607.12366`.
- Teo--Kane, `arXiv:1006.0690`.
- Monin et al., `arXiv:1611.02912`.
- Hanisch et al., `arXiv:0911.5074`.
- Mesland, `arXiv:0904.4383`, `1304.3802`.
- Deeley--Goffeng--Mesland, `arXiv:1607.07143`.
- Cattaneo--Mnev--Reshetikhin/BV-BFV introduction, `arXiv:1905.08047`.
- Ludewig, `arXiv:1909.04212`.
- Rennie--Várilly, `arXiv:math/0610418`.
- Ćaćić, `arXiv:1101.5908`.
- Gordon--Szabó, `arXiv:math/0003007`.
- Redlich et al., fixed-charge group projection, `arXiv:hep-ph/0302245`.
- Cattaneo--Mnev--Wernli, BV--BFV cylinders, `arXiv:2012.13983`.
- Dai--Freed, boundary eta invariants and determinant lines,
  `arXiv:hep-th/9405012`.
- Krajewski, finite spectral-triple diagrams and blockwise first order,
  `arXiv:hep-th/9701081`.
- Masson--Nieuviarts, graph formulation of finite spectral triples,
  `arXiv:2207.04466`.
- Chindris, quiver moment maps and symplectic/GIT quotients,
  `arXiv:0807.4734`.
- Andreae, McKean--Singer formula and index-theoretic supertraces,
  `arXiv:2307.11061`.
- Devastato--Martinetti, twisted spectral triples and linked scalar/vector
  fluctuations, `arXiv:1411.1320`.
- D'Alesio, noncommutative derived Poisson reduction,
  `arXiv:2012.04451`.
- D'Alesio, derived representation schemes and Nakajima varieties,
  `arXiv:2006.09282`.
- Bozec et al., derived/preprojective quiver geometry,
  `arXiv:2102.12336`.
- Anel--Calaque, shifted symplectic reduction of derived critical loci,
  `arXiv:2106.06625`.
- Cattaneo--Moshayedi, BV--BFV formalism, `arXiv:1905.08047`.
- Crawley-Boevey--Etingof--Ginzburg, noncommutative geometry and quiver
  moment maps, `arXiv:math/0502301`.
- Dubois-Violette--Madore--Masson--Mourad, bimodule connections and
  curvature, `arXiv:q-alg/9512004`.
- Beggs, Dirac operators from bimodule connections, `arXiv:1508.04808`.
- Ballandras, norm-square moment maps and central levels,
  `arXiv:2010.08294`.
- Bürgisser et al., invariant theory for torus actions,
  `arXiv:2102.07727`.
- Marcolli--Pierpaoli, finite Dirac parameters in spectral cosmology,
  `arXiv:1101.2174`.
- Brain--Mesland--van Suijlekom, gauge theory and the unbounded Kasparov
  product, `arXiv:1306.1951`.
- Aschieri et al., affine spaces of noncommutative connections,
  `arXiv:2006.02761`.
- Brain--Majid, Grassmann connections on projective modules,
  `arXiv:math/0701893`.
- Mesland--Rennie, existence and uniqueness of Hermitian torsion-free
  bimodule connections, `arXiv:2403.13735`.
- Dąbrowski--Mukhopadhyay--Požar, spectral torsion of the internal
  Standard-Model geometry, `arXiv:2511.08159`.
- Mesland--Rennie--van Suijlekom, curvature of differentiable Hilbert
  modules, `arXiv:1911.05008`.
- Beggs--Blake, noncommutative fibre bundles via bimodules,
  `arXiv:2302.00489`.
- Katanaev, geometric theory of dislocations and disclinations,
  `arXiv:cond-mat/0407469`.
- de Juan--Cortijo--Vozmediano, dislocations and torsion,
  `arXiv:0909.4068`.
- Arrighi--Forets--Nesme, Dirac equation as a local quantum walk,
  `arXiv:1307.3524`.
- Bisio--D'Ariano--Tosini, emergent Dirac evolution from a quantum cellular
  automaton, `arXiv:1212.2839`.
- Fukui--Fujiwara, index theorems for Majorana modes on defects,
  `arXiv:0911.2558`, `arXiv:1003.4814`.
- Di Molfetta--Pérez, quantum-walk simulation of neutrino oscillations,
  `arXiv:1607.00529`.

## Links

- [[version5-project-literature-novelty-gate]] — project-wide verdict.
- [[version5-ordinary-spectral-moment-map-no-go-gate]] — exact boundary
  between ordinary spectral data and oriented moment-map data.
- [[version5-nonordinary-architecture-fork-gate]] — post-no-go architecture
  comparison and frozen height--Hodge kill-test.
- [[version5-oriented-height-hodge-ko6-gate]] — exact two-height
  counterexample closing orientation derivation from the current KO6 data.
- [[version5-twisted-family-automorphism-gate]] — closes canonical twists of
  the current algebra and reduces reopening to three selective duplications.
- [[version5-minimal-twist-doubling-budget-gate]] — selects the real-scalar
  flip as the cheapest four-summand representation test.
- [[version5-real-scalar-flip-twisted-ko6-gate]] — real twisted geometry
  passes, while its ordinary spectral action retains the wrong mixed sign.
- [[version5-flip-twisted-trace-positivity-gate]] — closes faithful positive
  rho-trace and finite modular rescues of the real central flip.
- [[version5-derived-moment-map-minimal-data-gate]] — separates the exact
  preprojective identity from the missing positive star-polarization and
  physical real-form origin.
- [[version5-parent-architecture-status-freeze-gate]] — applies the original
  early-stop rule and freezes the complete Version V architecture ledger.
- [[version5-m300-coordinate-algebra-wellposedness-gate]] — separates the
  full trace carrier from the missing coordinate algebra and bimodule data.
- [[version5-affine-ko6-reference-corner-gate]] — восстанавливает
  аффинный KO6-бимодуль и выделяет коммутантное размещение семейной цепи.
- [[version5-problem-statement-gate]] — Tome V problem statement.
- [[version5-defect-transport-reframing-gate]] — переход от статического
  выбора к проверке локального переноса дефектного класса.
- [[version5-open-paths-assessment-2026-08-15]] — surviving route ranking.
- [[external-literature-spectral-determinants]] — earlier determinant literature gate.
- [[version4-pati-salam-literature-reaudit]] — corrected Pati--Salam scenario ledger.

## Source Notes

- `s2t/gates/version5_project_literature_novelty_gate.tex`
- Internal corpus search: `wiki/`, `s2t/gates/`, `s2t/docs/`.
- External targeted search performed 2026-08-15 against primary arXiv and
  journal records.