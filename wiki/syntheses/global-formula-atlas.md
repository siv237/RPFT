# Глобальный атлас ключевых формул Томов I--VII

> Status: working
> Type: synthesis
> Updated: 2026-08-26

## Назначение и область охвата

Это каноническая формульная карта проекта для изучения математической и
физической интуиции. Она собирает итоговые формулы, которые пережили
заключения, заморозки и ретроспективные аудиты Томов I--VII, а также точные
no-go тождества, ограничивающие их смысл.

Атлас не копирует каждую промежуточную строку сотен гейтов. Единицей отбора
служит формула, которая:

1. вошла в итоговый статус тома или глобальный ledger;
2. является точным тождеством, теоремой внутри объявленной модели либо
   ключевой пересмотренной формулой;
3. имеет самостоятельную интуитивную роль;
4. снабжена первичным источником и ссылками на её позднейшее чтение.

Доказательные статусы берутся из [[global-theorem-and-no-go-ledger]].
Происхождение формул до томов и ранние альтернативные ветви вынесены в
[[pre-tome-formula-genealogy]], а полный механический список их вхождений — в
[[pre-tome-formula-source-index]].

## Легенда

| Метка | Значение |
|---|---|
| **Строго** | математическое утверждение не зависит от физической интерпретации |
| **Строго внутри модели** | точное следствие объявленного носителя или действия |
| **Условно** | требуется невыведенная нормировка, мера, масштаб или физическая карта |
| **Пересмотрено** | формула сохранена, но её прежняя роль сужена |
| **No-go** | точное тождество или расчёт запрещает заявленный вывод в данном классе |
| **Норма программы** | правило проверки, а не закон природы |

---

## I. Язык единого источника и устойчивости описаний

### I-F1. Инвариантное ядро при слабой деформации

$$
\mathcal I(\delta\mathfrak S)\simeq\mathcal I(\mathfrak S),
\qquad
\mathcal R_{\mathrm{type}}(\delta\mathfrak S)
=\mathcal R_{\mathrm{type}}(\mathfrak S).
$$

**Статус:** норма программы.

**Интуиция:** смена координат, базиса или масштаба чтения не должна создавать
новую физику. Новый язык считается описанием того же объекта только тогда,
когда сохраняются его инварианты и тип редукции.

**Вхождения:**

- `s2t/docs/tome1/03_deformations_dynamics_and_compression.tex`;
- `s2t/docs/tome1/01_invariant_kernel_and_structural_regimes.tex`;
- [[tome1-s2t-research-program]];
- [[tome1-to-tome2-traceability]].

### I-F2. Квазидействие как методический, а не физический поток

$$
\mathcal A_{\mathrm q}[\mathfrak S]
=\mathcal A_{\mathrm{inv}}
+\mathcal A_{\mathrm{reg}}
+\mathcal A_{\mathrm{sel}},
\qquad
\frac{d\mathfrak S}{dt}
=-\nabla\mathcal A_{\mathrm q}[\mathfrak S].
$$

**Статус:** условная схема Тома I.

**Интуиция:** можно организовать поиск как спуск по штрафу за потерю
инвариантов, выход из допустимого класса и ухудшение модели. Но этот параметр
`t` не является физическим временем, пока не выведены метрика, мера и энергия.

**Вхождения:**

- `s2t/docs/tome1/05_status_axioms_lemmas_and_quasi_action.tex`;
- [[tome1-s2t-research-program]];
- [[global-theorem-and-no-go-ledger]].

---

## II. Геометрия, спектральные формулы и условные наблюдаемые мосты

### II-F1. Геометрическое ядро

$$
K=\mathbb{RP}^3\times S^1,
\qquad
S_{\mathrm{geo}}=4\pi^3+\pi^2+\pi.
$$

**Статус:** геометрическая комбинация сохранена; физическое чтение отдельных
слагаемых требует заявленной нормировки.

**Интуиция:** три геометрических вклада сжимаются в одно безразмерное число:
объёмный, факторизационный/голономный и спиновый циклический каналы.

**Вхождения:**

- `s2t/docs/tome2_s2t_spectral_closure.tex`;
- `corpus/S2T_FINAL_PAPER.md`;
- [[tome2-s2t-spectral-closure]];
- [[tome2-proof-chain]];
- [[theorem-status-ledger-2026-08-04]].

### II-F2. Примитивный цикл Грама

$$
Q_{\mathrm{cycle}}=\operatorname{diag}(\pi,\pi^{-1}),
\qquad
\|Q_{\mathrm{cycle}}\|_{\mathrm{sd}}=\pi+\pi^{-1}.
$$

**Статус:** строго для выбранного примитивного цикла.

**Интуиция:** прямой и двойственный масштабы входят парой; самодвойственная
норма минимально хранит оба направления, не выбирая одно из них.

**Вхождения:**

- `s2t/gates/version4_project_retrospective_entropy_measure_gate.tex`;
- `s2t/gates/version4_tome2_red_door_reverse_audit.tex`;
- [[global-theorem-and-no-go-ledger]];
- [[theorem-status-ledger-2026-08-04]].

### II-F3. Спектральное вакуумное число

$$
S_{\mathrm{vac}}
=S_{\mathrm{geo}}
-\frac{1}{24S_{\mathrm{geo}}}
-\frac{1}{\pi^4S_{\mathrm{geo}}^2}
=137.035999173522\ldots
$$

**Статус:** пересмотрено. Числовое воспроизведение сохраняется;
`S_geo` устойчив, ветвь `1/24` условна, а обязательное происхождение полного
$\pi^{-4}$-остатка из одной Maxwell--ghost схемы не доказано.

**Интуиция:** большое геометрическое ядро получает две малые спектральные
поправки. Точность числа не заменяет доказательства того, что обе поправки
обязаны происходить из одного физического определителя.

**Вхождения:**

- `corpus/S2T_FINAL_PAPER.md`;
- `s2t/docs/tome2_s2t_spectral_closure.tex`;
- [[tome2-svac-em-block-audit]];
- [[global-falsification-closure-audit]];
- [[global-theorem-and-no-go-ledger]].

### II-F4. Ко-точный спектральный контроль

$$
\lambda_n=(n+1)^2,
\qquad
d_n^{S^3}=2n(n+2).
$$

На факторпространстве $\mathbb{RP}^3$ остаётся соответствующая
паритетно-разрешённая часть башни.

**Статус:** строго для спектрального оператора и выбранной проекции.

