# RPFT / UGSM / S2T — карта проекта

> Рабочая помойка черновиков по физике превращается в структурированную базу.
> Этот файл — навигатор: где какие файлы лежат, что они содержат и насколько актуальны.
> Смысловой центр проекта — вики `wiki/` (читайте `wiki/index.md` первым). Свежая работа — в `s2t/`.

Условные обозначения актуальности:

- **[Активно]** — живая работа, меняется в текущих сессиях.
- **[Справочно]** — законченные/промежуточные тексты, на которые опираются.
- **[Архив]** — старые черновики, сохранены как история, напрямую не развиваются.
- **[Служебное]** — инфраструктура (лицензия, схемы, экспорт).

---

## Служебный слой проекта

| Файл | Содержание | Актуальность |
|---|---|---|
| `AGENTS.md` | Схема для LLM-агента: структура репо, правила ведения вики, протокол отчётов | [Активно] |
| `llm-wiki.md` | Паттерн LLM Wiki (идея и правила из первого источника) | [Справочно] |
| `formalization_candidates/` | Самодостаточные Markdown-спецификации строгих результатов для будущего переноса в Lean | [Активно] |
| `formal/` | Зарезервированный слой реальных Lean-проектов, challenge/solution и метаданных; пока без формальных доказательств | [Служебное] |
| `s2t/docs/BUILD.md` | Безопасная для Prism инструкция полной сборки после разделения `docs/`, `gates/` и `assets/` | [Активно] |
| `LICENSE` | MIT-лицензия | [Служебное] |

## wiki/ — основа проекта (LLM-вики, вынесена из s2t)

Схема и правила ведения — в `wiki/wiki-schema.md` и `AGENTS.md`. Хронология действий — в `wiki/log.md`.

| Путь | Содержание | Актуальность |
|---|---|---|
| `wiki/index.md` | Навигационный каталог: читать первым | [Активно] |
| `wiki/wiki-schema.md` | Схема LLM-вики, правила именования и ведения | [Справочно] |
| `wiki/log.md` | Хронологический журнал всех действий (июль–август 2026) | [Активно] |
| `wiki/concepts/*.md` (8) | Понятия, включая RPFT/UGSM/TOE/S2T, спектрально-корреляционный источник, переходный примитив и исполняемый LCF proof eDSL | [Активно] |
| `wiki/sources/*.md` (327) | Описания источников: тома, программа S2T, каталог, литература, корпуса, внешние барионные отчёты, дотомовый и полный живой формульные индексы | [Активно] |
| `wiki/syntheses/*.md` (66) | Сводки и результаты: глобальный формульный атлас, генеалогия, точные и семантические эквивалентности формул, реестр строгих результатов и закрытых путей, систематика томов, дорожные карты, формальная верификация, интуитивные карты и ретроспективная развилка к отображению полного пространства полей в шум | [Активно] |
| `wiki/questions/*.md` (629) | Гейты и вопросы: по сути индекс всех проверок проекта | [Активно] |
| `wiki/lints/*.md` (8) | Периодические проверки здоровья вики, включая аудит дедупликации, ссылок и внешних формульных замечаний | [Справочно] |

---

## архив-2025-2026/ — исторические слои по хронологии

| Папка | Содержание | Период | Актуальность |
|---|---|---|---|
| `архив-2025-2026/2025-12-истоки/` | `base/` (26 параметров СМ, `fabric_promt3.md`), `habr/` (черновики статей print1/2) | 12.2025 | [Архив] |
| `архив-2025-2026/2025-12-пепер/` | `peper/` — первая «бумага» (article RU/EN, `main.tex`, скрипты, графики) | 12.2025–02.2026 | [Архив] |
| `архив-2025-2026/2025-12..2026-01-строгость/` | `rigorous/`, `rigorous-en/` — строгие выводы (RU+EN, 23+ файлов, `CRITIQUE.md`, `30_qed_one_loop_proof.md`, `31_geometry_proof.md`) | 12.2025–01.2026 | [Справочно] |
| `архив-2025-2026/2026-01-дедукция/` | `deductive_logic/` (00–09, `plan.md`), `ai-promts/` (First-principles-00…03) | 01.2026 | [Архив] |
| `архив-2025-2026/2026-02-проработка/` | `Проработка/` — русские черновики (`atlas.md`, `standart_model*.md`, `mendeleev.md`, `lagrangian_derivation.md`, `kappa_lens.py`, `det_ratio_pi.py`, подпапка `old/`) | 12.2025–02.2026 | [Архив] |

## corpus/ — финальные артефакты

| Файл | Содержание | Актуальность |
|---|---|---|
| `corpus/S2T_FINAL_PAPER.md`, `corpus/S2T_FINAL_PAPER_V2.md` | «Спектральное замыкание СМ на RP^3 × S^1» — главный текст программы S2T (версия II.C, 28.05.2026), вывод 26 параметров СМ из трёх чисел | [Справочно] |
| `corpus/Трактат 1 том.pdf` | Каноническая PDF-сборка Тома I — постановка исследовательской программы | [Справочно] |
| `corpus/tome2_s2t_spectral_closure-4.pdf` | Том II — спектральное замыкание (ячейка S_vac) | [Справочно] |
| `corpus/main-44.pdf` | Ранняя 12-страничная сборка Тома I; побайтно совпадает с `s2t/assets/main-4.pdf` | [Архив] |

---

## s2t/ — живой исследовательский слой

Последние и самые свежие данные (активность по 31.08.2026). 2151 исходный
артефакт верхнего уровня, разложенный по типам: 751 `results/*.json`,
729 `audits/*.py`, 602 `gates/*.tex`, 45 `docs/*`,
24 `assets/*` (png/pdf). Генерируемые LaTeX-файлы в этот счёт не входят.
Git-истории у файлов нет — завезены одним коммитом «add s2t» (09.08.2026),
хронология воспроизводится по namespace имён и `wiki/log.md`.

### Каталоги s2t

| Папка | Содержание | Актуальность |
|---|---|---|
| `s2t/gates/` (602) | Гейт-документы `*.tex`: `version3_*` (27), `version4_*` (115), ветви `version5_*`, `version6_*`, `version7_*`, `version8_*` и тематические пространства | [Активно] |
| `s2t/audits/` (729) | Вычислительные аудиты `*.py` (включая аудиты Томов VI–VIII) | [Активно] |
| `s2t/results/` (751) | Численные результаты `*.json`, парные к аудитам по имени | [Активно] |
| `s2t/docs/` | Тома, интеграционные тексты и файлы сборки; Том VIII завершён, Том IX открыт как программа единого динамического parent | [Активно] |
| `s2t/assets/` (24) | Графики `*.png` и PDF верхнего уровня (`ugsm_dynamics_audit-3.pdf` и др.) | [Справочно] |
| `s2t/proofdsl/` | Prism-safe pure-Python LCF eDSL: точные SymPy-типы, морфизмы, представления, GKSL-конструктор, опциональный Z3 и тесты | [Активно] |

