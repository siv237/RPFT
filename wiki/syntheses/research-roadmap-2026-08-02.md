# Research Roadmap After The August 2026 Audit

> Status: active
> Type: synthesis / decision roadmap
> Updated: 2026-08-02

## Простое резюме

Финальная проверка `C6` завершена отрицательно и зафиксирована в [[c6-final-same-scheme-verdict]]: внутри текущей Maxwell--ghost схемы обязательная компенсация ненулевого геометрического блока не найдена. Это не провал всей теории. Это понижение одного сильного утверждения: точное `pi^-4` теперь считается структурной компрессией, а не доказанной детерминантной теоремой.

Проект уже вышел из стадии общего мифа и получил несколько устойчивых расчётных опор. Главная проблема теперь не в отсутствии идей, а в одном узком месте: можно ли честно вывести электромагнитный вклад `S_vac` из единого детерминантного функционала, не обрезая высшие оболочки вручную и не подгоняя число `10`.

Прямой тест `T5` теперь выполнен: полная таблица `36 x 25` имеет ранг `0`, поскольку внешний `dG` переводит скалярную утечку в точную одноформу, ортогональную коэкзактному факторпространству. Ближайший курс теперь --- вычислить cross-return block, где вариация одноформенного оператора действует на эту точную форму до финальной коэкзактной проекции.

## Что уже удалось

- Геометрический носитель `RP^3 x S^1`, объём факторпространства, спиновое накрытие и роль `Z2`-голономии образуют согласованный каркас.
- `S_geo` имеет сильную структурную поддержку и не зависит от незакрытого маршрута `C6`.
- Ветвь `kappa_Cas=1/24`, ранг `P02=1+9=10`, множитель `pi^2/2` и знак коэкзактного бозонного блока дают содержательную, но пока условную схему `S_vac`.
- Масса тау и мост к эффективному сектору Хиггса остаются текущими успешными замыканиями.
- Для `C6` получен реальный операторный прогресс: построена низкооболочечная база, найдена ненулевая утечка `n=1 -> n=3`, собран ненулевой connection-блок и зафиксированы формулы вариации коэкзактного проектора.
- Проверки `T1` и `T3` дали ненулевые свидетели перехода `ell=2 -> ell=4`; `T2` на константе зануляется.

## Что не удалось или стало опасным

- Наивная компенсация коэкзактной башни ghost/exact-секторами не работает.
- Прямое Maxwell--ghost--Dirac попарное сокращение не поддерживается спектрами без искусственных коэффициентов.
- Независимая добавка от коэкзактной башни ухудшает численное совпадение; допустим только вывод внутри единой схемы.
- Ранг `10` нельзя получать ручным сохранением только `ell=0,2`: оператор проектора допускает и реально создаёт высшие чётные оболочки.
- Connection-блок не сокращается сам; отмена, если она существует, обязана включать Ricci, projector, Hilbert/basis, principal и scheme blocks.
- Точное поглощение требует `N_need=10.0099700224`, поэтому близость к целому `10` не считается доказательством.
- Минимальная двухпороговая EW/QCD-модель не даёт полного низкоэнергетического замыкания.

## Приоритеты

| Приоритет | Задача | Готовый результат | Критерий решения |
|---|---|---|---|
| `P0` | `T5`: спарить опасные `T1/T3` scalar leaks с низкими одноформенными базисами через `dG` | таблица `36 x 25`, ранг `0` | выполнено: прямой outer-`dG` канал закрыт точной ортогональностью |
| `P0` | Вычислить projector cross-return block `Pi Delta_{1,A} Pi_B + A<->B` | quotient-normalized `n=1/n=3` матрица | определить, может ли varied one-form operator вернуть точную форму в коэкзактный сектор |
| `P0` | Свести Maxwell, ghost, `det'`, zero modes, Hodge Jacobian и gauge volume в одной схеме | единый нормированный функционал и таблица конечных остатков | число `N_need-10` выведено или признано невыводимым в выбранной схеме |
| `P1` | Дособрать Ricci и Hilbert/basis blocks вместе с уже вычисленными principal/connection blocks | полный `C_delta2[1,1]`, затем `C_delta2[3,3]` | независимая перепроверка знаков, рангов и нормировок |
| `P1` | Внешняя проверка lens-space determinant route | воспроизводимый пакет скриптов, JSON и источников | результат повторяется без скрытых ручных чисел |
| `P1` | Нейтринная overlap lemma | определённое пространство, мера и вывод `N_nu^2=pi+pi^-1` либо no-go | переход нейтринной строки из гипотезы в доказательство или честный отказ |
| `P2` | Полный EW/QCD threshold solver | KK/breaking thresholds и двухпетлевой RG | нет скрыто подогнанных масс |

