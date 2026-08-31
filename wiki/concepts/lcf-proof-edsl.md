# LCF proof eDSL проекта S2T

> Status: working
> Type: concept
> Updated: 2026-08-29

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
- `s2t/proofdsl/tests/test_proofdsl.py`