### Вспомогательные папки s2t

| Папка | Содержание | Актуальность |
|---|---|---|
| `RPFT-main/` | Шесть уникальных или изменённых файлов старого снапшота; канонические зеркала находятся в `архив-2025-2026/` | [Служебное] |
| `reproduction_package/` | Манифесты воспроизведения: `FREEZE_MANIFEST.json`, `DEPENDENCY_GRAPH.json`, `THEOREM_STATUS_LEDGER.json`, `REPRODUCTION_PROTOCOL.md`, папки `specification/`, `submission/` | [Справочно] |
| `17705966/` | Архив PDF-версий «ТОЕ» (ТОЕ 2…13, TOE4.2, TOE5, TOE.pdf) | [Справочно] |
| `prism-uploads/` | Односторонний экспорт (изображение) | [Служебное] |
| `tmp_preview/` | Временные превью (`main_p1.png`) | [Служебное] |
| `repository-export/` | Git-bundle-экспорт (файл пуст — токен отозван) | [Служебное] |
| `raw/` | Будущие неизменяемые источники (пока пусто) | [Служебное] |

## корзина/ — временная обратимая дедупликация

| Путь | Содержание | Актуальность |
|---|---|---|
| `корзина/rpft-main-duplicates/` | 109 фактически перемещённых побайтовых зеркал; ещё 18 из исходных 127 уже отсутствовали в снапшоте при повторном применении | [Служебное] |
| `корзина/MANIFEST.md` | Старый путь, канонический архивный оригинал, путь в корзине и SHA-256 каждой пары | [Активно до очистки] |

### Тома-трактаты (ключевые документы в `s2t/docs/`)