## Последовательность работ

### Этап 1 — Решающий projector gate

1. Зафиксировать quotient-normalized `n=1` и `n=3` one-form bases и соглашения внутреннего произведения.
2. Прямой `T5` выполнен: `T1/T3` outer-`dG` каналы зануляются структурно.
3. Не считать это закрытием всего projector block: вычислить `Pi Delta_{1,A} Pi_B + A<->B`.
4. Возвращаться к `T4` и высшим оболочкам только если cross-return operator действительно связывает их с финальным коэкзактным сектором.

### Этап 2 — Бинарный вердикт по `C6`

Ветка успеха:

- полный one-form quotient уничтожает опасные scalar leaks или их удаляет доказанная компенсация;
- все operator blocks собраны в одной нормировке;
- конечный остаток объясняет требуемый коэффициент без подгонки;
- `S_vac` можно поднимать с условного уровня только после независимого воспроизведения.

Ветка понижения статуса:

- высшие оболочки дают ненулевой несокращаемый вклад;
- scalar ghost half-power или scheme residue меняет эффективный ранг;
- точное `pi^-4` остаётся численно сильной структурной компрессией, но не теоремой;
- `S_geo`, тау, Higgs EFT и остальные независимые результаты сохраняются без изменений.

### Этап 3 — Независимая проверка

1. Стабилизировать вычислительные скрипты и входные данные.
2. Для каждого заявленного числа хранить формулу, происхождение параметров и машинно-читаемый результат.
3. Повторить ключевые таблицы альтернативным способом: символически и численно.
4. Подготовить короткую таблицу `claim -> evidence -> assumptions -> failure mode`.

### Этап 4 — Следующая физическая строка

После вердикта `C6` главным содержательным направлением становится neutrino overlap lemma. EW/QCD остаётся следующим большим вычислительным проектом, но не должно отвлекать ресурсы до фиксации нейтринной меры и воспроизводимого детерминантного пакета.

## Правила остановки

- Не продолжать поиск «почти целых» коэффициентов без операторного источника.
- Не добавлять новый сектор только для компенсации малого остатка.
- Не считать selection rule доказательством зануления коэффициента.
- После ненулевого `T5` разрешены только два честных пути: считать высшие оболочки или понизить статус `pi^-4`.
- После трёх независимых неудач same-scheme компенсации закрыть текущую rescue-ветвь и переключить основной ресурс на neutrino/reproducibility tracks.

## Контрольные точки

| Контрольная точка | Ожидаемый статус |
|---|---|
| `M1` | выполнено: таблица `T5` имеет ранг `0`; прямой `T4` в outer-`dG` позиции также удаляется ортогональностью |
| `M2` | Hilbert similarity выполнена: apparent `80 -> 180` полностью representation-compensated; determinant neutral |
| `M3` | principal+connection+Ricci `C11` собран: все `55` пар ненулевые; geometric cancellation failed |
| `M4` | окончательный verdict: theorem / conditional / downgraded для `pi^-4` |
| `M5` | воспроизводимый пакет и обновлённая maturity matrix |
| `M6` | neutrino overlap proof или формальный no-go |

## Следующее конкретное действие

Решающий `C6` цикл завершён. Следующее конкретное действие теперь состоит не в продолжении поиска компенсации рядом с тем же числом, а в смене доказательного приоритета:

