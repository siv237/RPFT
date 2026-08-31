# Глобальный атлас ключевых формул Томов I--VIII

> Status: working
> Type: synthesis
> Updated: 2026-08-31

## Назначение и область охвата

Это каноническая формульная карта проекта для изучения математической и
физической интуиции. Она собирает итоговые формулы, которые пережили
заключения, заморозки и ретроспективные аудиты Томов I--VIII, а также точные
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
кандидата. Последующий VII-N7 доказал, что этот кандидат не проходит
строгий первый порядок неизменённой конечной геометрии.

**Интуиция:** относительный семейный угол не появляется от повышения степени
старого дерева. Чтобы след впервые увидел путь между разными рёбрами, нужно
сначала замкнуть настоящий цикл; минимальная цена на прежних фермионных
вершинах — две сопряжённые лептокварковые стрелки.

**Вхождения:**

- `s2t/gates/version7_minimal_h15_mixed_connector_admission_gate.tex`;
- `s2t/audits/s2t_v7_minimal_h15_mixed_connector_admission_gate.py`;
- `s2t/results/s2t_v7_minimal_h15_mixed_connector_admission_gate_results.json`;
- [[version7-minimal-h15-mixed-connector-admission-gate]].

### VII-N7. Диагональное первопорядковое препятствие для $R_2$

Для блока между неприводимыми бимодулями условие первого порядка содержит

$$
[[D,a],JbJ^{-1}]_{ij,kl}
=(a_i-a_k)D_{ij,kl}(b_j-b_l),
$$

поэтому ненулевое ребро требует

$$
i=k\qquad\text{или}\qquad j=l.
$$

Но два ребра $R_2$ имеют вид

$$
(\mathbb H,\mathbb C)\to(\mathbb C,M_3),
\qquad
(\mathbb H,M_3)\to(\mathbb C,\mathbb C),
$$

то есть меняют обе координаты. Перестановка координат действием $J$ не
изменяет этот факт.

**Статус:** строгий no-go для стандартной алгебры и представления,
фиксированных вершин, обычной Real-структуры и строгого первого порядка.
Спектральное действие и цветовой вакуум этой ветви не достигнуты.

**Интуиция:** абстрактный граф хиральностей может нарисовать прямоугольник,
которого нет в диаграмме бимодулей. Физическая стрелка должна сначала
оказаться в одной строке или одном столбце полной диаграммы Краевского.

**Вхождения:**

- `s2t/gates/version7_r2_real_first_order_admission_gate.tex`;
- `s2t/audits/s2t_v7_r2_real_first_order_admission_gate.py`;
- `s2t/results/s2t_v7_r2_real_first_order_admission_gate_results.json`;
- [[version7-r2-real-first-order-admission-gate]].

### VII-F9. Минимальная архитектурная цена после $R_2$

Без первого порядка появляется квадратичная флуктуация
$$
D_A=D+A_{(1)}+\widetilde A_{(1)}+A_{(2)}.
$$
При сохранении строгого первого порядка полный перебор даёт
$$
N_{\rm new}^{\rm strict}=2,
\qquad
Q_L\to u_R\to X_L\to e_R\to L_L\to Y_R\to Q_L.
$$
**Статус:** строгая архитектурная классификация; ни одна физическая ветвь
ещё не выбрана.

**Вхождения:** `s2t/gates/version7_r2_minimal_architecture_branch_gate.tex`,
[[version7-r2-minimal-architecture-branch-gate]].

### VII-N9. Нулевой $A_{(2)}$ на допущенной опоре

Для исправленного поля
$$
D_{\mathrm{adm}}=\sum_{a=u,d,e}X_a\otimes T_a
$$
первый порядок факторизуется до семейного множителя и даёт
$$
[[X_a\otimes T_a,\pi(b)],\pi^o(c)]=0,
\qquad A_{(2)}[D_{\mathrm{adm}}]=0.
$$
Ненулевой $A_{(2)}$ появляется только после вставки запрещённого
$D_{R_2}$.

**Статус:** строгий no-go для вывода $R_2$ обобщённой флуктуацией из
текущего допущенного родителя. Явно новая модель без первого порядка не
исключена.

**Вхождения:** `s2t/gates/version7_r2_generalized_fluctuation_seed_origin_gate.tex`,
[[version7-r2-generalized-fluctuation-seed-origin-gate]].

### VII-N10. Аномальный запрет минимальной зеркальной пары

Каноническая двухвершинная пара имеет содержание
$$
X_L\sim(\mathbf1,\mathbf1)_{-1},\qquad
Y_R\sim(\mathbf1,\mathbf2)_{-1/2}.
$$
Её коэффициенты и глобальная чётность равны
$$
\mathcal A_{221}=\frac12,\qquad
\mathcal A_{111}=-\frac34,\qquad
N_{\mathbf2}^{\rm new}=1\pmod2.
$$
Произвольные заряды локально сокращаются только при $x=y=0$, но mod-2
препятствие остаётся. Вектороподобный ремонт требует также $X_R,Y_L$.

**Статус:** строгий no-go для двухвершинного физического admission;
четырёхвершинное завершение пока является новым кандидатом.

**Вхождения:** `s2t/gates/version7_minimal_mirror_pair_real_anomaly_gate.tex`,
[[version7-minimal-mirror-pair-real-anomaly-gate]].

### VII-P12. Безаномальный носитель с сохранённым хиральным индексом

Четырёхвершинное расширение имеет
$$
X_L,X_R\sim(\mathbf1,\mathbf1)_{-1},\qquad
Y_L,Y_R\sim(\mathbf1,\mathbf2)_{-1/2}
$$
и сохраняет индекс
$$
I_{\rm four\ vertex}=(1,-1,-1,1,-1)=I_{H_{15}}.
$$
Общие семейные массы оставляют
$$
\dim\ker M_e=3,\qquad \dim\ker M_L^*=3,
$$
но полный первопорядковый граф разрешает `11` новых блоков при `6` блоках
целевого ремонта.

**Статус:** условно положительный носитель; аномалии и индекс закрыты,
селектор рёбер и ориентации лёгкого ядра не выведен.

**Вхождения:** `s2t/gates/version7_four_vertex_vectorlike_selector_gate.tex`,
[[version7-four-vertex-vectorlike-selector-gate]].

### VII-N11. Копийная $U(2)$-орбита движет ядро при постоянном действии

Для прямоугольной массы
$$
P_{\ker M}=I_6-M^\dagger(MM^\dagger)^{-1}M
$$
и копийного вращения $M^U=M(U\otimes I_3)$ выполняется
$$
M^U(M^U)^\dagger=MM^\dagger,
\qquad
P_{\ker M^U}=(U\otimes I_3)^\dagger P_{\ker M}(U\otimes I_3).
$$
Одновременно
$$
[P_3\otimes I_2,I_4\otimes U]=0,
\qquad
I\otimes M_2(\mathbb C)\subset\pi(\mathcal A_{\rm SM})'.
$$

**Статус:** точный no-go для существующего аффинно-Hodge-родителя как
селектора старой/новой копии; его ранговый результат сохраняется.

**Вхождения:** `s2t/gates/version7_affine_hodge_copy_selector_no_go_gate.tex`,
[[version7-affine-hodge-copy-selector-no-go-gate]].

### VII-P13. Двухшаговая инцидентность условно выбирает паритет ядра

Для пары графовых близнецов с тремя общими соседями
$$
qA_{\max}^2q=3\begin{pmatrix}1&1\\1&1\end{pmatrix},
\qquad
S=\frac13qA_{\max}^2q-q=\sigma_x.
$$
Модулярный вес даёт на Hodge-орбите
$$
W_\beta(\theta)=\frac12(1-\tanh\beta\sin2\theta),
\qquad
W_\beta''(\pi/4)=2\tanh\beta>0.
$$

**Статус:** условно положительный селектор чётной/нечётной комбинации.
Каноничность максимальной бинарной инцидентности и физическая редукция
рёбер не выведены.

**Вхождения:**
`s2t/gates/version7_modular_copy_projector_origin_gate.tex`,
[[version7-modular-copy-projector-origin-gate]].

### VII-N12. Базисно-независимая инцидентность не создаёт обмен копий

Для независимых разрешённых стрелок
$$
|e_1\rangle\langle e_1|+|e_2\rangle\langle e_2|=I_2,
\qquad C_{\rm iso}=3I_2.
$$
Нецентральный обмен появляется только из когерентной суммы
$$
|e_1+e_2\rangle\langle e_1+e_2|=I_2+\sigma_x,
$$
причём относительная фаза вращает `sigma_x` по полной копийной орбите.

**Статус:** точный no-go для внутреннего вывода максимальной единичной
инцидентности из текущего представления и пространства всех допустимых
блоков. Требуется новый динамический конденсат когерентности стрелок.

**Вхождения:**
`s2t/gates/version7_universal_incidence_parent_admissibility_gate.tex`,
[[version7-universal-incidence-parent-admissibility-gate]].

### VII-P14. Ранга-один конденсат порождает копийный проектор

Для поля стрелочной когерентности `B in M_(2x3)(C)` выполняется точное
тождество
$$
\|W(B)\|_F^2=4\|\Lambda^2B\|_F^2=4\det(BB^\dagger).
$$
Поэтому потенциал
$$
\mathcal S_{\rm coh}(B)
=\left(\Tr BB^\dagger-3\right)^2+\|W(B)\|_F^2
$$
имеет нули ровно при `Tr(BB*)=3` и `rank B=1`. В нуле и в представителе
ненулевого вакуума полные вещественные спектры равны
$$
\Spec\Hess_0\mathcal S_{\rm coh}=\{-12\}^{\times12},
\qquad
\Spec\Hess_{B_0}\mathcal S_{\rm coh}
=\{0\}^{\times7}\cup\{24\}^{\times5}.
$$
При `B_*=sqrt(3)uv*` копийное состояние становится чистым:
$$
R_{\rm copy}=\frac{B_\star B_\star^\dagger}
{\Tr B_\star B_\star^\dagger}=uu^\dagger,
\qquad R_{\rm copy}^2=R_{\rm copy}.
$$

**Статус:** условно положительный эффективный потенциал. Геометрия
минимумов, запуск и поперечный гессиан закрыты; единая Real-градуированная
кривизность, выводящая радиальное и внешнеквадратное слагаемые с общей
нормировкой, не построена.

**Вхождения:**
`s2t/gates/version7_edge_coherence_rank_one_condensate_gate.tex`,
[[version7-edge-coherence-rank-one-condensate-gate]].

### VII-P15. Один спектральный полином выводит ранга-один потенциал

Для градуированной цепи комплексных размерностей `1 -> 6 -> 3` с
`A_B(1)=vec(B)` и `C_B=(1/2)d(Lambda^2)_B` выполняются
$$
C_BA_B=\Lambda^2B,
\qquad
\Tr\mathcal D_B^2=3T,
\qquad
\Tr\mathcal D_B^4=\frac94T^2+\frac{15}{4}d,
$$
где `T=Tr(BB*)` и `d=det(BB*)`. Следовательно,
$$
\frac49\left(
\Tr\mathcal D_B^4-\mu\Tr\mathcal D_B^2+\mu^2
\right)
=\left(T-\frac{2\mu}{3}\right)^2+\frac53d.
$$
При `mu=9/2` полный гессиан имеет спектры
$$
\Spec\Hess_0=\{-12\}^{\times12},
\qquad
\Spec\Hess_{B_0}
=\{0\}^{\times7}\cup\{10\}^{\times4}\cup\{24\}.
$$

**Статус:** положительный градуированный спектральный родитель. Ручная
норма миноров устранена, относительный коэффициент `5/3` выведен.
Строгая Real-бимодульная конечная тройка и абсолютный масштаб не выведены.

**Вхождения:**
`s2t/gates/version7_edge_coherence_spectral_parent_gate.tex`,
[[version7-edge-coherence-spectral-parent-gate]].

### VII-N13. Пространство стрелок не является физическим бимодулем

Для блока конечного оператора строгий первый порядок требует
$$
[[D,a],JbJ^{-1}]_{ij,kl}
=(a_i-a_k)D_{ij,kl}(b_j-b_l)=0.
$$
Над `C + H + M3(C)` единственный одномерный тип равен `(C,C)`, тогда как
шестимерные типы равны
$$
\mathcal H^{(6)}
\in\{(\mathbb H,M_3),(M_3,\mathbb H)\}.
$$
Общей координаты нет, поэтому неприводимых строгих цепей `1 -> 6 -> 3`
не существует. В фактическом носителе четыре кандидата имеют вид
$$
\{e_R,X_R\}\longrightarrow Q_L\longrightarrow\{u_R,d_R\},
$$
и каждый проваливается на первом ребре.

**Статус:** точный no-go для фермионного вложения спектральной цепи в
неизменённый носитель. Следовые тождества сохраняются на комплексе
пространства стрелок; его полевой суперсвязностный статус позднее закрыт
положительно в VII-P16.

**Вхождения:**
`s2t/gates/version7_edge_coherence_bimodule_admission_gate.tex`,
[[version7-edge-coherence-bimodule-admission-gate]].

### VII-P16. Полевой суперсвязностный носитель не требует новых фермионов

На ассоциированном градуированном пучке пространства стрелок

$$
E^0=\mathbb C,\qquad E^1=\operatorname{Hom}(W,V),\qquad
E^2=\operatorname{Hom}(\Lambda^2W,\Lambda^2V)
$$

ориентированная часть удовлетворяет

$$
d_B^2=\Lambda^2B,\qquad
\|d_B^2\|^2=\det(BB^\dagger),\qquad
\rank B\leq1\Longleftrightarrow d_B^2=0.
$$

Эрмитова часть сохраняет спектральный потенциал, а вариационная метрика
равна

$$
\Tr(\delta\mathcal D_B\,\delta\mathcal D_B)
=3\Tr(\delta B\,\delta B^\dagger).
$$

**Статус:** положительный вспомогательный полевой носитель. Новые
фермионные вершины и независимые калибровочные связности не требуются;
полный `U(3)` каналов не получает физического статуса. Открыта конкуренция
шести целевых и пяти остальных разрешённых рёбер.

**Вхождения:**
`s2t/gates/version7_edge_coherence_field_space_superconnection_gate.tex`,
[[version7-edge-coherence-field-space-superconnection-gate]].

### VII-N14. Ранг один несовместим с целевой графовой опорой

Внутри прямоугольника строк `(L_L,Y_L)` и столбцов `(e_R,X_R,Y_R)`
целевая маска имеет вид

$$
M_{\rm target}^{B}
=\begin{pmatrix}1&0&1\\0&0&1\end{pmatrix}.
$$

Для ненулевых требуемых амплитуд

$$
B_{\rm target}=\begin{pmatrix}a&0&b\\0&0&c\end{pmatrix},
\qquad
\det B_{\{e,Y\}}=ac\ne0,
\qquad
\rank B_{\rm target}=2.
$$

Поэтому условие вакуума `Lambda^2 B=0` не может сохранить точную целевую
опору. На ней действие равно

$$
\mathcal S_B=(x+y+z-3)^2+\frac53xz
$$

и не имеет стационарной точки при `xyz != 0`. Шесть новых рёбер вне `B`
остаются спектаторами, расширяя сигнатуру гессиана до `(0,19,5)`.

**Статус:** точный no-go для ранга-один когерентности как селектора
целевого шестирёберного ремонта. Вспомогательный суперсвязностный носитель
не отменён; следующий кандидат должен видеть цикл полного колчана.

**Вхождения:**
`s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex`,
[[version7-edge-coherence-full-graph-competition-gate]].

### VII-P17. Старый фон выделяет один примитивный шестикромочный цикл

Для взвешенного небэктрекингового оператора полного графа

$$
H(x)_{(a,b),(c,d)}=\delta_{bc}(1-\delta_{ad})x_{\{c,d\}}
$$

шестой след содержит четырнадцать простых циклов одинаковой кратности:

$$
\Tr H(x)^6=12\sum_{\mathcal C\in\mathfrak C_6}
\prod_{e\in\mathcal C}x_e.
$$

Но совместное укоренение на двух старых рёбрах `H15` даёт

$$
\mathcal R_6(x)
=12x_{Q_Lu_R}x_{u_RX_L}x_{X_Le_R}
x_{e_RL_L}x_{L_LY_R}x_{Y_RQ_L}.
$$

Это единственный примитивный шестикромочный цикл, проходящий через оба
корневых ребра. Типосохраняющая группа уменьшается с порядка четыре до
единицы после фиксации старой опоры.