| Файл | Содержание | Актуальность |
|---|---|---|
| `tome1_s2t_research_program.tex` | Канонический сборщик сегментной редакции Тома I; восемь частей лежат в `s2t/docs/tome1/`, PDF остаётся `corpus/Трактат 1 том.pdf` | [Справочно] |
| `tome2_s2t_spectral_closure.tex` | Том II — спектральное замыкание | [Справочно] |
| `tome3_s2t_parent_action.tex` | Том III — parent action (родительское действие) | [Справочно] |
| `tome4_s2t_observed_reconstruction.tex` | Том IV — наблюдаемая реконструкция | [Активно] |
| `tome5_s2t_parent_architecture.tex` | Том V — родительская архитектура; класс 15 и минимальный дефицит `1/7` доказаны, динамическое рождение материи не закрыто | [Справочно—Активно] |
| `tome6_s2t_matter_birth.tex` | Том VI завершён. Сохранены классификация, кинематика, статический проекторный переход, поле `Q`, точный compacton и Real-чётный ток `4*pi²`, но автономное рождение материи не выведено. Контракт `R0--R6`: `1` пройден, `1` частичен, `5` провалены; динамическая архитектура заморожена | [Справочно—Активно] |
| `version6_final_conclusion_and_next_program.tex` | Итог по десяти задачам Тома VI, положительным результатам, строгим запретам и входным условиям `P0--P6` следующей программы | [Активно] |
| `tome7_s2t_rank_change_parent.tex` | Том VII завершён. Класс `S_eta=S_E+eta||R_U||²` даёт переход `(7,0,20) -> (0,0,27)` на 27-мерном срезе при всех `eta>0`; единственная массовая метрика, семейные фазы и полное физическое замыкание не получены | [Справочно—Активно] |
| `version7_introduction_and_problem_statement.tex` | Входной контракт Тома VII: общий носитель, одна суперсвязность, одна норма кривизны и полный физический гессиан до любой карты к частицам | [Справочно] |
| `version7_final_conclusion_and_next_program.tex` | Итог по десяти задачам Тома VII: качественный универсальный класс, точные запреты количественного чтения и три условия возможного продолжения | [Активно] |
| `tome8_s2t_correlation_transition.tex` | Том VIII завершён: 155 содержательных гейтов; полное ядро, QMS, 42-channel dynamics и условный charged mediator получены, four-slot physical parent и общий `E_*` не выведены | [Справочно—Активно] |
| `version8_final_conclusion_and_next_program.tex` | Итог Тома VIII и входной контракт Тома IX: единый parent должен выбрать endpoint, `E_*`, `chi` и transport primitive | [Активно] |
| `tome9_s2t_dynamic_parent.tex` | Том IX — единый динамический родитель, физический масштаб и закон транспорта; программа открыта admission-гейтом `6/6` | [Активно] |
| `version9_introduction_and_problem_statement.tex` | Входной контракт Тома IX: четыре независимых слота, шесть критериев успеха и запрет target-loaded калибровки | [Активно] |
| `../gates/version9_four_slot_dynamic_parent_program_admission_gate.tex` | Первый гейт Тома IX: continuous rank `2`, четыре независимых slot-типа и admission `6/6`; общий parent остаётся `0/1` | [Активно] |
| `../gates/version9_four_slot_common_carrier_architecture_gate.tex` | Общий carrier `H24 tensor K45 tensor K45` размещает endpoint menu, `L44` и transport-ветви индексов `45/1` в одной алгебре; architecture `8/8`, selector `0/4` | [Активно] |
| `../gates/version9_four_slot_common_parent_functional_architecture_gate.tex` | Одна bounded polynomial parent-family условно выбирает endpoint, `E_*`, `chi` и transport (`4/4`); coefficient origin остаётся `0/4` | [Активно] |
| `../gates/version9_four_slot_parent_selector_coefficient_origin_gate.tex` | Closure-defects выбирают условный endpoint `H24`, но energy, coupling и transport-bias свободны; coefficient origin `1/4`, raw slot closure `0/4` | [Активно] |
| `../gates/version9_endpoint_extension_raw_parent_origin_gate.tex` | Type-aware no-go: raw `H21`, `F42`, noise и cotangent carriers не создают три состояния `H24`; candidate origin `0/6`, требуется новый complex module dimension `3` | [Активно] |
| `../gates/version9_endpoint_extension_minimal_finite_module_architecture_gate.tex` | Минимальная endpoint-алгебра `M2(C) direct_sum M3(C)`: complex dimension `13`, Hermitian increment `11`, architecture `10/10`; dynamic parent-origin открыт | [Активно] |
| `../gates/version9_endpoint_finite_module_parent_action_origin_gate.tex` | Fixed-parent no-go: multiplicity jump `(1,1,1)` не является вариацией `D`; candidate origin `0/7`, unseeded projector minima образуют `Gr_C(3,24)` real dimension `126`, target seed тавтологичен | [Активно] |
| `../gates/version9_endpoint_finite_geometry_configuration_space_admission_gate.tex` | Три endpoint-фазы образуют carrier `H21 direct_sum H23 direct_sum H24` dimension `68` с phase algebra `C^3`; architecture `9/9`, block-Dirac rank `46`, creation reachability `0/3` | [Активно] |
| `../gates/version9_endpoint_finite_geometry_creation_operator_architecture_gate.tex` | Configuration-source и five-channel family frame порождают `M6(C)`; GKSL architecture `10/10`, endpoint reachability `3/3`, source/rate parent-origin `0/4` | [Активно] |
| `../gates/version9_endpoint_finite_geometry_creation_operator_parent_origin_gate.tex` | Unique phase zero mode выводит configuration-source; channel commutant dimension `3`, normalized rate simplex dimension `2`, rate origin `0/3`, creation parent-origin `1/4` | [Активно] |
| `version8_introduction_and_problem_statement.tex` | Краткий входной контракт Тома VIII: отсев старых вариантов, происхождение нового объекта, рабочая/нулевая гипотезы и стоп-критерий | [Активно] |
| `version8_temporary_boundary_and_retrospective_return.tex` | Теоретический переход после локального барионного запрета: объясняет временную остановку и выводит следующий вопрос об отображении полного пространства полей в шум | [Активно] |
| `../gates/version8_field_to_noise_chain_map_pullback_metric_gate.tex` | Точный полево-шумовой изоморфизм: ранг 42, нулевое ядро, 504 калибровочных тождества и перенос `G_поле=K`; динамическая мобильность остаётся отдельным вопросом | [Активно] |
| `../gates/version8_field_noise_metric_to_parent_hessian_comparison_gate.tex` | Постояннополевой гессиан имеет ранг 30 и калибровочное ядро 12, тогда как следовая метрика имеет ранг 42; их скалярное отождествление невозможно | [Активно] |
| `../gates/version8_spacetime_kinetic_factorization_and_gauge_fixing_gate.tex` | Поперечно-продольная факторизация: ранг 36 до фиксации, ядро 12, ранг 48 после фиксации и точный обратный оператор с внутренним множителем `K_к^-1` | [Активно] |
| `../gates/version8_transverse_noise_mobility_environment_origin_gate.tex` | Общая среда точно наследует форму `K_к^-1 tensor P_T`, ранг 36 и ядро 12, но масштабирование связи меняет скорость как `g²`, сохраняя нормированную форму; абсолютные часы не выведены | [Активно] |
| `../gates/version8_full_field_kinetic_supermetric_assembly_gate.tex` | Полный главный символ размерности 168 имеет ранг 156 и ядро 12; после фиксации ранг 168 и обратный оператор точны, но независимые веса двух блоков остаются свободными | [Активно] |
| `../gates/version8_full_field_kinetic_relative_weight_parent_origin_gate.tex` | Явный репер Клиффорда и общий коэффициент `a4` дают веса `2` и `2/3`, то есть отношение `3:1`; результат условен до вывода пространственно-временного дираковского подъёма | [Активно] |
| `../gates/version8_full_field_a4_dirac_lift_origin_gate.tex` | Масштабы product-Dirac оператора `1` и `2` сохраняют все 42 внутренних коммутатора, но меняют квадрат внешнего символа `1 -> 4`; конечный родитель не выбирает базовую геометрию | [Активно] |
| `../gates/version8_full_42_carrier_base_k_determinant_compatibility_gate.tex` | На полном носителе получены ранги `28+3`, девять ненарушенных калибровочных направлений и фиксированно-фоновый босонный числитель `4659176/3249`; его физический статус снят последующей BV-проверкой | [Справочно—Активно] |
| `../gates/version8_full_42_carrier_bv_vacuum_quotient_gate.tex` | Хиральный проектор ранга 42 фиксирует фермионный вклад `-92`; ограничение прежнего гессиана на трёхмерную калибровочную орбиту имеет ранг 3 и след 34, поэтому полный `B` не закрыт | [Активно] |
| `../gates/version8_gauge_invariant_vacuum_hessian_reconstruction_gate.tex` | Орбитальная метрика `14I_3` задаёт горизонтальный проектор; quotient-гессиан имеет ранг 26, три голдстоуна и одну физическую плоскую моду, квадратичный числитель равен `211725392/159201` | [Активно] |
| `../gates/version8_horizontal_flat_direction_parent_lift_gate.tex` | Фазовая плоскость имеет метрику `diag(6,20)`, орбита оставляет комбинацию `4:3`; грамовы концы неизменны на всех порядках, а прямоугольные максимальные миноры не дают скаляр без нового правила свёртки | [Активно] |
| `../gates/version8_horizontal_phase_determinant_line_admission_gate.tex` | Кофакторный вектор порождает ядро и преобразуется как `z^33`, но `Hom_G(E_s,C)=0`; Real-пара фазу сокращает, а фоновые свёртки неканоничны | [Активно] |
| `../gates/version8_horizontal_phase_heavy_arrow_cycle_admission_gate.tex` | Полный граф имеет цикл-ранг 3 и тяжёлую проекцию ранга 3, но `Q_Lu_R` является листом и `qC=0`; обычные циклические следы горизонтальную фазу не видят | [Активно] |
| `../gates/version8_horizontal_phase_real_oriented_cycle_admission_gate.tex` | Повышающая часть имеет `N²=0`; Real-обратные стрелки сопряжены и имеют противоположные веса, полный оператор меняется подобием, а независимая обратная копия удвоила бы носитель `40 -> 80` | [Активно] |
| `../gates/version8_horizontal_phase_complex_symplectic_polarization_admission_gate.tex` | Пространство инвариантных кососимметрических форм имеет размерность 11, но максимальный ранг 14 и радикал 6; невырожденная достройка требует шесть новых комплексных направлений | [Активно] |
| `../gates/version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate.tex` | Сбалансированный носитель размерности 26 имеет невырожденную инвариантную форму и 23-мерное семейство поляризаций, но дефицит трёх концевых копий `H_+` запрещает считать его внутренней флуктуацией текущего родителя | [Активно] |
| `../gates/version8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate.tex` | На 26-мерном носителе получено ненулевое отображение момента размерности 13, однако котангенциальный `U(1)` сохраняет `Omega`, коммутирует с gauge-действием и оставляет любую норму момента фазонезависимой | [Активно] |
| `../gates/version8_horizontal_phase_cotangent_complex_structure_metric_selector_gate.tex` | Следовая метрика размерности 42 имеет нульность не меньше 10 на новом 52-мерном носителе; два различных совместимых продолжения сохраняют один старый след, поэтому `J` не выбран | [Активно] |
| `../gates/version8_polar_morita_connector_admission_gate.tex` | Подготовительный red-team после Тома VII: формальный `T0:C21 -> C22` требует невыведенного отождествления state-модуля с пространством меток стрелок; новый том пока не открыт | [Активно] |
| `../gates/version8_colorless_hodge_gauge_anchor_no_go_gate.tex` | Подготовительный no-go: финальный бесцветный Hodge-вакуум имеет нулевой gauge-индекс, поэтому его активный след не калибрует `f0`; весь ненулевой индекс несут заглушённые рёбра | [Активно] |
| `../gates/version8_second_family_tensor_inheritance_no_go_gate.tex` | Подготовительная ретроспекция: известные семейные тензоры либо требуют закрытого коннектора, либо провалили слепой тест, либо остаются невыбранным меню; все три старых входа в Том VIII закрыты | [Активно] |
| `../gates/version8_moving_kernel_second_fundamental_form_gate.tex` | Последний внутренний spatial-тест: движущийся проектор даёт каноническую кинематику фиксированного ранга, но остаётся факторизованным и расходится как `1/epsilon` на общем rank-drop пути | [Активно] |
| `../gates/version8_full_correlation_kernel_locality_reconstruction_gate.tex` | Археологическое переоткрытие раннего полного ядра: spectrum-only no-go сохраняется, но `C_tau` вместе с алгеброй наблюдаемых точно возвращает конечную локальность; происхождение самой алгебры остаётся открытым | [Активно] |
| `../gates/version8_linking_dirichlet_quantum_markov_semigroup_gate.tex` | Linking-инцидентность выводит симметричную квантово-марковскую полугруппу на `M11 direct_sum M10` без нового коэффициента; неподвижная алгебра размерности 41 оставляет открытым селектор классических событий | [Активно] |
| `../gates/version8_markov_fixed_algebra_selector_gate.tex` | Полный gauge-набор сокращает неподвижную алгебру `41 -> 2` устойчиво по всем положительным весам; получены центральные quark/lepton проекторы рангов 12 и 9 и зафиксирован отсутствующий межсекторный переход | [Активно] |
| `../gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex` | Полный мультиплет существующих цветных стрелок не имеет линейного синглета, но его квадратичная Kraus-сумма gauge-ковариантна и сокращает центральную `C^2` до скаляра без цветного конденсата | [Активно] |
| `../gates/version8_kraus_bridge_parent_action_hessian_gate.tex` | Полевая форма Kraus-моста положительна и сохраняет сигнатуры Тома VII, но при нулевых cross-arrow вакуумных координатах скорость канала равна нулю; требуется происхождение ковариации | [Активно] |
| `../gates/version8_cross_arrow_covariance_origin_gate.tex` | Полярный linking-гессиан выводит общую ось корреляции `QLYR–XLdR`, но не единственную форму или масштаб ковариации; конечная Stinespring-дилатация позднее получена | [Активно] |
| `../gates/version8_minimal_covariant_stinespring_carrier_gate.tex` | Минимальный одношаговый Stinespring-носитель имеет комплексную размерность 13 и использует существующую cross-arrow опору; вероятность и непрерывный шумовой поток остаются открыты | [Активно] |
| `../gates/version8_intrinsic_noise_clock_dilation_gate.tex` | Collision-limit выводит каноническое безразмерное шумовое время, но модульный поток не создаёт диссипацию, а физическая скорость и источник свежих ancilla не получены | [Активно] |
| `../gates/version8_full_primitive_markov_generator_assembly_gate.tex` | Linking-, gauge- и cross-формы собраны в одну примитивную полугруппу с единственным стационарным состоянием; относительные и абсолютная скорости остаются свободными | [Активно] |
| `../gates/version8_correlation_kernel_short_time_rate_selector_gate.tex` | Полная матрица процесса точно восстанавливает шесть скоростей при известном времени и пять относительных без него; независимый физический источник ядра ещё не получен | [Активно] |
| `../gates/version8_physical_correlation_kernel_parent_action_origin_gate.tex` | Родительский гессиан фиксирует равновесную ковариацию, но допускает разные мобильности и разные физические ядра; открыт закон флуктуации–диссипации | [Активно] |
| `../gates/version8_fluctuation_dissipation_mobility_origin_gate.tex` | Общая следовая метрика условно фиксирует равную cross-мобильность, но полный шестисемейный шумовой кадр и физический масштаб времени остаются открыты | [Активно] |
| `../gates/version8_canonical_noise_frame_common_trace_gate.tex` | Общий KMS-след строит 19-мерный базис-независимый Casimir стабилизаторной ветви; поздний gauge-аудит потребовал расширения полной ветви до 27 измерений | [Активно] |
| `../gates/version8_noise_isotropy_symmetry_admission_gate.tex` | Симметрийный red-team разделяет 19D-стабилизаторную и 27D-полную gauge-ветви; оба коммутанта нетривиальны, поэтому trace-изотропия не вынуждена | [Активно] |
| `../gates/version8_gauge_closed_noise_parent_hessian_gate.tex` | Старый 27D вещественный полевой срез и 27D complex noise quotient не совпадают: transfer-realification имеет размерность 30, пересечение равно 23; полный родительский гессиан требует нового общего пространства полей | [Активно] |
| `../gates/version8_gauge_closed_field_space_superconnection_gate.tex` | Полный field space `15 complex transfer + 12 real gauge` ковариантно собран без новых частиц; fixed polar сохраняет лишь стабилизатор, а moving polar негладок в rank-zero | [Активно] |
| `../gates/version8_smooth_relative_background_order_parameter_gate.tex` | Кварк-лептонная градуировка даёт гладкую gauge-ковариантную relative-кривизну и вакуумную жёсткость ранга 12, но её шестая степень оставляет исходный гессиан нулевым | [Активно] |
| `../gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex` | Новый relative-член сохраняет старый переход; полное gauge-замыкание допускает класс `(10,0,20) -> (0,0,30)`, но оставляет два свободных edge-Hodge веса | [Активно] |
| `../gates/version8_gauge_closed_edge_hodge_origin_gate.tex` | Casimir, цепная степень, секторная градуировка и KMS-след не различают блок `4 incidence + 4 heavy`; происхождение двух edge-Hodge масс локализовано как кратностный барьер | [Активно] |
| `../gates/version8_real_incidence_multiplicity_quotient_gate.tex` | Real меняет ориентацию `10x11 <-> 11x10`, но сохраняет непрерывную gauge- и Real-совместимую орбиту проекторов блока `4+4`; копийный селектор не получен | [Активно] |
| `../gates/version8_bimodule_multiplicity_separator_gate.tex` | Полные endpoint-метки требуют расширения `15 -> 20 complex`, но канонически разделяют `10 incidence + 10 heavy`; единый edge-уровень даёт переход `(20,0,20) -> (0,0,40)` при `beta<2/3` | [Активно] |
| `../gates/version8_dynamic_physical_closure_redteam_gate.tex` | Red-team граница Тома VIII: операторный процесс математически содержателен, но уникальные скорости, физическое время, микроскопическая среда и независимое наблюдаемое не выведены | [Активно] |
| `../gates/version8_page_wootters_stinespring_history_gate.tex` | Конечный history-мост: условные срезы часов `0,1,2` точно возвращают итерации Kraus-канала и согласуются с collision-limit; канонический автономный унитарий и физическая секунда остаются открыты | [Активно] |
| `../gates/version8_canonical_autonomous_clock_unitary_extension_no_go_gate.tex` | Фазовое семейство на 252-мерном дополнении сохраняет тот же канал и gauge-ковариантность; даже Real-чётность оставляет `z=±1`, поэтому автономный clock-Hamiltonian из Kraus-карты не выводится | [Активно] |
| `../gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex` | Явный самосопряжённый Hamiltonian на минимальной среде даёт cross-arrow GKSL в collision-limit; пространство gauge-допустимых interaction-связей восьмимерно, а rate-метрик четырёхмерно | [Активно] |
| `../gates/version8_trace_dual_cross_interaction_selector_gate.tex` | Полевой суперслед даёт `K_B=3I_12`; при явном принципе метрически двойственной среды cross-rate метрика условно фиксируется как `I_12/3` с точностью до общего масштаба времени | [Активно] |
| `../gates/version8_metric_dual_environment_parent_action_origin_gate.tex` | Два положительных gauge-совместимых bath-completion имеют один полевой блок `K_B`, но разные генераторы; `K_BR=I` единственно выбирает dual-rate, однако не следует из старого действия | [Активно] |
| `../gates/version8_full_noise_cotangent_carrier_admission_gate.tex` | Исправленная смешанно-вещественная типизация даёт полный noise/field carrier размерности 42; текущему 25-jump QMS недостаёт 17 направлений | [Активно] |
| `../gates/version8_full_noise_trace_frame_metric_gate.tex` | Девять linking-orbit и восемь internal направлений закрывают дефицит; полный 42-real Hermitian frame имеет невырожденную точную trace-Gram метрику | [Активно] |
| `../gates/version8_full_noise_42_jump_gksl_fixed_algebra_gate.tex` | Полный 42-jump GKSL сохраняет trace/unit и endpoint-алгебру; старый 25-jump span обеспечивает `Fix=C I21` и примитивность | [Активно] |
| `../gates/version8_full_noise_repeated_interaction_hamiltonian_gate.tex` | Полный 42-jump процесс имеет star-Hamiltonian на `C903`, минимальную среду 43 и gauge closure по 504 коммутаторным тестам | [Активно] |
| `../gates/version8_full_noise_physical_time_scale_no_go_gate.tex` | Точная scale-орбита полного collision-процесса сохраняет `g^2 t`; абсолютная секунда требует независимого energy/rate anchor и расписания соударений | [Активно] |
| `../gates/version8_full_noise_toeplitz_ancilla_chain_dilation_gate.tex` | Toeplitz-сдвиг на bilateral chain из `C43`-ячеек реализует все конечные итерации `Phi_h^n` одним Floquet-унитарием без внешнего reset | [Активно] |
| `../gates/version8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate.tex` | Product-vacuum имеет локальный commuting-projector parent с gap `1`, но полный conveyor имеет GNVW-индекс `43` и не генерируется конечновременным Lieb--Robinson-локальным Hamiltonian | [Активно] |
| `../gates/version8_index_balanced_ancilla_conveyor_gate.tex` | Встречная `C43`-цепь сокращает индекс `43*(1/43)=1`; два nearest-neighbour SWAP-слоя точно сохраняют свежие ancilla и `Phi_h^n`, но единый статический Hamiltonian ещё не выведен | [Активно] |
| `../gates/version8_static_local_hamiltonian_embedding_or_no_go_gate.tex` | Bloch-eigenchannels встречного conveyor имеют windings `(-1,+1)`, поэтому на минимальном number-preserving двухцепочечном носителе нет периодического статического finite-range логарифма | [Активно] |
| `../gates/version8_clock_augmented_static_hamiltonian_conveyor_gate.tex` | Трёхпозиционные часы дают точное статическое однократное исполнение двух слоёв при времени `pi/2`; для локальной сериализации длины `2L` ограничение силы связи требует времени не меньше `pi L/2`, а возврат конечных часов для повторяемого конвейера остаётся открытым | [Активно] |
| `../gates/version8_bounded_strength_autonomous_clock_thermodynamic_limit_gate.tex` | При ошибке часов `A exp(-cd)` полный конечный конвейер имеет ошибку не более `2LA exp(-cd)`; для точности `delta` достаточно `d=O(log(L/delta))`. Глобальная равномерность при фиксированном ресурсе не получена, локальный предел наблюдаемых условно допустим | [Активно] |
| `../gates/version8_local_observable_clocked_qms_limit_and_time_anchor_gate.tex` | Ошибка совместного предела равна не более `C_u/n+nA exp(-cd)`; при `d_n>=(1+alpha)log(n)/c` она стремится к нулю. Локальная непрерывная полугруппа получена автономно, но общая масштабная орбита часов и скорости шума сохраняет свободу секунды | [Активно] |
| `../gates/version8_typed_clock_energy_to_noise_rate_anchor_gate.tex` | Размерный слабый предел даёт `Gamma=E_int^2 tau_C/hbar^2=chi^2 E_C/hbar` и `Gamma/Omega=chi^2`; текущий родитель не выбирает `E_C` и `chi`, поэтому абсолютная скорость остаётся открытой | [Активно] |
| `../gates/version8_clock_energy_anchor_candidate_audit_gate.tex` | Проверены обрезание, радиусы, две щели, компактон и наблюдаемые массы; ни один кандидат не имеет выведенного отображения в энергию часов и амплитуду столкновения | [Активно] |
| `../gates/version8_minimal_mixed_clock_collision_parent_gate.tex` | Резонансная передача кванта от двухуровневых часов в 42-мерную среду даёт точный `[H_0,G]=0` и прежний шумовой генератор; `chi` и общий масштаб `E_C` остаются свободными | [Активно] |
| `../gates/version8_baryon_canonical_weights_geta_no_go_gate.tex` | Шесть весов барионного пакета точно совпадают со стабилизаторной точкой общего КМС-следа; внешняя мишень недостижима для всех `eta>0`, но остаток 8,21 % не является безусловным предсказанием | [Активно] |
| `../gates/version8_baryon_directed_transfer_convention_selector_gate.tex` | Прямое ограничение общего КМС-следа фиксирует множитель `x` и исходные пружины; связывающая часть совпадает, а стрелочная в прежнем трёхкварковом отображении была меньше ровно вдвое | [Активно] |
| `../gates/version8_baryon_three_particle_lift_normalization_gate.tex` | Ковариационный отрезок `-1/2<=c<=1` даёт одинаковый одночастичный генератор и разные трёхчастичные расщепления; отношения `3` и `3/2` точны, но общая среда не выбрана | [Активно] |
| `../gates/version8_baryon_common_environment_correlation_origin_gate.tex` | Независимые ячейки `c=0` и общая ячейка `c=1` редуцируются к одному однокопийному родителю; происхождение коллективной барионной корреляции не выведено | [Активно] |
| `../gates/version8_baryon_em_total_charge_identity_scope_gate.tex` | Зарядовое тождество и рисунок `(4,1,0,1)` точны, но свёртка электромагнитной энергии к `Q_tot^2/T` требует дополнительных коэффициентов и отсутствия пространственных и магнитных членов | [Активно] |
| `../gates/version8_baryon_em_spatial_kernel_origin_gate.tex` | Положительность неоднородного парного ядра не защищает знак; перестановочное усреднение даёт `T(E_n-E_p)=-(mu+2 g_bar)/3`, но кулоновское растяжение оставляет величину `g_bar` свободной | [Активно] |
| `../gates/version8_baryon_em_magnetic_hyperfine_origin_gate.tex` | Слабый изоспин отделён от физического спина; один `S=1/2` не фиксирует знак, а полностью симметричная спин-ароматная ветвь условно даёт `O_n-O_p=-1/3` при свободном магнитном контакте | [Активно] |
| `../gates/version8_baryon_spin_flavor_permutation_carrier_gate.tex` | Цветовой эпсилон и принцип Паули допускают три согласованные перестановочные ветви с магнитными разностями `-1/3`, `1` и `1/3`; симметричную ветвь должен выбрать отдельный пространственный родитель | [Активно] |
| `../gates/version8_baryon_spatial_ground_state_symmetry_origin_gate.tex` | Центральное `S3`-семейство делает основным любой перестановочный тип; симметричную ветвь гарантирует лишь улучшающая положительность полугруппа отсутствующего координатного родителя | [Активно] |
| `../gates/version8_baryon_electromagnetic_closure_redteam_gate.tex` | Полная разность сведена к трём ветвям; общий отрицательный знак требует `-A_el<z<A_el/3`, но ни `z`, ни ветвь теорией не выбраны | [Активно] |
| `../gates/version8_baryon_connected_three_body_kernel_admission_gate.tex` | Одинаковые одно- и двухчастичные ограничения оставляют одномерную третью кумулянту; текущий слабый предел её не сохраняет | [Активно] |
| `../gates/version8_baryon_cubic_trace_connected_operator_gate.tex` | Центрированный 42-мерный кадр порождает связный оператор `W3` с опорой `140 TTG+28 GGG` и нулевыми частичными следами | [Активно] |
| `../gates/version8_baryon_cubic_trace_parent_action_coefficient_origin_no_go_gate.tex` | Квадратичное действие, ограниченность и стационарность не выбирают коэффициент `lambda_3` | [Активно] |
| `../gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex` | Одна норма `Tr(mZ+Z^2)^2` фиксирует `lambda_3^2/(alpha beta)=4`, но центральный фон `mI/2` чётен и не реализует ненулевую дискретную часть оператора Дирака | [Активно] |
| `../gates/version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate.tex` | Нечётный конечный фон даёт только `TTT+TGG`, не пересекающиеся с `TTG+GGG` канонического `d_abc`; стандартные допустимые кубические вершины производны и нулевые при нулевом импульсе | [Активно] |
| `../gates/version8_baryon_derivative_cubic_vertex_to_six_point_kernel_or_stop_gate.tex` | Полный перебор 13244 троек даёт дизъюнктные опоры `d=140 TTG+28 GGG` и `C=106 TTG+10 GGG`; локальная производная ветвь к статическому `W3` закрыта | [Активно] |
| `../gates/version8_baryon_nonlocal_six_point_kernel_admission_gate.tex` | Два положительных рациональных форм-фактора имеют общий ненулевой статический предел и разные импульсные формы; нелокальный класс допустим, но спектральная мера не выбрана | [Активно] |
| `../gates/version8_baryon_nonlocal_kernel_spectral_measure_parent_origin_gate.tex` | Одно положительное вспомогательное поле реализует однополюсное ядро, но масштабирование `m²,g² -> q m²,q g²` сохраняет статический коэффициент и меняет форму | [Активно] |
| `../gates/version8_baryon_spectral_scale_anchor_candidate_audit_gate.tex` | Масштаб базы, часы, шум, гессиан, cutoff/радиус и наблюдаемая масса дают `0/6` внутренних типизированных якорей спектральной массы | [Активно] |
| `../gates/version8_baryon_spectral_scale_anchor_minimal_new_data_gate.tex` | Форма однополюсного ядра требует выбранных `a,c`, полный оператор дополнительно требует независимой амплитуды `lambda_3` | [Активно] |
| `../gates/version8_baryon_base_scale_selector_architecture_gate.tex` | `a²(c-c0)²` оставляет масштаб плоским; логарифмический родитель при `B>0` условно выбирает `(mu²,c0)`, но входы ещё не выведены | [Активно] |
| `../gates/version8_baryon_dimensional_transmutation_input_origin_gate.tex` | Ранние уровни дают строгие `B0=67/(64π²)>0` и `b=2`, но полный KK-коэффициент, абсолютная RG-шкала и внутренняя карта `c0` остаются открыты | [Активно] |
| `../gates/version8_baryon_c0_typed_internal_map_candidate_audit_gate.tex` | Семь внутренних безразмерных отношений дают `0/7` типизированных карт в pole Hessian; совпадение двух значений `4` не разрешает их отождествление | [Активно] |
| `../gates/version8_baryon_c0_minimal_cross_carrier_morphism_architecture_gate.tex` | Между двумя тривиальными инвариантными прямыми существует одномерное семейство карт `M_kappa`; положительность фиксирует знак, но не модуль нормировки | [Активно] |
| `../gates/version8_baryon_c0_common_trace_embedding_normalization_gate.tex` | Нормированный trace прямой суммы имеет свободные центральные веса `p,q`; изометрия даёт `kappa=sqrt(p/q)`, поэтому без linking-бимодуля нормировка не выбирается | [Активно] |
| `../gates/version8_baryon_c0_linking_algebra_offdiagonal_bridge_admission_gate.tex` | Минимальный `M2` linking-блок с imprimitivity bridge устраняет центральные веса и условно фиксирует `kappa=1`, но происхождение стрелки в 42-carrier ещё открыто | [Активно] |
| `../gates/version8_baryon_c0_existing_42_carrier_linking_bridge_classification_gate.tex` | Старый 42-frame аннулирует внешнюю auxiliary-линию, а `H21` не содержит neutral singlet; требуемого bridge в текущем носителе нет | [Активно] |
| `../gates/version8_baryon_c0_minimal_neutral_endpoint_extension_gate.tex` | Минимальное расширение требует двух neutral states `21->23`; Lie-замыкание моста добавляет три Hermitian направления и даёт невырожденный frame `42->45` | [Активно] |
| `../gates/version8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate.tex` | Расширенный 45-frame задаёт GKSL-динамику, но имеет неподвижную `C^2`: новый `M2`-блок деполяризуется изолированно и не переносит популяцию в старый 42-носитель | [Активно] |
| `../gates/version8_baryon_c0_old_new_gauge_covariant_connector_classification_gate.tex` | Допустимые charged-singlet коннекторы образуют трёхмерное комплексное пространство; две квадратуры дают примитивный frame `47`, но направление `RP2` и скорость не выбраны | [Активно] |
| `../gates/version8_baryon_c0_connector_multiplicity_and_rate_parent_selector_gate.tex` | Общий след выбирает только радиус коннектора: изотропный parent оставляет `RP2`, а направление и абсолютная скорость дают строгий реестр `0/2` | [Активно] |
| `../gates/version8_baryon_c0_extended_endpoint_bimodule_weight_origin_gate.tex` | Локальная `C3+M2`-алгебра диагонализует три ветви, но оставляет симплекс следов; полное Hom-замыкание даёт `M5` и frame `51`, не выбирая одиночную карту `c0` | [Активно] |
| `../gates/version8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate.tex` | Полный connector-пакет имеет Choi/Kraus rank `3`, одиночная карта — `1`; центральные ограничения могут совпасть после rescaling, но полные генераторы операторно неэквивалентны | [Активно] |
| `../gates/version8_baryon_c0_multiplicity_environment_pure_state_selector_gate.tex` | Gauge и Real-условия оставляют всю чистую орбиту `RP2`; trace/Gibbs выбирает смешанное `I3/3`, а entropy/purity не выбирает направление, поэтому уникальный селектор имеет реестр `0/5` | [Активно] |
| `../gates/version8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate.tex` | Минимальный селектор имеет вид `epsilon I3+Delta(I3-P)` с `P in RP2`; конечный Gibbs-state полнорангов, а direction/cooling/absolute-gap данные имеют реестр `0/3` | [Активно] |
| `../gates/version8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate.tex` | Старый Hessian нулевой, полные trace/Kossakowski-источники скалярны, локальные веса свободны; анизотропный `R4+` имеет простой спектр, но требует новой family-to-environment карты | [Активно] |
| `../gates/version8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate.tex` | Текущий `Hom_SO3(3,1^3)=0` и запрет сохраняется на `A4`; после условного повышения среды до стандартной тройки Hom становится линией `R I3`, но требуется новый endpoint-ковариантный parent | [Активно] |
| `../gates/version8_baryon_c0_multiplicity_environment_so3_action_parent_origin_gate.tex` | Три текущие стрелки не `SO(3)`-инвариантны; минимальное замыкание удваивает среду до `3+3`, требует три новые комплексные стрелки и оставляет source-селектор `RP1` | [Активно] |
| `../gates/version8_baryon_c0_so3_closed_environment_source_line_selector_gate.tex` | Ни одна точка остаточного `RP1` не является нечётным семейным интертвейнером: grading имеет тип `1+2`, минимальный parity-дефект равен `4` | [Активно] |
| `../gates/version8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate.tex` | Минимальная плюс-ветвь добавляет одну charged-singlet линию, выбирает source `a0` и требует endpoint-замыкание `M3`; полный тип `1+3` оставляет два rate-веса | [Активно] |
| `../gates/version8_baryon_c0_family_triplet_singlet_relative_rate_selector_gate.tex` | Представление `1+3` допускает весь луч `r>0`; equal-per-arrow даёт `r=1`, equal-per-sector — `r=1/3`, а полный чётный `M4` запрещён grading | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_trace_weight_parent_origin_gate.tex` | Обычный след и максимум энтропии условно дают `p=1/4`, но Gibbs-класс реализует любой `p` через свободную щель `beta Delta`; parent-origin ledger равен `0/6` | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_weight_minimal_hamiltonian_data_gate.tex` | После факторизации нуля энергии минимальный селектор веса одномерен: `theta=beta Delta`; Gibbs-функционал строго выпуклый, но абсолютная энергия и скорость релаксации остаются отдельными данными | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_parent_action_origin_gate.tex` | Центрированные grading и семейный Casimir совпадают и условно фиксируют направление `Q`; положительность допускает оба знака, а физический коэффициент имеет ledger `0/5` | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_coefficient_selector_gate.tex` | Шесть естественных нормировок одного `Q` дают шесть разных модулей; чётный потенциал сохраняет знак, KMS видит только `beta lambda`, итоговый selector ledger `0/8` | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_minimal_source_parent_architecture_gate.tex` | Минимальный квадратичный parent требует линейный источник `j` и жёсткость `m²>0`; архитектура проходит `7/7`, но вакуум видит лишь `j/m²`, а происхождение коэффициентов остаётся `0/2` | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_source_stiffness_parent_origin_gate.tex` | Незавешенный след на скалярном фоне имеет нулевой линейный отклик; квадратичный след и grading/Casimir-вставка условно дают формы `m²,j`, но текущий parent-origin закрыт как `0/8` | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_dynamical_source_carrier_admission_gate.tex` | Один Real-singlet `s` с потенциалом `M lambda²/2-gs lambda+u s⁴/4` создаёт два устойчивых ненулевых вакуума без внешнего `j`; архитектура `8/8`, происхождение `0/4`, знак парно вырожден | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_existing_scalar_source_carrier_classification_gate.tex` | Буквального активного Real-singlet нет (`0/8`); из двух составных singlet-инвариантов только радиус когерентности `Tr(BB*)` уже имеет точный условный конденсат `3`, но его портал к `Q` отсутствует | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate.tex` | На общей матрице `1-6-3` кубический момент даёт портал `-15 lambda Tr(BB*)/8` с фиксированным отношением `5`, но чётный inherited-parent его не содержит, а канальный угол `1+2` не типизирован как family-triplet | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate.tex` | Текущий product-group Hom из канального угла `1+2` в family-triplet равен нулю и для `SO(3)`, и для `A4`; условное channel-повышение даёт единственный Hodge-map `Lambda²R3 -> R3`, но требует трёх новых структур | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_coherence_channel_triplet_promotion_bimodule_compatibility_gate.tex` | Фактический коммутант типов равен `M2(C)+C`, поэтому стандартные `SO(3)` и `A4` не смешивают текущие каналы; один новый изотипический endpoint условно создаёт допустимый триплет, но требует четырёх новых parent-входов | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate.tex` | Один новый `Z_R` нарушает аномалии и хиральный индекс; минимальная пара `Z_L+Z_R` структурно допустима, но открывает девять новых рёбер, оставляет шесть лишних и не даёт `SO(3)`-ковариантной ненулевой массы | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate.tex` | Неотрицательный совместный parent точно даёт `P_B+P_M=I3` и совмещает coherence-линию с массовым ядром; исходный счёт шести внешних полей пересмотрен последующим carrier-аудитом до трёх | [Активно] |
| `../gates/version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_full_graph_aligned_parent_embedding_gate.tex` | Carrier-коррекция оставляет вне `B+M` только три комплексных поля; положительные массы дают сигнатуру `(0,4,14)`, но образуют свободный трёхмерный конус и не выбирают разреженную опору | [Активно] |
| `version5_post_conclusion_architecture_decision.tex` | Постзаключительное архитектурное решение: развилка десяти идей, выбранный маршрут, альтернативы, стоп-критерий и последовательность дальнейших проверок | [Активно] |
| `theory_completion_program.tex` | Методическая программа Shadow-to-Theory: перевод структурного паттерна в строгую, проверяемую теорию | [Справочно] |

### Сборка LaTeX

Собирать документы следует из корня репозитория. Общий файл
`s2t/docs/s2t_paths.tex` подключает гейты из `s2t/gates/`. Полные команды
сборки и очистки находятся в безопасном для Prism файле `s2t/docs/BUILD.md`.

Краткий пример:

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error s2t/docs/tome1_s2t_research_program.tex
```

