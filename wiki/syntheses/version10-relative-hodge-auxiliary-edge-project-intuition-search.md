# Интуитивная проверка relative-Hodge auxiliary edge Тома X

> Status: working
> Type: synthesis
> Updated: 2026-09-03

## Summary

Формульный блок внутренне согласован: `Q=T+B=6Y`, смешанная поляризация
суперсвязностной кривизны и положительный relative-Hodge projector решают
три разные задачи без взаимного противоречия. Разрыв находится ровно в
происхождении независимой восьмимерной бозонной копии. Чистая suspension
почти наверняка даст только каноническое градуированное удвоение, но не
физическую auxiliary-координату. Сильнейшая новая зацепка --- соединить
уже полученный superconnection-section `s_Q(Sigma)=Q Sigma` с
Mathai--Quillen Thom-мультиплетом. Более дорогая физическая альтернатива ---
полный off-shell хиральный мультиплет с `F_Sigma`.

## Проверка логики формул

Текущая цепочка правильно разделена на четыре слоя.

1. **Оператор зарядов** уже выведен:

   $$
   Q=T+B=(3,-3,7,1,-1,-7,3,-3)=6Y.
   $$

   Независимость `T` и `B` и единственность коэффициентов `(1,1)` не
   оставляют скрытой непрерывной ручки.

2. **Смешанный источник** условно выведен одной кривизностью:

   $$
   \frac12\{\Phi(A_\Sigma),\Phi(\Sigma)\}
   \longmapsto A_\Sigma^T(L-R)\Sigma
   =A_\Sigma^TQ\Sigma.
   $$

   Коэффициент `1/2` является поляризационным, а не подогнанным.

3. **Положительный селектор разности** существует как Hodge-оператор
   двухузлового графа:

   $$
   P_{\rm rel}=\frac12
   \begin{pmatrix}I&-I\\-I&I\end{pmatrix},
   \qquad P_{\rm rel}^2=P_{\rm rel}\ge0.
   $$

   Поэтому отрицательный знак endpoint-веса не требует неопределённой
   физической метрики: он может быть результатом положительной нормы
   относительной компоненты.

4. **Независимость поля** действительно обязательна:

   $$
   P_{\rm rel}(\Sigma,\Sigma)=0,
   \qquad
   \operatorname{rank}P_{\rm rel}(0,A_\Sigma)=8.
   $$

   Следовательно, переименование одной `Sigma` двумя буквами запрещено не
   философски, а точным ядром проектора.

Главный вывод проверки: локальные формулы не конфликтуют. Они образуют
условный composite parent, но четвёртый слой не унаследован из текущего
полевого реестра.

## Что дала литература

### 1. Чистая suspension --- диагностический, а не завершающий маршрут

Quillen-удвоение естественно создаёт `E^+ \oplus E^-`, нечётный оператор и
кривизность. Mapping cone и Clifford-normal doubling аналогично создают
relative/boundary data. Но в этих конструкциях вторая копия прежде всего
задаёт градуировку, K-класс или граничный цикл. Без отдельного интеграла по
полю и без action principle она не становится независимой бозонной
координатой. Это заранее объясняет, почему текущий кандидат имеет `5/6`, а
не `6/6`.

### 2. Off-shell `F_Sigma` точно имеет нужный кинематический тип

В хиральном мультиплете auxiliary-поле `F_Sigma`:

- независимо от `Sigma` до уравнения движения;
- бозонно и не распространяется;
- несёт то же gauge-представление;
- входит квадратично и устраняется точно.

Схематически

$$
 \mathcal L_{\rm aux}
 =\langle F_\Sigma,F_\Sigma\rangle
 +\langle F_\Sigma,s_Q(\Sigma)\rangle+\text{h.c.},
 \qquad s_Q(\Sigma)=Q\Sigma,
$$

а elimination даёт норму `s_Q`. Однако это не бесплатная локальная
заплатка: нужны фермионный партнёр, замыкание supersymmetry off shell,
holomorphic/gauge-invariant источник и новый аномальный/RG-аудит. Текущий
field ledger явно не supersymmetric, а исследования almost-commutative
supersymmetry показывают, что правильный список полей ещё не гарантирует
правильные коэффициенты спектрального действия.

### 3. Mathai--Quillen даёт более близкую к проекту конструкцию

Выберем associated bundle `E_Sigma` с теми же весами и Real-структурой,
что у `Sigma`, и секцию

$$
 s_Q:\Sigma\longmapsto Q\Sigma.
$$

Mathai--Quillen-мультиплет содержит нечётную fiber-координату `chi_Sigma`
и независимую бозонную координату `H_Sigma` того же bundle-типа. Его
ковариантная nilpotent-пара имеет схему

$$
 \delta\chi_\Sigma=H_\Sigma+\cdots,
 \qquad \delta H_\Sigma=\cdots,
$$

а `delta`-точный функционал содержит положительную Gaussian-норму
`||H_Sigma||^2`, линейную связь с `s_Q` и обязательный фермионный
Jacobian/curvature sector. После Gaussian integration возникает фактор
`exp(-||s_Q||^2/2t)`.

Это соединяет три уже найденные части проекта:

$$
 \text{mixed superconnection curvature}
 \Rightarrow s_Q=Q\Sigma,
 \qquad
 \text{Thom multiplet}
 \Rightarrow H_\Sigma,
 \qquad
 \text{graph Hodge}
 \Rightarrow P_{\rm rel}.
$$

Но условие жёсткое: если удалить `chi_Sigma`, nilpotent differential и
curvature/Jacobian terms, конструкция снова станет обычным HS-переписыванием
с вручную добавленным полем и не закроет origin.

## Ранжирование маршрутов

