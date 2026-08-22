# Спектральный примитив перехода и локальная квантовая динамика

> Status: working
> Type: source
> Updated: 2026-08-21

## Summary

Первичная литература предоставляет строгий язык для новой выбранной
парадигмы: соответствия Мориты описывают типизированные переходы между
алгебрами, операторные расширения создают конечранговые boundary-дефекты,
а локальные квантовые блуждания имеют дираковский непрерывный предел.

## Key Points

- Сильная эквивалентность Мориты позволяет считать бимодуль первичным
  носителем перехода между двумя операторными углами.
- Двусторонний сдвиг и оператор числа создают тёплицеву поляризацию и
  компактный дефект одностороннего сдвига.
- Индекс устойчив к компактным деформациям, но целый класс `15` не
  является автоматически примитивным: вопрос неделимости требует полной
  эквивариантной категории.
- Конечный граф спектральной тройки делает отсутствие ребра физическим
  условием: три заряженных ребра `u,d,e` связывают блоки `H15` только в
  компоненты рангов `12` и `3`.
- Неограниченная картина `KK`-теории позволяет ограничить оператор числа
  и сдвиг на конечнократные редуцирующие подпространства; Real-удвоение
  классифицируется средствами `KR/KO`-теории.
- Обратимое локальное правило шага может давать общий световой конус и
  дираковскую дисперсию без фундаментальной непрерывной верёвки.
- В конечной спектральной геометрии вершины конечной диаграммы задают
  мультиплеты, а рёбра — юкавские связи. Поэтому отсутствие `nu_R` в
  `H15` является отсутствием степени-один нейтринного ребра, а не
  малым значением его коэффициента.
- Без `nu_R` регулярная нейтринная ветвь естественно имеет высшую
  степень: квадратичный хиггсовский ковариант задаёт направление, а
  оператор Вайнберга использует две лептонные и две хиггсовские ноги.

## Значение для проекта

После отрицательного теста исключённого объёма проект не обязан вводить
новую микроскопическую струну. Его собственный строгий остаток уже имеет
вид

`локальный переход -> композиция -> голономия/индекс -> конечранговый дефект`.

Первый тест минимальной опоры уже дал ответ: полный контрольный угол
`M15(C)` неприводим, но физический gauge- и дираковский граф имеет две
связные компоненты. Поэтому ранг `15` является пакетом поколения, а не
неделимым атомом.

Компонентный гейт усилил вывод: ранги `12` и `3` имеют собственные
граничные и неограниченные циклы. Однако аддитивность K-класса и следового
действия не является энергией связывания и не принуждает общий
пространственный центр.

Аудит колокализации сопоставил эту границу с теоремой Каллиаса и
механизмом Jackiw--Rebbi. Один общий профиль массы действительно мог бы
локализовать несколько коэффициентных мод на одном солитоне, но проект не
выводит требуемый spin-cover-носитель. Поэтому литературный механизм
доступен условно, а не реализован родителем.

Хиггс-разрешённый аудит затем дал точное разложение
`15=6_up+6_down+2_e+1_nu`. Нормированная нейтринная линия существует
только при `H!=0`: в симметричной точке нет инвариантного проектора
ранга один. Зато ненормированный ковариант
`tilde(H)tilde(H)^dagger` регулярным образом обращается в ноль. Это
прямо поддерживает язык спектрального перехода с меняющимся рангом, а
не фундаментальной непрерывной нити.

Ретроспективный аудит паринга сопоставил этот носитель с фермионным
спектральным действием Sakellariadou--Sitarz. Литература подтверждает
допустимость хиггс-квадратичного майорановского члена без правого
нейтрино, но сама конструкция требует нескалярной части спектральной
функции. Проектное контрсемейство показало, что её чётный коэффициент не
следует из нечётной кинетической нормировки. Поэтому литература
подтверждает операторный тип, но не параметрически чистую амплитуду.

Локализационный аудит сопоставил радиальный квадрат `M300` с механизмами
конденсата в сердцевине струн. Работы Witten, Achucarro--Vachaspati и
Forgacs--Lukacs подтверждают общий критерий: второе поле меняет фазу в
ядре лишь при наличии смешанного взаимодействия требуемого знака и
достаточной силы. В текущем проекте радиальный член имеет противоположный
эффект: он повышает минимум `|H|^2`, а портал формы имеет нулевой
коэффициент.