**Интуиция:** факторизация меняет не локальные собственные значения, а меню
допустимых мод и их кратности. Это важнее простого деления объёма пополам.

**Вхождения:**

- `s2t/docs/tome2_s2t_spectral_closure.tex`;
- [[tome2-svac-em-block-audit]];
- [[theorem-status-ledger-2026-08-04]].

### II-F5. Заряженно-лептонная связь

$$
\rho_0=\pi^2+2\pi+\frac23,
\qquad
\frac{m_\tau}{m_\mu}=\rho_0-\frac{\alpha}{3}.
$$

**Статус:** условно. Формула уникальна в замороженной малосложной грамматике,
но операторное происхождение нормировки проекции не закрыто.

**Интуиция:** три ортогональных геометрических канала дают Gram-норму, а
компактная поправка действует аддитивно на оператор перехода. Слабое место —
не арифметика, а обязательность выбранного оператора и коэффициента.

**Вхождения:**

- `s2t/docs/tome2_s2t_spectral_closure.tex`;
- [[tau-formula-uniqueness-normalization]];
- [[pi-arithmetic-magnet-gate]];
- [[theorem-status-ledger-2026-08-04]].

### II-F6. Нейтринная коллективная норма

$$
\|\boldsymbol\Xi_\nu\|^2=23+\pi^{-1}.
$$

**Статус:** строго внутри канонической graded-superconnection
configuration metric; условно как физический массовый знаменатель.

**Интуиция:** ранг тяжёлого подпространства и дефектная циклическая линия
складываются в одной ненормированной метрике. Другой спектральный kernel не
обязан сохранять те же веса.

**Вхождения:**

- `s2t/docs/tome2_s2t_spectral_closure.tex`;
- `s2t/gates/family_connection_defect_gap_bridge.tex`;
- `s2t/gates/version3_role_graded_hessian_gate.tex`;
- [[global-theorem-and-no-go-ledger]].

### II-N1. Ранг сам по себе не является массовым знаменателем

Для $M_H=M_*P_H$ и нормированного $w\in\operatorname{im}P_H$:

$$
w^TM_H^+w=\frac1{M_*}.
$$

Для ненормированного democratic-вектора ранга 23:

$$
w_{\mathrm{dem}}^TM_H^+w_{\mathrm{dem}}=\frac{23}{M_*},
\qquad
\log\det{}'M_H=23\log M_*.
$$

**Статус:** точный no-go.

**Интуиция:** размерность пространства появляется либо в числителе
ненормированной суммы, либо как кратность логарифма определителя, но не
автоматически как собственное значение $23M_*$.

**Вхождения:**

- `s2t/docs/tome2_s2t_spectral_closure.tex`;
- [[current-status-and-next-vectors]];
- [[global-theorem-and-no-go-ledger]].

---

## III. Одношкальная скрытая U(1)-теория

### III-F1. Нормировки, вакуум и спектр

$$
\kappa=2,
\qquad
g^2=\frac38,
$$

$$
|x|=|z|=\frac{\chi}{\sqrt2},
\qquad
\arg(xz)=\pm\frac\pi2,
$$

$$
m_s^2=4\chi^2,
\qquad
m_f=\chi,
\qquad
m_A^2=3\chi^2.
$$

**Статус:** строго внутри замороженной Version III.H.

**Интуиция:** одно действие фиксирует все безразмерные отношения, а один
размерный вход $\chi$ задаёт общую шкалу. Две CP-сопряжённые ветви остаются
точно вырожденными.

**Вхождения:**

- `s2t/docs/version3_final_status_freeze.tex`;
- `s2t/gates/version3_a4_gauge_coupling_gate.tex`;
- `s2t/gates/version3_dimensional_product_consistency_gate.tex`;
- [[version3-final-status-freeze]].

### III-F2. Положительный Coleman--Weinberg seed

$$
N_0=67,
\qquad
B_0=\frac{67}{64\pi^2}>0.
$$

**Статус:** строго внутри модели.

**Интуиция:** знак однопетлевого коэффициента следует из полного счёта
физических нулевых мод, а не выбирается вручную.

**Вхождения:**

- `s2t/docs/version3_final_status_freeze.tex`;
- `s2t/gates/version3_base_k_spectral_renormalization_gate.tex`;
- `s2t/gates/version3_a4_gauge_coupling_gate.tex`;
- `s2t/docs/version4_observed_closure_specification.tex`.

### III-N1. Точное прямое суммирование не создаёт портал

$$
\Gamma_{\mathrm{unif}}
\not\longrightarrow
\{S_{\mathrm{vac}},\Gamma_{\mathrm{hidden}},
\Gamma_{\mathrm{EW/QCD}},\Gamma_\nu\}
$$

для замороженного минимального direct-sum completion.

**Статус:** no-go архитектуры III.H.

**Интуиция:** математически согласованные блоки, поставленные рядом, остаются
разными теориями, если нет состояний или операторов, несущих оба заряда.

**Вхождения:**

- `s2t/docs/version3_final_status_freeze.tex`;
- [[version3-final-status-freeze]];
- [[global-theorem-and-no-go-ledger]].

---

## IV. Конечная геометрия и семейные структуры

### IV-F1. Минимальный кватернионный baseline

$$
\mathcal A_F
=\mathbb C\oplus\mathbb H\oplus M_3(\mathbb C).
$$

**Статус:** строго внутри restricted finite-algebra class.

**Интуиция:** комплексный, кватернионный и цветовой матричный блоки являются
минимальной конечной алгеброй, способной нести локальную gauge-алгебру СМ
после центрального ограничения.

**Вхождения:**

- `s2t/gates/version4_tome_conclusion.tex`;
- [[version4-tome-conclusion]];
- [[version4-observed-reconstruction-roadmap]].

### IV-F2. Pati--Salam determinant identity

$$
\|\delta_h(D_\Delta^2)\|^2
=4\det(\Delta\Delta^\dagger).
$$

**Статус:** строго внутри объявленной конечной геометрии.

**Интуиция:** норма вариации ребра считывает площадь/ранг через определитель,
связывая дифференциальную геометрию графа с алгебраической невырожденностью.

**Вхождения:**

- `s2t/gates/version4_tome_conclusion.tex`;
- связанные Pati--Salam-гейты `s2t/gates/version4_pati_salam_*.tex`;
- [[version4-tome-conclusion]].

### IV-F3. Аффинный семейный триплет