1. зафиксировать `S_vac` как условный результат;
2. собрать таблицу воспроизводимости `claim -> evidence -> assumptions -> failure mode`;
3. начать доказательство neutrino overlap lemma;
4. параллельно подготовить внешний lens-space determinant gate;
5. не возвращаться к `C6` без новой обязательной симметрии, тождества или сектора.

Итог для перспективности: точная вакуумная ветвь стала слабее, но программа в целом стала научно сильнее благодаря ясной границе доказанного и условного.

## 2026-08-03 Внешний lens-space gate

Первый внешний этап выполнен в [[external-l21-spectrum-determinant-reproduction]]. Подтверждены untwisted scalar/coexact spectra на `L(2,1)`, внутренние multiplicities `6` и `30`, а также опубликованный scalar determinant на `RP^3`.

Влияние на план:

- пункт внешней проверки больше не является только подготовительным;
- спектральная база признана воспроизводимой;
- twisted determinant нельзя смешивать с ordinary Maxwell;
- scalar half-residual подтверждён независимо;
- точный `pi^-4` не переоткрывается.

Следующий внешний расчёт: перейти от `RP^3` к `RP^3 x S^1`, выполнить Matsubara sum для untwisted coexact tower и независимо проверить значение `T_coex^{RP3}` с разделением zero-winding и finite-winding частей.

Этот расчёт теперь выполнен в [[external-rp3xs1-winding-determinant-audit]]. Значение `T_coex^{RP3}` подтверждено, но выявлено различие между Casimir-energy zeta function и Euclidean one-loop `log det`.

Новая последовательность:

1. решить, является ли первичным объектом `S_vac` Casimir energy или Euclidean effective action;
2. вывести соответствующий Maxwell--FP prefactor, знак и радиусную размерность;
3. включить scalar half-determinant в той же схеме;
4. только после этого сравнивать полный результат с `pi^-4`;
5. при отсутствии такого моста оставить вакуумную ветвь замороженной и перейти к neutrino overlap lemma.

Для перспективности это смешанный результат: spectral tower подтверждена очень сильно, но точная вакуумная нормировка стала менее перспективной.

## 2026-08-03 Neutrino Overlap First Gate

Главный параллельный sprint дал первый бинарный результат. Вывод `pi+pi^-1` непосредственно из spin/gauge holonomy невозможен как gauge-invariant утверждение: holonomy задаётся классом `exp(i theta)`, тогда как `theta+theta^-1` зависит от ветви угла.

Остаётся более содержательная ветвь:

```text
Q_cycle=diag(g,g^-1), det Q_cycle=1,
Tr Q_cycle=pi+pi^-1 при g=pi.
```

Следующий приоритет --- не дальнейший подбор скаляров, а построение положительного self-adjoint `Q_cycle` из геометрии или спектральной меры. Если это удаётся, его квадратный корень должен войти в Dirac matrix element. Если нет, абсолютная нейтринная шкала понижается, а безразмерный `R_nu` сохраняется.

Этот результат даёт пищу основной программе: единый источник обязан различать unitary phase sector и positive reciprocal metric sector, а затем задавать закон их coupling.

## 2026-08-03 Qcycle Constructed

Positive reciprocal metric sector теперь имеет явную модель. На systolic projective line `gamma=RP1` длины `pi` integral-normalized generators `1` и `ds/pi` дают Hodge Gram matrix

```text
Qcycle=diag(pi,pi^-1).
```

Primitive self-duality на lattice `Z^2` однозначно выбирает `v_nu=(1,1)` с точностью до знака, поэтому

```text
||Qcycle^(1/2)v_nu||^2=pi+pi^-1.
```

Перспективность нейтринной ветви повышается: искомый коэффициент больше не является только скалярной вставкой. Следующий и последний крупный gap этой ветви --- ambient Dirac embedding: restriction/defect map к циклу и EFT vertex, которая действительно помещает этот norm в `m_D`.

Для основной теории это важный результат: минимальное ядро может содержать torsion/systolic cycle вместе с его intrinsic primal-dual Hodge metric.

