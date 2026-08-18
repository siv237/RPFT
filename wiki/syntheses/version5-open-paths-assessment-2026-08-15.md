# Version V: оценка открытых путей продолжения

> Status: working
> Type: synthesis
> Updated: 2026-08-15

## Summary

На 15 августа 2026 года исходная Version IV закрыта как единая физическая
теория, но проект не исчерпан. Сохраняются три допустимых класса новой
архитектуры:

1. совместная вариация normalized state и carrier geometry в духе TOE 6.5;
2. boundary-source / Wilson--defect архитектура с каноническим fixed-charge
   path integral;
3. новая finite geometry, существенно отличающаяся от закрытых rank-one
   Pati--Salam и ordinary family--defect реализаций.

Наиболее фундаментален первый путь, наиболее быстро фальсифицируем второй,
наиболее близок к observed representation problem третий. Ни один из них не
может считаться продолжением Version IV посредством локального ремонта:
каждый требует отдельной Version V с заранее замороженными объектами,
мерой, статистикой, контрчленами и blind observables.

## Problem

Проект накопил большое число точных identities, геометрических модулей и
машинно воспроизводимых no-go. Главный дефицит находится не на уровне
существования подходящих чисел или представлений. Отсутствует единый prior
functional, который одновременно:

- выбирает background/carrier и вакуум;
- фиксирует относительные веса gauge, scalar, Yukawa и defect sectors;
- имеет полный устойчивый Hessian после gauge quotient;
- допускает контролируемый RG transport;
- проходит две независимые blind-проверки.

Итоговый ledger Тома IV фиксирует `R_sci=4/10`,
`N_closed_physical=0`. Представления и аномалии закрыты только частично или
условно; единое действие, RG, EW/QCD, flavour, абсолютный масштаб и
cross-tome bridge не закрыты.

## Search for solution

Проверены:

- финальная спецификация и заключение Тома IV;
- theorem/no-go ledgers Томов II--IV;
- carrier, full-field counterterm и Gaussian topology gates;
- Pati--Salam rank-selector и final rank-one no-go chain;
- family--defect chain от tetrahedral projector до KO6, junk quotient и
  fermionic-measure no-go;
- Wilson rotor, mapping-cone response и old-problem rotation audits;
- ретроспективный аудит RPFT/UGSM/TOE, выделивший незавершённую программу
  TOE 6.5.

Основные источники перечислены в конце страницы.

## Что уже нельзя повторять

Следующие маршруты закрыты внутри текущих предпосылок:

- объявлять точные арифметические совпадения физическими предсказаниями без
  prior operator и measure;
- восстанавливать gauge unification fitted thresholds, найденными из тех же
  наблюдаемых;
- использовать произвольный Yukawa/readout map при наличии нескольких
  равно допустимых maps;
- получать family moment-map square из ordinary `Tr D_F^4`: mixed sign
  противоположен требуемому;
- извлекать `Sym3(R)` moment map из ordinary degree-two quotient: particle
  middle sector целиком удаляется junk;
- объявлять imaginary Hubbard--Stratonovich contour следствием текущего
  Gaussian Pfaffian: Pfaffian зависит от `rho^2+r^2`, а нужен
  `(rho^2-r^2)^2`;
- стабилизировать полный Pati--Salam `Sigma_4` sector одним rank-one color
  projector: остаётся обязательное восьмимерное `su(3)`-ядро;
- сравнивать топологии полным determinant до фиксации Einstein,
  Weyl-squared, Euler, nonminimal-scalar и vector-mass data;
- одновременно использовать Gibbs free energy и positive bare heat trace
  как один и тот же variational selector: для одного heat operator их
  ordering противоположен;
- выводить абсолютный Planck-scale vacuum локальным heat-kernel expansion в
  режиме `R/Lambda^2` порядка единицы или больше;
- добавлять новый коэффициент или менять representation после раскрытия
  blind data.

## Открытый путь A: carrier-first / corrected TOE 6.5

### Содержание

Определить один normalized parent problem

