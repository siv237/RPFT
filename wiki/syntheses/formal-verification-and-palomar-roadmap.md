# Формальная верификация и маршрут к Palomar

> Status: working
> Type: synthesis
> Updated: 2026-09-01

## Назначение

Проект сохраняет действующий процесс LLM-вики, LaTeX-гейтов и вычислительных
аудитов, но добавляет промежуточный слой точных спецификаций для будущей
формализации на Lean. Это не замена физического исследования и не
автоматическое повышение доказательного статуса: спецификация отделяет
математическое ядро результата от интерпретации, численного свидетельства и
открытых физических выводов.

## Структура

- `formalization_candidates/` — человекочитаемые Markdown-контракты;
- `formalization_candidates/_template/` — обязательная форма нового задания;
- `formal/` — будущие Lean-проекты, challenge/solution и метаданные;
- `s2t/proofdsl/` — исполняемый LCF-подобный промежуточный слой для точной
  проверки конечномерных объектов до переноса в Lean;
- `wiki/syntheses/global-theorem-and-no-go-ledger.md` — источник статуса,
  который формализация не вправе самовольно повышать.

Каждый кандидат содержит точное утверждение, определения, предпосылки, карту
первичных источников, список неутверждений и план разбиения на леммы.

## Первая очередь

| Кандидат | Математическое ядро | Текущий статус |
|---|---|---|
| `spinodal_threshold` | `F_beta''(1/3)=9/2-3 beta/7`, порог `21/2` | `spec-frozen` |
| `compacton_two_site_existence` | ряд `kappa_m` и собственное состояние `F Psi=i Psi` | `candidate` |
| `c4_unitary_weight_preservation` | сохранение `w_±` и `D_chi` унитарным коммутирующим шагом | `spec-frozen` |

Компакттонный кандидат ещё не заморожен: полное определение нелинейной монеты
должно быть перенесено из первичного гейта в самодостаточную спецификацию.

## Формульный реестр первой очереди

Ниже формулы выписаны непосредственно в вики, чтобы страница оставалась
читаемой без перехода к LaTeX-гейтам или заданиям формализации. Это полный
набор ключевых формул **первых трёх кандидатов**, а не полный каталог всех
формул Томов I--VII.

### 1. Точный спинодальный порог

Одноосная семья состояний:

$$
R(a)=\operatorname{diag}\!\left(a,\frac{1-a}{2},\frac{1-a}{2}\right),
\qquad 0<a<1.
$$

Свободная энергия и энтропийная часть:

$$
\mathcal F_\beta(a)=S(a)+\beta E(a),
\qquad
S(a)=a\log a+(1-a)\log\frac{1-a}{2}.
$$

Рациональные инварианты и энергетическая часть:

$$
q_2(a)=\frac{3a^2-2a+1}{2},
\qquad
q_3(a)=\frac{3a^3+3a^2-3a+1}{4},
$$

$$
E(a)=\frac{2}{7}\left(1-\frac{q_2(a)^2}{q_3(a)}\right)+1-q_2(a).
$$

Точная кривизна в изотропной точке:

$$
\left.\frac{\partial^2\mathcal F_\beta}{\partial a^2}
\right|_{a=1/3}
=\frac92-\frac{3\beta}{7}.
$$

Отсюда следует точный порог смены знака ограниченной кривизны:

$$
\boxed{\beta_{\mathrm{sp}}=\frac{21}{2}=10.5}.
$$

Это не доказательство устойчивости по всем направлениям поля и не
динамическая теорема о распаде.

### 2. Двухузловой compacton

Сбалансированный внутренний вектор удовлетворяет

$$
v=(\ell,e),
\qquad
\|\ell\|^2=|e|^2=\frac14,
\qquad
\|v\|^2=\frac12.
$$

Активная частота равна

$$
a=\|\ell\|\,|e|=\frac14.
$$

Условие полного переворота и дискретный ряд связей:

$$
\cos(\kappa a)=0,
\qquad
\kappa a=\frac{(2m+1)\pi}{2},
$$