$$
P_1=\frac14J_4,
\qquad
P_3=I-P_1,
\qquad
\operatorname{rank}P_3=3.
$$

**Статус:** строго как конечномерное разложение.

**Интуиция:** четыре аффинные метки распадаются на равномерный синглет и
трёхмерный относительный сектор. Число три здесь является рангом носителя,
а не доказанным числом поколений.

**Вхождения:**

- `s2t/gates/version4_affine_family_carrier_gate.tex`;
- `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex`;
- `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex`;
- [[version4-tome-conclusion]].

### IV-F4. Разложение средней и бесследовой кривизны

$$
\frac13\Tr(XX^T-|\Phi|^2I_3)^2
=\left(|\Phi|^2-\frac13\Tr XX^T\right)^2
+\frac13\Tr\left(XX^T-\frac13\Tr(XX^T)I_3\right)^2.
$$

**Статус:** точное тождество.

**Интуиция:** отклонение матрицы от скалярного состояния ортогонально
разделяется на ошибку среднего размера и анизотропную бесследовую часть.

**Вхождения:**

- `s2t/gates/version4_tome_conclusion.tex`;
- `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex`;
- [[version4-tome-conclusion]].

### IV-F5. Точная трёхцикловая голономия

Для четырёх тетраэдрических направлений и ориентации $\nu=\pm1$:

$$
\mathcal A_{a,\nu}
=-\frac{2\pi\nu}{3L}\Omega(h_a)\,ds,
$$

$$
\operatorname{Hol}_\gamma(\mathcal A_{a,\nu})
=\exp\left[-\nu\frac{2\pi}{3}\Omega(h_a)\right]
=C_{a,\nu}.
$$

**Статус:** строго.

**Интуиция:** дискретный трёхцикл не назначается после вычисления, а является
точной голономией плоской связности, построенной из того же проекторного
направления.

**Вхождения:**

- `s2t/gates/version4_family_defect_holonomy_realization_gate.tex`;
- `s2t/gates/version4_family_defect_three_cycle_lock_gate.tex`;
- `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex`;
- [[version4-tome-conclusion]].

### IV-F6. KO6-колчан и скалярность pairing-ребра

$$
[Y,A]=0\quad\forall A\in M_3(\mathbb R)
\quad\Longrightarrow\quad
Y=\Phi I_3,
$$

$$
\dim_{\mathbb C}\mathcal H_F=18,
$$

$$
D_p=
\begin{pmatrix}
0&X^\dagger&0\\
X&0&\bar\Phi I_3\\
0&\Phi I_3&0
\end{pmatrix},
\qquad
D_F=D_p\oplus\bar D_p.
$$

При этом

$$
D_F=D_F^\dagger,
\qquad
\{D_F,\Gamma_F\}=0,
\qquad
[D_F,J_F]=0,
\qquad
\{J_F,\Gamma_F\}=0.
$$

**Статус:** строго на алгебраическом уровне finite spectral triple.

**Интуиция:** условие первого порядка действует как лемма Шура и запрещает
произвольную семейную матрицу на pairing-ребре; Real/KO6-завершение удваивает
цепочку сопряжённо, не добавляя свободную flavour-структуру.

**Вхождения:**

- `s2t/gates/version4_family_defect_ko6_quiver_embedding_gate.tex`;
- `s2t/gates/version4_family_defect_gauge_family_locking_gate.tex`;
- `s2t/gates/version4_family_defect_quiver_moment_map_gate.tex`;
- [[version4-tome-conclusion]].

### IV-N1. Нулевое физическое замыкание

$$
N_{\mathrm{closed\ physical}}=0.
$$

**Статус:** итоговый no-go Тома IV, а не отсутствие математических
результатов.

**Интуиция:** ни один построенный блок одновременно не прошёл представления,
единое действие, нормировки, RG и два независимых blind-теста.

**Вхождения:**

- `s2t/gates/version4_tome_conclusion.tex`;
- [[version4-tome-conclusion]];
- [[global-theorem-and-no-go-ledger]].

---

## V. Real/KO-класс, индекс и нормированный дефект

### V-F1. Суперразмерность и класс пятнадцать

$$
\frac{20-15}{35}=\frac17,
\qquad
(20-15)\,3=15,
$$

$$
\kappa_{15}=15
\in KO_6(M_{105}(\mathbb C)_{\mathbb R}).
$$

**Статус:** строго в коэффициентной архитектуре Тома V.

**Интуиция:** разность двух неравноранговых углов становится стабильным
коэффициентным классом после семейной кратности три. Это класс перехода, а не
число частиц события.

**Вхождения:**

- `s2t/docs/version5_final_conclusion_and_next_program.tex`;
- `s2t/gates/version5_one_seventh_k0_bridge_gate.tex`;
- `s2t/gates/version5_real_toeplitz_kr_classification_gate.tex`;
- [[version5-final-conclusion-and-next-program]].

### V-F2. Явный Real-унитарий и ориентированные индексы

$$
V_{15}(z)=
\left(zq_0+1-q_0,
z^{-1}\overline{q_0}+1-\overline{q_0}\right),
$$

$$
\operatorname{wind}(V_{15})=(+15,-15).
$$

**Статус:** строго.

**Интуиция:** Real-объект хранит две сопряжённые ориентации. Их обычные
индексы сокращаются глобально, но каждая ветвь локально остаётся ненулевой.

**Вхождения:**

- `s2t/gates/version5_real_toeplitz_ko7_unitary_representative_gate.tex`;
- `s2t/docs/version5_post_conclusion_architecture_decision.tex`;
- `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex`;
- [[version5-final-conclusion-and-next-program]].

### V-F3. Индексная нижняя граница и дефект 1/7

$$
\dim\ker T+\dim\operatorname{coker}T\ge15,
$$

$$
\delta_{\mathrm{cl}}=\frac{15}{105}=\frac17,
\qquad
\frac{15+15}{105+105}=\frac17.
$$

**Статус:** строго в фиксированном ориентированном секторе.

**Интуиция:** ненулевой индекс запрещает совершенную обратимость. Деление на
полный коэффициентный ранг превращает минимальное число отсутствующих
направлений в нормированный дефект.

**Вхождения:**

- `s2t/gates/version5_topological_closure_deficit_gate.tex`;
- `s2t/gates/version5_one_seventh_toeplitz_boundary_map_gate.tex`;
- `s2t/docs/version5_final_conclusion_and_next_program.tex`;
- `s2t/docs/version6_introduction_and_problem_statement.tex`;
- [[global-theorem-and-no-go-ledger]].