`F[rho,M] = Tr(rho H_C[M]) + Gamma_fluc[rho,M] - tau^-1 S(rho)`,

где `H_C=-log(Chat)/tau`, `rho` является нормированным состоянием, а `M`
принадлежит заранее объявленному comparison class carriers.

### Почему путь остаётся открыт

- Он ближе всего к исходной корреляционной идее TOE и не предполагает
  заранее `RP3 x S1`.
- Для restricted comparison class уже существуют условные положительные
  результаты: `S4`-ordering, stationary ratio
  `a/sigma=1.3513921957` и Gibbs--Fisher radial geometry.
- Ретроспективный аудит показал, что именно совместная variation spectral
  density, fluctuation determinant и information entropy была предложена,
  но не выполнена как единая задача.

### Главные препятствия

- `Gamma_fluc` не определяет cross-topology ordering до parent derivation
  конечных gravitational/topological coefficients.
- Нужно выбрать первичную семантику: normalized Gibbs functional или bare
  positive spectral action. Их нельзя складывать с произвольным весом и
  нельзя выдавать за один functional.
- Полный shape Hessian, gauge modes, ghosts, BV/BRST quotient и massive
  vector completion ещё не вычислены в одной схеме.
- Gaussian bare action условно фиксирует topology weights, но ordering
  зависит от cutoff time; связь cutoff с correlation scale ещё не выведена
  независимо.

### Первый kill-gate

До новых спектральных сумм требуется документ `Version V.C Core Axioms`,
который фиксирует:

1. фундаментальный operator и domain carriers;
2. primary functional и его знак;
3. bare или renormalized статус gravitational coefficients;
4. допустимый counterterm basis и renormalization conditions;
5. полный field ledger и statistics;
6. две blind dimensionless observables, не связанные с выбором carrier.

После этого вычисляется совместный Hessian `delta^2_(rho,M) F` на
`S4`, `S2 x S2` и как минимум одном deformation family. Наличие negative
physical mode или underived finite coefficient закрывает этот вариант без
phenomenology.

### Оценка

- Стратегическая ценность: очень высокая.
- Вычислительная готовность: средняя-низкая.
- Риск недоопределённости: высокий.
- Рекомендация: основной фундаментальный путь Version V, но только после
  короткого axioms/counterterm gate.

## Открытый путь B: boundary-source / Wilson--defect

### Содержание

Построить canonical boundary path integral или superconnection, который
одновременно действует на:

- sterile square-root root line;
- charge-two pairing field;
- real family triplet;
- quantized rotor/fixed-charge sector.

Его saddle должен без neutrino/flavour inputs выбрать root sector,
condensed unit winding, tetrahedral three-cycle axis и exact-one Majorana
kernel.

### Почему путь остаётся открыт

- Operator level уже содержит точную пару Wilson coefficients: восемь
  unit-charge planes дают `8/3`, а unique minimal odd momentum branch
  `(1,1,1,3,3,3,3,3)` даёт inverse coefficient `8`.
- Family geometry уже даёт tetrahedral projector, exact `Z3` stabilizer,
  three-cycle holonomy и gauge--family lock.
- Этот route способен одним parent action атаковать два независимых
  blocker: defect-source и family-selector origin.

### Главные препятствия

- Fixed-charge ensemble, eight-plane multiplicity, zero-mode prescription
  и BV content пока не выведены.
- Existing Wilson axes и angle не совпадают с tetrahedral three-cycle data;
  значит, старый Wilson saddle нельзя просто переименовать.
- Current family--defect KO6 action закрыт: ordinary trace, mapping cone,
  degree-two calculus и Gaussian Pfaffian не дают требуемый moment-map
  potential.
- Новая boundary construction рискует стать engineered model, если каждое
  представление выбирается ради одного коэффициента.

### Первый kill-gate

Заранее фиксируется минимальная graded boundary Hilbert space и один trace.
Из quadratic action должны следовать одновременно:

1. fixed-charge projection и odd branch;
2. nonzero pairing condensate;
3. `2pi/3` family holonomy и axis из three-cycle orbit;
4. exact-one real BdG zero mode;
5. второй normalization-sensitive result, не использованный при выборе
   representation.

Если хотя бы один relative weight вводится отдельно, route остаётся
математическим boundary model, но не candidate parent theory.

### Оценка

- Стратегическая ценность: высокая, но секторная.
- Вычислительная готовность: самая высокая из трёх ветвей.
- Риск конструктивной подгонки: очень высокий.
- Рекомендация: лучший timeboxed proof-of-principle; не расширять его к
  flavour phenomenology до parent-action pass.

## Открытый путь C: новая finite geometry

Этот класс имеет два подмаршрута, оба являющиеся новой геометрией.

### C1. Pati--Salam reopening

Сохранён exact selector
`4 det(Delta Delta^dagger)`, canonical edge normalization и irreducible
relative cycle. Но current rank-one background структурно не видит восемь
`su(3)` directions в `Sigma_4` и две directions в `phi`.

Допустимое reopening требует:

- fundamental diagonal carrier effective rank не меньше трёх; или
- нескольких independently derived noncommuting projectors с trivial common
  stabilizer; или
- другой connected representation, которая даёт full physical Hessian и
  корректный Goldstone count.

Первый gate — classification theorem для минимальных admissible carriers,
а не ещё один потенциал на прежнем rank-one projector.

### C2. Family--defect reopening

Сохранены explicit KO6 quiver, first-order selection `Y=Phi I3` и точная
moment-map identity. Допустимые изменения:

- выведенный four-fermion kernel в `Sym3(R)` channel;
- modified differential calculus, в котором нужная middle curvature не
  является junk;
- dynamical Cartan-torsion mediator;
- новый finite carrier с правильным relative sign.

Каждый вариант обязан вывести kinetic normalization и quartic из одного
объекта. Imaginary HS transform сам по себе не является origin.

### Оценка

- Стратегическая ценность: высокая для observed gauge/matter sector.
- Вычислительная готовность: средняя для classification, низкая для полной
  phenomenology.
- Риск разрастания model space: очень высокий.
- Рекомендация: начинать только с конечной классификации минимального menu и
  строгого rank/sign theorem; без этого поиск быстро становится
  неограниченным.

## Вспомогательные, но не самостоятельные направления

### Формализация spectral-correlational source

Нужно определить общий объект через algebra/operators, admissible states,
measure и две projection maps к TOE и UGSM. Это может стать аксиоматическим
основанием Version V, но без Hessian и observables само по себе не даёт
физического замыкания.

### Standalone affine family selector

Двенадцать incidence operators порождают full `M3`, а SO(3) condition
оставляет восемь three-cycles. Ветка полезна как finite classification
problem, но без sector map и relative weight не должна быть primary route.

### External reproduction

Внешняя независимая репликация существующих ledgers обязательна параллельно
любой новой физике. Она повышает научный статус математических результатов,
но не меняет `N_closed_physical`.

### EW/QCD и flavour computations

Их следует временно использовать только как blind endpoints. Новые threshold
scans, Yukawa maps и low-energy fits до parent-action pass имеют высокий риск
повторения уже закрытых маршрутов.

## Рекомендуемый порядок продолжения

### Фаза 0: заморозка границы Version V

Создать короткую preregistration/specification без вычисленных observed
numbers. В ней выбрать ровно одну primary architecture, один comparison
class, один measure и два blind endpoints.

### Фаза 1: два коротких архитектурных спринта

1. Carrier sprint: решить, может ли parent principle однозначно фиксировать
   sign и finite gravitational/topological weights.
2. Boundary sprint: проверить, может ли один minimal trace вывести
   fixed-charge sector, condensate и family axis.

Это не означает развитие двух Version V одновременно. Цель спринтов —
получить по одному бинарному architecture gate, после чего выбрать один
survivor.

### Фаза 2: один полный Hessian