$$
\boxed{\kappa_m=2(2m+1)\pi},
\qquad m=0,1,2,\ldots,
\qquad \kappa_0=2\pi.
$$

При $s_m=(-1)^m$ двухузловой профиль задаётся формулами

$$
\Psi_0=|{-}\rangle\otimes v,
\qquad
\Psi_1=|{+}\rangle\otimes i s_m v,
\qquad
\Psi_n=0\quad(n\ne0,1).
$$

Для дискретного шага первичного гейта выполняется

$$
F_{\kappa_m}(\Psi)=i\Psi,
$$

а комплексно-сопряжённая ветвь имеет собственную фазу $-i$. При расстройке
$\kappa=2\pi(1+\varepsilon)$ одношаговая утечка равна

$$
P_{\mathrm{leak}}
=\sin^2\!\left(\frac{\pi\varepsilon}{2}\right).
$$

Формулы доказывают точное существование орбиты внутри заданной модели, но не
её нелинейную устойчивость, физический масштаб или идентификацию с частицей.

### 3. Характерный C4-селектор и унитарный запрет очистки

Редуцированный четырёхтактный шаг:

$$
U_4=
\begin{pmatrix}
0&-1\\
1&0
\end{pmatrix},
\qquad
U_4^2=-I,
\qquad
U_4^4=I.
$$

Проекторы характеров $\pm i$:

$$
P_{\pm i}=\frac14\sum_{n=0}^{3}(\pm i)^{-n}U_4^n,
\qquad
\operatorname{rank}P_{\pm i}=1.
$$

Для нормированного состояния:

$$
w_\pm=\langle\Psi,(P_{\pm i}\otimes I_3)\Psi\rangle,
\qquad
w_++w_-=1.
$$

Коэффициент-свободный дефект характерной чистоты:

$$
\mathcal D_\chi(\Psi)
=1-\left|\langle\Psi,(U_4\otimes I_3)\Psi\rangle\right|^2
=4w_+w_-\ge0.
$$

Его нулевое множество состоит ровно из двух ветвей:

$$
\mathcal D_\chi(\Psi)=0
\quad\Longleftrightarrow\quad
F\Psi=+i\Psi\ \text{или}\ F\Psi=-i\Psi,
$$

что в блочной записи эквивалентно

$$
v_R=\pm i v_L.
$$

Если линейный унитарный шаг $T$ коммутирует с $U_4$, то он коммутирует с
$P_{\pm i}$ и сохраняет

$$
w_\pm(T\Psi)=w_\pm(\Psi),
\qquad
\mathcal D_\chi(T\Psi)=\mathcal D_\chi(\Psi).
$$

Поэтому $C_4$-эквивариантная унитарная динамика не может очистить смешанный
характер до одной из ветвей $\pm i$. Запрет не распространяется автоматически
на открытую, неунитарную или нелинейную динамику.

## Полнота выписки

- Формулы первой очереди: **выписаны в вики**.
- Спецификации первой очереди: **созданы**.
- Полный механический формульный каталог живого корпуса Томов I--VII:
  **создан**, см. [[live-formula-source-index]]. Семантическая классификация
  всего корпуса остаётся незавершённой.
- Lean-проверка: **ещё не выполнялась**.

## Исполняемый LCF-прототип

На 29 августа 2026 года добавлен первый работающий слой
[[lcf-proof-edsl]]. Его доверенное Python-ядро единолично создаёт значения
`Theorem`, а SymPy-проверки не допускают `Float`. Реальный no-go Тома VIII
переписан без SVD: разложение endpoint- и transfer-представлений по
изотипическим блокам точно даёт

$$
 \dim\operatorname{Hom}_G(E,T)=13,
 \qquad
 \max_{J\in\operatorname{Hom}_G(E,T)}\rank J=9<20.
$$

