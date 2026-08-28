# Version VII: циклически-изотипический проектор рёбер

> Status: working
> Type: question
> Updated: 2026-08-27

## Summary

Найдена точная комбинация двух независимо определённых признаков:

- участие нового ребра в единственном `H15`-укоренённом цикле;
- равенство калибровочных представлений его левого и правого концов.

Объединение соответствующих проекторов совпадает ровно с шестью нужными
рёбрами из одиннадцати. Производная градуировка даёт отрицательный
квадратичный знак целевым рёбрам и положительный — пяти нежелательным без
ручных коэффициентов и меток `old/new`.

## Projector Construction

Циклический проектор имеет ранг четыре:

$$
E_C=\{L_LY_R,Q_LY_R,X_Le_R,X_Lu_R\}.
$$

Изотипический проектор также имеет ранг четыре:

$$
E_I=\{L_LY_R,Y_LY_R,X_Le_R,X_LX_R\}.
$$

Их пересечение имеет ранг два, поэтому

$$
P_*=P_C+P_I-P_CP_I,
\qquad \operatorname{rank}P_*=6.
$$

Опора `P_*` буквально совпадает с полем
`desired_cycle_plus_vector_masses` предыдущего аудита. Дополнение ранга
пять совпадает с `allowed_but_unselected_edges`.

## Quadratic Grading

Проектор задаёт каноническую инволюцию

$$
\Gamma_E=I-2P_*.
$$

Квадратичная форма имеет знаки

$$
q_E(z)=\sum_{e\notin E_*}\|z_e\|^2
-\sum_{e\in E_*}\|z_e\|^2.
$$

На одном поколении вещественный гессиан имеет сигнатуру `(12,0,10)`;
для одиннадцати семейных матриц `3x3` — `(108,0,90)`.

## Status Boundary

Это первый точный селектор всего меню `6 из 11`, однако ещё не полное
действие. Не выведены общий масштаб отрицательной массы, квартичная
стабилизация, ненулевой минимум всех шести блоков и происхождение
`Gamma_E` из одной Real-суперсвязности.

Следующий гейт должен реализовать градуировку как нуль-форменную часть
одного полевого суперсвязностного родителя и вычислить полный вакуумный
гессиан без независимого стабилизирующего веса.

## Links

- [[version7-baseline-rooted-primitive-cycle-admission-gate]]
- [[version7-four-vertex-vectorlike-selector-gate]]
- [[version7-edge-coherence-full-graph-competition-gate]]
- [[version7-edge-coherence-formula-intuition-map]]
- [[quiver-spectral-action-nonbacktracking-cycle-literature-2026]]
- [[version7-rank-change-parent-program]]
- [[global-theorem-and-no-go-ledger]]
- [[live-formulas-gates-version7-23]]

## Source Notes

- `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex`
- `s2t/audits/s2t_v7_rooted_cycle_isotypic_edge_projector_gate.py`
- `s2t/results/s2t_v7_rooted_cycle_isotypic_edge_projector_gate_results.json`