Классификация прямого коннектора использовала диаграммный принцип
Краевского и бимодульную формулировку Paschke--Sitarz: физическая стрелка
определяется представлениями координатной алгебры и оператором Дирака, а
не одной принадлежностью окружающей полной матричной алгебре. Это
подтвердило нулевые прямые интертвинеры семейных полей с Хиггсом и
сохранило только непрямой кандидат в модуле составных одноформ.

Двухшаговый аудит затем применил стандартное градуированное произведение
нечётных операторов, суперсвязности Quillen и представленный junk-фактор.
Градуировка сокращает смешанный оператор, а обычный фактор форм удаляет
бесследовую семейную двухформу. Литературный аппарат тем самым не
восстанавливает портал, а объясняет структурную причину его отсутствия.

Последующее архитектурное решение остановило поиск ещё одного скрытого
коннектора в той же конечной геометрии. Бозонный вихрь и спектральный
конечранговый дефект сохраняются как самостоятельные строгие сектора.
Следующая литературная граница относится к гомотопической классификации
дефектов вакуумного многообразия одного хиггсовского дублета: требуется
отделить локальный нуль поля от топологически защищённого дефекта.

Топологический аудит выполнил это разделение. Для стандартной глобальной
формы электрослабого действия вакуум одного комплексного дублета равен
`S3`, поэтому `pi0=pi1=pi2=0`. Вложенные электрослабые струны и
монопольные конфигурации могут существовать динамически, но нуль Хиггса не
принуждается топологией. Ненулевая `pi3` описывает текстуру, которая может
оставаться на вакуумной сфере и потому не создаёт смены ранга
`W_nu:0→1`.

Динамический аудит затем разделил чистый Хиггс и полный gauge--Higgs
сектор. Канонический скалярный функционал в трёх измерениях не допускает
статического комка по тождеству Деррика. Gauge-кривизна добавляет
масштабирующийся как `R^-1` член и разрешает электрослабый сфалерон с
локальным `H=0`. Но известная отрицательная мода делает его событием
перехода между вакуумами. Это направляет спектральную программу к
фермионному потоку, а не к идентификации сфалерона как частицы.

Аудит спектрального потока подтвердил физическую схему перехода через
нулевую моду, но закрыл прямое числовое отождествление с классом `15`.
При `Delta N_CS=1` один левый слабый дублет даёт одно пересечение;
поэтому одно поколение имеет поток `3+1=4`, три поколения — `12`, а
аномальные заряды удовлетворяют `Delta B=Delta L=1` на поколение.
Проектный ранг `15=12+3` имеет иной носитель: он включает полные левые и
правые блоки одного поколения. Для связи нужен явный операторный внешний
продукт, а не совпадение целых чисел.

Product-map аудит проверил эту возможность в кольце слабых
представлений. Один и тот же `H15` равен `4[doublet]+7[singlet]`.
Забывающая карта размерности даёт `15`, тогда как физическое индексное
спаривание даёт `4`, поскольку синглеты не имеют слабого сфалеронного
потока. Формальный Kasparov-product с забытым проектором ранга `15`
математически даёт `15`, но использует этот ранг как вход и не сохраняет
gauge-представления. Эквивариантный продукт возвращает физическое число
`4`; прямой anomaly--Toeplitz мост закрыт.

Архитектурная развилка после этого отрицательного результата отделила
классификацию от динамики. Класс `15` сохранён как KO6/Toeplitz-ledger
полного однопоколенного пакета и сумма компонентных классов `12+3`.
Одновременно сняты недоказанные чтения как числа частиц, единого
связанного солитона и multiplicity сфалеронного рождения. Переход,
действующий также на правые слабые синглеты, требует нового оператора и
не может считаться скрытой частью стандартного сфалерона.

Компонентный observable-аудит затем разделил точные selection rules и
динамические вероятности. K-ранги имеют отношение `4:1`, физический
сфалеронный поток — `3:1`, а зарядовое правило — `1:1`; нормированные
кандидаты попарно различны. Литературные расчёты сфалеронной скорости
также требуют температуры, барьерной энергии, real-time динамики и
prefactor. Поэтому веса `4/35` и `1/35` нельзя интерпретировать как
branching fractions текущего проекта.