### Гейты, аудиты и результаты (namespace-связки)

Каждая проверка представлена тройкой одноимённых файлов + страницей в wiki:

```
s2t/gates/version4_<topic>.tex        — гейт-документ (что проверено, вывод, next gate)
s2t/audits/s2t_v4_<topic>.py          — вычислительный аудит (numpy-скрипт)
s2t/results/s2t_v4_<topic>_results.json — численные результаты аудита
wiki/questions/version4-<topic>-gate.md — сводка вопроса/решения
```

| namespace | Что содержит | Актуальность |
|---|---|---|
| `s2t_v3_*.py` + `s2t_v3_*_results.json`, `s2t_*.py/.json` | Старые аудиты (C6-инфраструктура, определительные и паритетные проверки, июль-поток C6) | [Справочно] |
| `s2t_v4_*.py` + `*_results.json` | Аудиты Версии IV | [Активно] |
| `wilson_*, family_*, bl_*, majorana_*, state_menu_*, su5_*, pati_salam_*, external_*, k1_k14_*, c6_*` | Тематические гейты/аудиты | [Активно] |
| `*_no_go`, `*_gate`, `*_trilemma`, `final_freeze_*` | Суффиксы статуса: гейт, тупик, трилемма, заморозка | [Активно] |

---

## Быстрая навигация