**Статус:** точный положительный относительный наблюдаемый. Он выбирает
четыре новых циклических ребра, но не две вектороподобные массы. После
фиксации старого фона выражение имеет степень четыре по новым полям, поэтому
его квадратичный гессиан в нуле равен нулю. Полный динамический родитель не
получен.

**Вхождения:**
`s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex`,
[[version7-baseline-rooted-primitive-cycle-admission-gate]].

### VII-P18. Циклический и изотипический признаки дают точное меню

На пространстве одиннадцати новых стрелок циклический и изотипический
проекторы имеют ранги четыре, а их пересечение — ранг два. Поэтому

$$
P_*=P_C+P_I-P_CP_I,
\qquad P_*^2=P_*,
\qquad \rank P_*=6.
$$

Опора `P_*` совпадает ровно с шестью целевыми рёбрами, а дополнение ранга
пять — с нежелательными. Производная инволюция

$$
\Gamma_E=I-2P_*,
\qquad
q_E(z)=\sum_{e\notin E_*}\|z_e\|^2-\sum_{e\in E_*}\|z_e\|^2
$$

даёт отрицательный квадратичный знак целевым и положительный знак
конкурирующим блокам. Вещественная семейная сигнатура равна `(108,0,90)`.

**Статус:** точный положительный селектор `6 из 11` на пространстве
стрелок. Относительный вес не вводится, но происхождение `Gamma_E`, общий
масштаб и квартичная стабилизация из одной Real-суперсвязности не доказаны.

**Вхождения:**
`s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex`,
[[version7-rooted-cycle-isotypic-edge-projector-gate]].

### VII-P19. Одна Hodge-норма запускает и стабилизирует точное меню

На двухступенном пространстве стрелок фиксированный нильпотентный
дифференциал удовлетворяет

$$
[\delta_E,\delta_E^\dagger]
=-\operatorname{diag}(\Gamma_E,-\Gamma_E).
$$

Поэтому одна норма суммарного отображения момента редуцируется к

$$
\mathcal S_\mu(z)
=\sum_{e\in E_*}(|z_e|^2-\mu^2)^2
+\sum_{e\notin E_*}(|z_e|^4+2\mu^2|z_e|^2).
$$

Нуль имеет сигнатуру `(12,0,10)`, а минимум — `(0,6,16)`. В семейном
подъёме минимум равен `mu U(3)^6` на целевых рёбрах и нулю на пяти
нежелательных; вакуумная сигнатура `(0,54,144)`.

**Статус:** положительный единый полевой Hodge-родитель. Квадратичный запуск
и квартика имеют один источник и не требуют относительного веса. Физическое
Real-бимодульное вложение, масштаб, кинетика и семейные ориентации открыты.

**Вхождения:**
`s2t/gates/version7_edge_grading_hodge_superconnection_parent_gate.tex`,
[[version7-edge-grading-hodge-superconnection-parent-gate]].

### VII-P20. Real-модуль стрелок оставляет одну относительную голономию

Два цвета Hodge-родителя образуют один нечётный бимодульный объект,

$$
\mathbb A_E=\nabla_E+d_Z+\mu\delta_E,
\qquad [\delta_E,\rho_E(a)]=[d_Z,\rho_E(a)]=0.
$$

Последнее равенство одновременно означает, что обычные внутренние одноформы
этого вспомогательного оператора исчезают:

$$
\Omega^1_{D_E}(\mathcal A_F)
=\operatorname{span}\{a[D_E,b]\}=0.
$$

Шесть новых рёбер сами образуют лес, но вместе с тремя замороженными рёбрами
`H15` полный граф имеет первый цикл-ранг `b_1=1`. Поэтому относительный
семейный quotient даёт

$$
54\longrightarrow 9,
\qquad
\mathcal M_C=U(3)/\operatorname{Ad}U(3),
\qquad \dim\mathcal M_C^{\rm generic}=3.
$$

**Статус:** положительное Real-эквивариантное соответствие пространства
стрелок и точный частичный семейный quotient. Стандартная физическая
внутренняя флуктуация закрыта; спектральный потенциал трёх собственных фаз,
масштаб и связь с CKM/PMNS не выведены.

**Вхождения:**
`s2t/gates/version7_real_arrow_bimodule_forest_quotient_gate.tex`,
[[version7-real-arrow-bimodule-forest-quotient-gate]].

### VII-P21. Шестой момент впервые видит циклическую голономию

Для семейно-слепого полного графа первые моменты равны

$$
\operatorname{Tr}D^2=18(2r^2+1),
\qquad
\operatorname{Tr}D^4=6(18r^4+10r^2+5),
$$

а первая зависимость от остаточной голономии возникает при степени шесть:

$$
\operatorname{Tr}D^6
=54+144r^2+306r^4+324r^6
+12r^4\operatorname{ReTr}W_C.
$$

Поэтому `c6 Tr D^6` выбирает `W_C=I3` при `c6<0` и `W_C=-I3` при
`c6>0`; голономный гессиан имеет сигнатуру `(0,0,9)`. Радиальный масштаб
зависит от

$$
a=36c_2+60c_4+144c_6,
\quad b=108c_4+270c_6,
\quad c=324c_6,
\quad a+2br^2+3cr^4=0.
$$

**Статус:** точная положительная спектральная видимость единственного цикла
и lifting его линейных нулей при `c6 != 0`. Минимум только центральный;
`H15` не определяет коэффициенты профиля, поэтому масштаб и CKM/PMNS не
выведены.

**Вхождения:**
`s2t/gates/version7_cycle_holonomy_spectral_moment_scale_gate.tex`,
[[version7-cycle-holonomy-spectral-moment-scale-gate]].

### VII-N15. Одна циклическая классовая функция не выводит смешивание

Высшие характеры имеют точную лестницу первого появления

$$
k_{\min}(m)=6m,
$$

а двенадцатый момент впервые содержит второй оборот:

$$
[\operatorname{Tr}D^{12}]_{\rm hol}
=(360r^4+1560r^6+3072r^8+2592r^{10})\operatorname{ReTr}W_C
+12r^8\operatorname{ReTr}W_C^2.
$$

Нецентральная фаза двухгармонического потенциала требует

$$
b>0,
\qquad |a|<4b,
\qquad \cos\theta_*=-\frac{a}{4b}.
$$

При `r=1` для `c6 TrD6+c12 TrD12` это означает свободную настройку

$$
-636<\frac{c_6}{c_{12}}<-628.
$$

Одновременно

$$
\mathcal S_f(UW_CU^\dagger)=\mathcal S_f(W_C),
$$

поэтому одна голономная классовая функция ограничивает собственные фазы, но
не выбирает относительные семейные оси.

**Статус:** точный структурный no-go для параметр-свободного CKM/PMNS в
текущем одноконтурном семейно-слепом родителе; индивидуальные моменты
степеней `6`--`30` дополнительно проверены численно и сохраняют `-I3`.
Ветвь заморожена до второго независимо выведенного некоммутирующего
семейного тензора.

**Вхождения:**
`s2t/gates/version7_higher_cycle_character_mixing_freeze_gate.tex`,
[[version7-higher-cycle-character-mixing-freeze-gate]].

### VII-P22/N18. Product heat-kernel сводит квартику к одному моменту

Для произведённого оператора

$$
\mathcal D_E=i\gamma^\mu\partial_\mu\otimes I
+\gamma^5\otimes a\Phi_E(x)
$$

общий коэффициент `a4` равен `C0=f0/(8 pi²)`, а конечные следы дают

$$
Z=4C_0a^2,\qquad \kappa=2C_0a^4.
$$

После канонической нормировки

$$
\lambda_E=\frac{\kappa}{Z^2}=\frac{\pi^2}{f_0},
\qquad
M_0^2=\frac{\kappa\mu^2}{Z}=\frac{a^2\mu^2}{2}.
$$

**Статус:** частичный положительный результат. Рескейлинг нечётного поля,
`f2` и cutoff сокращаются; вся остаточная безразмерная свобода сведена к
одному `f0`. Численная квартика не выведена, пока тот же физический след не
содержит доказанный gauge-кинетический якорь.

**Вхождения:**
`s2t/gates/version7_spacetime_kinetic_potential_ratio_admission_gate.tex`,
[[version7-spacetime-kinetic-potential-ratio-admission-gate]].

### VII-N19. Редуцированный Hodge-след не фиксирует физический gauge-индекс

При полном конечном индексе `q_G` gauge-нормировка формально дала бы

$$
f_0=\frac{6\pi^2}{q_Gg^2},\qquad
\lambda_E=\frac{q_G}{6}g^2.
$$

Но на выбранных рёбрах индуцированные гиперзаряды равны

$$
(Y_t-Y_s)_{E_*}=\left(0,-\frac23,0,0,\frac53,0\right),
$$

тогда как Hodge-след присваивает каждому ребру единичный вес. Поэтому

$$
q_G^{\rm tot}=q_G^{H_{15}}+q_G^{\rm edge}
$$

нельзя вычислить из редуцированного одиннадцатимерного пространства меток.

**Статус:** точный no-go прямого переноса старого `q_G=2`. Условное
`lambda_E=g²/3` не является предсказанием до раскрытия полных
калибровочных представлений и повторного вычисления Hodge-гессиана.

**Вхождения:**
`s2t/gates/version7_common_gauge_f0_anchor_gate.tex`,
[[version7-common-gauge-f0-anchor-gate]].

### VII-N20. Полный шестирёберный вакуум нарушает цвет

Минимальный gauge-подъём сохраняет опору Hodge-проектора при любых
положительных следовых весах и даёт

$$
(n_-,n_0,n_+)_{0}=(20,0,22),\qquad
(n_-,n_0,n_+)_{*}=(0,14,28).
$$

Но два обязательных ненулевых поля имеют типы

$$
\phi_{Q_LY_R}\in(3,1)_{2/3},\qquad
\phi_{X_Lu_R}\in(3,1)_{5/3},
$$

тогда как

$$
(\mathbb C^3)^{SU(3)}=\{0\}.
$$

**Статус:** структурная опора `6 из 11` устойчива, но её фундаментальный
ненулевой вакуум физически закрыт: два triplet VEV неизбежно нарушают
`SU(3)_c`. Допустим только составной цветосинглетный маршрут с нулевыми
фундаментальными цветными средними.

**Вхождения:**
`s2t/gates/version7_full_gauge_weighted_edge_carrier_gate.tex`,
[[version7-full-gauge-weighted-edge-carrier-gate]].

### VII-N21. Классический составной цикл не обходит цветовой запрет

После фиксации двух старых корней переменная часть цикла равна

$$
C=z_{u_RX_L}z_{X_Le_R}z_{L_LY_R}z_{Y_RQ_L}.
$$

Она gauge-инвариантна как полное замкнутое слово, но

$$
C\ne0\Longrightarrow
z_{u_RX_L}\ne0,\qquad z_{Y_RQ_L}\ne0,
$$

и имеет

$$
\nabla C(0)=0,\qquad \operatorname{Hess}_0C=0.
$$

**Статус:** точный no-go классического составного обхода. Ненулевой цикл
снова требует цветные фундаментальные множители, а в нуле не создаёт
квадратичной неустойчивости. Переоткрытие возможно только через квантовую
меру или виртуальное интегрирование массивных цветных мостов.

**Вхождения:**
`s2t/gates/version7_color_preserving_composite_cycle_parent_gate.tex`,
[[version7-color-preserving-composite-cycle-parent-gate]].

### VII-N22. Виртуальный цветной мост связывает, но не запускает

Для цветных полей `a,b` и бесцветных рёбер `p,q` тяжёлый блок равен

$$
K(pq)=
\begin{pmatrix}
M_a^2&-\kappa\overline{pq}\\
-\kappa pq&M_b^2
\end{pmatrix},
\qquad
\Delta=M_a^2M_b^2-\kappa^2|pq|^2.
$$

В области `Delta>0` классическое исключение даёт `a=b=0`. Три цветовые
копии в конечномерном гауссовом интеграле дают

$$
\Gamma_0=3\log\Delta
=3\log(M_a^2M_b^2)
-\frac{3\kappa^2}{M_a^2M_b^2}|pq|^2+O(|pq|^4),
$$

но

$$
\operatorname{Hess}_{p=q=0}\Gamma_0=0.
$$

**Статус:** частичный структурный проход. Нулевые цветные средние сохраняют
`SU(3)_c`, а детерминант создаёт gauge-инвариантное нелинейное сцепление.
Однако он не даёт квадратичного запуска; в четырёх измерениях коэффициент
квартики логарифмически перенормируется и не фиксируется текущим конечным
графом.

**Вхождения:**
`s2t/gates/version7_virtual_colored_bridge_schur_complement_gate.tex`,
[[version7-virtual-colored-bridge-schur-complement-gate]].

### VII-P23. Gauge-Casimir kernel совпадает с изотипическим проектором

На полном носителе новых рёбер положительный gauge-Casimir имеет ядро

$$
\ker\mathcal C_G=(\mathcal E_{\rm new})^{G_{SM}},
\qquad P_G=\mathbf1_{\{0\}}(\mathcal C_G).
$$

Полный аудит даёт точное совпадение

$$
P_G=P_I,qquad\rank P_G=4,
$$

и разбиение

$$
11=2_{\rm conn}+2_{\rm virtual}+2_{\rm mass}+5_{\rm forbidden}.
$$

Производная Hodge-градуировка `Gamma_G=I-2P_G` имеет полные сигнатуры

$$
(n_-,n_0,n_+)_{0}=(8,0,34),qquad
(n_-,n_0,n_+)_{*}=(0,4,38).
$$

**Статус:** положительный физический селектор. Четыре ненулевых ребра
являются gauge-синглетами, два цветных циклических ребра остаются
виртуальными и массивными, а лёгкий хиральный лептонный пакет сохраняется.
Не закрыты совместный determinant-гессиан, масштаб и Real-физическое
вложение.

**Вхождения:**
`s2t/gates/version7_color_preserving_quadratic_selector_origin_gate.tex`,
[[version7-color-preserving-quadratic-selector-origin-gate]].

### VII-P24/N23. Совместный гессиан устойчив локально, но не глобально

Для нормированных амплитуд двух циклических singlet-коннекторов

$$
V=(r^2-1)^2+(s^2-1)^2+\gamma\log(1-ar^2s^2)
$$

симметричная ветвь `r=s=sqrt(u)` удовлетворяет

$$
\gamma=\frac{2(u-1)(1-au^2)}{au}.
$$

Её радиальные собственные значения равны

$$
\lambda_{\parallel}=8\frac{1-au^2(2u-1)}{1-au^2},
\qquad \lambda_{\perp}=8(2u-1).
$$

Поэтому открытая локально устойчивая область задаётся точным условием

$$
au^2(2u-1)<1,
$$

которое автоматически сохраняет тяжёлую цветную щель `au²<1`.

**Статус:** условный локальный проход и глобальный no-go конечномерного
контроля. Четыре singlet-радиала положительны, четыре фазы плоские, но
`V -> -infinity` на границе тяжёлой щели. Параметры `a,gamma` и полный
четырёхмерный потенциал не выведены.

**Вхождения:**
`s2t/gates/version7_singlet_vacuum_virtual_cycle_combined_hessian_gate.tex`,
[[version7-singlet-vacuum-virtual-cycle-combined-hessian-gate]].

### VII-F37. Профильный инвариант и Gaussian-крайняя ветвь

Четырёхмерные уровни `a2`, `a4`, `a6` оставляют комбинацию

$$
R_\chi=\frac{f_2f_{-2}}{f_0^2}.
$$

Для чистого теплового профиля `chi_t(x)=exp(-t x)` она точно равна единице,
тогда как положительная двухмасштабная смесь даёт

$$
R_\chi=1+\frac{w(1-w)(t_1-t_2)^2}{t_1t_2}\ge1.
$$

**Статус:** частичный Gaussian-проход и общий no-go. Факт одного профиля не
фиксирует его моментный инвариант; при `chi'(0)=0` шестой цикл исчезает, а
четырёхмерный determinant-вес дополнительно требует контрчлена.

Последующий полный слабый расчёт VII-F38 показал, что для использованной
здесь up-пары физический циклический коэффициент равен нулю; локальная
determinant-модель сохраняет статус абстрактного контрольного блока.

**Вхождения:**
`s2t/gates/version7_common_spectral_profile_singlet_virtual_ratio_gate.tex`,
[[version7-common-spectral-profile-singlet-virtual-ratio-gate]].

### VII-F38. Слабая ортогональность обнуляет up-цикл

Полный слабый след даёт

$$
\widetilde H^\dagger H=0,
\qquad [xy]\operatorname{Tr}\Phi_u^6=0.
$$