### V-F4. Хопфова Real-пара

$$
c_1(L)=+1,
\qquad
c_1(L^*)=-1,
$$

после коэффициентного умножения:

$$
(c_1,[q_0])\longmapsto(+15,-15).
$$

**Статус:** строго.

**Интуиция:** геометрическая ориентация линии и коэффициентный внутренний
класс умножаются, связывая пространственный дефект с Real-парой.

**Вхождения:**

- `s2t/docs/version5_final_conclusion_and_next_program.tex`;
- `s2t/gates/version5_hopf_pair_odd_core_extension_gate.tex`;
- `s2t/gates/version5_real_toeplitz_bott_comparison_map_gate.tex`;
- [[version5-final-conclusion-and-next-program]].

### V-N1. Минимум внутри сектора не запускает материю

$$
\mathcal S_{\mathrm{loop}}(I)=0,
\qquad
\min_{\operatorname{wind}=15}\mathcal S_{\mathrm{loop}}=\frac17.
$$

**Статус:** точная граница.

**Интуиция:** $1/7$ — минимальная цена уже выбранного ненулевого сектора, но
абсолютный нулевой вакуум дешевле. Топология классифицирует материю, не
заставляя её родиться.

**Вхождения:**

- `s2t/docs/version5_final_conclusion_and_next_program.tex`;
- `s2t/gates/version5_toeplitz_parent_action_variational_gap_gate.tex`;
- [[global-theorem-and-no-go-ledger]].

### V-N2. Наблюдательная условность

$$
O\subset M,
\qquad
\mathbb P(M\mid O)=1,
$$

но

$$
\mathbb P(M\mid O)=1
\centernot\Longrightarrow
\mathbb P(M)=1.
$$

**Статус:** строгая логическая граница.

**Интуиция:** всякий внутренний наблюдатель требует устойчивой материальной
памяти, но это ничего не говорит о безусловной мере нематериальных историй.

**Вхождения:**

- `s2t/docs/version5_final_conclusion_and_next_program.tex`;
- [[matter-inevitability-and-observer-conditioning]];
- [[transition-primitive]];
- [[global-theorem-and-no-go-ledger]].

---

## VI. Фазовый переход, поле порядка и локализованные решения

### VI-F1. Проекторный статический функционал и спинодаль

$$
R(a)=\operatorname{diag}\left(a,\frac{1-a}{2},\frac{1-a}{2}\right),
$$

$$
\mathcal F_\beta(a)=S(a)+\beta E(a),
$$

$$
S(a)=a\log a+(1-a)\log\frac{1-a}{2},
$$

$$
q_2(a)=\frac{3a^2-2a+1}{2},
\qquad
q_3(a)=\frac{3a^3+3a^2-3a+1}{4},
$$

$$
E(a)=\frac27\left(1-\frac{q_2(a)^2}{q_3(a)}\right)+1-q_2(a),
$$

$$
\left.\frac{\partial^2\mathcal F_\beta}{\partial a^2}\right|_{a=1/3}
=\frac92-\frac{3\beta}{7},
\qquad
\boxed{\beta_{\mathrm{sp}}=\frac{21}{2}}.
$$

Точка равновесного перехода внутри модели:

$$
\beta_c=1.5426695409\ldots
$$

**Статус:** строго для указанного статического функционала.

**Интуиция:** первый порядок и спинодаль различны: глобальный минимум меняется
раньше, чем локальная кривизна изотропной ветви становится отрицательной.

**Вхождения:**

- `s2t/gates/version6_modular_cooling_projective_transition_gate.tex`;
- [[version6-modular-cooling-projective-transition-gate]];
- [[formal-verification-and-palomar-roadmap]];
- `formalization_candidates/spinodal_threshold/`.

### VI-F2. Бозонное поле порядка и вакуумная орбита

$$
Q(x)=R(x)-\frac{I_3}{3},
\qquad
Q^T=Q,
\qquad
\Tr Q=0,
$$

$$
\mathcal M_{\mathrm{vac}}=SO(3)/O(2)=\mathbb{RP}^2.
$$

Локальный спектр в упорядоченном фоне:

$$
\operatorname{Spec}\Hess_{R_*}\mathcal F
=\{4.5081528\ldots,
17.8845270\ldots,17.8845270\ldots,0,0\}.
$$

**Статус:** строго внутри статической модели.

**Интуиция:** пять компонент симметричной бесследовой матрицы распадаются на
три массивные деформации формы и две безмассовые моды вращения директора.

**Вхождения:**

- `s2t/gates/version6_projective_order_parameter_field_spectrum_gate.tex`;
- [[version6-projective-order-parameter-field-spectrum-gate]];
- [[version6-final-conclusion-and-next-program]].

### VI-F3. Топологическое меню дефектов поля Q

$$
\pi_1(\mathbb{RP}^2)=\mathbb Z_2,
\qquad
\pi_2(\mathbb{RP}^2)=\mathbb Z,
\qquad
\pi_3(\mathbb{RP}^2)=\mathbb Z.
$$

**Статус:** строго.

**Интуиция:** одна вакуумная орбита допускает линейные дисклинации, точечные
ежи и хопфовы текстуры. Группа гомотопий доказывает класс конфигураций, но не
массу, радиус или квантовую статистику.

**Вхождения:**

- `s2t/gates/version6_projective_order_parameter_field_spectrum_gate.tex`;
- `s2t/gates/version6_spatial_projective_defect_energy_spectrum_gate.tex`;
- [[version6-projective-order-parameter-field-spectrum-gate]];
- [[global-theorem-and-no-go-ledger]].

### VI-F4. Двухузловой compacton

$$
\|\ell\|^2=|e|^2=\frac14,
\qquad
a=\|\ell\|\,|e|=\frac14,
$$

$$
\cos(\kappa a)=0
\quad\Longrightarrow\quad
\boxed{\kappa_m=2(2m+1)\pi},
$$

$$
\Psi_0=|{-}\rangle\otimes v,
\qquad
\Psi_1=|{+}\rangle\otimes i(-1)^m v,
\qquad
F_{\kappa_m}(\Psi)=i\Psi.
$$

При $\kappa=2\pi(1+\varepsilon)$:

$$
P_{\mathrm{leak}}
=\sin^2\left(\frac{\pi\varepsilon}{2}\right).
$$

**Статус:** строго как точное конечноподдержанное решение.

