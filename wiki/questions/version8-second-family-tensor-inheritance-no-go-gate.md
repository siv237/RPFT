# Наследование второго семейного тензора

> Status: mature
> Type: question
> Updated: 2026-08-28

## Summary

В базе проекта есть независимые семейные операторы, но ни один не является
готовым входным примитивом Тома VIII. Cross-loop требует уже закрытого
коннектора, моментный коммутатор провалил замороженный слепой тест, а
двенадцать incidence-направлений не имеют канонического селектора.

## Key Points

- `Tr D_F^4=104+16 cos(theta) Tr(P_- H_u H_d)` выводит cross-word, но
  предполагает общий коннектор и оставляет CP-чётную развилку.
- `K_s=[Z4_s,Z6_s]/(2i)` является настоящим вторым тензором, однако
  mass-selected ветвь имеет `s12>0.99`, не проходит mass-train и CKM-blind.
- 12 из 16 аффинных incidence-операторов порождают `M3(C)`, но текущая
  геометрия не выбирает один оператор, вес и секторное назначение.
- Утверждение закрывает наследование записанных кандидатов, а не все будущие
  геометрии.
- После проверки примитивов A, B и C Том VIII нельзя открывать простым
  продолжением старой архитектуры.

## Links

- [[version8-qlyr-ur-real-connector-lift-gate]] — закрытие примитива A.
- [[version8-colorless-hodge-gauge-anchor-no-go-gate]] — закрытие примитива C.
- [[version7-higher-cycle-character-mixing-freeze-gate]] — одна голономия
  не выбирает семейные оси.
- [[global-theorem-and-no-go-ledger]] — глобальный статус.

## Source Notes

- `s2t/gates/version4_common_updown_krajewski_loop_gate.tex`
- `s2t/results/s2t_v4_common_updown_krajewski_loop_gate_results.json`
- `s2t/gates/version4_moment_commutator_modular_gate.tex`
- `s2t/results/s2t_v4_moment_commutator_modular_gate_results.json`
- `s2t/gates/version4_incidence_operator_menu_gate.tex`
- `s2t/results/s2t_v4_incidence_operator_menu_gate_results.json`
- `s2t/gates/version8_second_family_tensor_inheritance_no_go_gate.tex`
- `s2t/audits/s2t_v8_second_family_tensor_inheritance_no_go_gate.py`
- `s2t/results/s2t_v8_second_family_tensor_inheritance_no_go_gate_results.json`