Это новый статус `lcf-checked`, расположенный между `spec-frozen` и
`lean-draft`. Он означает воспроизводимую точную проверку малым ядром, но не
формальную верификацию самого ядра. Z3 пока возвращает только solver evidence
и не имеет права повышать утверждение до `Theorem`.

Интеграционный гейт [[version8-lcf-proofdsl-architecture-gate]] добавил
повторно используемый `GateSpec`, реестр и CLI. В реестре уже восемь
результатов и пятьдесят четыре обязательства: no-go полнорангового коннектора,
спинодальный порог `21/2`, точная двухмерная неподвижная алгебра,
linking-GKSL, gauge-twirl Kraus-мост, его parent-action, полярная
cross-ковариация и минимальная Stinespring-дилатация.

На 1 сентября 2026 года реестр расширен до `57` гейтов и `455`
обязательств. Первый перенос Version 9 —
[[version9-endpoint-creation-kms-relative-shape-selector-source-minimal-invariant-parent-architecture-gate]] —
проверяет десятью kernel-theorems algebraic core invariant logdet parent:
weighted trace/determinant, stationary gradient, spectra constrained и
log-ratio Hessian, doubled rank `4` и full rank/determinant
`12/(5184/25)`. Глобальная weighted AM–GM-лемма пока остаётся вне kernel.

Второй перенос Version 9 —
[[version9-endpoint-creation-kms-relative-shape-logdet-parent-measure-origin-gate]] —
проверяет determinant degrees `5/10`, exact effective signs и
coordinate-Jacobian no-go. Berezin/Gaussian integration identities остаются
внешними леммами; kernel сертифицирует только их algebraic consequences.

Третий перенос Version 9 —
[[version9-endpoint-creation-kms-logdet-auxiliary-fermion-module-admission-gate]] —
проверяет functorial carrier dimension `10`, complementary package
projectors `5+5`, odd parity, family covariance, physical decoupling и
rank `20` Berezin pairing. Происхождение Grassmann statistics остаётся
вне kernel и вынесено в следующий origin-гейт.

Четвёртый перенос Version 9 —
[[version9-endpoint-creation-kms-logdet-auxiliary-fermion-statistics-parent-origin-gate]] —
перебирает все tensor-product gradings, доказывает odd ranks `2,5,5,8`,
package-swap restriction и rank-two defect ближайшего candidate. Paired
Berezin Jacobian cancellation также проверена точно; BRST origin parity
остаётся внешней структурной задачей.

Пятый перенос Version 9 —
[[version9-endpoint-creation-kms-logdet-minimal-brst-complex-architecture-gate]] —
проверяет nilpotent quartet matrix `40x40`, rank/nullity `20/20`,
ghost-number degree, parity, zero cohomology, FP determinant rank `10`
и annihilation physical inclusion. Origin shift gauge symmetry не входит
в LCF-утверждение и остаётся следующим гейтом.

Шестой перенос Version 9 —
[[version9-endpoint-creation-kms-logdet-brst-shift-symmetry-parent-origin-gate]] —
проверяет rank `10` required translation map, rank/cokernel `6/4` KMS
tangent, shape rank `4`, phase nullity `1` и zero type/transport
tangents. Positive rank-ten Hessian exact нарушает full translation.

Седьмой перенос Version 9 —
[[version9-endpoint-creation-kms-logdet-minimal-stueckelberg-shift-parent-architecture-gate]] —
проверяет rank-ten orbit, rank-ten quotient, Hessian rank/nullity `10/10`,
orbit-kernel equality, positive spectrum и exact cancellation
`det D_aux/(det D_aux)=1`.

Восьмой перенос Version 9 —
[[version9-endpoint-creation-kms-logdet-physical-fermion-loop-parent-origin-gate]] —
проверяет rank `5` physical target, single/target determinant degrees
`5/10`, Real lift square, exchange mismatch rank `10`, а также exact
determinants conditional doubled и composite kernels.

