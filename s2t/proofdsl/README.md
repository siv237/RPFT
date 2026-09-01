# S2T proof eDSL

Легковесный pure-Python слой для точных конечномерных доказательств проекта.
Архитектура следует LCF-принципу: значение `Theorem` выдаёт только малое
доверенное ядро `kernel.py`; тактики и решатели не создают теорем напрямую.

## Уже реализовано

- неизменяемые типизированные `Space`, `Morphism` и представления;
- запрет матриц неправильной формы и несогласованной композиции;
- отказ от `Float` внутри точного ядра;
- точная SymPy-проверка равенств, рангов и уравнений интертвинера;
- изотипический расчёт `Hom_G` и строгой верхней границы ранга;
- типизированный конечномерный GKSL-конструктор;
- необязательный Z3-адаптер, который пока возвращает только solver evidence;
- точный пример no-go коннектора Тома VIII.
- шаблон `GateSpec`, реестр обязательств и детерминированные JSON-сертификаты;
- второй независимый пример: точный спинодальный порог `beta=21/2`.
- точный общий коммутант QMS: `13 -> 2` с проекторами рангов `12+9`.
- полный linking-GKSL: trace-preserving, unital, corner-invariant и
  `dim Fix=41`, проверенные на точном матричном базисе.
- полный gauge-twirl Kraus-мост: точное замыкание 12 jump-направлений под
  12 генераторами `SU(3) x SU(2) x U(1)`, отсутствие линейного синглета и
  сокращение центральной `C^2` до единицы при всех положительных скоростях.
- parent-action Kraus-моста: точные коэффициенты `7/36`, гессиан
  `7 I_12/18`, сохранение сигнатур для всех неотрицательных весов и
  древесный no-go ненулевой скорости при `z=0`.
- полярная cross-ковариация: точная алгебраическая коизометрия, шесть
  одинаковых `QLYR–XLdR`-пар, нулевое сцепление с 15 прочими модами и
  общая ось при всех `eta>0`.
- минимальная Stinespring-дилатация: точное окно `0<=p<=1/6`, типизированный
  `KrausChannel`, Kraus/Choi-ранг `13`, полный endpoint-тест и точный no-go
  конечной полугруппы.
- внутреннее шумовое время: полный рациональный спектр cross-генератора,
  матричная полугруппа, инвариантность ядра при `kappa>0`, модульный no-go и
  collision-limit `Phi_(u/n)^n -> exp(u L)` в операторной норме.
- полный примитивный QMS: 25 самосопряжённых jump-операторов, скалярная
  неподвижная алгебра и строгая примитивность для всего положительного
  шестимерного конуса весов без случайного scan.
- KMS-no-go: единственное центральное стационарное состояние `I21/21`,
  положительные transfer-следы `13,6,6` и условное, но не выбранное отношение
  направленных скоростей `exp(-beta_Delta)`.
- цепно-модульный родитель: 13 точных боровских пар с частотами `±2`,
  gauge-инвариантность и две примитивные ориентации с отношениями
  `exp(-2)` и `exp(2)`.
- первый гейт Version 9: invariant logdet parent двух KMS-shapes;
  десять обязательств проверяют weighted trace/determinant, stationary
  gradient, точные spectra и полный Hessian rank/determinant `12/(5184/25)`.
- второй гейт Version 9: measure-origin logdet parent; десять обязательств
  проверяют determinant degrees `5/10`, fermionic/bosonic signs и
  несовпадение coordinate Jacobian с invariant determinant.
- третий гейт Version 9: auxiliary fermion module admission; десять
  обязательств проверяют type/package decomposition, odd parity,
  determinant degree `10`, physical decoupling и Berezin rank `20`.
- четвёртый гейт Version 9: statistics parent-origin; десять обязательств
  проверяют все odd ranks `2,5,5,8`, package-swap no-go, rank-two defect
  и paired Berezin Jacobian cancellation.
- пятый гейт Version 9: minimal BRST complex; десять обязательств проверяют
  nilpotence, rank/nullity `20/20`, zero cohomology, ghost-number degree,
  FP determinant и physical decoupling.
- шестой гейт Version 9: BRST shift-origin; десять обязательств проверяют
  required rank `10`, inherited ranks `6/4/1/0`, flat spectator Hessian
  и нарушение translations любой positive quadratic формой.
- седьмой гейт Version 9: minimal Stückelberg parent; десять обязательств
  проверяют orbit/kernel ranks `10/10`, positive spectrum, FP determinant
  и exact boson/ghost determinant cancellation.
- восьмой гейт Version 9: physical fermion-loop origin; одиннадцать
  обязательств проверяют physical rank `5`, determinant degrees `5/10`,
  Real-pairing mismatch rank `10`, doubled и composite kernel identities.
- девятый гейт Version 9: minimal fermion bath; двенадцать обязательств
  проверяют carrier/coupling ranks `10/5`, Schur determinant, positive
  witness spectrum и determinant defect `1024-243=781`.

## Доверенная граница

`kernel.py` — единственный модуль, создающий `Theorem`. Z3 в MVP не входит в
доверенную границу: ответ `unsat` не повышается до теоремы, пока его proof-
объект не будет воспроизводимо проверяться ядром. SymPy используется только
для точных выражений без чисел с плавающей точкой.

## Запуск

Из корня репозитория:

```bash
python -m pytest -q s2t/proofdsl/tests
python -m s2t.proofdsl.examples.version8_connector_no_go
python -m s2t.proofdsl.verify --pretty
```

Контрольный пример выводит точные значения

```text
dim Hom_G(E_endpoint,T_bimod) = 13
max rank = 9
```

Новый гейт переносится копированием
`s2t/proofdsl/templates/gate_template.py`, разбиением утверждения на
обязательства и регистрацией в `registry.py`. Гейт получает статус
`lcf-checked` только если каждое обязательство вернуло настоящий объект
`Theorem` из доверенного ядра.

Для linking/QMS-гейтов важно предъявлять обе половины коммутанта
самосопряжённого оператора: `A X = Y A` и `X A† = A† Y`. Одностороннее
условие в текущем физическом примере оставляет размерность `4`, а полный
набор даёт требуемую размерность `2`.

## Ограничения MVP

- Python обеспечивает дисциплину конструкторов, но не является защищённой
  средой против намеренной рефлексии и подмены модулей.
- Проверяются конечномерные точные объекты; аналитические пределы, спектры
  неограниченных операторов и численная сходимость остаются внешними леммами.
- Z3 не установлен в текущем Prism-окружении и остаётся опциональным.
- Полная положительность GKSL-полугруппы сейчас является доверенным правилом
  непрерывного конструктора. Для cross-arrow генератора отдельный конечный
  шаг уже имеет точный Kraus/Choi-сертификат; collision-limit остаётся
  аналитической задачей.