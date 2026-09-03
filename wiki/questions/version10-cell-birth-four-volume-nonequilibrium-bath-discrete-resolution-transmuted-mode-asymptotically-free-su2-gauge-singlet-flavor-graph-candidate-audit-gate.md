> Status: working
> Type: question
> Updated: 2026-09-02

# Аудит кандидатов flavor-графа

## Вопрос

Какой граф на шестнадцати flavor-метках может физически породить
единственную демократическую линию, не подставляя требуемый селектор?

## Результат

Проверены нулевой граф, `K16`, `C16`, `P16`, `Q4`, `K8,8`, K43-блочная,
ванная, fitted- и target-loaded конструкции. Матрица `10x6` имеет полный
ранг `6`, оценки `(4,4,4,3,4,4,3,3,3,5)`, строгих проходов `0/10`.

`Q4` структурно выделен равенством `16=2^4`: он четырёхрегулярен, имеет
лапласианов спектр `0^(1),2^(4),4^(6),6^(4),8^(1)` и единственную
демократическую нулевую моду. Однако K43-кратность не задаёт ни
четырёхбитную разметку, ни Hamming-смежность, ни вес ребра. Поэтому это
кандидат на следующий typed-embedding gate, а не закрытие происхождения.

## Связи

- Предыдущий: [[version10-cell-birth-four-volume-nonequilibrium-bath-discrete-resolution-transmuted-mode-asymptotically-free-su2-gauge-singlet-democratic-flavor-selector-parent-origin-gate]].
- Следующий: `version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_hypercube_q4_flavor_graph_typed_embedding_gate`.
- Гейт: `s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate.tex`.
- Аудит: `s2t/audits/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate.py`.
- Результат: `s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate_results.json`.