**Интуиция:** нелинейная монета полностью переворачивает два встречных
хиральных блока, а сдвиг замыкает их на двух узлах. Дискретность связи не
доказывает устойчивость орбиты.

**Вхождения:**

- `s2t/gates/version6_spectral_transition_discrete_compacton_existence_gate.tex`;
- [[version6-spectral-transition-discrete-compacton-existence-gate]];
- [[formal-verification-and-palomar-roadmap]];
- `formalization_candidates/compacton_two_site_existence/`.

### VI-F4a. Тождество граничных классов Каллиаса и Тёплица

Для положительного собственного проектора массы

$$
P_+(n)=\frac{I_2+n\cdot\sigma}{2}
$$

северная и южная карты на экваторе связаны формулой

$$
v_N=e^{i\varphi}v_S,
\qquad
g_L(z)=z,
\qquad
c_1(L)=\operatorname{wind}(g_L)=1.
$$

После умножения на проектор $q_0$ ранга 15:

$$
g_{15}(z)=zq_0+1-q_0=V_+(z),
\qquad
\operatorname{wind}\det g_{15}=15.
$$

Индексы согласуются с ориентационным знаком:

$$
\operatorname{ind}\mathcal D_{\mathrm{Callias}}=15,
\qquad
\operatorname{ind}T_{g_{15}}=-15.
$$

**Статус:** строго как тождество граничного $K$-класса; физический
спинорный носитель из конечного родителя остаётся условным.

**Интуиция:** пространственный ёж и Toeplitz-петля оказываются двумя
описаниями одной функции склейки, а не просто двумя вычислениями одного
целого числа.

**Вхождения:**

- `s2t/gates/version6_callias_toeplitz_index_comparison_gate.tex`;
- `s2t/gates/version6_composite_connection_callias_fredholm_gate.tex`;
- `s2t/gates/version5_real_toeplitz_ko7_unitary_representative_gate.tex`;
- [[version6-callias-toeplitz-index-comparison-gate]];
- [[global-theorem-and-no-go-ledger]].

### VI-F5. C4-характерная чистота

$$
U_4=
\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\qquad U_4^2=-I,
\qquad U_4^4=I,
$$

$$
P_{\pm i}=\frac14\sum_{n=0}^3(\pm i)^{-n}U_4^n,
$$

$$
\mathcal D_\chi(\Psi)
=1-|\langle\Psi,U_4\Psi\rangle|^2
=4w_+w_-\ge0.
$$

$$
\mathcal D_\chi=0
\quad\Longleftrightarrow\quad
U_4\Psi=\pm i\Psi.
$$

**Статус:** строго на точном $F^2=-1$-многообразии.

**Интуиция:** дефект измеряет не энергию, а смешанность двух характеров.
Ноль означает чистую ориентацию четырёхтактного цикла.

**Вхождения:**

- `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex`;
- [[version6-spectral-transition-compacton-c4-affine-selector-admissibility-gate]];
- [[formal-verification-and-palomar-roadmap]];
- `formalization_candidates/c4_unitary_weight_preservation/`.

### VI-N1. Унитарная C4-динамика не очищает характер

Если $T$ унитарен и $[T,U_4]=0$, то

$$
w_\pm(T\Psi)=w_\pm(\Psi),
\qquad
\mathcal D_\chi(T\Psi)=\mathcal D_\chi(\Psi).
$$

**Статус:** точный no-go.

**Интуиция:** симметричная когерентная эволюция умеет различать сектора, но
не умеет переносить вероятность между ними. Для очистки нужна открытая,
измерительная, шумовая или нелинейно несохраняющая веса структура.

**Вхождения:** те же, что у VI-F5.

### VI-F6. Радиационная спектральная плотность

$$
\rho_{\mathrm{rad}}(0)
=\frac1{2\pi}\sum_{4k=0}
\frac{\|\widehat r_1(k)\|^2}{4}
=2\pi,
$$

$$
\Gamma_{\mathrm{cycle}}
=2\pi\rho_{\mathrm{rad}}(0)|\delta|^2
=4\pi^2|\delta|^2.
$$

**Статус:** строго как норма исходящего пакета; пересмотрено как физическая
скорость или охлаждение.

**Интуиция:** $4\pi^2$ возникает как произведение фазового пространства и
точной спектральной плотности, но канал истощает всё compacton-ядро, а не
очищает его до одной ветви.

**Вхождения:**

- `s2t/gates/version6_spectral_transition_discrete_compacton_character_resolved_radiation_form_factor_gate.tex`;
- `s2t/gates/version6_spectral_transition_real_pair_radiative_cooling_parent_gate.tex`;
- [[version6-spectral-transition-discrete-compacton-character-resolved-radiation-form-factor-gate]];
- [[version6-final-conclusion-and-next-program]].

### VI-F7. Внутренняя щель прямой бозонной нити

После удаления двух переносных нулевых мод:

$$
\Delta_{\mathrm{int}}=3.61933633,
$$

$$
\Delta_{\mathrm{next}}=3.6649900191,
\qquad
\Delta_{\mathrm{next}}-\Delta_{\mathrm{int}}
=0.0456536888>0.
$$

**Статус:** строго как континуальный предел проверенного полного поперечного
тензорно-калибровочного гессиана.

**Интуиция:** симметрийные нули отвечают свободному переносу центра, а первая
настоящая внутренняя деформация отделена положительной щелью. Это доказывает
линейную устойчивость прямого профиля, но не замкнутого кольца.

**Вхождения:**

- `s2t/gates/version6_bosonic_defect_full_tensor_internal_gap_gate.tex`;
- `s2t/gates/version6_bosonic_defect_full_tensor_high_angular_coercivity_gate.tex`;
- [[version6-bosonic-defect-full-tensor-internal-gap-gate]];
- [[version6-final-conclusion-and-next-program]].

### VI-N2a. Спокойное кольцо сжимается

Ведущее действие мировой поверхности:

$$
S_0=-T\int d^2\sigma\sqrt{-\gamma},
\qquad
T=1.5744530783.
$$

Для статического кольца:

$$
E_0(R)=2\pi TR,
\qquad
\frac{dE_0}{dR}=2\pi T>0.
$$

**Статус:** точный no-go в контролируемом нулемодовом приближении.

**Интуиция:** поперечно устойчивая нить не становится частицей после простого
замыкания: натяжение монотонно уменьшает радиус. Нужен выведенный ток,
топологический поворот или ответ массивных мод.