Девятый перенос Version 9 —
[[version9-endpoint-creation-kms-logdet-minimal-fermion-bath-architecture-gate]] —
проверяет carrier/coupling ranks `10/5`, exact Schur complement, positive
witness spectrum `{1^(5),3^(5)}`, determinants `243/1024` и zero-coupling
target face.

Гейт [[version8-linking-qms-gksl-lcf-migration-gate]] закрыл этот приоритет
на конечномерном уровне. Trace-preservation исчерпывающе проверено на
`441` матричной единице, инвариантность и явная формула endpoint-алгебры —
на `221` элементах, а `dim Fix=41` следует из точного ранга `180` системы
`220x221`. Открытая формальная граница теперь локализована: правило
полной положительности GKSL входит в доверенное Python-ядро, но ещё не имеет
независимого Choi/Kraus или Lean-сертификата.

Гейт [[version8-gauge-twirl-kraus-lcf-migration-gate]] закрыл следующий
приоритет. Вместо двенадцати случайных преобразований проверено точное
замыкание 12 jump-направлений под восемью генераторами `su(3)`, тремя
`su(2)` и гиперзарядом. Индуцированные матрицы действия кососимметричны,
их общее ядро нулевое, а квадратичная Kraus-сумма независима от любого
ортогонального выбора базиса. Центральная матрица имеет характеристический
многочлен `lambda(lambda-7/3)` и одномерное ядро при любых положительных
скоростях.

Гейт [[version8-kraus-bridge-parent-action-lcf-migration-gate]] затем
заменил конечный scan веса символом `lambda_bridge>=0`. На полном диапазоне
точно сохраняются сигнатуры `(7,0,20)` и `(0,0,27)`, а полевая добавка имеет
гессиан `7 I12/18`. При этом в классическом вакууме одновременно исчезают
энергия, градиент и все коэффициенты `z_a^2` GKSL-генератора. Следующий
приоритет — внутреннее происхождение ненулевой cross-ковариации.

Гейт [[version8-cross-arrow-covariance-lcf-migration-gate]] реализовал
первую точную проверку проекта в нетривиальном алгебраическом поле
`Q(sqrt(2),2 cos(pi/7))`. Полярная коизометрия проверена без SVD; полный
cross-блок равен `I6 tensor B`, а сцепление с оставшимися 15 модами равно
нулю. Пара `B` положительна и имеет два различных собственных значения,
поэтому все `(32/5)I+2 eta B` при `eta>0` имеют одну ось. Неточность теперь
локализована не в угле, а в `eta` и масштабе меры.

Гейт [[version8-minimal-covariant-stinespring-lcf-migration-gate]] закрыл
конечномерную часть следующего приоритета. Спектр Gram-оператора точно равен
`{0^9,1^6,2^3,3^2,6}`, поэтому Kraus-карта существует при `0<=p<=1/6`.
Её Choi/Kraus-ранг и минимальная среда равны `13`; endpoint-инвариантность
проверена на `221` матричной единице. Производная в нуле даёт исходный
GKSL-генератор, но точный композиционный контрпример запрещает считать
конечное семейство полугруппой. Следующий приоритет — строгий collision-limit
и происхождение физического масштаба времени.

Гейт [[version8-intrinsic-noise-clock-lcf-migration-gate]] заменил
collision scan строгим конечномерным правилом Чернова. Полный рациональный
спектр на endpoint-алгебре имеет ядро `46`, щель `1/2` и максимум `8`.
Матричная экспонента образует безразмерную полугруппу, а
`Phi_(u/n)^n -> exp(uL)` в операторной норме. Модульные потоки центральных
состояний точно фиксируют секторные проекторы и не дают диссипацию.
Физический масштаб `kappa` остаётся вне вывода; следующий перенос — полный
примитивный Markov-генератор.

Гейт [[version8-full-primitive-markov-generator-lcf-migration-gate]] заменил
48 случайных весов доказательством для всего положительного конуса. Полный
процесс имеет 25 самосопряжённых jump-операторов, а пересечение базовой
`C^2` с cross-ядром равно `C I21`. Следовая обратимость выполняется для
каждого семейства отдельно и поэтому не выбирает скорости. Следующий
приоритет — нетривиальный KMS-селектор.