| Маршрут | Что закрывает | Главный долг | Вердикт |
|---|---|---|---|
| Mathai--Quillen + текущая mixed curvature | независимая бозонная копия, положительная bundle metric, section `Q Sigma` | полный cohomological multiplet и доказательство физического статуса | лучший минимальный кандидат |
| Off-shell chiral `F_Sigma` | точное same-representation auxiliary field и elimination | новая supersymmetry, fermion partner, holomorphy, anomaly/RG | лучший физический, но дорогой кандидат |
| Чистая superconnection suspension | копия, grading, odd edge | нет независимой меры и dynamics | полезный no-go/discriminator |
| Mapping-cone cylinder | relative incidence и boundary difference | нет унаследованных ideal/boundary data | резервный геометрический маршрут |
| Одинокое HS-поле | алгебраическое завершение квадрата | не выводит ни поле, ни source | уже закрыто |

## Уточнённый следующий тест

Запланированный
`version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_suspension_auxiliary_copy_parent_origin_gate`
следует сохранить, но сделать разделяющим гейтом. Он должен проверить:

1. является ли вторая копия самостоятельной переменной интегрирования или
   только K-теоретической стабилизацией;
2. существует ли унаследованный nilpotent differential, превращающий её в
   contractible/Thom-пару;
3. выводится ли секция `s_Q=Q Sigma` из уже построенной mixed curvature до
   введения auxiliary field;
4. даёт ли один положительный bundle metric и `H_Sigma^2`, и relative
   Hodge projector без независимых нормировок;
5. сокращаются ли determinant/Jacobian contributions полного multiplet;
6. совместимы ли `J`, grading и веса `±1,±3,±7` со всей парой, а не только
   с бозонным блоком.

Стоп-критерий: если suspension создаёт лишь `Sigma tensor C^2`, но не
nilpotent pair, section и measure, её нужно зафиксировать как
стабилизационную конструкцию, а следующим кандидатом сделать отдельный
Mathai--Quillen Thom auxiliary-copy gate. Off-shell chiral route следует
открывать только после отрицательного результата этого более
консервативного теста.

## Результат следующего гейта

[[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-superconnection-suspension-auxiliary-copy-parent-origin-gate]]
подтвердил именно эту развилку. Bare suspension получил `3/7`: он не
создаёт независимую переменную. Thom-достройка получила `6/7`, точно дала
rank-8 contractible pair и требуемый Schur complement, но её differential
и полная мера пока не унаследованы. Следующий расчёт должен искать общий
parent Mathai--Quillen-мультиплета, не повторяя уже закрытый HS-route.

Этот следующий расчёт также выполнен. Полный quartet
`(Sigma,psi_Sigma,chi_Sigma,H_Sigma)` условно замкнул differential,
cohomology и measure: determinant ratio равен `1`, conditional score
повысился до `7/8`. Одновременно получен точный no-go: carrier grading не
порождает Grassmann statistics, а inherited odd rank равен `0/16`.
Поэтому следующий маршрут теперь узок и проверяем: аудит возможных
источников именно двух odd Thom-полей, а не новый поиск бозонного
auxiliary-поля.

Аудит odd-полей также завершён. Наличие физических Callias-фермионов не
решает задачу: они дают Grassmann statistics, но не differential
`delta Sigma=psi_Sigma` и не ацикличный auxiliary sector. Из двенадцати
кандидатов не прошёл ни один; shift-BRST и formal Mathai--Quillen routes
получили `6/7`, провалив только inherited origin. Поэтому следующий
расчёт обязан проверять происхождение rank-8 shift symmetry поля `Sigma`,
а не перебирать новые названия для уже существующих фермионов.

Этот discriminator теперь выполнен. `Sigma` Hessian имеет только
двумерное ядро, поэтому требуемый rank-8 shift физически отсутствует.
Stückelberg double условно восстанавливает всю BRST/MQ архитектуру, включая
FP determinant `3969`, но ровно ценой новой неунаследованной копии. Тем
самым локальная ветвь достигла строгого no-go и должна передать результат
финальному заключению Тома X, а не продолжать цепь эквивалентных
auxiliary-расширений.

## Verdict

Интуитивный блок формул выдерживает проверку. Ошибка была бы не в знаке,
ранге или поляризации, а в попытке объявить градуированное удвоение новым
физическим полем. Самая содержательная зацепка --- читать искомую копию не
как вторую частицу `Sigma`, а как бозонную координату Thom/contractible
пары над секцией `Q Sigma`. Это сохраняет идею «auxiliary, но не новый
on-shell particle» и одновременно объясняет, какие дополнительные поля и
тождество меры обязаны появиться.

## Links

- [[off-shell-auxiliary-copy-mathai-quillen-supersymmetry-literature-2026]]
- [[field-space-superconnection-bv-mapping-cone-literature-2026]]
- [[quillen-mckean-singer-common-trace-no-go-literature-2026]]
- [[version7-auxiliary-carrier-project-intuition-search]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-relative-hodge-auxiliary-edge-origin-candidate-audit-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-mathai-quillen-thom-multiplet-common-parent-origin-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-mathai-quillen-odd-pair-statistics-candidate-audit-gate]]
- [[version10-particle-wrinkle-dislocation-callias-equal-charge-twist-m4-h15-r2-mathai-quillen-shift-symmetry-parent-origin-gate]]
- [[current-status-and-next-vectors]]

## Source Notes

- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_odd_auxiliary_cross_bilinear_candidate_audit_gate.tex`
- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_superconnection_mixed_curvature_parent_origin_gate.tex`
- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_common_parent_admission_gate.tex`
- `s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_relative_hodge_auxiliary_edge_origin_candidate_audit_gate.tex`
- `wiki/sources/off-shell-auxiliary-copy-mathai-quillen-supersymmetry-literature-2026.md`