Итоговый status-аудит разделил семь уровней замыкания. KO6/Toeplitz-
классификация и локальная кинематика смены ранга закрыты; сфалерон и
selection rules дают контроль, но не проектную динамику. Не выведены
эндогенный trigger, мера и скорость, а также устойчивый endpoint.

Для следующей модели литература о распаде ложного вакуума фиксирует
минимальную динамическую дисциплину: седло и экспонента должны следовать
из одного действия, а квантовый prefactor требует отдельного определения.
Поэтому контракт `R0--R6` запрещает заменять скорость индексом или
топологическим весом и требует устойчивого конечного решения.

## Links

- [[transition-primitive]]
- [[version5-transition-primitive-scientific-language-gate]]
- [[version5-real-toeplitz-unbounded-parent-cycle-gate]]
- [[version5-one-seventh-toeplitz-boundary-map-gate]]
- [[version5-local-defect-transfer-operator-gate]]
- [[version6-single-thread-scale-hierarchy-branch-decision-gate]]
- [[version6-spectral-transition-minimal-support-gate]]
- [[version6-spectral-transition-component-boundary-gate]]
- [[version6-spectral-transition-component-colocalization-gate]]
- [[version6-spectral-transition-higgs-resolved-support-gate]]
- [[version6-spectral-transition-neutrino-line-parent-gate]]
- [[version6-spectral-transition-weinberg-pairing-parent-gate]]
- [[version6-spectral-transition-rank-change-localization-gate]]
- [[version6-spectral-transition-radial-bridge-vortex-connector-gate]]
- [[version6-spectral-transition-morita-two-step-connector-gate]]
- [[version6-spectral-transition-connector-architecture-branch-decision-gate]]
- [[version6-spectral-transition-higgs-vacuum-topology-localization-gate]]
- [[version6-spectral-transition-higgs-zero-finite-energy-saddle-gate]]
- [[version6-spectral-transition-sphaleron-spectral-flow-gate]]
- [[version6-spectral-transition-anomaly-to-toeplitz-product-map-gate]]
- [[version6-spectral-transition-class15-physical-role-branch-decision-gate]]
- [[version6-spectral-transition-componentwise-creation-observable-gate]]
- [[version6-spectral-transition-dynamic-closure-status-gate]]
- [[version6-spectral-transition-new-model-minimal-requirements-gate]]
- [[version6-spectral-transition-new-model-candidate-menu-gate]]
- [[version6-spectral-transition-candidate-menu-retrospective-correction-gate]]
- [[version6-spectral-transition-discrete-nonlinear-parent-reopening-gate]]
- [[version6-spectral-transition-discrete-equivariant-coin-selector-gate]]
- [[version6-spectral-transition-discrete-chiral-coin-closure-gate]]
- [[version6-spectral-transition-discrete-composite-higgs-spatial-binding-gate]]
- [[version6-spectral-transition-discrete-compacton-existence-gate]]
- [[version6-spectral-transition-discrete-compacton-stability-quantization-gate]]
- [[version6-spectral-transition-discrete-compacton-physical-scale-map-gate]]
- [[version6-spectral-transition-discrete-compacton-dynamical-capture-gate]]
- [[dynamical-dirac-soliton-candidate-literature-2026]]
- [[nonlinear-quantum-walk-discrete-dirac-literature-2026]]

## Source Notes

- L. G. Brown, P. Green, M. A. Rieffel, *Stable Isomorphism and Strong
  Morita Equivalence of C*-Algebras*, Pacific Journal of Mathematics 71
  (1977), 349--363.
- M. Pimsner, D. Voiculescu, *Exact Sequences for K-Groups and Ext-Groups
  of Certain Cross-Product C*-Algebras*, Journal of Operator Theory 4
  (1980), 93--118.
- A. Bisio, G. M. D'Ariano, A. Tosini, *Quantum Field as a Quantum
  Cellular Automaton: the Dirac Free Evolution in One Dimension*,
  arXiv:1212.2839.
- P. Arrighi, M. Forets, V. Nesme, *The Dirac Equation as a Quantum Walk:
  Higher Dimensions, Observational Convergence*, arXiv:1307.3524.
- T. Krajewski, *Classification of Finite Spectral Triples*, Journal of
  Geometry and Physics 28 (1998), 1--30; arXiv:hep-th/9701081.