Down-ветвь и слабая дублетная пара вместо этого имеют

$$
[xy]\operatorname{Tr}\Phi_d^6=12,
\qquad [xy]\operatorname{Tr}\Phi_W^6=12.
$$

**Статус:** строгий no-go прежнего up-цикла и перенос ветви. Gaussian
умножает два выживших билинейных члена на `-1/6`, давая коэффициент `-2`,
но их совместная тяжёлая устойчивость ещё не проверена.

**Вхождения:**
`s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex`,
[[version7-full-product-a6-cycle-coefficient-gate]].

### VII-F39. Точный Gaussian не стабилизирует weak-конкурента

На полном носителе

$$
S_t(\Phi)=\operatorname{Tr}e^{-t\Phi^2},\qquad
H_t=H_d(t)\oplus H_W(t).
$$

При `t=1` down-блок положителен, но weak-блок имеет восемь отрицательных
собственных значений. На диапазоне `10^-4 <= t <= 10^2` отрицательная
weak-мода не исчезает, а корневой градиент singlet-фона ненулевой.

**Статус:** вычислительный no-go автономного точного Gaussian. Ручное
добавление Hodge-потенциала запрещено; открыт вывод одного общего
Hodge--cycle функционала.

**Вхождения:**
`s2t/gates/version7_weak_aligned_cycle_competition_gate.tex`,
[[version7-weak-aligned-cycle-competition-gate]].

### VII-F40. Полные Casimir-веса открывают общее тяжёлое окно

Для полного рёберного Hodge-момента

$$
h_e(t)=8t c_e e^{-t c_e^2},
\qquad c_W=\frac9{10},\quad c_d=\frac85,
$$

сумма Hodge- и точного cycle-гессианов положительна при

$$
0<t<2.36617354515.
$$

При `t=1` двадцатимерный тяжёлый блок имеет сигнатуру `(0,0,20)` и
минимальную моду `1.03081235398`.

**Статус:** строгий вычислительный проход тяжёлого сектора; корневая
стационарность на этом шаге ещё не использовалась.

**Вхождения:**
`s2t/gates/version7_exact_profile_hodge_cycle_unification_gate.tex`,
[[version7-exact-profile-hodge-cycle-unification-gate]].

### VII-F41. Семь корней замыкают формальный локальный вакуум

При одной шкале `t=1` формальная конструкция

$$
\mathcal S_{\rm form}
=-\Tr_{H_{15}}e^{-\mathfrak m_{\rm ch}^2}
-\Tr_Ee^{-\mathfrak m_C^2}
+\Tr_{\rm phys}e^{-\Phi(r)^2}
$$

имеет положительную семикомпонентную стационарную точку. Полный смешанный
гессиан по семи корням и двадцати тяжёлым направлениям удовлетворяет

$$
(n_-,n_0,n_+)=(0,0,27),
\qquad \lambda_{\min}=1.14399252085.
$$

**Статус:** формальный локальный вакуумный проход. Физический статус остаётся
открытым, пока три следовых блока, их знаки и кратности не выведены из одной
Real-суперсвязности.

**Вхождения:**
`s2t/gates/version7_common_carrier_root_stationarity_gate.tex`,
[[version7-common-carrier-root-stationarity-gate]],
[[version7-real-superconnection-common-trace-origin-gate]].

### VII-N24/P25. Индексный no-go и размерностный резонанс `22 -> 21`

Для обычной нечётной нуль-формы

$$
\mathbb A_0=\begin{pmatrix}0&B^*\\B&0\end{pmatrix}
$$

тепловой суперслед равен индексу и не имеет динамического гессиана:

$$
\Str e^{-t\mathbb A_0^2}=\dim\ker B-\dim\ker B^*.
$$

При этом кратности семи корней дают 22 Hodge-уровня, а физический carrier
имеет размерность `21=11+10`. Это естественные размеры прямоугольного
Hodge--Dirac комплекса с дефектом один. Текущие квадраты не спариваются:

$$
\rank\mathfrak m_H^2=22,
\qquad \rank\Phi^2=20.
$$

**Статус:** обычный суперслед закрыт, буквальное склеивание текущих блоков
закрыто. Положительно сохранён новый конструктивный класс — одна сдвинутая
Hodge-кривизна на carrier `22 -> 21`.

**Вхождения:**
`s2t/gates/version7_real_superconnection_common_trace_origin_gate.tex`,
[[version7-real-superconnection-common-trace-origin-gate]],
[[version7-derived-relative-involution-curvature-norm-gate]].

### VII-P26/N25. Положительная относительная норма проходит при половинном весе

На ориентированном физическом блоке $A:\mathbb C^{11}\to\mathbb C^{10}$
определена относительная Gram-кривизна

$$
\mathcal S_V=\frac12\left(
\|A^*A-A_0^*A_0\|^2+\|AA^*-A_0A_0^*\|^2\right).
$$

Вместе с выведенной рёберной Hodge-нормой действие

$$
\mathcal S_\beta=\mathcal S_E+\beta\mathcal S_V
$$

имеет правильный селективный запуск точно при `0 <= beta < 8/15`. Для
`beta=1/2`

$$
(n_-,n_0,n_+)_{0}=(7,0,20),\qquad
(n_-,n_0,n_+)_{*}=(0,0,27),
$$

с тяжёлой щелью `0.4` в нуле и вакуумной щелью `5.6`.

**Статус:** строгий локальный проход положительной кривизностной модели при
одном отношении. Полное замыкание не достигнуто: `beta=1/2` ещё не выведено
из Real-полуследа и общей Hodge-метрики; равный вес `beta=1` проваливается.

**Вхождения:**
`s2t/gates/version7_derived_relative_involution_curvature_norm_gate.tex`,
[[version7-derived-relative-involution-curvature-norm-gate]],
[[version7-real-half-trace-curvature-weight-gate]].

### VII-N26. Общий Real-полуслед не выводит половинный вес

Оба текущих блока уже имеют одну Hodge-нормировку:

$$
\mathcal S_E=\frac12\Tr\mathfrak m_E^2,
\qquad
\mathcal S_V=\frac12\Tr\mathfrak m_V^2.
$$

Real-удвоение и один общий физический полуслед действуют на них одинаково,
поэтому

$$
\beta_{\rm Real\ half\ trace}=1,
\qquad
(n_-,n_0,n_+)_{0}=(21,0,6).
$$

Получение `beta=1/2` дополнительным полуследом только физического блока
эквивалентно ручному центральному весу. Оба текущих момента являются
нуль-форменными эндоморфизмами, поэтому степень формы и клиффордов след пока их
не различают.

**Статус:** строгий no-go для одного общего Real-полуследа. Открыт новый,
более узкий тест представленного исчисления степеней форм и клиффордова следа.

**Вхождения:**
`s2t/gates/version7_real_half_trace_curvature_weight_gate.tex`,
[[version7-real-half-trace-curvature-weight-gate]],
[[version7-clifford-form-degree-weight-origin-gate]].

### VII-N27. Клиффордов след не превращает индексную половину в секторный вес

Для антисимметричной двухформы нормированное клиффордово представление
удовлетворяет

$$
\frac14\operatorname{tr}_{\rm spin}(c(F)^*c(F))
=\sum_{\mu<\nu}|F_{\mu\nu}|^2
=\frac12\sum_{\mu,\nu}|F_{\mu\nu}|^2.
$$

Половина справа удаляет двойной счёт упорядоченных индексов. Она не является
весом относительно скалярной Hodge-нормы. Поскольку оба текущих момента
являются пространственно-временными нуль-формами и чётными внутренними
моментами,

$$
\beta_{\rm Clifford}=1,
\qquad
(n_-,n_0,n_+)_{0}=(21,0,6).
$$

**Статус:** строгий no-go для текущего произведённого исчисления. Открыт
только тест кратностей вложения в один простой носитель с единственным
нормированным следом.

**Вхождения:**
`s2t/gates/version7_clifford_form_degree_weight_origin_gate.tex`,
[[version7-clifford-form-degree-weight-origin-gate]],
[[version7-common-irreducible-trace-multiplicity-gate]].

### VII-P27/N28. Размерностный резонанс `11/21` проходит только как скаляр

Нормированный source-проектор физического носителя имеет след

$$
\tau_{21}(P_{11})=\frac{11}{21}<\frac8{15}.
$$

Если использовать это число как глобальный вес физической нормы, получается

$$
(n_-,n_0,n_+)=(7,0,20),
\qquad
\lambda_{\rm heavy}^{\min}=\frac4{35}.
$$

Но честная вставка проектора действует не как скаляр на всей кривизне:

$$
(n_-,n_0,n_+)_{P_{11}}=(8,0,19),
\qquad
(n_-,n_0,n_+)_{P_{10}}=(17,0,10).
$$

Кроме того, текущие опорные квадраты имеют ранги `22` и `20`, поэтому не
являются двумя Gram-концами одного прямоугольного оператора. Блочная алгебра
`M22 direct_sum M21` сохраняет один свободный центральный вес, а простой
completion `M43` вводит 462 комплексных коннектора.

**Статус:** положительная числовая зацепка, но no-go простого следа и
текущих кратностей. Открыта инцидентная передаточная или марковская карта.

**Вхождения:**
`s2t/gates/version7_common_irreducible_trace_multiplicity_gate.tex`,
[[version7-common-irreducible-trace-multiplicity-gate]],
[[version7-incidence-transfer-markov-weight-gate]].

### VII-P28/N29. Полярный quotient выводит локальную половину, полный expectation — нет

Для фоновой инцидентности `A0:C11 -> C10` полярная часть удовлетворяет

$$
UU^*=I_{10},\qquad P=U^*U,\qquad \operatorname{rank}(I-P)=1,
$$

и раскрывает не скаляр `11/21`, а операторное разложение

$$
21=10_{\rm source\ support}+10_{\rm target}+1_{\rm defect}.
$$

Однократная UCP-карта

$$
T_U(X,Y)=\frac12(UXU^*+Y)
$$

даёт в нуле точное тождество

$$
\operatorname{Hess}_0 S_{\rm quot}
=\frac12\operatorname{Hess}_0 S_V,
$$

а вместе с рёберной нормой — сигнатуру `(7,0,20)`, тяжёлую щель `2/5` и
положительный вакуумный гессиан с минимальной модой `4.582763...`.

Полное сохраняющее след условное ожидание помещает усреднённый `M10` в оба
согласованных угла. Поэтому его нулевой гессиан вдвое больше quotient-
гессиана и возвращает провальную сигнатуру `(21,0,6)`.

**Статус:** положительный локальный операторный проход и no-go полного
expectation. Открыт вывод однократного quotient из физического фактора форм,
Real- или BRST--BV-редукции.

**Вхождения:**
`s2t/gates/version7_incidence_transfer_markov_weight_gate.tex`,
[[version7-incidence-transfer-markov-weight-gate]],
[[version7-index-defect-reduced-linking-quotient-gate]].

### VII-P29/N30. Наследуемая quotient-метрика возвращает полный вес

Для согласованных полярных кривизн

$$
Z=\frac{X+Y}{2},\qquad D=\frac{X-Y}{2}
$$

параллелограммное тождество имеет вид

$$
\frac12(\|X\|^2+\|Y\|^2)=\|Z\|^2+\|D\|^2.
$$

В нуле антисимметричная и дефектная части начинаются с квадратичного порядка,
поэтому индуцированная диагональная метрика удовлетворяет

$$
\operatorname{Hess}_0\|Z\|^2
=\operatorname{Hess}_0 S_V.
$$

Если `c` измеряет норму относительно сырого действия `1/2||Z||²`, тяжёлый
сектор положителен только при

$$
0\le c<\frac{16}{15}.
$$

Сырой `c=1` даёт `(7,0,20)`, но наследуемый `c=2` даёт `(21,0,6)`.
Общий Real-полуслед, прежний лесной quotient, текущий junk и BRST--BV-
фактор нулевой точки не понижают эту метрику.

**Статус:** no-go существующих редукций как источника половины. Локальный
UCP-кандидат сохраняется только условно; открыт смешанный полярный
кривизностный блок.

**Вхождения:**
`s2t/gates/version7_index_defect_reduced_linking_quotient_gate.tex`,
[[version7-index-defect-reduced-linking-quotient-gate]],
[[version7-polar-transfer-cross-curvature-origin-gate]].

### VII-P30. Относительная полярная кривизна устраняет вес из запуска

Для полярной коизометрии `U:C11 -> C10` и двух Gram-кривизн

$$
C_s=A^*A-A_0^*A_0,
\qquad
C_t=AA^*-A_0A_0^*
$$

правое правило Лейбница фиксирует кривизну связывающего бимодуля

$$
\mathcal R_U=C_tU-UC_s.
$$

Полярное переплетение фона даёт

$$
(A_0A_0^*)U=U(A_0^*A_0),
\qquad
\mathcal R_U(0)=0,
$$

поэтому

$$
\operatorname{Hess}_0\frac12\|\mathcal R_U\|^2=0.
$$

Вместе с рёберной Hodge-нормой это даёт `(7,0,20)` со щелью `18/5` без
ручного коэффициента. В вакууме связывающая добавка имеет ранг `22`, а
полный гессиан равен `(0,0,27)` с минимальной модой `3.9368554658...`.
Самосопряжённое завершение удовлетворяет

$$
\frac14\left\|
\begin{pmatrix}0&\mathcal R_U\\\mathcal R_U^*&0\end{pmatrix}
\right\|^2
=\frac12\|\mathcal R_U\|^2.
$$

Половина здесь удаляет две ориентации одного внедиагонального блока, а не
настраивает секторный вес. Знак суммы сохраняет фон и даёт провал
`(27,0,0)`.

**Статус:** положительный локальный полярно-связывающий родитель. Открыта
сборка рёберного и связывающего блоков квадратом одной Real-суперсвязности.

**Вхождения:**
`s2t/gates/version7_polar_transfer_cross_curvature_origin_gate.tex`,
[[version7-polar-transfer-cross-curvature-origin-gate]],
[[version7-real-linking-superconnection-assembly-gate]].

### VII-P31/N31. Трёхступенная факторизация проходит, полный квадрат — нет

На комплексе

$$
H_0=\mathbb C^{11},\qquad
H_1=\mathbb C^{11}\oplus\mathbb C^{10},\qquad
H_2=\mathbb C^{10}
$$

стрелки

$$
B_0=\binom{A^*U}{A},\qquad
B_1=(A,-UA^*)
$$

дают точное тождество

$$
B_1B_0=AA^*U-UA^*A=\mathcal R_U.
$$

Относительная кривизна является крайним блоком `d²`. Но полный квадрат
`Q²=(d+d*)²` содержит также диагональные Gram-блоки и даёт в нуле
`(27,0,0)`. Полный вес допустим только при `0 <= alpha < 1/15`, тогда как
стандартные значения `1`, `1/2`, `1/4`, `1/8` не проходят. Блок
`Hom(H0,H2)` отдельно сохраняет `(7,0,20)` и вакуум `(0,0,27)`, но его
представленный quotient ещё не выведен.

**Статус:** положительная факторизация и no-go полного обычного квадрата;
открыт quotient компоненты длины два.

**Вхождения:**
`s2t/gates/version7_real_linking_superconnection_assembly_gate.tex`,
[[version7-real-linking-superconnection-assembly-gate]],
[[version7-linking-chain-degree-two-curvature-quotient-gate]].

### VII-P32/N32. Обычный junk удаляет endpoint, степень цепи его сохраняет

Для узловой алгебры `C³` на блоках `11,21,10` представлены ранги

$$
\operatorname{rank}\Omega^1=4,\qquad
\operatorname{rank}\Omega^2=6,\qquad
\operatorname{rank}J^2=2.
$$

Оба блока длины два лежат в `J²`, поэтому обычный Connes-quotient удаляет
`R_U`. Но оператор степени

$$
N=\operatorname{diag}(0I_{11},I_{21},2I_{10})
$$

задаёт относительную производную

$$
\delta_N(F)=\frac12[N,F],
$$

которая убивает диагональные возвраты и сохраняет ровно `R_U,R_U*`.
Полученная норма gauge-ковариантна, не зависит от ориентации цепи и даёт
`(7,0,20)` в нуле и `(0,0,27)` в вакууме.

**Статус:** no-go ordinary junk и положительный канонический relative
mapping-cone quotient. Открыт общий цепно-Hodge след.

**Вхождения:**
`s2t/gates/version7_linking_chain_degree_two_curvature_quotient_gate.tex`,
[[version7-linking-chain-degree-two-curvature-quotient-gate]],
[[version7-common-chain-number-hodge-relative-trace-gate]].