**Вхождения:**

- `s2t/gates/version6_bosonic_defect_curved_string_effective_action_gate.tex`;
- `s2t/gates/version6_bosonic_defect_full_tensor_internal_gap_gate.tex`;
- [[version6-bosonic-defect-curved-string-effective-action-gate]];
- [[global-theorem-and-no-go-ledger]].

### VI-N2. Масштабное нулевое направление

$$
\frac{a}{\Delta t}=c,
\qquad
E\Delta t=\frac{\pi\hbar}{2},
$$

$$
(a,\Delta t,E)
\longmapsto
(\lambda a,\lambda\Delta t,E/\lambda),
$$

$$
L=2a,
\qquad
\boxed{EL=\pi\hbar c},
\qquad
\frac{L}{\lambda_C}=\pi.
$$

**Статус:** точное условное произведение и точный no-go абсолютного масштаба.

**Интуиция:** скорость и квазиэнергетическая фаза дают две связи для трёх
размерных величин. Они фиксируют произведение энергии и размера, но оставляют
одну непрерывную гомотетию.

**Вхождения:**

- `s2t/gates/version6_spectral_transition_discrete_compacton_physical_scale_map_gate.tex`;
- [[version6-spectral-transition-discrete-compacton-physical-scale-map-gate]];
- [[global-theorem-and-no-go-ledger]].

### VI-N3. Финальная незамкнутая динамическая цепочка

$$
I\longrightarrow T_{\mathrm{sing}}
\longrightarrow(V_{15},V_{-15}).
$$

**Статус:** открытая целевая цепочка; отрицательно закрыта для архитектуры
Тома VI как автономный процесс.

**Интуиция:** классифицированы начальный, переходный и дефектный типы, но они
не являются решениями одного действия с одним временем и одной мерой.

**Вхождения:**

- `s2t/docs/version6_final_conclusion_and_next_program.tex`;
- `s2t/docs/version6_introduction_and_problem_statement.tex`;
- [[version6-final-conclusion-and-next-program]];
- [[version6-spectral-transition-post-radiative-bridge-final-dynamic-status-gate]].

---

## VII. Рангоизменяющий общий родитель

### VII-F1. Фундаментальное поле и производный порядок

$$
E_{\mathrm{aff}}
=\operatorname{Hom}(\mathbb C^4,\operatorname{im}P_3),
\qquad
\Phi(x)\in\Gamma(X,E_{\mathrm{aff}}\widehat\otimes
\mathcal Y_{\mathrm{phys}}),
$$

$$
R_\Phi
=\frac{\Tr_{\mathcal Y_{\mathrm{phys}}}(\Phi\Phi^*)}
{\Tr(\Phi\Phi^*)},
\qquad
Q_\Phi=R_\Phi-\frac13I_3.
$$

**Статус:** определение нового родительского кандидата; общий носитель
предварительно проходит входной тест `P0`.

**Интуиция:** семейная ось и ранг больше не задаются проектором до динамики.
Они читаются из одного хирально, пространственно и Real-типизированного поля.
Нормированное состояние существует только вне нулевой страты, тогда как само
поле и действие определены также в вакууме.

**Вхождения:**

- `s2t/docs/version7_introduction_and_problem_statement.tex`;
- [[version7-rank-change-parent-program]];
- [[version7-rank-changing-superconnection-admission-gate]].

### VII-F2. Единая кривизностная энергия и вакуумный гессиан

$$
\mathcal S_7[\Phi,\nabla_X]
=\int_X\operatorname{tr}_{\mathrm{norm}}
(\mathbb F_\Phi^*\mathbb F_\Phi)d\mu_X,
$$

$$
\Hess_0\mathcal S_7(\eta,\eta)
=2\|L_0\eta\|^2
+4\operatorname{Re}\langle\mathbb F_0,\widehat\eta^2\rangle.
$$

**Статус:** точная вариационная формула внутри нового кандидата; `P1`
предварительно пройден, `P2` сделан вычислимым, но знак полного физического
гессиана ещё не установлен.

**Интуиция:** положительная кинетическая часть не может сама запустить
переход. Возможная отрицательная мода обязана происходить из нецентральной
кривизны того же родителя, а не из добавленной после результата массы.

**Вхождения:**

- `s2t/docs/version7_introduction_and_problem_statement.tex`;
- `s2t/gates/version7_rank_changing_superconnection_admission_gate.tex`;
- [[version7-rank-changing-superconnection-admission-gate]].

### VII-N1. Плоский ранговый суррогат стабилен

$$
\Hess_0\mathcal S_7=\frac87I_{24}>0.
$$

**Статус:** строгий конечномерный отрицательный контроль.

**Интуиция:** наличие ранговых страт ещё не является механизмом рождения.
Если полный родитель не даст отрицательную моду, Том VII остановится до
локализованных решений и наблюдаемой карты.

**Вхождения:**

- `s2t/gates/version7_rank_changing_superconnection_admission_gate.tex`;
- `s2t/audits/s2t_v7_rank_changing_superconnection_admission_gate.py`;
- `s2t/results/s2t_v7_rank_changing_superconnection_admission_gate_results.json`;
- [[version7-rank-changing-superconnection-admission-gate]].

### VII-N2. Развилка стационарности чистой нормы кривизны

$$
\left.\frac{d\mathcal S_7}{dt}\right|_{t=0}
=4\operatorname{tr}_{\mathrm{norm}}(D_F^4)>0
\qquad(D_F\ne0),
$$

$$
\Hess_0\mathcal S_7(\eta,\eta)
=2\|L_0\eta\|^2\ge0.
$$

**Статус:** строгий no-go для первого чистого кривизностного родителя
Тома VII.

**Интуиция:** ненулевой конечный оператор нельзя одновременно считать
фиксированным фоном и стационарным нулевым полем. Если же весь оператор
сделать динамическим, исчезает источник отрицательной моды. Поэтому следующий
кандидат обязан заранее выводить стационарный ненулевой фон, а не исправлять
действие после вычисления.

**Вхождения:**

- `s2t/gates/version7_full_physical_rank_field_hessian_gate.tex`;
- `s2t/audits/s2t_v7_full_physical_rank_field_hessian_gate.py`;
- `s2t/results/s2t_v7_full_physical_rank_field_hessian_gate_results.json`;
- [[version7-full-physical-rank-field-hessian-gate]].

### VII-F3. Хиральная Hodge-неустойчивость и rank-7 минимум