Гейт [[version8-page-wootters-stinespring-history-gate]] добавил точный
конечный history-слой над минимальной дилатацией. Для часов `0,1,2`
ветвевое частичное прослеживание совпадает с `Phi_*^n` без остатка, а
frustration-free history-parent имеет 21-мерное семейство стационарных
нулевых мод. При этом продолжение изометрии `C21 -> C273` до полного
унитарного такта оставляет дополнение размерности 252 и семейство `U(252)`;
LCF-успех не является выводом автономного Page--Wootters Hamiltonian.

Следующий [[version8-canonical-autonomous-clock-unitary-extension-no-go-gate]]
закрыл попытку получить этот Hamiltonian одним продолжением канала. Формула
`V_z=P_W+z(I-P_W)` сохраняет Stinespring-образ и тот же reduced channel;
ковариантность сохраняет всё `U(1)`-семейство, а Real-чётность оставляет
по меньшей мере `z=±1`. Положительный маршрут теперь обязан предъявить
микроскопическое взаимодействие или самостоятельное действие часов.

Гейт [[version8-microscopic-repeated-interaction-hamiltonian-gate]] выполнил
положительную часть этого требования. Звёздный `H_int` типизирован на
`C273`, самосопряжён и имеет правильную GKSL-касательную. Одновременно LCF-
коммутантный тест запретил преждевременную уникальность: две cross-семьи
образуют эквивалентные gauge-копии, поэтому допустимые самосопряжённые
interaction-связи имеют размерность `8`, а симметричные rate-метрики —
`4`. Совпадение с точным конечным
Kraus-шагом также прекращается после первого порядка.

Гейт [[version8-trace-dual-cross-interaction-selector-gate]] затем проверил
первый геометрический селектор оставшейся rate-свободы. Точная полевая
метрика полного `M_2x3(C)`-модуля равна `3I_12`; при отдельном принципе
«минимальная среда есть метрически двойственный модуль относительно того же
суперследа» получается `R=I_12/3`. Все `C=O/sqrt(3)` дают один reduced
channel после смены ортогонального кадра среды. Статус остаётся условным:
сам принцип двойственности, физический масштаб и веса остальных семейств
из родительского действия ещё не выведены.

Гейт [[version8-metric-dual-environment-parent-action-origin-gate]] провёл
эту проверку отрицательно. Parent-Hessian с bath-блоками `3I_12` и
`diag(3I_6,(3/2)I_6)` имеют один полевой блок и сохраняют gauge-типизацию,
но их rate-метрики не пропорциональны и дают разные генераторы. Поэтому
`K_BR=I` является точной минимальной спецификацией недостающего Riesz-
принципа, а не теоремой старого действия.

## Лестница статусов

```text
gate/result
  -> candidate
  -> spec-frozen
  -> lcf-checked
  -> lean-draft
  -> lean-verified
  -> palomar-ready
```

Переход требует всё более сильной проверки. Markdown не проверяется ядром
Lean. Статус `lean-verified` допустим только после воспроизводимой сборки без
`sorry` и недекларированных аксиом. Статус `palomar-ready` дополнительно
требует раздельных challenge/solution, метаданных и проверки Comparator.

## Граница утверждений

Формализуются сначала локальные математические результаты, а не весь трактат.
В частности:

- точная кривизна не равна доказательству рождения материи;
- существование двухузловой орбиты не равно её устойчивости или
  идентификации с частицей;
- сохранение характерных весов является запретом для заданного класса
  унитарной динамики, но не для всех открытых или нелинейных эволюций.

## Связи

- [[global-formula-atlas]]
- [[global-theorem-and-no-go-ledger]]
- [[version6-modular-cooling-projective-transition-gate]]
- [[version6-spectral-transition-discrete-compacton-existence-gate]]
- [[version6-spectral-transition-compacton-c4-affine-selector-admissibility-gate]]