### VII-P33/N33. Один общий след замыкает качественную динамику, но не массы

Рёберная Hodge-кривизна и relative-компонента цепи помещаются в один
самосопряжённый носитель

$$
\mathcal K_{\rm common}=\mathcal K_E\oplus\mathcal H_{\rm link},
\qquad
\dim_{\mathbb C}\mathcal K_{\rm common}=54+42=96,
$$

$$
\mathbb F_{\rm common}
=\operatorname{diag}\!\left(\mathbb M_E,
i\,\delta_N(Q_A^2-Q_{A_0}^2)\right).
$$

Один незавешенный след удовлетворяет

$$
\frac12\operatorname{Tr}_{96}\mathbb F_{\rm common}^2
=\mathcal S_E+\|\mathcal R_U\|_{\rm HS}^2+\mathrm{const}.
$$

Он даёт `(7,0,20)` в нуле и `(0,0,27)` в вакууме. Более того, замена
linking-нормы на любой неотрицательный вес не меняет эти сигнатуры:
linking-гессиан нулевой в начале и положительно полуопределён в вакууме.
Поэтому качественный селектор больше не зависит от относительной
нормировки.

Однако подносители размерностей `54` и `42` не связаны унитарным обменом;
текущая симметрия допускает независимое положительное перескалирование.
Следовательно, общий след существует, но единственность количественной
Hodge-метрики и массовые отношения ещё не выведены.

**Статус:** положительное качественное замыкание и запрет преждевременного
массового предсказания. Открыт total-degree бикомплекс.

**Вхождения:**
`s2t/gates/version7_common_chain_number_hodge_relative_trace_gate.tex`,
[[version7-common-chain-number-hodge-relative-trace-gate]],
[[version7-bicomplex-total-degree-hodge-metric-gate]].

### VII-N34/P34. Полная степень не фиксирует метрику и оставляет дефект 12

Для любого бикомплекса

$$
d_h^2=d_v^2=d_hd_v+d_vd_h=0
$$

замена `d_v -> c d_v`, `c>0`, сохраняет все соотношения. На минимальном
квадрате оператор полной степени также удовлетворяет

$$
[N_{\rm tot},d_h+c d_v]=d_h+c d_v
$$

при любом `c`. На текущем 96-мерном носителе семейство

$$
G_\eta=P_E+\eta P_L,
\qquad \eta>0,
$$

совместимо с полной степенью, Real-сопряжением и изометрической
Hodge-инволюцией. Поэтому bigrading не выводит `eta`, а вакуумные спектры
при разных весах не являются общим перескалированием.

Одновременно максимальная изометрия `C42 -> C54` оставляет

$$
\operatorname{rank}(I_{54}-UU^*)=54-42=12
=\dim_{\mathbb C}E_{\rm aff}.
$$

Последнее равенство является новой размерностной зацепкой, но не
отождествлением бимодулей.

**Статус:** no-go единственности метрики из total-degree, Real и одной
Hodge-инволюции; качественный вакуум остаётся закрытым. Открыт тест
аффинного дефектного дополнения.

**Вхождения:**
`s2t/gates/version7_bicomplex_total_degree_hodge_metric_gate.tex`,
[[version7-bicomplex-total-degree-hodge-metric-gate]],
[[version7-affine-defect-bicomplex-completion-gate]].

### VII-N35. Дефект 12 исчезает после сжатия к опоре кривизны

Связывающий контейнер раскладывается как

$$
\mathcal H_{\rm link}=H_0\oplus H_1\oplus H_2,
\qquad
(\dim H_0,\dim H_1,\dim H_2)=(11,21,10),
$$

но relative curvature удовлетворяет

$$
P_{H_1}\mathbb M_L=\mathbb M_LP_{H_1}=0.
$$

Поэтому endpoint-сжатие к `H0 direct_sum H2` имеет размерность `21` и
точно сохраняет норму:

$$
\frac12\operatorname{Tr}_{42}\mathbb M_L^2
=\frac12\operatorname{Tr}_{21}\widetilde M_L^2.
$$

Нулевое дополнение `M_L direct_sum 0_k` также не меняет действие. Значит,
разность `54-42=12` зависит от выбранного контейнера; для минимальной
endpoint-опоры она равна `54-21=33`. Кроме того,

$$
E_{\rm aff}\simeq\mathbf1\oplus\mathbf2
\oplus2\,\mathbf3\oplus\mathbf3'
$$

как `S4`-модуль, тогда как действие на предполагаемом дефекте не задано.

**Статус:** no-go аффинного дополнения по совпадению размерностей. Общий
качественный вакуум не изменён; открыт след минимальной опоры.

**Вхождения:**
`s2t/gates/version7_affine_defect_bicomplex_completion_gate.tex`,
[[version7-affine-defect-bicomplex-completion-gate]],
[[version7-minimal-curvature-support-trace-gate]].

### VII-N36. Минимальная опора не устраняет центральный вес

Сжатое связывающее семейство имеет одномерный коммутант и потому порождает

$$
\mathcal A_L=M_{21}(\mathbb C).
$$

Однако диагональный рёберный суррогат порождает

$$
\mathcal A_E\simeq\mathbb C^{54},
\qquad
\mathcal A_{\rm gen}=\mathbb C^{54}\oplus M_{21}(\mathbb C),
\qquad
\dim Z(\mathcal A_{\rm gen})=55.
$$

Даже при замене суррогата физическим фактором остаётся
`M22(C) direct_sum M21(C)` и один относительный вес. Превращение контейнера
в простой `M75(C)` потребовало бы нового блока

$$
\operatorname{Hom}(\mathbb C^{21},\mathbb C^{54}),
\qquad \dim_{\mathbb C}=1134,
$$

а физического `M43(C)` — `462` комплексных компонент. Для положительных
весов сигнатуры `(7,0,20)` и `(0,0,27)` сохраняются, но собственные значения
гессиана меняются.

**Статус:** no-go единственного общего следа на минимальных опорах.
Качественный родитель закрыт; количественная массовая метрика не выведена.

**Вхождения:**
`s2t/gates/version7_minimal_curvature_support_trace_gate.tex`,
`s2t/results/s2t_v7_minimal_curvature_support_trace_gate_results.json`,
[[version7-minimal-curvature-support-trace-gate]],
[[version7-qualitative-parent-mass-metric-freeze-gate]].

### VII-P37/N37. Качественный класс замкнут, количественный родитель нет

Финальный класс действий имеет вид

$$
\mathcal S_\eta=\mathcal S_E+\eta\|\mathcal R_U\|_{\rm HS}^2,
\qquad \eta>0.
$$

В начале связывающая часть имеет нулевой гессиан, а в целевой точке

$$
\operatorname{Hess}_{A_0}\mathcal S_\eta=H_E+2\eta H_L,
\qquad H_E>0,\quad H_L\geq0,\quad \operatorname{rank}H_L=22.
$$

Поэтому для всех положительных весов

$$
(7,0,20)_0\longrightarrow(0,0,27)_{A_0}.
$$

Этот переход является строгим на 27-мерном амплитудно-тяжёлом срезе. Но
семейные фазы, единственная массовая метрика, общий
калибровочно-пространственный след и абсолютный масштаб не выведены.

**Статус:** строгий качественный универсальный класс и no-go полного
количественного чтения текущего родителя. Том VII завершён.

