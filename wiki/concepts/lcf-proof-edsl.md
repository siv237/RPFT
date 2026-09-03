# LCF proof eDSL проекта S2T

> Status: working
> Type: concept
> Updated: 2026-09-01

## Summary

`s2t/proofdsl/` — малое pure-Python eDSL для точных конечномерных
утверждений проекта. Только доверенное ядро может создать значение
`Theorem`; неправильные размерности, композиции, представления и GKSL-
данные отвергаются до появления доказанного объекта.

## Problem

Существующие Python-аудиты сильны как вычислительные свидетели, но
используют массивы, численные допуски и локальные соглашения. Требовался
промежуточный уровень между аудитом и будущим Lean-проектом, на котором
нетипизированная склейка не может незаметно получить статус теоремы.

## Search for solution

- Создано закрытое LCF-подобное ядро `kernel.py`.
- Введены точные пространства, морфизмы, матричные и изотипические
  представления.
- SymPy допускается только без `Float` и проверяет точные равенства,
  ранги и интертвинеры.
- Конструктор Линдблада принимает только эндоморфизмы, эрмитов гамильтониан
  и доказуемо неотрицательные точные скорости.
- Z3 изолирован как необязательный источник solver evidence и пока не может
  создавать `Theorem`.
- Последний no-go Тома VIII перенесён на точное разложение неприводимых
  представлений.
- Первый гейт Version 9 зарегистрирован как десять kernel obligations:
  invariant logdet parent KMS-shapes имеет точные spectra Hessian,
  doubled rank `4` и общий rank/determinant `12/(5184/25)`.
- Второй гейт Version 9 сертифицирует algebraic core measure-origin:
  determinant degree `5+5`, fermionic/bosonic effective signs и
  несовпадение coordinate Jacobian с invariant determinant.
- Третий гейт Version 9 сертифицирует minimal auxiliary module: package
  ranks `5+5`, odd parity, family covariance, physical decoupling и
  rank `20` antisymmetric Berezin pairing.
- Четвёртый гейт Version 9 сертифицирует statistics-origin no-go:
  inherited grading candidates имеют odd ranks `2,5,5,8`, ближайший
  swap-covariant defect имеет rank `2`.
- Пятый гейт Version 9 сертифицирует minimal BRST complex:
  `Q²=0`, rank/nullity `20/20`, zero cohomology, FP rank `10` и
  physical decoupling.
- Шестой гейт Version 9 сертифицирует shift-origin no-go: required rank
  `10`, KMS tangent rank `6`, cokernel `4` и incompatibility positive
  auxiliary Hessian с full translations.
- Седьмой гейт Version 9 сертифицирует Stückelberg architecture:
  Hessian rank/nullity `10/10`, orbit-kernel equality, positive spectrum
  и determinant cancellation.
- Восьмой гейт Version 9 сертифицирует physical-loop no-go: target carrier
  rank `5`, determinant degrees `5/10`, Real exchange mismatch rank `10`,
  exact doubled и composite determinant identities.
- Девятый гейт Version 9 сертифицирует minimal fermion bath: carrier rank
  `10`, coupling rank `5`, exact Schur factorization, positive witness
  spectrum `{1^(5),3^(5)}` и determinant defect `781`.
- Десятый гейт Version 9 сертифицирует normalized Keldysh admission:
  causal damping/noise ranks `5/5`, witness determinant/target
  `32768/1024`, normalized ratio `1` и vacuum action `0`.
- Одиннадцатый гейт Version 9 сертифицирует spectral-density no-go:
  evaluation rank/nullity `3/4`, equal-rate positive profiles и exact
  moment defects `107/105`, `214/105`; registry `59/480`.
- Двенадцатый гейт Version 9 сертифицирует measure-anomaly no-go:
  paired Jacobian `1`, inherited/augmented ranks `3/4`, isotropic traces
  `6,0,0/10`; registry `60/492`.
- Тринадцатый гейт Version 9 сертифицирует minimal axiom admission:
  shape rank `4`, determinant `9lambda^4/25`, zero-axiom rank `0`;
  registry `61/503`.
- Четырнадцатый гейт Version 9 сертифицирует augmented closure:
  common Hessian rank/nullity `14/0`, determinant `5184/25`; registry
  `62/512`.