Для выбранной архитектуры вычислить off-shell Hessian, gauge quotient,
ghost/Jacobian factors и BV/BRST complex. До этого момента запрещены mass,
CKM, coupling и absolute-scale claims.

### Фаза 3: normalization theorem

Показать, что один measure фиксирует минимум два независимых sector weights.
Если второй sector требует нового коэффициента, архитектура не проходит.

### Фаза 4: blind physics

Только после предыдущих фаз выполнить RG и раскрыть две preregistered
dimensionless observables из независимых sectors. Провал одной из них не
ремонтируется внутри той же версии.

## Итоговая приоритизация

| Приоритет | Путь | Почему | Условие немедленной остановки |
|---|---|---|---|
| 1 | Carrier-first / TOE 6.5 | атакует главный common-measure и vacuum-selection gap | sign или finite topology weights остаются свободными |
| 2 | Boundary-source / Wilson--defect | наиболее конкретные reusable modules и короткий parent gate | fixed-charge, condensate или axis требуют отдельного input |
| 3 | New finite geometry | ближе всего к observed representation и scalar vacuum | menu не имеет конечной классификации либо Hessian сохраняет kernel |
| 4 | Affine selector / formal bridge | полезные supporting theorems | попытка выдать classification за physical prediction |

## Expected result

После выполнения предложенной последовательности проект должен либо:

- получить одну действительно новую Version V architecture с prior measure,
  устойчивым physical Hessian и двумя blind endpoints; либо
- быстро и честно закрыть оставшиеся классы, сохранив математическое ядро как
  самостоятельный результат.

Оба исхода научно сильнее продолжения численных совпадений без общего
functional origin.

## Compliance check

- Выводы согласованы с финальным gate Тома IV и его machine ledger.
- Закрытые маршруты не переоткрываются без явного изменения архитектуры.
- Положительные mathematical modules отделены от physical closure.
- Для каждого открытого пути указан первый falsifiable kill-gate.
- Рекомендация сохраняет требования Version V: one architecture, one
  measure, full Hessian/BV, two blind observables, external reproduction.

## Links

- [[version5-problem-statement-gate]] — формальная постановка Тома V и Gate V.0.
- [[version4-tome-conclusion]] — итоговый статус и граница Version V.
- [[version4-observed-reconstruction-roadmap]] — хронология Тома IV.
- [[project-retrospective-source-audit-2026-08-11]] — незавершённая TOE 6.5 route.
- [[project-negative-space-audit-2026-08-11]] — omissions и full-field determinant.
- [[version4-one-kernel-sign-trilemma-gate]] — несовместимость двух sign readings.
- [[version4-gaussian-bare-spectral-topology-gate]] — conditional bare topology measure.
- [[version4-old-problem-rotation-audit]] — readiness и cross-clue старых ветвей.
- [[version4-family-defect-ko6-quiver-embedding-gate]] — positive KO6 embedding и wrong-sign quartic.
- [[version4-family-defect-degree-two-junk-gate]] — closure ordinary calculus route.
- [[version4-family-defect-relative-auxiliary-moment-gate]] — auxiliary/HS sign problem.
- [[pati-salam-project-wide-rescue-archaeology]] — Pati--Salam rescue scope.
- [[formalize-common-source]] — аксиоматическая задача общего источника.

## Source Notes

- `s2t/gates/version4_tome_conclusion.tex`
- `s2t/results/s2t_v4_tome_conclusion_results.json`
- `s2t/gates/version4_project_retrospective_entropy_measure_gate.tex`
- `s2t/gates/version4_full_field_carrier_counterterm_gate.tex`
- `s2t/gates/version4_gaussian_bare_spectral_topology_gate.tex`
- `s2t/gates/version4_one_kernel_sign_trilemma_gate.tex`
- `s2t/gates/version4_old_problem_rotation_audit.tex`
- `s2t/gates/version4_family_defect_fermionic_measure_hs_gate.tex`
- `s2t/gates/version4_pati_salam_rank_one_connected_curvature_no_go.tex`
- `s2t/docs/version4_observed_closure_specification.tex`