**Вхождения:**
`s2t/gates/version7_qualitative_parent_mass_metric_freeze_gate.tex`,
`s2t/docs/version7_final_conclusion_and_next_program.tex`,
`s2t/results/s2t_v7_qualitative_parent_mass_metric_freeze_gate_results.json`,
[[version7-qualitative-parent-mass-metric-freeze-gate]],
[[version7-final-conclusion-and-next-program]].

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
| Обычный суперслед сокращается до индекса, но полный реестр выделяет carrier `22 -> 21` | VII-N24/P25 |
| Положительная относительная Hodge-норма даёт селективный запуск и устойчивый вакуум при `beta=1/2` | VII-P26/N25 |
| Общий Real-полуслед сохраняет `beta=1` и не выводит требуемую половину | VII-N26 |
| Нормированный клиффордов след является Hodge-изометрией и также сохраняет `beta=1` | VII-N27 |
| Размерностный вес `11/21` проходит численно, но не равен corner-вставке одного следа | VII-P27/N28 |
| Полярное разложение заменяет `11/21` структурой `10+10+1`; однократный quotient даёт половину, полный expectation — двойной счёт | VII-P28/N29 |
| Индуцированная метрика диагонального quotient равна `||Z||²`, поэтому текущие редукции не выводят сырой половинный вес | VII-P29/N30 |
| Ранг должен быть свойством одного физического поля, а не выбранной целью | VII-F1 |
| Эндогенный запуск требует заранее выведенного стационарного фона | VII-F2, VII-N1, VII-N2 |
| Хиральная размерностная асимметрия может дать запуск и защищённое ядро одним квадратом | VII-F3 |
| Аффинный триплет поднимает одну ядерную линию в три без повторного семейного множителя | VII-F4 |
| Поперечная устойчивость не означает выбора смешивания на плоском endpoint | VII-F5 |
| Общий Хиггс и обычная вторая степень не создают межрёберный класс | VII-F6 |
| Повышение степени без нового коннектора сохраняет разложение по рёбрам | VII-F7 |
| Первый смешанный цикл требует новой типизированной стрелочной пары | VII-F8 |
| Графовая стрелка должна пройти полные бимодульные метки | VII-N7 |
| Нелинейный член не возникает без первопорядково нарушающего seed | VII-N9 |
| Real-удвоение не заменяет аномальное сокращение физического Weyl-сектора | VII-N10 |
| Вектороподобное удвоение может сохранить хиральный индекс, но не выбирает ориентацию ядра | VII-P12 |
| Функционал от сингулярных чисел постоянен на грассманиане ядер | VII-N11 |
| Модулярный вес способен выбрать паритет ядра только после независимого происхождения инцидентности | VII-P13 |
| Радиальная неустойчивость плюс внешний квадрат создают ранга-один когерентность и производный проектор | VII-P14 |
| Полные второй и четвёртый моменты одной цепи фиксируют радиальный и ранговый каналы | VII-P15 |
| Совпадение размерностей пространства стрелок и фермионного модуля не обеспечивает первый порядок | VII-N13 |
| Кривой комплекс пространства стрелок может быть полевым суперсвязностным носителем без новых частиц | VII-P16 |
| Ранг одного прямоугольника не выбирает не прямоугольную опору физического цикла | VII-N14 |
| Пространство разрешённых стрелок задаёт скалярную ковариацию, а не когерентный обмен | VII-N12 |
| Одна циклическая классовая функция видит собственные фазы, но не выбирает относительные семейные оси | VII-N15 |
| Три неэквивалентных фоновых ребра дают трёхмерное семейство атрибуций Hodge-уровня | VII-N16 |
| Одна масса замыкает линейный Hodge-спектр с отношением `sqrt(2)`, но не фиксирует эффективную квартику | VII-P17/N17 |
| Product `a4` сокращает нормировку нечётного поля и оставляет `lambda_E=pi²/f0` | VII-P22/N18 |
| Формальное `lambda_E=q_Gg²/6` не замыкается, потому что редуцированный Hodge-след не определяет физический `q_G` | VII-N19 |
| Полный gauge-подъём сохраняет селектор, но два обязательных triplet VEV нарушают `SU(3)_c` | VII-N20 |
| Классический составной цикл gauge-инвариантен, но имеет нулевой гессиан и требует ненулевых цветных множителей | VII-N21 |
| Виртуальный цветной мост сохраняет цвет и даёт отрицательную singlet-квартику, но не запускает нуль | VII-N22 |
| Ядро gauge-Casimir и изотипический проектор независимо выбирают один цветосохраняющий четырёхрёберный вакуум | VII-P23 |
| Singlet-вакуум и виртуальный цикл локально совместимы в открытой области, но конечномерный глобальный минимум отсутствует | VII-P24/N23 |
| Полные Casimir-веса стабилизируют совместный down--weak тяжёлый сектор | VII-F40 |
| Семь корней и двадцать тяжёлых мод образуют формальный положительный локальный вакуум | VII-F41 |
| Относительная полярная кривизна сохраняет селективный запуск без ручного секторного веса | VII-P30 |
| Трёхступенный квадрат порождает относительную кривизну, но полный самосопряжённый квадрат возвращает Gram-каналы | VII-P31/N31 |
| Обычный junk удаляет endpoint-путь, а каноническая степень цепи выделяет его relative-коммутатором | VII-P32/N32 |
| Один 96-мерный след замыкает селектор и вакуум при любой положительной linking-нормировке, но не фиксирует массовые отношения | VII-P33/N33 |
| Total-degree и Hodge-звезда допускают семейство метрик; дефект `54-42=12` совпадает с размерностью аффинного носителя | VII-N34/P34 |
| Средняя ступень linking-цепи тождественно нулевая, поэтому дефект `54-42=12` является артефактом контейнера, а не аффинным индексом | VII-N35 |
| Минимальная связывающая опора порождает `M21(C)`, но общая алгебра сохраняет нетривиальный центр и относительный следовой вес | VII-N36 |
| Весь класс `S_eta`, `eta>0`, сохраняет качественный переход `(7,0,20) -> (0,0,27)`, но не фиксирует массовую метрику и семейные фазы | VII-P37/N37 |
| Полный шумовой носитель замыкает безразмерную динамику; смешанный родитель закрывает энергетический учёт, но сохраняет свободу единицы времени | VIII-P29--VIII-N54, [[version8-time-formula-intuition-map]] |
| Канонический общий КМС-след фиксирует шесть барионных весов; полная электромагнитная ветвь остаётся вне параметр-свободного замыкания | VIII-P39--P48/N55--N64, [[version8-baryon-electromagnetic-closure-redteam-gate]] |
| После произвольного выбора `j` формальный `T_j=diag(j,jU*)` порождает весь угол размерности `462`, но `j:C11_state->C11_edge` не выведено | VIII-N1 |
| Hodge-дефект `X_E T_j-T_jX_V=jQ` имеет норму один для всех `j in U(11)` и потому не выбирает 121-мерную ориентацию | VIII-N2 |
| Полный arrow-модуль имеет 10 прямых и 14 Real-интертвинеров; выбранная Real-Hodge-опора оставляет единственный канал `Y_R->Q_L` в `u_R`, но его ранг не выше трёх | VIII-P1/N3 |
| Нормированный слабый след `J=Tr_w/sqrt(2)` проходит gauge/Real-подъём, но финальный цветосохраняющий проектор даёт `J P_G=0` | VIII-P2/N4 |
| Финальный четырёхрёберный Hodge-вакуум имеет gauge-индекс `(0,0,0)`, а полный `(13,2,3/2)` целиком несут семь заглушённых рёбер | VIII-N5 |
| `K_s=[Z4_s,Z6_s]/(2i)` является вторым семейным тензором, но его замороженная ветвь имеет `s12>0.99`; 12 incidence-альтернатив порождают `M3(C)`, не имея канонического селектора | VIII-N6 |
| `B_X=(I-P_X)(nabla P_X)P_X` каноничен при постоянном ранге, но на ограниченном rank-drop пути имеет `||B_X||=1/epsilon` и остаётся факторизованным по рёберному носителю | VIII-P3/N7 |
| Полный `C_tau=exp(-tau H)` в фиксированной алгебре наблюдаемых возвращает `H=-log(C_tau)/tau` и конечную локальность, хотя спектр и все следы коспектральной пары совпадают | VIII-P4/N8 |
| `L_A=-ad(D_A)^2/2` задаёт унитальную сохраняющую след квантово-марковскую полугруппу между `M11` и `M10`, но `dim ker L_A=41` не выбирает классическую алгебру событий | VIII-P5/N9 |
| Совместные linking- и gauge-формы Дирихле дают `ker L = C P_q direct_sum C P_l` с рангами `(12,9)` при всех положительных весах; межсекторный переход отсутствует | VIII-P6/N10 |
| Полная cross-arrow опора `QLYR direct_sum XLdR` даёт gauge-ковариантную Kraus-сумму с центральным спектром `{0,7/3}` и снимает `C^2`, хотя линейный синглет и единственная скорость отсутствуют | VIII-P7/N11 |
| Полевая форма `E_bridge=(7/36) sum z_a^2` сохраняет обе сигнатуры Тома VII, но при `z=0` даёт нулевую древесную скорость; два мультиплета оставляют веса `c_Q,c_X` и щель `7(c_Q+c_X)/6` | VIII-P8/N12 |
| Linking-гессиан на cross-arrow опоре равен `I6 tensor [[0.92493,-0.44926],[-0.44926,0.58178]]` и фиксирует мягкую ось `55.45092°`, но форма зависит от `eta`, а масштаб — от гауссовской, квантовой или тепловой нормировки | VIII-P9/N13 |
| `K0=sqrt(I-p sum Da²), Ka=sqrt(p)Da` даёт точный канал при `0<=p<=1/6`; его минимальный Kraus-ранг 13 использует cross-arrow представление, но семейство не образует полугруппу | VIII-P10/N14 |
| Collision-limit `p=u/n` сходится к `exp(u L_cross)`, тогда как модульный поток фиксирует `P_q,P_l`; положительное `kappa L` сохраняет структуру и оставляет физическую скорость свободной | VIII-P11/N15 |
| `L_full=L_link+L_SU3+L_SU2+L_U1+L_QLYR+L_XLdR` имеет `ker L_full=C I21` и щель `0.1112337884`; все положительные веса сохраняют примитивность, а trace detailed balance их не выбирает | VIII-P12/N16 |
| `rho=aI11 direct sum bI10` совместимо с KMS текущего примитивного процесса только при `a=b=1/21`; после направленного разбиения `gamma_up/gamma_down=e^{-beta Delta}` | VIII-N17 |
| `N=diag(0 I11,I21,2 I10)` даёт `[N_boundary,V]=2V`; направленный процесс имеет `b/a=e^{-2}` и щель `0.0212599674`, но `2I-N` даёт также допустимое `e^2` | VIII-P13/N18 |
| `N_boundary-I=Gamma=diag(-I11,+I10)`, `index(U)=-Tr Gamma=1`; прямой Hodge-путь равен `[1+20(1-t²)²]/21`, обратный — `[1+20(1+t²)²]/21` | VIII-P14/N19 |
| `L_k=sum_r kappa_r L_r` имеет шестимерный положительный KMS-конус; degree-only метрика `G_f=f(0)P0+f(4)P2` оставляет отношение `f(4)/f(0)`, а `f(x)=x` даёт `dim ker L=3` | VIII-N20 |
| `L=tau^{-1} log C_tau=dC_tau/dtau|_0` восстанавливает шесть скоростей из полной матрицы процесса; без известного `tau` сохраняются пять отношений, но не общий масштаб | VIII-P15/N21 |
| `A=MH`, `Sigma=H^-1` дают `A Sigma+Sigma A*=2M`: одна равновесная мера допускает разные `M` и разные ядра `exp(-tau MH)` | VIII-N22 |
| `K_B=3I12` условно даёт `M_B proportional I12/3` и `kappa_Q/kappa_X=1`, но `D[sV]=s²D[V]` делает общие коэффициенты зависимыми от шумового кадра | VIII-P16/N23 |
| `G_ab=Tr(rho_N F_a*F_b)` после quotient `25 -> 19` задаёт базис-независимый Casimir стабилизатора; его веса не имеют полного gauge-статуса | VIII-P17/N24 |
| Полная gauge-ветвь имеет `dim N_tr=5+10=15`, `dim N_full=27`; коммутанты стабилизаторной и полной ветвей равны `10` и `16`, поэтому изотропия не вынуждена | VIII-P18/N25 |
| `e^{-2}e^2=1` и `ker(kappa L)=ker L` при `kappa>0`: внутренняя ориентация и примитивность не фиксируют физическую стрелу, rate-метрику или единицу времени; восемь требований динамического замыкания остаются открыты | VIII-N33 |
| Старый полевой срез `T_VII` имеет размерность 27 real, полный transfer-noise модуль — 30 real, `dim intersection=23`; поэтому 27D noise-parent Hessian не наследуется по совпадению размерностей | VIII-N26 |
| `F_fields=Omega1(g_s+g_t) direct_sum Gamma(Hom(E_s,E_t))` даёт 42-real gauge-замкнутый внутренний слой; fixed polar имеет полный gauge-дефект, а moving `Pol(A)` скачок `sqrt(10)` в нуле | VIII-P19/N27 |
| `B(A)=Gamma_t A-A Gamma_s` имеет ранг 6 complex и даёт gauge-ковариантную `R_B=AA*B-BA*A`; `||R_B(tA)||²=t^6||R_B(A)||²`, поэтому вакуумный гессиан имеет ранг 12, а исходный равен нулю | VIII-P20/N28 |
| `T_15=I_5 direct_sum H_10`; двухмассовое gauge-инвариантное завершение при `(m_I,m_H)=(4,3.6)` даёт `(10,0,20) -> (0,0,30)`, но скан весов меняет исходную сигнатуру | VIII-P21/N29 |
| `Spec C_G={0 x1,1 x8,16/9 x6}` и `Spec B={-2 x3,0 x9,2 x3}` оставляют совместный блок ранга 8 с разложением `4 incidence + 4 heavy`; лучший спектральный `P_I` имеет ошибку `sqrt(2)` | VIII-N30 |
| Real-подъём `P -> diag(P,conj P)` совместим со всей орбитой `P(theta)=e^{i theta K}Pe^{-i theta K}`; Real-fixed слой имеет 30 real параметров и не снимает кратность `4+4` | VIII-N31 |
| Endpoint-бимодульное замыкание даёт `T_bimod=I_10 direct_sum H_10`; единый уровень имеет edge-массы `-4/+4`, окно `0<=beta<2/3` и при `beta=1/2` переход `(20,0,20) -> (0,0,40)` | VIII-P22/N32 |
| `|H_2(psi)>=3^{-1/2} sum_(n=0)^2 |n> W_n...W_1|psi>` после clock-условия и следа по среде даёт `Phi_*^n(rho_0)` точно; ветви `1,13,169`, но продолжение `C21 -> C273` оставляет `U(252)` | VIII-P23/N34 |
| `V_z=P_W+z(I-P_W)`, `|z|=1`, удовлетворяет `V_zW=W` и сохраняет тот же канал; gauge допускает `U(1)`, а Real-чётность оставляет `z=±1`, поэтому полный clock-unitary не каноничен | VIII-N35 |
| `H_int=sum_a D_a tensor (|a><0|+|0><a|)` на `C21 tensor C13` имеет `<0|H_int^2|0>=G` и при `U_h=exp(-i sqrt(h)H_int)` даёт `Phi_h=I+hL_cross+O(h^2)`; real gauge-коммутант самосопряжённых interaction-связей имеет размерность `8`, symmetric rate-метрика `C^T C` — `4`, а точный конечный Kraus-шаг различается на `O(h^2)` | VIII-P24/N36 |
| `K_B(delta B_1,delta B_2)=Tr(delta D_B^(1)delta D_B^(2))=3I_12`; при условии `E_jump=(E_cross)^*` относительно того же следа получаем `R=K_B^-1=I_12/3`, `C=O/sqrt(3)`, `O^TO=I`; ортогональная свобода — кадр среды, а общий множитель времени остаётся свободным | VIII-P25/N37 |
| Одна полевая форма `S_field=(1/2)x^T(3I_12)x` допускает `R_1=I_12/3` и `R_2=diag(I_6/3,2I_6/3)` с разными GKSL-генераторами; только добавочное Riesz-условие `K_BR=I_12` единственно выбирает `R_1` | VIII-N38 |
| `dim_R N_mix=2*15+12=42=dim_R F_full`, тогда как текущий кадр имеет `25` jump-направлений и коразмерность `17`; uniform-комплексфикация дала бы ошибочные `54 real` | VIII-P26/N39 |
| Linking closure имеет ранги `1->4->5->5`; `5 complex linking + 10 complex heavy` после realification и добавления `12 Hermitian gauge` дают `42-real` frame, `rank K_trace=42`, `K_trace R=I_42` | VIII-P27/N40 |
| `L_42(X)=sum_(a=1)^42(F_a X F_a-(1/2){F_a^2,X})`; старый 25-jump span содержится в полном, поэтому `Fix L_42=C I_21`, а invertible trace-dual whitening сохраняет fixed algebra | VIII-P28/N41 |
| `H_int^42=sum_(a=1)^42 F_a tensor (|a><0|+|0><a|)` действует на `C21 tensor C43=C903`, имеет vacuum second moment `sum F_a^2` и при `h=u/n` даёт `exp(uL_42)`; масштаб и fresh ancilla остаются внешними | VIII-P29/N42 |
| `H_int^42 -> gH_int^42` влечёт `L_42 -> g²L_42`, а `t_phys -> t_phys/g²` сохраняет `g²t_phys`; поэтому `t_*=hbar/E_*` требует независимого `E_*` и collision-расписания | VIII-P30/N43 |
| `V=(I21 tensor S_chain)U_col^(0)` на `otimes_(m in Z)(C43,|0>)` удовлетворяет `Tr_chain Ad(V)^n(rho tensor omega_vac)=Phi_h^n(rho)` для всех конечных `n`; внешний reset устранён, но vacuum-chain остаётся ресурсом | VIII-P31/N44 |
| `H_Lambda=sum_m(I-|0><0|_m)` имеет единственный тензорный вакуум и щель `1`, но `ind_GNVW(S_43)=43`; локальный родитель состояния не порождает конечновременной локальный сдвиг | VIII-P32/N45 |
| Встречные цепи дают `ind(S_A S_B^(-1))=43*(1/43)=1`; два слоя `W_0=prod SWAP(A_m,B_m)`, `W_1=prod SWAP(B_m,A_(m+1))` точно реализуют локальный конвейер и сохраняют `Phi_h^n` | VIII-P33/N46 |
| Минимальный одночастичный шаг `U(k)=diag(e^(-ik),e^(ik))` имеет числа намотки `(-1,+1)`; периодический конечнодальний статический логарифм, сохраняющий число, невозможен | VIII-N47 |
| Для трёхсостоянийных часов `A=[[0,sqrt(2),0],[sqrt(2),0,sqrt(2)],[0,sqrt(2),0]]` выполнено `exp(-i pi A/2)|0>=-|2>`; два слоя исполняются точно один раз, но часы не возвращаются | VIII-P34/N48 |
| При `epsilon_d<=A exp(-cd)` глобальная ошибка конечного конвейера не превосходит `2LA exp(-cd)`, поэтому достаточно `d>=c^(-1)log(2AL/delta)`; локальный и глобальный пределы различны | VIII-P35/N49 |
| Совместная ошибка часов и столкновений ограничена `C_u/n+nA exp(-cd)`; расписание `d_n>=(1+alpha)c^(-1)log n` даёт локальный предел `exp(uL_42)` без внешнего переключателя | VIII-P36/N50 |
| Преобразование `(Omega,Gamma,t_phys)->(lambda Omega,lambda Gamma,t_phys/lambda)` сохраняет наблюдаемые комбинации; автономный процесс не фиксирует абсолютную секунду | VIII-N51 |
| `tau_C=hbar/E_C`, `E_int=chi E_C` дают `Gamma=chi^2E_C/hbar` и `Gamma/Omega=chi^2`; мост размерностно корректен, но текущий родитель не выбирает ни `E_C`, ни `chi` | VIII-P37/N52 |
| Шесть кандидатов на `E_C` — обрезание, радиусы, щель `L_42`, щель вакуумного проектора, компактон и наблюдаемые массы — сохраняют масштабную свободу либо не имеют типизированного отображения в часы | VIII-N53 |
| `G=sum_a F_a tensor (|a,0_C><0,1_C|+h.c.)` удовлетворяет `[H_0,G]=0`, `<eta|G|eta>=0`, `<eta|G^2|eta>=sum_aF_a^2`; полный шум имеет энергосохраняющий родитель, но `H_mix=E_C(H_0+chi G)` сохраняет свободу `chi` и орбиту `(E_C,t)->(lambda E_C,t/lambda)` | VIII-P38/N54 |
| Шесть весов `kappa_L,kappa_3,kappa_2,kappa_1,kappa_Q,kappa_X` являются точными функциями `x=e^-2` общего КМС-следа; для барионного среза `v_eta` строго убывает, а `eta*=52(105133x²+28806x-13799)/(16609x(x+5)(25x+13))<0`, поскольку `e^-2<1/7` | VIII-P39/N55 |
| Три комплексные `QLYR`-стрелки дают `C_Q=I6/[2(a+b)]`, связывающая инцидентность — `C_L=I6/[13(a+b)]`; исходный КМС-угол сохраняет множитель `x`. Поэтому прежнему стрелочному члену требуется множитель `2`, связывающему — `1`, а прямой кандидат равен `v_dir=52(25x²+38x+13)/(375x³+3916x²+7267x+2782)` | VIII-P40/N56 |
| Ковариация трёх копий `R_c=(1-c)I3+c11^T` вполне положительна при `-1/2<=c<=1` и не меняет одночастичный генератор; `K3=3J1q`, `Delta3/Delta2=3/2`, но `v_c=c v_dir`, поэтому общий шум `c=1` не следует из одночастичной теории | VIII-P41/N57 |
| Вакуумный второй момент многокопийной среды равен `sum_(a,r,s) R_rs F_a^(r)F_a^(s)`; независимые ячейки дают `R=I3`, общая ячейка — `R=11^T`, и обе редуцируются к одному однокопийному родителю. На парном контрольном наблюдаемом квадрат различия равен `8c²` | VIII-P42/N58 |
| На всём трёхкварковом носителе `A=sum_r Q_r²`, `C=sum_(r!=s)Q_rQ_s` удовлетворяют `A+C=Q_tot²`; общий оператор `(mu A+lambda C)/T` сворачивается к `Q_tot²/T` только при `mu=lambda=1`, а `E_n-E_p=-(mu+2lambda)/(3T)` отрицательно лишь условно на положительном электростатическом конусе | VIII-P43/N59 |
| Для фиксированных меток `T(E_n-E_p)=-mu/3+2(g_23-2g_12)/3`, поэтому положительное неоднородное ядро может сменить знак; после перестановочного усреднения `T(E_n-E_p)=-(mu+2g_bar)/3`, но для кулоновского ядра растяжение `psi_s=s^(3d/2)psi(sr)` даёт `<1/r>_s=s<1/r>` и не выбирает величину `g_bar` | VIII-P44/N60 |
| Два точных состояния с `S=1/2` дают `O_n-O_p=2` и `-4/3`; после выбора полностью симметричного спин-ароматного сектора `I=S=1/2` получается `O_p=4/3`, `O_n=1` и условно `E_n^mag-E_p^mag=-zeta h/(3T)`, причём контакт масштабируется как `s^d` | VIII-P45/N61 |
| Характеры `S_3` дают матрицу инвариантных кратностей `I_3`: цветовой эпсилон допускает пары `(1,1)`, `(1_sgn,1_sgn)`, `(2,2)`. В секторе `I=S=1/2` магнитные разности равны `-1/3`, `1`, `1/3`; симметричную ветвь выбирает только условие `ker(H_space-E0)=1` | VIII-P46/N62 |
| Центральное семейство `H=alpha T2+beta T3` имеет уровни `3alpha+2beta`, `-3alpha+2beta`, `-beta` и делает основным любой тип `S_3`; только улучшающая положительность полугруппа вместе с симметрией вынуждает `U_pi psi0=psi0` | VIII-P47/N63 |
| При `A_el=mu+2g_bar>0` три полные разности равны `-A_el-z`, `-A_el+3z`, `-A_el+z` в единицах `3T`; общий отрицательный знак эквивалентен `-A_el<z<A_el/3`, но `z` и ветвь не выведены | VIII-P48/N64 |
| Семейство `p_theta=(1+theta x1x2x3)/8` имеет одинаковые одно- и двухчастичные ограничения, но третью кумулянту `theta`; отображение попарных маргиналов имеет ранг `7` и одномерное ядро. Звёздный родитель нечётен по чётности среды, а ограниченная третья кумулянта подавляется как `u epsilon kappa_3`, поэтому текущий GKSL-предел не определяет шеститочечное барионное ядро | VIII-P49/N65 |
| Центрированный кадр `Fhat_a=F_a-Tr(F_a)I/21` сохраняет двойной коммутатор и ранг `42`. Кубический тензор `d_abc=Tr(Fhat_a{Fhat_b,Fhat_c})/2` имеет `168=140 TTG+28 GGG` ненулевых компонент и задаёт связный `W3=d^abc Fhat_a tensor Fhat_b tensor Fhat_c` с нулевыми частичными следами; коэффициент `lambda_3` текущим действием не выведен | VIII-P50/N66 |
| На луче `A=Fhat_0+Fhat_40` моменты равны `(Tr A²,Tr A³,Tr A⁴)=(38,-3,134)`. Квадратичный родитель имеет нулевую третью вариацию; чистый кубический член не ограничен снизу, а положительная квартика допускает любое `lambda_3`. Стационарность даёт лишь `lambda_3=(76alpha+536beta)/9` и устойчивость `beta>19alpha/134` | VIII-N67 |
| Сдвинутая кривизна `R_m(Z)=((m/2)I+Z)²-(mI/2)²=mZ+Z²` даёт одной нормой `Tr R_m²=m²Tr Z²+2mTr Z³+Tr Z⁴`, поэтому `lambda_3²/(alpha beta)=4` и кубическая вариация равна `12m d_abc`. Но `Gamma M+M Gamma=m Gamma`: ненулевой центральный фон чётен, так что настоящая градуированная суперкривизна не получена | VIII-P51/N68 |
| Для любого нечётного `D` выполнено `Tr(D_odd S_even)=0`. Поэтому его кубическая опора лежит в `TTT+TGG` и не пересекает `140 TTG+28 GGG` тензора `d_abc`; на физическом инцидентном фоне она равна `130 TTT+35 TGG`. Допустимые `TTG/GGG`-вершины полной суперкривизны содержат производные и исчезают при нулевом импульсе | VIII-N69 |
| Блочное отображение `J(delta A,delta B_s,delta B_t)=[[delta B_s,delta A*],[delta A,delta B_t]]` имеет матрицу `I_42`, ранг `42` и нулевое ядро; все `504` тождества `J delta_X=i ad_X J` выполнены точно. Следовая метрика переносится как `G_поле=J* K J=K`, но семейство `diag(s_п I_30,s_к I_12)` оставляет относительную нормировку и физическую мобильность невыбранными | VIII-P52/N70 |
| На постояннополевом срезе `H_пост=diag(H_A,0_12)` имеет ранг `30`, тогда как следовая метрика `K` имеет ранг `42`, а её калибровочный блок — ранг `12` и след `367/3`. Поэтому не существует `c` с `H_пост=cK`; при ненулевом импульсе появляется отдельный множитель `p²g^{mu nu}-p^mu p^nu` и необходимость фиксации калибровочной свободы | VIII-N71 |
| Калибровочный гессиан факторизуется как `H_0=K_к tensor p²P_T`, имеет ранг `36` и ядро `12`. После фиксации `H_xi=K_к tensor p²(P_T+xi^-1P_L)` имеет ранг `48` и обратный `K_к^-1 tensor p^-2(P_T+xi P_L)`; поперечная часть независима от `xi`, но абсолютная мобильность не выбрана | VIII-P53/N72 |
| Корреляция среды `C_1=K_к^-1` задаёт форму ранга `36`, но `g→2g` даёт `M_2=4M_1` при той же нормированной форме; `t→t/4` сохраняет `g²t`. Среда не выбирает абсолютный масштаб | VIII-P54/N73 |
| Полный главный символ `H_0=diag(K_п tensor I4,K_к tensor P_T)` имеет размерность `168`, ранг `156` и ядро `12`; после фиксации `H_xi` имеет ранг `168` и точный блочный обратный. Независимые веса `w_п,w_к` сохраняют эту структуру, поэтому их отношение не выбрано | VIII-P55/N74 |
| Для `D=i gamma^mu(partial_mu+B_mu)+gamma5 Phi` общий коэффициент `a4` даёт `c_Phi=2`, `c_F^+=2/3` и отношение `w_п/w_к=3`. Это строгий выбор внутри стандартного лапласова подъёма, но сам подъём ещё не выведен из конечного 42-мерного родителя | VIII-P56/N75 |
| Семейство `D_r=r D_M tensor I21+gamma5 tensor D_F` сохраняет `[D_r,I4 tensor a]=gamma5 tensor[D_F,a]` для всех 42 внутренних направлений, но внешний квадрат меняется `I4 -> 4I4` при `r:1->2`. Конечный родитель не выбирает геометрию базы | VIII-N76 |
| На полном носителе `rank H_Phi=28`, `nullity H_Phi=2`, `rank H_B=3`, `nullity H_B=9`; после нормировки `Tr M_Phi^4=23053/18`, `Tr M_B^4=36897/722`, поэтому `N_bos=4659176/3249`. Полный `B` не закрыт без BV-фактора и фермионной кратности при `Tr D_F^4=46` | VIII-P57/N77 |
| Полная хиральная проекция `P_phys=(I_84+gamma_5 tensor Gamma_F)/2` имеет ранг `42` и даёт фермионный момент `2 Tr D_F^4=92`. Однако `rank X_orb=rank(X_orb^T H_Phi X_orb)=3` и след ограничения равен `34`, поэтому прежний гессиан нарушает голдстоуновский критерий; `4360268/3249` остаётся лишь фиксированно-фоновым кандидатом | VIII-P58/N78 |
| Орбитальная метрика равна `14I_3`; её ортогональный проектор даёт `H_quot=Q^T H_Phi Q` с рангом `26` и ядром `3_Goldstone+1_horizontal`. Точные моменты: `Tr M_Phi,quot^4=1118917/882`, `N_bos^BV=226371884/159201`, `N_quad^BV=211725392/159201`. Последнее число условно до нелинейного родительского подъёма | VIII-P59/N79 |
| Фазовая плоскость `Z=(z_u,z_r)` имеет метрику `diag(6,20)` и орбитальную связь с единственной строкой `(-6,8)`, поэтому горизонтальная комбинация равна `v_0=4z_u+3z_r`, `||v_0||_K²=276`. Семейство `A(z)=diag(z^4I_3,z^3I_7)A_0` сохраняет оба грамовых конца; максимальные миноры `10x11` имеют носитель размерности `C(11,10)C(10,10)=11`, не скаляр | VIII-P60/N80 |
| Кофактор максимальных миноров равен `(0,0,0,0,0,0,-1,0,0,1,0)^T`, имеет норму `2` и преобразуется как `c(A(z))=z^33c(A_0)`. Determinant-гиперзаряды обоих концов равны `-2`, но `dim Hom_G(E_s,C)=0`; Real-норма остаётся `2`. Значит, фазочувствительная линия существует, а канонической скалярной тривиализации нет | VIII-P61/N81 |
| Полная бимодульная опора имеет `rank partial=8` на `9` вершинах и `11` рёбрах, поэтому `b1=3`; инцидентностная часть является лесом. Для точного базиса циркуляций `C` тяжёлая проекция имеет ранг `3`, но листовое ребро `Q_Lu_R` имеет нулевую строку и `qC=0` при `q=(4,3,...,3)`. Все обычные тяжёлые голономии горизонтально нейтральны | VIII-P62/N82 |
| Повышающая матрица полного двуслойного колчана удовлетворяет `N²=0`, а Real-завершение `D_R=N+N*` нечётно и преобразуется как `D_R(z)=G(z)D_R(1)G(z)^-1`. Нечётные моменты `1,3,5` равны нулю, чётные `2,4,6` равны `(22,110,682)` и фазонезависимы. Независимая обратная копия изменила бы размерность `40 -> 80`; условия `alpha beta=-1` и `beta=conjugate(alpha)` несовместимы | VIII-N83 |
| Представление переноса раскладывается как `H_+ + 4H_- + C_+ + C_- + 4S_0`. Пространство инвариантных кососимметрических форм имеет размерность `11`, но `rank Omega<=14` и `dim ker Omega>=6`; две различные формы достигают ранга `14`. Для одного бозонного поля `Phi^T Omega Phi=0`. Невырожденная достройка требует `6` новых комплексных направлений и размерности `26` | VIII-P63/N84 |
| Сбалансированное представление `4H_+ + 4H_- + C_+ + C_- + 4S_0` имеет размерность `26 complex = 52 real`. Явная форма удовлетворяет `Omega_0^2=-I`, `det Omega_0=1`, `rank Omega_0=26`; пространство инвариантных форм 23-мерно. Текущий endpoint имеет `m_+=1` вместо `4`, поэтому котангенциальной достройке недостаёт `3` копий, или `6` комплексных направлений | VIII-P64/N85 |
| На `T_26` матрицы `K_a=Omega_0 rho(X_a)` симметричны и задают ненулевое отображение момента `mu_a=x^T K_a x/2`; ранг 14 записанных компонент равен `13` из-за одной центральной зависимости. Котангенциальная фаза `q->zq`, `p->z^-1p` сохраняет `Omega_0`, коммутирует с gauge-действием и даёт `mu(S_zx)=mu(x)`, поэтому `lambda||mu-zeta||²` горизонтальную фазу не поднимает | VIII-P65/N86 |
| Реалификация нового носителя имеет размерность `52`, старый полный след — `42`, поэтому любой pullback имеет `rank<=42` и `nullity>=10`; transfer-only метрика оставляет `22` нулевых направления. Семейство `G_s=I_42 direct_sum diag(s,s^-1)^5`, `J_s=-Omega G_s` удовлетворяет `J_s²=-I`, `Omega J_s=G_s>0` и одинаково ограничивается на старый след, но различно при `s=1,2` | VIII-N87 |
| Полный перебор `C(44,3)=13244` троек центрированного кадра даёт `supp d=140 TTG+28 GGG` и `supp C=106 TTG+10 GGG` при пустом пересечении. `C_abc=Tr(F_a[F_b,F_c])` антисимметричен и имеет нулевую полную симметризацию; производная вершина линейна по импульсу и даёт `K_6^derivative(0)=0`, поэтому локальный маршрут к ненулевому `lambda_3 W3` закрыт | VIII-N88 |
| Нелокальное одевание `K_f(k)=lambda_3 f(k²)W3` допускает положительные формы `f_1=1/(z+1)` и `f_2=1/(2(z+1))+2/(z+4)` с общим `f(0)=1`, но различными наклонами `-1,-5/8` и значениями `1/2,13/20` при `z=1`. Поэтому класс существует, а спектральная мера не выбирается текущими условиями | VIII-P51/N89 |
| Вспомогательный родитель `(z+m²)phi²/2-g phi J` даёт дополнением Шура `-g²J²/(2(z+m²))`. Статическое условие фиксирует `g²/m²=lambda_3`, но орбита `(m²,g²)->(qm²,qg²)` сохраняет `f(0)=1` и меняет `f'(0)=-1/(qm²)`; конечная геометрия не выбирает масштаб базы | VIII-P52/N90 |
| Контракт спектрального якоря требует веса `L^-2`, внутреннего выбора, типизированной карты в `K6` и разрыва орбиты. Масштаб базы, часы, шум, вакуумный гессиан, cutoff/радиус и наблюдаемая масса дают индикаторы `(0,0,0,0,0,0)` | VIII-N91 |
| Для `m²=ca` форма `f=ca/(z+ca)` требует независимо выбранных масштаба `a` и карты `c`: свидетели равны `1/2` и `2/3` при изменении любого входа. Нормировка удаляет `lambda_3`, поэтому полный оператор требует третьего независимого datum | VIII-P53/N92 |
| Классический родитель `a²(c-c0)²` имеет вакуум `c=c0`, произвольное `a` и гессиан `diag(0,2a²)`. Логарифмический родитель при `B>0` условно даёт минимум `(mu²,c0)` с гессианом `diag(2B,2mu⁴)`, но входы трансмутации не выведены | VIII-P54/N93 |