- Пятнадцатый гейт Version 9 сертифицирует blind predictions: contrast
  rank `2`, unit ratios/responses и zero variance; registry `63/521`.
- Шестнадцатый гейт Version 9 сертифицирует program status: conditional
  `6/6`, physical `3/6`, axiom-dependency rank `3`; registry `64/529`.
- Семнадцатый гейт Version 9 сертифицирует reopening criterion: deficit
  `(1,1,1)`, package-map rank `2`, conditional/physical coverage `3/3` и
  `0/3`; registry `65/538`.
- Восемнадцатый гейт Version 9 сертифицирует common-origin carrier:
  covariance dimension `10`, Hessian rank/determinant `6/36`, scale-orbit
  nullity `1`; registry `66/548`.
- Девятнадцатый гейт Version 9 сертифицирует Gaussian reference-state
  no-go: covariance-space `55`, Lyapunov rank/nullity `55/0`, coefficient
  orbit nullity `1`; registry `67/560`.
- Двадцатый гейт Version 9 сертифицирует reference-scale no-go: candidate
  matrix `8x5` rank `4`, pass `0/8`, relative-scale rank/nullity `7/1`;
  registry `68/572`.
- Двадцать первый гейт Version 9 сертифицирует финал Тома IX и контракт X:
  conditional/physical scores `6/6` и `3/6`, deficit rank `3`, Tome X
  dependency rank/determinant `6/1`; registry `69/585`.

## Expected result

Первый прототип должен отказывать на незаконных конструкциях и
воспроизводить хотя бы один реальный проектный no-go без численного допуска.

## Compliance check

- Тесты: `22 passed`.
- Точный пример: `dim Hom_G=13`, `max rank=9`.
- Попытка прямого создания `Theorem`: отвергается.
- Морфизм неправильной формы и несогласованная композиция: отвергаются.
- `Float` и отрицательная скорость Линдблада: отвергаются.
- След построенного GKSL-генератора: символически равен нулю.
- Z3 в Prism отсутствует; сетевой индекс пакетов закрыт ответом `403`,
  поэтому backend сохранён опциональным и не входит в успешную проверку MVP.
- `GateSpec` проверяет именованные обязательства, реестр и канонические
  JSON-сертификаты; второй перенос точно вывел спинодальный порог `21/2`.
- Третий перенос подтвердил неподвижную алгебру `C^2`, но уточнил, что
  одностороннее linking-условие оставляет размерность `4`; необходимы обе
  половины коммутанта самосопряжённого `D_A`.
- Четвёртый перенос проверил linking-GKSL на полных матричных базисах и
  точно восстановил `dim Fix=41`; полная положительность всё ещё использует
  доверенное правило GKSL, а не отдельный Choi proof-object.
- Пятый перенос заменил случайный gauge-аудит Kraus-моста точным замыканием
  12 jump-направлений под 12 генераторами gauge-алгебры. Линейных
  инвариантов нет, но центральная `C^2` сокращается до единицы символически
  при любых двух положительных скоростях.
- Шестой перенос доказал символически для всех неотрицательных весов, что
  parent-term сохраняет сигнатуры `(7,0,20)` и `(0,0,27)`. Одновременно
  точное равенство `z_a^2=0` в вакууме подтверждает древесный no-go
  ненулевой скорости.
- Седьмой перенос ввёл точные алгебраические поля: полярная коизометрия и
  cross-гессиан восстановлены в `Q(sqrt(2),2 cos(pi/7))`. Шесть пар равны
  точно, связь с остальными 15 модами нулевая, а общая ось независима от
  положительного `eta`.
- Восьмой перенос добавил типизированный `KrausChannel`: окно
  `0<=p<=1/6`, Kraus/Choi-ранг `13`, endpoint-инвариантность и минимальность
  среды проверены точно. Производная в нуле даёт GKSL-генератор, но конечное
  семейство не является полугруппой.
- Девятый перенос вычислил полный точный спектр cross-генератора и заменил
  collision scan конечномерным правилом Чернова. Безразмерная полугруппа
  доказана, а физическая скорость оставлена открытой.
- Десятый перенос заменил scan положительных весов точным правилом
  пересечения ядер форм Дирихле и доказал скалярную неподвижную алгебру
  полного 25-jump процесса.