- A. H. Chamseddine, A. Connes, M. Marcolli, *Gravity and the Standard
  Model with Neutrino Mixing*, Advances in Theoretical and Mathematical
  Physics 11 (2007), 991--1089; arXiv:hep-th/0610241.
- M. F. Atiyah, *K-Theory and Reality*, Quarterly Journal of Mathematics
  17 (1966), 367--386.
- S. Baaj, P. Julg, *Théorie bivariante de Kasparov et opérateurs non
  bornés dans les modules hilbertiens*, Comptes Rendus de l'Académie des
  Sciences de Paris, Série I 296 (1983), 875--878.
- R. Jackiw, C. Rebbi, *Solitons with Fermion Number 1/2*, Physical
  Review D 13 (1976), 3398--3409.
- C. Callias, *Axial Anomalies and Index Theorems on Open Spaces*,
  Communications in Mathematical Physics 62 (1978), 213--234.
- S. Weinberg, *Baryon- and Lepton-Nonconserving Processes*, Physical
  Review Letters 43 (1979), 1566--1570.
- M. Sakellariadou, A. Sitarz, *Fermionic Spectral Action and the Origin
  of Nonzero Neutrino Masses*, Physics Letters B 795 (2019), 351--355;
  arXiv:1903.09149.
- E. Witten, *Superconducting Strings*, Nuclear Physics B 249 (1985),
  557--592.
- A. Achucarro, T. Vachaspati, *Semilocal and Electroweak Strings*,
  Physics Reports 327 (2000), 347--426; arXiv:hep-ph/9904229.
- G. H. Derrick, *Comments on Nonlinear Wave Equations as Models for
  Elementary Particles*, Journal of Mathematical Physics 5 (1964),
  1252--1254.
- F. R. Klinkhamer, N. S. Manton, *A Saddle-Point Solution in the
  Weinberg--Salam Theory*, Physical Review D 30 (1984), 2212--2220.
- F. R. Klinkhamer, C. Rupp, *Sphalerons, Spectral Flow, and Anomalies*,
  Journal of Mathematical Physics 44 (2003), 3619--3639;
  arXiv:hep-th/0304167.
- F. R. Klinkhamer, Y. J. Lee, *Spectral Flow of Chiral Fermions in
  Nondissipative Yang--Mills Gauge Field Backgrounds*, Physical Review D
  64 (2001), 065024; arXiv:hep-th/0104096.
- G. 't Hooft, *Computation of the Quantum Effects Due to a
  Four-Dimensional Pseudoparticle*, Physical Review D 14 (1976),
  3432--3450.
- M. F. Atiyah, I. M. Singer, *The Index of Elliptic Operators: I*,
  Annals of Mathematics 87 (1968), 484--530.
- G. G. Kasparov, *The Operator K-Functor and Extensions of
  C*-Algebras*, Mathematics of the USSR-Izvestiya 16 (1981), 513--572.
- G. D. Moore, *Measuring the Broken Phase Sphaleron Rate
  Nonperturbatively*, Physical Review D 59 (1999), 014503;
  arXiv:hep-ph/9805264.
- M. Barroso Mancha, G. D. Moore, *The Sphaleron Rate from 4D Euclidean
  Lattices*, Journal of High Energy Physics 01 (2023), 155;
  arXiv:2210.05507.
- P. Forgacs, A. Lukacs, *Stabilization of Semilocal Strings by Dark
  Scalar Condensates*, Physical Review D 95 (2017), 035003;
  arXiv:1612.03151.
- M. Paschke, A. Sitarz, *Discrete Spectral Triples and Their
  Symmetries*, Journal of Mathematical Physics 39 (1998), 6191--6205;
  arXiv:q-alg/9612029.
- D. Kucerovsky, *The KK-Product of Unbounded Modules*, K-Theory 11
  (1997), 17--34.
- D. Quillen, *Superconnections and the Chern Character*, Topology 24
  (1985), 89--95.
- B. Gripaios, O. Randal-Williams, *Topology of the Electroweak Vacua*,
  Physics Letters B 770 (2017), 309--313; arXiv:1610.05623.
- A. Achucarro, T. Vachaspati, *Semilocal and Electroweak Strings*,
  Physics Reports 327 (2000), 347--426; arXiv:hep-ph/9904229.