### Литературно направляемый следующий объект

Первый допуск выполнен отрицательно: двухточечные данные не определяют
трёхчастичный объект. Литературная формула задаёт уровень следующего
родительского поиска, но ещё не является выведенным ядром проекта:

$$
\Psi=K_{(3)}\Psi,
\qquad
K_{(3)}=K_{(3)}^{\rm irr}+\sum_{a=1}^{3}K_{(2)}^{(a)}.
$$

Точный контрпример

$$
p_\theta(x_1,x_2,x_3)=\frac18(1+\theta x_1x_2x_3)
$$

имеет одинаковые одно- и двухточечные ограничения при всех `theta`, но
третью кумулянту `theta`. Точный гейт дополнительно показал, что текущий
слабый столкновительный предел не сохраняет ограниченный третий порядок.
См. [[version8-baryon-connected-three-body-kernel-admission-gate]],
[[version8-post-electromagnetic-research-fork]] и
[[baryon-six-point-faddeev-literature-2026]].

## Наследованные входы барионной трансмутации

Текущий строгий zero-mode блок раннего уровня даёт

$$
B_0=\frac{67}{64\pi^2}>0,\qquad b=2,\qquad
\log\frac{\Lambda_L}{\mu_{\rm spec}}=\frac{32\pi^2}{3}.
$$

Полный коэффициент остаётся

$$
B_{\rm full}=\frac{67+c_\sigma^2+\Delta N_{\rm KK}}{64\pi^2},
$$

а общая масштабная орбита сохраняет `Lambda_DT/mu`. Поэтому вычислены два
безразмерных подблока, но не абсолютная шкала и не карта `c0`; см.
[[version8-baryon-dimensional-transmutation-input-origin-gate]].

Конечный аудит карты `c0` обнаруживает точное численное совпадение
скалярного mass-square ratio и суперкривизностного shape ratio:

$$
c_s=4,\qquad \frac{\lambda_3^2}{\alpha\beta}=4.
$$

Но ни один из этих объектов не является типизированным отношением
`m_pole²/a`. Семь кандидатов дают `0/7`; см.
[[version8-baryon-c0-typed-internal-map-candidate-audit-gate]].

Минимальная новая стрелка классифицируется точно:

$$
\operatorname{Hom}_G(L_{\rm src},L_{\rm aux})\cong\mathbb R,
\qquad c_0=\kappa r_*,\qquad \kappa>0.
$$

Условие изометрии даёт `kappa²=1` и положительное решение `kappa=1`, но
ещё не следует из текущего общего следа; см.
[[version8-baryon-c0-minimal-cross-carrier-morphism-architecture-gate]].

Для разделённой алгебры общий нормированный след имеет центральные веса
`p+q=1`, а pullback-изометрия даёт

$$
q\kappa^2=p,\qquad \kappa=\sqrt{p/q}.
$$

Следовательно, common trace без linking-бимодуля только переносит свободу
в отношение `p/q`; см.
[[version8-baryon-c0-common-trace-embedding-normalization-gate]].

Минимальный linking-блок устраняет эту свободу:

$$
EE^*=P_s,\qquad E^*E=P_a,\qquad
\tau_2(P_s)=\tau_2(P_a)=\frac12,
\qquad \kappa=1.
$$

При `r_star=4` это условно даёт `c0=4`, но требует классификации `E` в
существующем 42-carrier; см.
[[version8-baryon-c0-linking-algebra-offdiagonal-bridge-admission-gate]].

Существующий 42-carrier такой мост не содержит:

$$
\operatorname{Hom}_G(\mathbb C_0,H_{21})=0,\qquad
\operatorname{rank}Y=21,
$$

а его нулевое расширение удовлетворяет
`iota(X)P_aux=P_aux iota(X)=0`. Поэтому imprimitivity требует нового
endpoint state; см.
[[version8-baryon-c0-existing-42-carrier-linking-bridge-classification-gate]].

Минимальное исправление endpoint-дефицита имеет точный размер:

$$
H_{23}=H_{21}\oplus\mathbb C s_0\oplus\mathbb C a_0,
\qquad
\mathcal F_{45}=\iota(\mathcal F_{42})\oplus\operatorname{span}_{\mathbb R}\{X,Y,H\},
$$

$$
[X,Y]=2iH,\qquad K_{45}=K_{42}\oplus2I_3.
$$

См. [[version8-baryon-c0-minimal-neutral-endpoint-extension-gate]].

Динамика этого расширения имеет точный двухцентровый остаток:

$$
\operatorname{Fix}(\mathcal L_{45})
=\mathbb C P_{21}\oplus\mathbb C P_{\mathrm n},
\qquad
\mathcal L_{45}(X,Y,H)=-4(X,Y,H),
$$

а старо-новый блок удовлетворяет

$$
\mathcal L_{45}(B)=-\frac12(Q_{42}B+3B),
\qquad Q_{42}=\sum_aF_a^2>0.
$$

Когерентности затухают, но популяции двух центральных компонент не
обмениваются; см.
[[version8-baryon-c0-extended-45-frame-fixed-algebra-and-dynamics-gate]].

Минимальный калибровочно-ковариантный коннектор классифицируется системой

$$
G_jV=0,qquad (Y+I)V=0,qquad
\Gamma_{21}V+V\Gamma_{\mathrm n}=0,qquad
\dim_{\mathbb C}\mathcal V_{-1}^{\rm odd}=3.
$$

Его две квадратуры дают

$$
K_{47}=K_{45}\oplus2I_2,qquad
\operatorname{Fix}(\mathcal L_{47})=\mathbb C I_{23},
$$