- Одиннадцатый перенос доказал KMS-no-go: следовое состояние единственно,
  а направленное отношение скоростей остаётся функцией свободного разрыва.
- Двенадцатый перенос подтвердил цепную степень как общий боровский
  гамильтониан, но сохранил точную двухориентационную развилку.
- Тринадцатый зарегистрированный гейт добавил тип `KrausHistory`: для
  часов с показаниями `0,1,2` условные срезы точно дают `Phi_*^n`, а
  изометрический history-parent имеет 21-мерное семейство стационарных
  нулевых мод. Полный унитарный такт не каноничен на 252-мерном дополнении.
- Четырнадцатый гейт доказал эту неканоничность внутри LCF-ядра:
  complement-phase семейство `U(1)` сохраняет канал и ковариантность, а
  Real-чётный слой всё ещё содержит различные `z=+1,-1`.
- Первый перенос Version 9 зарегистрировал invariant logdet parent:
  десять obligations подтверждают determinant multiplicities `1+1+3`,
  spectra `{1,5/3}` и `{3/5,1}`, shape-rank `4` и полный Hessian
  `12/(5184/25)`.
- Второй перенос Version 9 проверил measure-origin determinant-следствия:
  complex fermionic sign совпадает с `-log det`, minimal doubled degree
  равна `10`, а coordinate Jacobian отличается множителем
  `(5/3)r_t^2`.
- Третий перенос Version 9 проверил auxiliary module admission:
  `G_aux=Pi(V_type tensor P_KMS)` имеет dimension `10`, не добавляет
  physical states, а его complex pairing имеет rank `20`. Текущий
  registry равен `51/392`.
- Четвёртый перенос Version 9 проверил все tensor gradings и paired
  measure covariance; all-odd target не получен, но independent measure
  orientation freedom устранена. Текущий registry равен `52/402`, тесты
  `58/58`.
- Пятый перенос Version 9 построил contractible quartet `(20|20)` и
  точный FP determinant двух KMS blocks.
- Шестой перенос Version 9 локализовал shift-rank defect `4` и отделил
  conditional spectator flatness от gauge-origin.
- Седьмой перенос Version 9 построил nontrivial shift parent, но доказал
  exact cancellation quotient-boson и ghost determinants. Текущий registry
  на этом шаге равен `55/432`, тесты `61/61`.
- Восьмой перенос Version 9 доказал determinant-capacity `1/2` физической
  target-мультиплеты и отделил algebraic realizations от их physical origin.
  На этом шаге registry равен `56/443`, тесты `62/62`.
- Девятый перенос Version 9 построил minimal coupled bath и точную
  determinant--interaction trilemma. Текущий registry равен `57/455`,
  тесты `63/63`.
- Десятый перенос Version 9 построил exact causal R/A/K kernel и доказал
  normalization--logdet obstruction. Текущий registry равен `58/468`.
- Финальный перенос Version 9 зафиксировал exact decomposition физического
  дефицита и отделил полную спецификацию Тома X от нулевого construction.
  После двадцать пятого гейта Тома X текущий registry равен `94/1048`, тесты
  `100/100`.
  Первый гейт растущей геометрии сертифицирует точные тождества
  `a^3=N/N0`, `a'/a=N'/(3N)` и
  `Lambda_growth=3 exp(-2 S_vac)/(8 pi)`, сохраняя physical-origin
  границу `0/3`.
  Гейт физического притока дополнительно сертифицирует закрытое сокращение,
  отрицательную кривизну `-2J/(1+J)`, положительную четвёртую вариацию и
  точный нарушенный свидетель `q=+-1/sqrt(2)`.

## Status boundary

Теорема eDSL сильнее обычного численного свидетельства, но слабее
проверенного Lean-результата: само Python-ядро ещё не доказано в независимом
proof assistant. Z3-ответ также не является теоремой, пока proof object не
воспроизведён доверенным ядром.

## Links