## 2026-08-03 Qcycle Seesaw Embedding

Cycle operator теперь встроен непосредственно в seesaw contraction:

```text
mD_cycle=y(1,1)Qcycle^(1/2),
MR_cycle=M0 I2.
```

Это даёт без подгонки

```text
-mD MR^-1 mD^T=-(y^2/M0)(pi+pi^-1).
```

Конструкция basis-invariant и не вводит новый массовый масштаб. Она также не меняет `R_nu`, поскольку cycle factor умножает всю light-neutrino matrix одним скаляром.

Новый главный gap узок: показать, что cycle-doublet является двумя каналами внутри существующего Majorana-модуля, а ambient Dirac vertex действительно выбирает primitive self-dual vector и identity heavy block. Это уже representation/EFT задача, а не поиск числового множителя.

## 2026-08-03 Majorana Dimension Gate

Representation audit показал, что текущий вывод `24-1=23` записан некорректно. Generation-singlet является полным внутренним spinor-модулем. При `8` real components на поколение его удаление даёт `24-8=16`, а не `23`.

Сохранить `23` можно только через новый объект:

```text
P_rank1=|u><u| on R24,
```

где `u` должен быть канонически выбран полной Dirac/Qcycle структурой. Такой вектор пока не найден.

Стратегический вывод:

- `Qcycle` и reciprocal factor являются реальным прогрессом;
- seesaw embedding работает как матрица;
- старый denominator proof не выдерживает representation check;
- следующий sprint должен искать rank-one kernel selector, а не улучшать численное совпадение;
- при неудаче нейтринная абсолютная шкала и `R_nu` должны быть понижены.

Rank-one sprint завершён отрицательно. Exact subgroup `Q8` уже запрещает invariant real line в четырёхмерном lowest-spinor модуле. Совместный `generation singlet x lowest RP3 spinor x self-dual cycle` projector имеет ранг `4`, поэтому текущие exact symmetries дают максимум кандидаты `24-4=20` или `24-8=16`, но не `23`. Следующая развилка физическая: либо вывести defect/condensate, реально выбирающий spinor polarization, либо перестроить нейтринный знаменатель на ковариантном блоке.

Первая defect-попытка дала условно положительный результат. Odd-winding class-D Majorana mass defect на systolic core имеет transverse mod-two index `1`; существующая nontrivial `Z2` flat line сокращает anti-periodic spin holonomy, оставляя одну longitudinal real zero mode. Совместный kernel имеет rank `1` и совместим с `Qcycle`. Поэтому `23` можно восстановить без ручного выбора polarization, но только после добавления и вывода нового mass order parameter. Следующий gate: получить этот order parameter из существующего S2T/Higgs или spectral sector и доказать forced odd winding.

Forced-winding gate частично закрыт. Smooth ambient `Z2` line локально тривиальна на core meridian, но на solid-torus complement у неё есть ровно две square-root branches `+i/-i`. Из relation `mu=2y` следует meridian holonomy `-1`; это дискретный pi-flux defect. В charge-two Majorana pair channel он заставляет winding `1`. Ветка совпадает с уже вычисленным `beta=1/4` gauge doublet, поэтому новая непрерывная фаза не вводится. Остался core-gluing theorem: вывести singular square-root line из действия и перенести её index-one transverse mode в periodic longitudinal kernel.

Локальный core-gluing theorem теперь закрыт. Nambu transition `diag(i,-i)` переносит zero-mode basis при сдвиге pair phase на `pi`; coefficient line видит только знаки spin и ambient torsion, `(-1)(-1)=+1`. Majorana reality оставляет один real coefficient и исключает Nambu doubling. Поэтому внутри условной defect-модели rank-one kernel и complement rank `23` согласованы. Остался не топологический, а action-level gate: вывести глобальный tubular BdG operator и доказать, что quotient kernel входит именно в heavy denominator.