$$
\mathcal S_{\rm ch}(Y)
=\frac1{15}\Tr_{H_{15}}
\left([d_Y,d_Y^\dagger]-\Gamma_{15}\right)^2,
$$

$$
\mathcal S_{\rm ch}(Y)
=\frac1{15}\left[1+2\sum_{j=1}^7(1-\sigma_j^2)^2\right]
\ge\frac1{15},
$$

$$
\Hess_0\mathcal S_{\rm ch}=-\frac8{15}I_{112},
\qquad
YY^\dagger=I_7,
\qquad
\dim_{\mathbb C}\ker Y=1.
$$

**Статус:** строгий положительный результат для хирального ядра
$H_L^{8}\to H_R^{7}$; полный аффинно-семейный подъём открыт.

**Интуиция:** градуировка создаёт отрицательную квадратичную часть, а тот же
квадрат коммутатора создаёт положительное квартетное насыщение. Неравенство
хиральных размерностей запрещает обратимость и оставляет одну ядерную линию
без заранее выбранного проектора.

**Вхождения:**

- `s2t/gates/version7_chiral_hodge_index_instability_gate.tex`;
- `s2t/audits/s2t_v7_chiral_hodge_index_instability_gate.py`;
- `s2t/results/s2t_v7_chiral_hodge_index_instability_gate_results.json`;
- [[version7-chiral-hodge-index-instability-gate]].

### VII-F4. Исправленный трёхпоколенный подъём

Исходный тензорный носитель сокращается с

$$
E_{\rm aff}\otimes\mathcal E_\rho\otimes\Lambda_{\rm ch}
$$

до минимального ковариантного поля

$$
\Psi\in E_{\rm aff}\otimes\Lambda_{\rm ch},
\qquad
\dim_{\mathbb C}\Psi=36.
$$

Канонический подъём имеет физические ранги

$$
P_L=P_3\otimes I_8,
\qquad
\rank P_L=24,
\qquad
\dim(\operatorname{im}P_3\otimes H_R)=21,
$$

и функционал

$$
\mathcal S_{\rm lift}(Z)
=\frac1{45}\left[
3+2\sum_{j=1}^{21}(1-\sigma_j^2)^2
\right]\ge\frac1{15}.
$$

Для $Z_\star=V\otimes Y_\star$:

$$
\rank Z_\star=21,
\qquad
\ker Z_\star
=(\operatorname{im}P_1\otimes H_L)
\oplus(\operatorname{im}P_3\otimes\ker Y_\star),
\qquad
11=8+3.
$$

**Статус:** строгий типизационный и линейно-алгебраический проход после
коррекции носителя. Полный Real/junk/BRST--BV гессиан открыт.

**Интуиция:** динамический аффинный модуль должен заменять локальный tangent
при выбранном $\rho$, а не умножаться на него. После удаления двойного
семейного счёта одномерное ядро одного поколения автоматически становится
тремя линиями на каноническом аффинном триплете.

**Вхождения:**

- `s2t/gates/version7_affine_physical_module_canonical_lift_gate.tex`;
- `s2t/audits/s2t_v7_affine_physical_module_canonical_lift_gate.py`;
- `s2t/results/s2t_v7_affine_physical_module_canonical_lift_gate_results.json`;
- [[version7-affine-physical-module-canonical-lift-gate]].

### VII-F5. Устойчивый, но неизолированный endpoint

Для трёх независимых физических рёбер

$$
X_a=U_aV,
\qquad U_a\in U(3),
$$

поэтому

$$
\mathcal M_{\rm vac}=U(3)_u\times U(3)_d\times U(3)_e,
\qquad
\dim_{\mathbb R}\mathcal M_{\rm vac}=27.
$$

Физический обобщённый гессиан равен

$$
\Spec(G^{-1}\Hess)=
\left\{
0^{(27)},
\left(\frac4{45}\right)^{(18)},
\left(\frac{16}{45}\right)^{(27)}
\right\}.
$$

Даже после общего семейного факторирования остаётся

$$
\dim\frac{U(3)^3}{U(3)_{\rm diag}}=18,
\qquad
\dim\frac{O(3)^3}{O(3)_{\rm diag}}=6.
$$

**Статус:** строгая поперечная устойчивость и строгий no-go изолированного
endpoint для текущего блочно-диагонального функционала.

**Интуиция:** действие фиксирует длины и ранги трёх рёбер, но не видит углы
между их семейными кадрами. Поэтому матрицы относительной ориентации
существуют как координаты вакуума, но не предсказываются.

**Вхождения:**

- `s2t/gates/version7_corrected_vacuum_relative_edge_hessian_gate.tex`;
- `s2t/audits/s2t_v7_corrected_vacuum_relative_edge_hessian_gate.py`;
- `s2t/results/s2t_v7_corrected_vacuum_relative_edge_hessian_gate_results.json`;
- [[version7-corrected-vacuum-relative-edge-hessian-gate]].

### VII-F6. Нулевая прямая межрёберная вторая степень

Для одного общего нормированного хиггсовского дублета

$$
\widetilde H=i\sigma_2\overline H,
\qquad
H^\dagger\widetilde H=0.
$$

Физические кромки и их аффинные подъёмы удовлетворяют

$$
T_aT_b^\dagger=T_a^\dagger T_b=0,
\qquad
D_aD_b^\dagger=D_a^\dagger D_b=0,
\qquad a\ne b.
$$

Поэтому

$$
D^\dagger D=\sum_aD_a^\dagger D_a,
\qquad
DD^\dagger=\sum_aD_aD_a^\dagger,
\qquad
[d,d^\dagger]=\sum_a[d_a,d_a^\dagger].
$$

**Статус:** строгий no-go для прямой физической common-Higgs кривизны
второй степени. Полный сырой универсальный калькулюс с произвольными
нуль-форменными вставками не объявлен классифицированным.

**Интуиция:** junk не обязан объяснять исчезновение смешивания: нужные
прямые слова уже равны нулю, а физический бимодульный коммутант трёх рёбер
диагонален. Первый оставшийся уровень межрёберной чувствительности является
квартичным или более высоким.

**Вхождения:**

- `s2t/gates/version7_common_higgs_degree_two_cross_edge_gate.tex`;
- `s2t/audits/s2t_v7_common_higgs_degree_two_cross_edge_gate.py`;
- `s2t/results/s2t_v7_common_higgs_degree_two_cross_edge_gate_results.json`;
- [[version7-common-higgs-degree-two-cross-edge-gate]].