1. Формулы, их смысл и источники → `wiki/syntheses/global-formula-atlas.md`
   - автономное время и шумовой конвейер → `wiki/syntheses/version8-time-formula-intuition-map.md`
2. Происхождение формул до томов → `wiki/syntheses/pre-tome-formula-genealogy.md`
3. Все дотомовые блочные формулы по файлам и строкам → `wiki/sources/pre-tome-formula-source-index.md`
4. Формулы живого корпуса по томам, документам и гейтам → `wiki/sources/live-formula-source-index.md`
5. Точные повторы, сопоставления с атласом и статусы → `wiki/syntheses/formula-equivalence-and-status-index.md`
6. Доказанное, условное и закрытые пути Томов I–VIII → `wiki/syntheses/global-theorem-and-no-go-ledger.md`
7. Текущее состояние и направления → `wiki/index.md`, `wiki/syntheses/current-status-and-next-vectors.md`
8. Хронология работ → `wiki/log.md`
9. Свежий журнал исследования → `wiki/syntheses/research-roadmap-2026-08-02.md`
10. Археология текущего селектора копий → `wiki/syntheses/version7-copy-selector-project-archaeology.md`
11. Термины → `GLOSSARY.md`
12. Историческая база → `архив-2025-2026/2025-12..2026-01-строгость/rigorous/`, `архив-2025-2026/2026-01-дедукция/`
13. Финальные тексты → `corpus/`
14. Интуиция следующего следового гейта → `wiki/syntheses/version7-minimal-support-trace-project-intuition-search.md`