Глобальный tubular EFT-кандидат построен, но action audit дал важный отрицательный результат. Mass operator `M0 P_H` на rank-23 quotient при нормированном coupling не содержит rank, при ненормированном democratic coupling даёт `23` в числителе, а determinant содержит `23 log M0`. Поэтому rank `23` сам по себе не выводит denominator `23 M0`. Последний gate теперь формулируется точно: вывести collective coefficient `Tr(P_H)+pi^-1` из loop self-energy, spectral trace или stiffness, не задавая его определением.

Collective-stiffness route дал условно положительное решение этого gate. Для единой deformation `Xi=(P_H,e1_dual)` каноническая Hilbert--Schmidt/Hodge норма равна `Tr(P_H^2)+||e1||^2=23+pi^-1`. Интегрирование auxiliary amplitude даёт требуемый inverse denominator и устойчиво к field rescaling. Остался один normalization theorem: вывести equal weights двух summands из единого superconnection/spectral trace. Общая метрика `alpha*Tr+beta*Hodge` снова открыла бы скрытую ручку.

Relative-weight theorem теперь закрыт внутри minimal graded-superconnection model. Tangent `bold Xi=P_H tensor e0_hat + P_kernel tensor e1` использует один trace--Hodge functional. `e0_hat` является normalized dynamical wavefunction, `e1` --- unit-period holonomy generator; cross-term исчезает по form degree и `P_H P_kernel=0`. Это даёт `23+pi^-1` без `alpha/beta`. Последняя задача нейтринной ветви теперь parent-level: вывести именно эту superconnection reduction из S2T spectral action.

Parent restriction построен явно: normalized radial profile и spectator `S1` mode редуцируют ambient variation к `bold Xi` без изменения нормы. Но kernel-family audit отделил две постановки. Canonical configuration metric даёт exact denominator; generic Hessian `Tr f((D0+a delta A)^2)` для heat/rational kernels расщепляет heavy и kernel weights около ненулевого background. Поэтому следующий выбор фундаментален: принять trace--Hodge configuration metric как первичный S2T kinetic functional или вывести специальную spectral-kernel identity.

Завершить same-scheme determinant Hessian после отрицательного геометрического результата:

```text
C_AB^full = C_principal+connection+Ricci
            + C_ghost/det'
            + C_zero/gauge
            + C_scalar-half
            + C_local-fixed-scheme.
```

Principal, connection и Ricci уже собраны; все `55` пар остаются ненулевыми. Следующий шаг должен либо вывести обязательную компенсацию из заранее фиксированной Maxwell--ghost схемы, либо запустить безопасное понижение статуса exact `pi^-4` absorption.

Финальный gate выполнен 2026-08-03. Внешнее воспроизведение спектра подтвердило coexact tower и standard-FP scalar half-residual, но одновременно показало функциональный разрыв: положительная Bessel-сумма `T_coex` относится к Casimir energy, тогда как Euclidean winding determinant задаётся логарифмическим произведением. Same-scheme аудит не нашёл обязательной компенсации. Поэтому C6 закрыт отрицательно для версии II.A, а exact `pi^-4` заморожен как strong structural compression. Дальнейшее расширение допустимо только как новая EM-модель, а не как продолжение недосчитанной старой таблицы.

Новая EM-ветвь начата с relative determinant, а не с новой поправки к `alpha`. Continuous `S1` holonomy ratio и discrete `RP3` `Z2` bundle ratio конечны и быстро сходятся без отдельной local subtraction. Первый gate положителен как construction, но отрицателен как vacuum selector: quarter-holonomy не stationary, а оба ratio монотонны по `R1/R3`. Следующий шаг --- не подбирать множитель, а построить единый configuration functional с геометрией, derived zero-mode measure и defect/superconnection sector.

Первый reciprocal completion дал положительный shape-selection результат. Functional `F_beta(r)=G_beta(r)+G_beta(1/r)` не содержит relative coefficient и точно симметричен по `log r`; поэтому `r=1` stationary. Численный spectral sweep показывает положительную кривизну и минимум при `r=1`, включая discrete quarter-sector, уже выбранный torsion square-root defect. Следующий theorem gate: поднять intrinsic `Qcycle` duality до ambient Maxwell--FP determinant и добавить zero-mode/gauge-volume measure. До этого результат не связывается с `alpha`.