### VII-F7. Полиномиальное разложение и квартичная константа

Из ортогональности кромок для любого $n\ge1$ следует

$$
\Tr(D^\dagger D)^n
=\sum_a\Tr(D_a^\dagger D_a)^n,
\qquad
\Tr(DD^\dagger)^n
=\sum_a\Tr(D_aD_a^\dagger)^n.
$$

На коизометрическом вакууме

$$
X_a=U_aV,
\qquad
\Tr(D^\dagger D)^2+\Tr(DD^\dagger)^2=42
$$

при любых $U_u,U_d,U_e\in U(3)$.

Family-only матрица

$$
W_{ab}=X_aX_b^\dagger=U_aU_b^\dagger
$$

видит относительный кадр, но требует внедиагонального сокращения меток,
тогда как

$$
\operatorname{End}_{\mathcal A_{\rm SM}-\mathcal A_{\rm SM}}
(\Lambda_{\rm ch})\simeq\mathbb C^3.
$$

**Статус:** строгий no-go для любого обычного односледового полиномиального
повышения степени на неизменённом физическом носителе.

**Интуиция:** относительная геометрия математически видима после забывания
физических меток, но именно операция забывания вставляет недостающий
коннектор. Настоящий смешанный след требует нового замкнутого пути в
физическом графе.

**Вхождения:**

- `s2t/gates/version7_quartic_cross_edge_invariant_admission_gate.tex`;
- `s2t/audits/s2t_v7_quartic_cross_edge_invariant_admission_gate.py`;
- `s2t/results/s2t_v7_quartic_cross_edge_invariant_admission_gate_results.json`;
- [[version7-quartic-cross-edge-invariant-admission-gate]].

### VII-F8. Минимальное прямоугольное дополнение H15

Текущий заряженный граф имеет вершины

$$
L=\{Q_L,L_L\},\qquad R=\{u_R,d_R,e_R\},
$$

и рёбра

$$
E_0=\{Q_Lu_R,Q_Ld_R,L_Le_R\}.
$$

Первый четырёхцикл требует двух новых рёбер. Единственное дополнение одним
комплексным скалярным мультиплетом равно

$$
R_2\sim(\mathbf3,\mathbf2)_{7/6},
\qquad
\overline Q_LR_2e_R+
\overline u_RR_2^Ti\sigma_2L_L+\mathrm{h.c.}
$$

**Статус:** строгая классификация минимального графового и калибровочного
кандидата. Не является допуском нового поля: полный Real/первый порядок,
спектральное действие и цветовой вакуум открыты.

**Интуиция:** относительный семейный угол не появляется от повышения степени
старого дерева. Чтобы след впервые увидел путь между разными рёбрами, нужно
сначала замкнуть настоящий цикл; минимальная цена на прежних фермионных
вершинах — две сопряжённые лептокварковые стрелки.

**Вхождения:**

- `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex`;
- `s2t/audits/s2t_v7_minimal_h15_mixed_connector_admission_gate.py`;
- `s2t/results/s2t_v7_minimal_h15_mixed_connector_admission_gate_results.json`;
- [[version7-minimal-h15-mixed-connector-admission-gate]].

---

## Сквозная карта интуиции

| Идея | Формульные узлы |
|---|---|
| Один объект должен переживать смену языка | I-F1, I-F2 |
| Геометрия задаёт меню и нормировки, но не гарантирует физическое чтение | II-F1--II-F6 |
| Ранг и красивое число не заменяют оператор | II-N1, IV-N1 |
| Одно действие действительно связывает отношения только внутри своей модели | III-F1, III-F2 |
| Прямое суммирование не является взаимодействием | III-N1 |
| Проекторы разделяют синглет и относительные направления | IV-F3, VI-F5 |
| Индекс измеряет неизбежную необратимость внутри ненулевого сектора | V-F2, V-F3 |
| Топология не запускает переход из нулевого сектора | V-N1 |
| Поле порядка создаёт пространство дефектов | VI-F1--VI-F3 |
| Точная локализация не равна устойчивой частице | VI-F4, VI-F6 |
| Симметричная унитарность сохраняет смесь | VI-N1 |
| Безразмерная фаза не фиксирует абсолютный масштаб | VI-N2 |
| Ранг должен быть свойством одного физического поля, а не выбранной целью | VII-F1 |
| Эндогенный запуск требует заранее выведенного стационарного фона | VII-F2, VII-N1, VII-N2 |
| Хиральная размерностная асимметрия может дать запуск и защищённое ядро одним квадратом | VII-F3 |
| Аффинный триплет поднимает одну ядерную линию в три без повторного семейного множителя | VII-F4 |
| Поперечная устойчивость не означает выбора смешивания на плоском endpoint | VII-F5 |
| Общий Хиггс и обычная вторая степень не создают межрёберный класс | VII-F6 |
| Повышение степени без нового коннектора сохраняет разложение по рёбрам | VII-F7 |
| Первый смешанный цикл требует новой типизированной стрелочной пары | VII-F8 |

## Что ещё требуется добавить

Атлас покрывает канонические формулы итоговых заключений и глобального
реестра. Следующие расширения должны выполняться отдельными проходами, не
смешиваясь с этим строгим ядром:

1. полный покомпонентный операторный каталог тензорного гессиана бозонной
   нити, превышающий уровень итоговой щели;
2. наблюдательные формулы Тома II с полным разделением train/blind;
3. промежуточные, но переиспользуемые формулы второй вариации C6;
4. семантическая классификация полного [[live-formula-source-index]]:
   механический слой уже завершён (4804 формулы из 427 файлов), а
   [[formula-equivalence-and-status-index]] пока закрывает точные повторы
   и консервативные сопоставления с каноническими formula-id.
   [[formula-semantic-atlas-matches]] восстановил тридцать
   formula-id, но полный корпус ещё не сгруппирован по произвольным заменам
   обозначений и нормировок вне канонического атласа.

Эти пункты являются задачами расширения атласа. Они не меняют статусы уже
внесённых формул.

## Связи

- [[global-theorem-and-no-go-ledger]]
- [[formula-equivalence-and-status-index]]
- [[formula-semantic-atlas-matches]]
- [[formal-verification-and-palomar-roadmap]]
- [[treatise-volume-systematics]]
- [[theorem-status-ledger-2026-08-04]]
- [[current-status-and-next-vectors]]