но Real-направление принадлежит `RP2`; см.
[[version8-baryon-c0-old-new-gauge-covariant-connector-classification-gate]].

Общий след на multiplicity-пространстве даёт только радиальную форму:

$$
S_{\rm iso}(z)=\frac a2\|z\|^2+\frac b4\|z\|^4,
\qquad
\mathcal M_{\rm vac}=\mathbb{RP}^2,
$$

$$
\operatorname{rank}\Hess S_{\rm iso}(z_*)=1,
\qquad \dim\ker\Hess S_{\rm iso}(z_*)=2,
\qquad N_{\rm derived}=0/2.
$$

См. [[version8-baryon-c0-connector-multiplicity-and-rate-parent-selector-gate]].

Расширенная концевая алгебра индуцирует семейство

$$
K_{\rm conn}(p,q)=\operatorname{diag}(p_0+q,p_1+q,p_2+q),
\qquad p_0+p_1+p_2+2q=1,
$$

а полное Hom-замыкание даёт

$$
\operatorname{Alg}(E_{\rm full})=M_5(\mathbb C),
\qquad K_{\rm conn}^{(5)}=\frac25I_3,
\qquad \operatorname{rank}\mathcal F_{51}=51.
$$

См. [[version8-baryon-c0-extended-endpoint-bimodule-weight-origin-gate]].

Полный и одиночный connector-процессы разделяются Kraus-рангом:

$$
C_{\rm full}=I_3,quad \operatorname{rank}C_{\rm full}=3,
\qquad
C_z=zz^*,quad \operatorname{rank}C_z=1,
$$

хотя центральный срез удовлетворяет

$$
D_{\rm cen}(I_3)=3D_0=D_{\rm cen}(3zz^*)
\qquad (\|z\|=1).
$$

См. [[version8-baryon-c0-full-multiplicity-frame-single-map-compatibility-gate]].

На минимальной multiplicity-среде скалярное gauge-действие не ограничивает
матрицу плотности, а Real-чистые состояния образуют

$$
\rho_z=zz^{\mathsf T},\qquad z^{\mathsf T}z=1,
\qquad [z]\in\mathbb{RP}^2.
$$

Канонические изотропные правила дают

$$
\rho_{\rm tr}=\rho_\beta=\frac13I_3,
\qquad
\operatorname*{argmin}_{\rho=\bar\rho}2(1-\operatorname{Tr}\rho^2)
=\{zz^{\mathsf T}:[z]\in\mathbb{RP}^2\}.
$$

Следовательно, trace/Gibbs выбирает смешанное состояние, а purity выбирает
орбиту без направления; итог `N_{unique pure selector}=0/5`. См.
[[version8-baryon-c0-multiplicity-environment-pure-state-selector-gate]].

Минимальный одноосный Hamiltonian выбранного projector имеет вид

$$
h(P;\varepsilon,\Delta)=\varepsilon I_3+\Delta(I_3-P),
\qquad
\operatorname{Spec}h=\{\varepsilon^{(1)},(\varepsilon+\Delta)^{(2)}\}.
$$

При `x=exp(-beta Delta)` его Gibbs-state равен

$$
\rho_{\beta,P}=\frac{P+x(I_3-P)}{1+2x},
\qquad
\operatorname{Tr}\rho_{\beta,P}^2
=\frac{1+2x^2}{(1+2x)^2}<1
$$

для всякого конечного `beta Delta`; точный projector возникает только при
`x -> 0`. См.
[[version8-baryon-c0-multiplicity-environment-hamiltonian-minimal-data-gate]].

Три собственных источника multiplicity-Hamiltonian дают

$$
H_{\rm old}=0_3,
\qquad H_{\tau_5}=\frac{2\alpha}{5}I_3,
\qquad H_C=\alpha_C I_3.
$$

Ранний семейный near miss имеет

$$
\operatorname{disc}\chi_{R_4^+}=\frac{164241}{16}>0,
\qquad
\sum_{i=0}^2\|[R_4^+,\Pi_i]\|_{\rm HS}^2=50,
$$

поэтому анизотропия существует на чужом носителе, но её endpoint-
совместимый перенос требует новой карты `T`. См.
[[version8-baryon-c0-multiplicity-environment-hamiltonian-parent-origin-gate]].

Текущая типизация двух qutrit-носителей даёт

$$
\mathcal E_{\rm fam}\simeq\mathbf3_{SO(3)},\qquad
\mathcal E_{\rm mult}\simeq\mathbf1^{\oplus3},\qquad
\operatorname{Hom}_{SO(3)}(\mathbf3,\mathbf1^{\oplus3})=0.
$$

После условного повышения target до стандартной тройки

$$
\operatorname{Hom}_{SO(3)}(\mathbf3,\mathbf3)=\mathbb R I_3,\qquad
T^{\mathsf T}T=I_3\Longrightarrow T=\pm I_3.
$$

Этот проход требует нового семейного действия, несовместимого с
неподвижностью всех endpoint-проекторов. См.
[[version8-baryon-c0-family-to-multiplicity-intertwiner-admission-gate]].

Текущая стрелочная реализация этого условного действия имеет вид

$$
W_{\rm cur}=\operatorname{span}\{E_{00},E_{11},E_{21}\}
\subset\operatorname{Hom}(\mathbb R^2,\mathbb R^3),
$$

но не замкнута относительно левого стандартного `SO(3)`-действия. Точное
минимальное замыкание равно

$$
\operatorname{span}(W_{\rm cur},J_aW_{\rm cur})
=M_{3\times2}(\mathbb R)\simeq\mathbf3\oplus\mathbf3,
$$

а общий семейный интертвейнер и его метрика равны

$$
T_{u,v}=\begin{pmatrix}uI_3\\vI_3\end{pmatrix},\qquad
T_{u,v}^{\mathsf T}T_{u,v}=(u^2+v^2)I_3.
$$

После изометрии остаётся `[u:v] in RP1`; см.
[[version8-baryon-c0-multiplicity-environment-so3-action-parent-origin-gate]].

Точная grading-проверка даёт

$$
\Delta_\Gamma(u,v)=8u^2+4v^2,qquad
\min_{u^2+v^2=1}\Delta_\Gamma=4>0,
$$

поэтому старый `RP1` не содержит допустимой нечётной точки. Минимальное
однородное завершение использует положительную ветвь:

$$
n_+=1<n_-=2,qquad
H_{mathbf3}^{(+)}=\operatorname{span}
\{e_R^{(t,0)},e_R^{(t,1)},e_R^{(t,2)}\}.
$$

Его endpoint- и rate-структуры равны

$$
\operatorname{Alg}(D_3,J_1,J_2,J_3)=M_3(\mathbb C),qquad
C_{SO(3)}=\gamma_1P_{mathbf1}+\gamma_3P_{mathbf3}.
$$

См. [[version8-baryon-c0-so3-closed-environment-source-line-selector-gate]]
и [[version8-baryon-c0-grading-compatible-family-triplet-endpoint-extension-gate]].

Для полного connector-типа `1+3` семейная covariance имеет вид

$$
C=\gamma_1P_{\mathbf1}+\gamma_3P_{\mathbf3},qquad
r=\frac{\gamma_3}{\gamma_1}>0.
$$

Два точных trace-one представителя дают

$$
\rho_{\rm arrow}=\frac14I_4\Rightarrow r=1,qquad
\rho_{\rm sector}=\frac12P_{\mathbf1}+\frac16P_{\mathbf3}
\Rightarrow r=\frac13.
$$

См. [[version8-baryon-c0-family-triplet-singlet-relative-rate-selector-gate]].

Центральное Gibbs-семейство переписывает тот же свободный вес через одну
безразмерную щель:

$$
p=\frac{1}{1+3e^{-\beta\Delta}},\qquad
r=e^{-\beta\Delta},\qquad
\beta\Delta=\log\frac{3p}{1-p}.
$$

Обычный след соответствует `p=1/4`, но любой вес получается симметричным
центральным переопределением

$$
Z_p=4pP_{\mathbf1}+\frac{4(1-p)}{3}P_{\mathbf3},\qquad
\rho_p=Z_p\frac{I_4}{4}.
$$

См. [[version8-baryon-c0-singlet-triplet-central-trace-weight-parent-origin-gate]].

После факторизации общего нуля энергии минимальный центральный гамильтониан
и его равновесный вес имеют вид

$$
h=\varepsilon I_4+\Delta P_{\mathbf3},\qquad
\theta=\beta\Delta,\qquad
p(\theta)=\frac{1}{1+3e^{-\theta}}.
$$

Gibbs-вариационный функционал строго выпуклый:

$$
\Phi_\theta(p)=(1-p)\theta-S(p),\qquad
\Phi_\theta''(p)=\frac{1}{p(1-p)}>0.
$$

См. [[version8-baryon-c0-singlet-triplet-central-weight-minimal-hamiltonian-data-gate]]
и [[singlet-triplet-gibbs-gap-literature-2026]].

На условном семейном endpoint центрированные grading и оператор Казимира
задают одно и то же направление щели:

$$
Q=P_{\mathbf3}-\frac34I_4,\qquad
\Gamma_4^0=\mathcal C_2^0=2Q,\qquad
h_{\rm cen}=\varepsilon I_4+\lambda Q.
$$

При этом два положительных представителя `P3` и `P1` соответствуют
противоположным знакам `lambda`, а квадратичный функционал удовлетворяет
`(lambda Q)^2=(-lambda Q)^2`.

См. [[version8-baryon-c0-singlet-triplet-central-gap-parent-action-origin-gate]].

Единичная нормировка этого направления не канонична:

$$
\operatorname{Tr}Q^2=\frac34,
\qquad
\left\{|\lambda|\right\}
=\left\{1,2,\frac2{\sqrt3},\frac43,\frac23,\frac4{\sqrt3}\right\}.
$$

Равновесие сохраняет масштабную орбиту
`(beta,lambda)->(beta/a,a lambda)`, а минимальная явно выбирающая структура
должна добавить нечётный источник:

$$
V_{\rm src}(\lambda)=\frac{m^2}{2}\lambda^2-j\lambda,
\qquad \lambda_*=\frac{j}{m^2}.
$$

См. [[version8-baryon-c0-singlet-triplet-central-gap-coefficient-selector-gate]].

Минимальный условно допустимый parent завершает квадрат:

$$
V_{\rm src}(\lambda)=\frac{m^2}{2}\lambda^2-j\lambda
=\frac{m^2}{2}\left(\lambda-\frac{j}{m^2}\right)^2
-\frac{j^2}{2m^2},
\qquad
\lambda_*=\frac{j}{m^2},
\qquad
V''(\lambda_*)=m^2.
$$

Его операторное поднятие на `h^0=lambda Q` равно

$$
\mathcal S_{\rm src}[h^0]
=\frac{m^2\operatorname{Tr}((h^0)^2)}{2\operatorname{Tr}Q^2}
-\frac{j\operatorname{Tr}(Qh^0)}{\operatorname{Tr}Q^2}.
$$

Вакуум сохраняется на луче `(m²,j)->(a m²,a j)`, поэтому положение
минимума без его физической кривизны не восстанавливает parent.

См. [[version8-baryon-c0-singlet-triplet-central-gap-minimal-source-parent-architecture-gate]].

Незавешенный спектральный след на скалярном фоне не создаёт источник:

$$
\left.\frac{d}{d\lambda}
\operatorname{Tr}(\varepsilon I_4+\lambda Q)^n\right|_{\lambda=0}
=n\varepsilon^{n-1}\operatorname{Tr}Q=0.
$$

Условная маркированная реализация использует единственное направление
`Gamma4^0=C2^0=2Q`:

$$
a_2\operatorname{Tr}((h^0)^2)
-g\operatorname{Tr}(\Gamma_4^0h^0)
=\frac34a_2\lambda^2-\frac32g\lambda,
\qquad
m^2=\frac32a_2,
\quad j=\frac32g.
$$

Формы существуют, но коэффициенты `a2,g` не выведены.

См. [[version8-baryon-c0-singlet-triplet-central-gap-source-stiffness-parent-origin-gate]].

Минимальный динамический носитель условно заменяет внешний источник:

$$
V(\lambda,s)=\frac M2\lambda^2-gs\lambda+\frac u4s^4
=\frac M2\left(\lambda-\frac gM s\right)^2
+\frac u4s^4-\frac{g^2}{2M}s^2.
$$

Нуль имеет `det Hess=-g²`, а два устойчивых вакуума удовлетворяют

$$
s_*^2=\frac{g^2}{uM},
\qquad
\lambda_*^2=\frac{g^4}{uM^3},
\qquad
j_*=gs_*,
\qquad
\det H_*=2g^2>0.
$$

Отражение `(s,lambda)->(-s,-lambda)` сохраняет энергию, поэтому знак не
выбран.

См. [[version8-baryon-c0-singlet-triplet-central-gap-dynamical-source-carrier-admission-gate]].

Буквальная классификация существующих носителей даёт `0/8`. После перехода
к составным singlet-инвариантам остаются

$$
I_H=H^\dagger H,
\qquad
I_B=\operatorname{Tr}(BB^*).
$$

Для условно выведенного rank-one конденсата когерентности

$$
B_*=\sqrt3\,uv^*,
\qquad
\operatorname{rank}B_*=1,
\qquad
I_B(B_*)=3.
$$

Разрешённый портал создал бы источник

$$
V_{BQ}=-\kappa_B\lambda I_B,
\qquad
j_{\rm eff}=3\kappa_B,
$$

но в наследованном parent смешанный гессиан равен нулю. См.
[[version8-baryon-c0-singlet-triplet-central-gap-existing-scalar-source-carrier-classification-gate]].

На общей coherence-матрице единственное бесследовое продолжение центрального
направления равно

$$
\widehat Q=\operatorname{diag}\left(-\frac34,0_6,\frac14I_3\right),
\qquad
\operatorname{Tr}(\widehat Q\mathcal D_B^2)=-\frac58T.
$$

Для `X=D_B+lambda Qhat` кубический момент содержит портал,

$$
\operatorname{Tr}X^3=-\frac{15}{8}\lambda T-\frac38\lambda^3,
\qquad
\frac{\kappa_B}{c_{\lambda^3}}=5,
$$

тогда как второй и четвёртый моменты чётны по `lambda`. Алгебраическая
форма существует, но coherence-угол имеет тип `1+2`, а не семейный `3`.
См. [[version8-baryon-c0-singlet-triplet-central-gap-edge-coherence-radius-portal-parent-origin-gate]].

Для текущей product-group intertwiner отсутствует:

$$
\operatorname{Hom}_{(U(2)\times U(1))\times SO(3)}
\left(\Lambda^2(\mathbb C^2\oplus\mathbb C),\mathbb C^3\right)=0.
$$

После условного повышения channel carrier до ориентированного стандартного
триплета возникает единственная линия

$$
\operatorname{Hom}_{SO(3)}(\Lambda^2\mathbb R^3,\mathbb R^3)=\mathbb R*,
\qquad
*^{\mathsf T}*=I_3,
\qquad
c=\pm1.
$$

См. [[version8-baryon-c0-singlet-triplet-central-gap-coherence-even-corner-family-triplet-intertwiner-gate]].

Фактический проектор канального типа ограничивает физические смешивания:

$$
P_Y=\operatorname{diag}(0,0,1),
\qquad
\{P_Y\}'=M_2(\mathbb C)\oplus\mathbb C,
\qquad
\mathfrak{so}(3)\cap\{P_Y\}'=\mathfrak{so}(2).
$$

Поэтому текущие три столбца не образуют физический стандартный триплет.
После добавления одного endpoint типа `(C,C,R)` условно возникает

$$
W_{\rm ext}=\mathbb C^3\oplus\mathbb C_Y,
\qquad
\{P_Y^{\rm ext}\}'=M_3(\mathbb C)\oplus\mathbb C,
\qquad
(\dim H_0,\dim H_1,\dim H_2)=(1,6,3).
$$

Это новая архитектура: прежний конденсат `(e,X,Y)` не переносится
автоматически на `(e,X,Z)`. См.
[[version8-baryon-c0-singlet-triplet-central-gap-coherence-channel-triplet-promotion-bimodule-compatibility-gate]].

Одновершинное изотипическое расширение нарушает физический Weyl-баланс:

$$
\Delta(\mathcal A_{221},\mathcal A_{\mathrm{grav}^21},\mathcal A_{111})
=(0,1,1),
\qquad
I_e:-1\longmapsto-2.
$$

Независимая вектороподобная пара восстанавливает аномалии и индекс, но
увеличивает строгий граф:

$$
|E_{\rm strict}|:14\longmapsto23,
\qquad
|E_{\rm new}|=9,
\qquad
|E_{\rm selected}|=3,
\qquad
|E_{\rm extra}|=6.
$$

При текущем тривиальном действии на двух левых синглетах ненулевая
channel-`SO(3)`-ковариантная масса отсутствует:

$$
M_ZL_i=0\quad(i=1,2,3)
\Longrightarrow M_Z=0.
$$

См. [[version8-baryon-c0-singlet-triplet-central-gap-minimal-isotypic-channel-extension-gate]].

Совместный coherence--mass функционал можно выбрать неотрицательным:

$$
\mathcal S_{BM}
=(\operatorname{Tr}BB^*-3)^2+4\det(BB^*)
+\|MM^*-I_2\|_F^2+\|MB^*\|_F^2.
$$

На его нулевом множестве

$$
P_B=\frac13B^*B,
\qquad P_M=M^*M,
\qquad P_B+P_M=I_3,
\qquad \ker M=\operatorname{im}P_B.
$$

Тем самым массовое ядро и coherence-линия выравниваются без внешнего
направляющего тензора. Последующий carrier-аудит уточнил: три из шести
нежелательных новых блоков уже являются компонентами полной матрицы `M`.
Вне `B+M` остаются три комплексных поля, поэтому до стабилизации точная
сигнатура равна `(0,10,8)`, а не `(0,16,8)`. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-vectorlike-mass-edge-selector-gate]].

После добавления трёх положительных норм

$$
\mathcal S_{\rm full}=\mathcal S_{BM}
+\mu_Y|z_Y|^2+\mu_u|z_u|^2+\mu_d|z_d|^2
$$

полный нормированный срез имеет

$$
(n_-,n_0,n_+)=(0,4,14),
\qquad
\det H_z=64\mu_Y^2\mu_u^2\mu_d^2.
$$

Три массы образуют свободный конус `(R_{>0})^3`; их происхождение не
выведено. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-full-graph-aligned-parent-embedding-gate]].

Один общий Hermitian edge-оператор даёт

$$
\frac12\operatorname{Tr}F_z^2
=2|z_Y|^2+3|z_u|^2+3|z_d|^2.
$$

Но общий положительный центральный trace имеет вид

$$
\frac12\operatorname{Tr}(G_pF_z^2)
=2p_Y|z_Y|^2+3p_u|z_u|^2+3p_d|z_d|^2,
\qquad p_Y,p_u,p_d>0,
$$

поэтому незавешенное отношение `2:3:3` условно, а две относительные
координаты остаются свободны. Gauge-index matrix имеет ранг `3` и не
создаёт дополнительного соотношения. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-parent-origin-gate]].

После проективной нормировки центральных весов две допустимые конвенции
дают

$$
p^{\rm count}=\left(\frac13,\frac13,\frac13\right)
\mapsto \left(\frac23,1,1\right),
\qquad
p^{\rm edge}=\left(\frac37,\frac27,\frac27\right)
\mapsto \left(\frac67,\frac67,\frac67\right).
$$

На вакууме trace-веса не получают динамической кривизны:

$$
\nabla_pS_z\big|_{z=0}=0,
\qquad
\operatorname{Hess}_pS_z\big|_{z=0}=0_{3\times3}.
$$

KMS лишь параметризует два отношения двумя разрывами. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-central-trace-simplex-selector-gate]].

Минимальные гамильтоновы координаты симплекса имеют вид

$$
(p_Y,p_u,p_d)=\frac{(1,e^{-\theta_u},e^{-\theta_d})}
{1+e^{-\theta_u}+e^{-\theta_d}},
\qquad
\det\frac{\partial(p_u,p_d)}{\partial(\theta_u,\theta_d)}=p_Yp_up_d.
$$

Общий mass-scale остаётся независимым:

$$
\boldsymbol\mu=\alpha(2p_Y,3p_u,3p_d),\qquad\alpha>0.
$$

См. [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-minimal-central-hamiltonian-data-gate]].

На двумерном бесследовом центре

$$
A=P_u-P_d,\qquad B=P_u+P_d-3P_Y,
\qquad \operatorname{Gram}(A,B)=\operatorname{diag}(12,48).
$$

Обычный trace-square даёт жёсткость, а минимальный ненулевой источник имеет
две компоненты:

$$
V(a,b)=6a^2+24b^2-j_Aa-j_Bb,
\qquad (a_*,b_*)=(j_A/12,j_B/48).
$$

См. [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-central-hamiltonian-parent-action-origin-gate]].

Для минимального двухисточникового parent

$$
V=6a^2+24b^2-j_Aa-j_Bb,
\qquad \operatorname{Hess}V=\operatorname{diag}(12,48),
$$

единственный минимум и щели равны

$$
(a_*,b_*)=(j_A/12,j_B/48),\qquad
\binom{\Delta_u}{\Delta_d}=\frac1{12}
\begin{pmatrix}1&1\\-1&1\end{pmatrix}\binom{j_A}{j_B}.
$$

Определитель карты равен `1/72`, а обратная карта есть

$$
j_A=6(\Delta_u-\Delta_d),\qquad j_B=6(\Delta_u+\Delta_d).
$$

См. [[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-parent-architecture-gate]].

Два существующих скалярных радиуса на выровненном вакууме имеют

$$
(T_B,T_M)=(\operatorname{Tr}BB^\dagger,
\operatorname{Tr}MM^\dagger)=(3,2),
\qquad
\left.\frac{\partial(T_B,T_M)}{\partial(r,s)}\right|_{1,1}
=\operatorname{diag}(6,4).
$$

Общий портал остаётся матричным:

$$
V_{\rm portal}=-(T_B,T_M)
\begin{pmatrix}c_{BA}&c_{BB}\\c_{MA}&c_{MB}\end{pmatrix}
\binom ab,
\qquad
\dim\operatorname{Hom}_G(\mathbb R^2,\mathbb R^2)=4.
$$

Унаследованный смешанный гессиан равен `0_{2×2}`. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-existing-scalar-carrier-classification-gate]].

Минимальный общий блок даёт кубический портал

$$
X=\begin{pmatrix}\lambda I&F\\F^\dagger&0\end{pmatrix},
\qquad \operatorname{Tr}X^3=d\lambda^3+3\lambda\operatorname{Tr}(FF^\dagger).
$$

Центральные charge-векторы равны

$$
q_Y=(0,-3),\qquad q_u=(1,1),\qquad q_d=(-1,1).
$$

Из девяти ordered assignments шесть имеют rank два; при `T_B=3,T_M=2`
и двух коэффициентах абсолютный determinant source-map равен `108` или
`162`. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-portal-matrix-parent-origin-gate]].

Для weighted incidence-map

$$
C(e_B,e_M)=\begin{pmatrix}3q_{e_B}&2q_{e_M}\end{pmatrix},
\qquad K=\operatorname{diag}(12,48),
$$

минимальное condition number достигается дважды:

$$
\mathcal M_{\min}=\{(u,Y),(d,Y)\},\qquad
\kappa_{\min}=\sqrt{\frac{27+3\sqrt{17}}{27-3\sqrt{17}}}.
$$

Однокоэффициентные gap-rays равны `(0,-1)` и `(-1,0)`. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-assignment-selector-gate]].

Для двух финальных цветных incidence-концов квадратичные гиперзарядные
индексы и Real-различитель равны

$$
I_1(u)=\frac{25}{3},\qquad I_1(d)=\frac{4}{3},\qquad
\Tr(A_{ud}Y_{\mathbb R}^2)=14,
$$

тогда как нечётные Real-моменты исчезают. Центрированный typed-оператор

$$
S_{ud}=Y_{\mathbb R}^2-\frac{29}{18}I
=\frac76(P_u-P_d),\qquad \Tr S_{ud}^2=\frac{49}{3}
$$

различает ветви, но его связь с динамическим incidence-носителем и знак этой
связи не выведены. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-parent-origin-gate]].

Минимальный единый бинарный носитель использует

$$
\Pi_{\rm inc}=p_u\otimes P_u+p_d\otimes P_d,
\qquad \rank\Pi_{\rm inc}=12,
$$

и typed-гамильтониан

$$
H_{\rm inc}=\frac{29}{6}I_2+\frac72\sigma_z,
\qquad E_u-E_d=7.
$$

Коммутатор с ним оставляет двумерную диагональную fixed algebra. Условный
скачок `L_down=|d><u|` имеет Heisenberg-ранг `3` и fixed algebra `C I2`, но
его системно-средовой parent и скорость не выведены. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-minimal-typed-discriminator-architecture-gate]].

Для бинарного endpoint-центра

$$
[Y_{ud},L_\downarrow]=-L_\downarrow,
\qquad [Y_{ud},L_\uparrow]=L_\uparrow,
$$

поэтому invariant off-diagonal Hom нулевой, хотя
`D_(exp(-i theta)L_down)=D_(L_down)`. Микроскопическая компенсация требует

$$
H_{\rm int}^{ud}=g(L_\downarrow\otimes b_+
+L_\uparrow\otimes b_+^\dagger),
\qquad [Y_{\rm env},b_+]=b_+,
$$

а также резонанса `E_+1-E_0=7 gamma`. Старый charged carrier имеет
кратность три и нулевой family-fixed слой. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-minimal-typed-discriminator-binary-carrier-parent-origin-gate]].

### VIII-CM2. Минимальная дилатация charged mediator

Статус: **строго внутри условно добавленного носителя**.

Минимальная комплексная среда и взаимодействие имеют вид
`K_C=C|0> direct sum C|+>` и
`G=g(L_down tensor b_+ + L_up tensor b_+^*)`. При совпадении щелей
`7 gamma` выполняются `[Y_tot,G]=0` и `[H_0,G]=0`. После начального вакуума
операторы Крауса равны `K0=P_d+cos(theta)P_u`,
`K1=-i sin(theta)L_down`, а параметр amplitude damping есть
`p_theta=sin(theta)^2`. Real closure минимально расширяет заряды до
`(0,+1,-1)`. Конечная дилатация периодична: при `theta=pi/6` композиция
двух редуцированных каналов даёт `7/16`, тогда как единая эволюция до
`pi/3` даёт `3/4`; точный дефект `5/16` запрещает чтение одного ancilla как
необратимой полугруппы. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-minimal-typed-discriminator-binary-carrier-charged-environment-mediator-architecture-gate]].

### VIII-CM3. Уникальный typed mediator в условном carrier

Статус: **строго внутри условного расширения; coarse-no-go пересмотрен**.

Точное семейное разложение charged multiplicity после глобального
замыкания равно `1 direct_sum 3`, а не irreducible `3`. Общий fixed layer
порождается `e_R^(s)`. Совместная система family-invariance и grading-
oddness для карт из `span(s0,a0)` имеет ранг `7` на восьми неизвестных и
одномерное решение `T=lambda|e_R^(s)><s0|`. Его charge равен `-1`, а
Real-сопряжённой карты — `+1`. Raw `H21` закрывает только `2/7` carrier-
условий; условные `H23/H24` и 47-frame дают `7/7`. Энергия, состояние и
скорость остаются `0/5`. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-minimal-typed-discriminator-binary-carrier-charged-environment-mediator-existing-carrier-admission-gate]].

### VIII-CM4. Барьер энергии, состояния и скорости mediator

Статус: **строгое no-go для текущего parent**.

Gauge- и Real-совместимый Hamiltonian имеет вид
`H_E=diag(e0,ec,ec)` и после общего shift содержит одну свободную щель
`Delta_E=ec-e0`. Resonance `Delta_E=7 gamma` является отдельным
условием. Invariant states образуют отрезок
`rho_E=diag(p0,pc,pc)`, `p0+2pc=1`; finite-temperature Gibbs-state
имеет rank `3`. Couplings `g=1` и `g=2` сохраняют carrier, но дают rate
ratio `4`. Старая Toeplitz cell содержит 42 прежние jump-метки и не
содержит новый singlet connector. Conditional shape равна `8/8`,
parent-origin — `0/5`. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-minimal-typed-discriminator-binary-carrier-charged-environment-mediator-energy-state-rate-parent-origin-gate]].

### VIII-CM5. Минимальный 45-мерный dynamic parent mediator

Статус: **строго внутри условной архитектуры**.

Общая ячейка и Real-замкнутое взаимодействие имеют вид

$$
\mathcal K_{45}=\mathbb C|0\rangle\oplus\mathcal N_{42}
\oplus\mathbb C|+\rangle\oplus\mathbb C|-\rangle,
\qquad
G_g=g(L_-\otimes b_++L_+\otimes b_-+\mathrm{h.c.}).
$$

Две новые линии минимальны для Real-замыкания. Полный заряд и свободная
энергия коммутируют с `G_g`, два environment-выхода ортогональны, поэтому

$$
\mathcal L_{44}=\mathcal L_{42}
+g^2\mathcal D_{L_-}+g^2\mathcal D_{L_+}.
$$

Product-vacuum имеет локальный projector-parent, но точный conveyor
`V_45=(I tensor S_45)U_col^(0)` имеет GNVW-index `45`. Conditional
architecture равна `10/10`, inherited physical parent — `0/5`. См.
[[version8-baryon-c0-singlet-triplet-central-gap-isotypic-channel-extra-edge-mass-two-source-cubic-incidence-up-down-binary-selector-minimal-typed-discriminator-binary-carrier-charged-environment-mediator-minimal-dynamic-parent-architecture-gate]].

### VIII-CM6. Консервативное вложение dynamic parent

Статус: **строгое structural admission**.

Для канонической изометрии старой cell в новую выполнены

$$
\iota:\mathcal K_{43}\hookrightarrow\mathcal K_{45},
\qquad \iota^*\iota=I_{43},
\qquad \iota^*h_{45}\iota=h_{43}.
$$

Покомпонентное продолжение на vacuum-reference chain сплетается со
сдвигами:

$$
\mathcal I=\bigotimes_m\iota_m,
\qquad S_{45}\mathcal I=\mathcal I S_{43}.
$$

При нулевом новом coupling старая reduced dynamics является точным
restriction новой. Structural admission равен `8/8`, все пять необходимых
форм присутствуют условно, но их physical origin равен `0/5`. См.
[[version8-baryon-c0-charged-mediator-dynamic-parent-data-admission-gate]].

### VIII-CM7. Минимальный четырёхслотовый пакет dynamic parent

Статус: **строгая dependency-классификация**.

Резонансная и часовая энергии объединяются:

$$
E_*=E_C=7\gamma,qquad
g=\chi E_*,\qquad
\tau_C=\frac{\hbar}{E_*},\qquad
\Gamma=\chi^2\frac{E_*}{\hbar}.
$$

Якобиан пяти scalar outputs по `(E_*,chi)` имеет rank `2`, причём
`det d(E_C,g)/d(E_*,chi)=E_*>0`. Поэтому минимальный пакет равен

$$
\mathcal D_{\min}=
\{\mathfrak e_{\rm endpoint},E_*,\chi,\mathfrak t_{\rm transport}\}.
$$

Пять apparent inputs сокращаются до четырёх независимых slots, но их
inherited selection остаётся `0/4`. См.
[[version8-baryon-c0-charged-mediator-dynamic-parent-minimal-new-data-gate]].

### VIII-CM8. Масштабная граница и переход к Тому IX

Статус: **строгое no-go текущего parent**.

$$
E_*=E_C=7\gamma,qquad
(E_*,t)\mapsto(\lambda E_*,t/\lambda),
\qquad \Gamma/(E_*/\hbar)=\chi^2.
$$

Resonance связывает gaps, но не выбирает общий scale. Шесть внутренних
candidate classes дали `0/6`; положительная программа переносится к
four-slot parent Тома IX. См.
[[version8-baryon-c0-charged-mediator-common-energy-scale-parent-origin-gate]]
и [[tome8-final-conclusion-and-tome9-program]].

## Что ещё требуется добавить

Атлас покрывает канонические формулы итоговых заключений и глобального
реестра. Следующие расширения должны выполняться отдельными проходами, не
смешиваясь с этим строгим ядром:

1. полный покомпонентный операторный каталог тензорного гессиана бозонной
   нити, превышающий уровень итоговой щели;
2. наблюдательные формулы Тома II с полным разделением train/blind;
3. промежуточные, но переиспользуемые формулы второй вариации C6;
4. семантическая классификация полного [[live-formula-source-index]]:
   механический слой синхронизирован до 6655 формул из 633 файлов, а
   [[formula-equivalence-and-status-index]] пока закрывает точные повторы
   и консервативные сопоставления с каноническими formula-id.
   [[formula-semantic-atlas-matches]] восстановил сорок
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
- [[version8-time-formula-intuition-map]]