- [[formal-verification-and-palomar-roadmap]]
- [[version8-bimodule-common-curvature-relative-weight-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]
- [[version8-markov-fixed-algebra-lcf-migration-gate]]
- [[version8-linking-qms-gksl-lcf-migration-gate]]
- [[version8-gauge-twirl-kraus-lcf-migration-gate]]
- [[version8-kraus-bridge-parent-action-lcf-migration-gate]]
- [[version8-cross-arrow-covariance-lcf-migration-gate]]
- [[version8-minimal-covariant-stinespring-lcf-migration-gate]]
- [[version8-intrinsic-noise-clock-lcf-migration-gate]]
- [[version8-full-primitive-markov-generator-lcf-migration-gate]]
- [[version8-kms-nontracial-relative-rate-lcf-migration-gate]]
- [[version8-page-wootters-stinespring-history-gate]]
- [[version8-canonical-autonomous-clock-unitary-extension-no-go-gate]]
- [[version9-endpoint-creation-kms-relative-shape-selector-source-minimal-invariant-parent-architecture-gate]]
- [[version9-endpoint-creation-kms-relative-shape-logdet-parent-measure-origin-gate]]
- [[version9-endpoint-creation-kms-logdet-auxiliary-fermion-module-admission-gate]]
- [[version9-endpoint-creation-kms-logdet-auxiliary-fermion-statistics-parent-origin-gate]]
- [[version9-endpoint-creation-kms-logdet-minimal-brst-complex-architecture-gate]]
- [[version9-endpoint-creation-kms-logdet-brst-shift-symmetry-parent-origin-gate]]
- [[version9-endpoint-creation-kms-logdet-minimal-stueckelberg-shift-parent-architecture-gate]]
- [[version9-final-conclusion-and-tome10-program-gate]]
- [[version9-endpoint-creation-kms-logdet-physical-fermion-loop-parent-origin-gate]]
- [[version9-endpoint-creation-kms-logdet-minimal-fermion-bath-architecture-gate]]
- [[version9-endpoint-creation-kms-logdet-keldysh-influence-functional-admission-gate]]
- [[version9-endpoint-creation-kms-logdet-reservoir-spectral-density-parent-origin-gate]]
- [[version9-endpoint-creation-kms-logdet-reservoir-measure-anomaly-parent-origin-gate]]
- [[version9-endpoint-creation-kms-logdet-minimal-new-parent-axiom-admission-gate]]
- [[version9-endpoint-creation-kms-logdet-axiom-augmented-common-parent-closure-gate]]
- [[version9-endpoint-creation-kms-logdet-axiom-augmented-blind-dimensionless-prediction-gate]]
- [[version9-endpoint-creation-kms-logdet-axiom-augmented-conditional-program-status-gate]]
- [[global-theorem-and-no-go-ledger]]

## Source Notes

- `s2t/proofdsl/README.md`
- `s2t/proofdsl/kernel.py`
- `s2t/proofdsl/structures.py`
- `s2t/proofdsl/lindblad.py`
- `s2t/proofdsl/history.py`
- `s2t/proofdsl/examples/version8_connector_no_go.py`
- `s2t/proofdsl/examples/version8_gauge_twirl_kraus.py`
- `s2t/proofdsl/examples/version8_kraus_parent_hessian.py`
- `s2t/proofdsl/examples/version8_cross_covariance.py`
- `s2t/proofdsl/examples/version8_stinespring.py`
- `s2t/proofdsl/examples/version8_noise_clock.py`
- `s2t/proofdsl/examples/version8_full_primitive.py`
- `s2t/proofdsl/examples/version8_page_wootters_history.py`
- `s2t/proofdsl/examples/version8_autonomous_clock_unitary.py`
- `s2t/proofdsl/examples/version9_kms_relative_shape_invariant_parent.py`
- `s2t/proofdsl/examples/version9_kms_logdet_measure_origin.py`
- `s2t/proofdsl/examples/version9_kms_auxiliary_fermion_module_admission.py`
- `s2t/proofdsl/examples/version9_kms_auxiliary_fermion_statistics_origin.py`
- `s2t/proofdsl/examples/version9_kms_minimal_brst_complex.py`
- `s2t/proofdsl/examples/version9_kms_brst_shift_symmetry_origin.py`
- `s2t/proofdsl/examples/version9_kms_minimal_stueckelberg_shift_parent.py`
- `s2t/proofdsl/examples/version9_kms_physical_fermion_loop_origin.py`
- `s2t/proofdsl/examples/version9_kms_minimal_fermion_bath.py`
- `s2t/proofdsl/tests/test_proofdsl.py`