Ambient bridge gate выполнен отрицательно. `RP3 x S1` spectra при `r` и `1/r` не изоспектральны, single response не dual, scalar zero-mode measure несёт `4 log r`, а Maxwell duality не создаёт additive inverse-radius sector. Поэтому reciprocal minimum понижен до свойства symmetrized candidate. Дальнейшее развитие возможно только как новая dual/winding-модель с явным operator intertwiner, а не как доказательство внутри II.A.

## 2026-08-04 Решающий gate нейтринной метрики

Условие равенства heavy- и kernel-весов решено как функциональное уравнение. Требование его выполнения для произвольного ненулевого background и гладкость при нуле единственным образом дают affine kernel `f(x)=A+B x`. Положительные heat-kernel смеси равенство не выполняют. Поэтому поиск специального удобного cutoff прекращается: либо canonical configuration metric принимается как первичный кинематический постулат, либо абсолютная нейтринная шкала остаётся условной.

Следующий независимый шаг после этого решения — полный EW/QCD threshold gate без fitted threshold masses. Электромагнитные `pi^-4` и reciprocal-radius ветви остаются замороженными.

Первый новый blind observable уже проверен. Из `v_S2T`, построенного без `G_F`, следует tree-level значение `G_F=1.1685251368e-5 GeV^-2`, превышающее контроль на `0.184%`. Это закрывает нулевой matching отрицательно. Универсальная поправка масштаба, фиксированная по `G_F`, не закрывает одновременно `M_W` и `M_Z`; поэтому следующий solver обязан выводить полный gauge/threshold matching из frozen spectrum.

Расширенный scorecard уточняет диагноз. Лептонно-скалярные строки (`m_tau`, `M_H`, tree-level proxy для `lambda_H`) близки к контролю; условные neutrino splittings также близки, но пока имеют малый доказательный вес. Все gauge-running строки проваливаются совместно. После фиксации `v` требуются разные поправки к `g2`, `gZ` и `g3`, причём сильная связь требует изменения примерно на `16.5%` по `g3`. Поэтому следующий сектор должен быть representation-dependent KK/threshold tower, а не общий множитель.

Первый representation-cone gate закрывает простейшую возможность отрицательно: полные поколения и complete-matter replicas дают слишком большой `SU(2)`-вклад. Требуемое направление близко к split-ray `U+2D+H`, но этот набор получен inverse-диагностикой и не может быть добавлен вручную. Следующий конструктивный шаг — вывести anomaly-free parent multiplet и quarter/Z2 holonomy projection, подавляющую doublet partners, после чего вычислить regulated KK tower sum.

Конструктивный шаг выполнен: vectorlike `SU(5)` parent и совместная `Z2/Z4` phase table оставляют ровно `U+2D+H`, не нарушая anomaly cancellation. Теперь задача больше не состоит в угадывании representations. Следующий gate — независимо вывести flat-character assignment и вычислить конечную determinant-разность periodic, quarter и half-shifted KK branches.

Determinant gate выполнен отрицательно для common-spectrum projected partners: их color/weak ratio фиксирован как `9/20` и не может приблизиться к требуемому `11.014`. Последующий correct-sign audit также закрывает промежуточный RG-бег periodic `U+2D+H`: positive matter beta сдвигает inverse couplings в противоположную сторону.

Минимальный zero-parameter кандидат `S_split=pi^2+1/(2pi)` сохраняется как geometric object, но его прежнее gauge-улучшение признано ошибочным из-за неверного RG-знака и потери `alpha_em` anchor.

Constrained-saddle gate частично закрыт. На фиксированном unit-radius carrier degree-one calibrated wrapping и unit-period core form дают точный устойчивый минимум `pi^2+1/(2pi)`. Но свободная вариация радиуса обнаруживает obstruction: `R=1` не stationary. Следующий шаг теперь точнее: вывести wrapping tension, cycle normalization и radius stabilization из одного parent functional; только после этого запускать полный two-loop matching.

Two-loop stress-test завершён отрицательно. При сохранении `alpha_em` split-sector даёт `sin2=0.206203` и `alpha_s=0.080177`; top-Yukawa sensitivity практически ничего не меняет. EW/QCD roadmap теперь должен искать finite matching требуемого отрицательного знака либо независимо выведенную UV-нормировку, а не ещё одну intermediate mass scale.

Finite-threshold cone audit также завершён отрицательно. Basis `XY/H3/Sigma8/Sigma3` достигает target только с логарифмами до `116`, то есть с состояниями далеко ниже `M_Z`; в физическом окне точного решения нет. Это является stop condition для минимальной logarithmic EW/QCD-ветви. Продолжение оправдано только при заранее выведенном nonlogarithmic matching operator; иначе основной ресурс следует перенести в лептонно-скалярный и operator-structure сектора.

Первый аудит перенесённого лептонного приоритета дал смешанный, но содержательный результат. Формула tau уникальна среди `1485` заранее ограниченных low-complexity candidates и остаётся внутри `0.78 sigma` текущего контроля. Однако seed `rho0=pi^2+2pi+2/3` в Tome II принят как premise, а записанная Bessel-сумма даёт coefficient `0.0616969`, не `1/3`; требуемый projection Jacobian имеет невыведенную величину `5.40275`. Следующий и теперь главный gate программы — явный charged-lepton operator и нормированный `RP3` projection trace.

Первый operator-candidate построен. Direct-sum tangent из constant `RP3`, constant `S1` и transverse angular channels имеет norm точно `pi^2+2pi+2/3`; primitive unit vector минимален. Для traceless relative sector pre-existing rank `9` и quotient factor `1/2` дают `J=9/2`, а не fitted `5.40275`. Новая формула предсказывает `m_tau=1776.90237 MeV` (`-0.31 sigma`). Результат конструктивен, но post-audit; решающий gate — вычислить ambient loop trace и определить, является ли trace unnormalized.

Ambient trace gate выполнен отрицательно для этого rescue. Поскольку traceless strains чётны, quotient group average даёт trace `9`, а не `9/2`; normalized quotient modes сокращают half-volume. Одна canonically normalized collective deformation даёт `J=1`, девять независимых — `J=9`. Поэтому `9/2` закрыт, а charged-lepton relation остаётся уникальным численным pattern без operator normalization theorem.

Единый parent-action gate также выполнен отрицательно. В minimal trace--Hodge action нейтринная deformation сохраняет norm `23+pi^-1`, но canonical lepton normalization заменяет raw seed на `8/3`, а loop coefficient остаётся `0.06169694`. Функциональное уравнение показывает, что равные heavy/kernel Hessian-веса при всех backgrounds даёт только affine kernel. Из требуемых двух независимых секторов проходит один; следующий допустимый шаг — не новый численный bridge, а вывод noncanonical measure/stiffness из prior symmetry или boundary principle.

## Связанные страницы

- [[current-status-and-next-vectors]] — подробный аудит успехов и неудач.
- [[theorem-status-ledger-2026-08-04]] — компактный реестр теорем, no-go и условий остановки.
- [[s2t-closure-roadmap]] — хронология замыкания `C6`.
- [[projector-coefficient-test-protocol]] — определения `T1--T5`.
- [[projector-t1-coefficient-witness]] — ненулевой `T1`.
- [[projector-t2-t3-coefficient-witness]] — нулевой `T2` и ненулевой `T3`.
- [[projector-t5-quotient-contraction-table]] — нулевая полная таблица прямых T5-спариваний и точная Hodge-лемма.
- [[ricci-c11-gauss-table]] — Ricci C11 и отрицательный verdict для geometric cancellation.
- [[projector-hilbert-rescue-sprint]] — projector/Hilbert rescue protocol.
- [[finite-gap-source-audit]] — аудит остатка `N_need-10`.
- [[neutrino-overlap-lemma]] — следующий физический proof target.
- [[ew-qcd-threshold-closure]] — отложенный полный threshold solver.