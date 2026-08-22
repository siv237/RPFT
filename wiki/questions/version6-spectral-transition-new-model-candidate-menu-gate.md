# Том VI: меню кандидатов новой модели спектрального рождения

> Status: stale
> Type: question
> Updated: 2026-08-21

## Problem

Шесть архитектур сравнены по контракту `R0--R6` и по числу новых структур,
которые пришлось бы внести вручную.

> Ретроспективная коррекция: выбор `D_F(x)` отменён страницей
> [[version6-spectral-transition-candidate-menu-retrospective-correction-gate]],
> поскольку соответствующая ветвь уже подробно проверена в Томе V.

## Search for solution

Проверены сфалерон, явный портал `Q,T,B--H`, Q-ball/фермионный мешок,
механизм Jackiw--Rebbi, динамическое поле конечного оператора Дирака и
дискретная сеть переходов.

## Expected result

Выбор означает только исследовательский приоритет. Полный допуск требует
последующего прохождения всех тестов `R0--R6`.

## Compliance check

- полностью допущенных моделей: `0`;
- сфалерон, ручной портал и Q-ball отклонены как готовые модели проекта;
- Jackiw--Rebbi сохранён как возможный подмеханизм endpoint;
- дискретная сеть отложена как фундаментальная перестройка;
- выбран динамический конечный оператор `D_F(x)`, поскольку он сохраняет
  `H15`, Real/gauge-типизацию и допускает единое спектральное действие;
- тесты `R2--R5` для него пока открыты.

## Следующий гейт

[[version6-spectral-transition-candidate-menu-retrospective-correction-gate]]
сверяет предварительный выбор с полным ledger Тома V.

## Links

- [[version6-spectral-transition-new-model-minimal-requirements-gate]]
- [[version6-spectral-transition-dynamic-closure-status-gate]]
- [[dynamical-dirac-soliton-candidate-literature-2026]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_new_model_candidate_menu_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_new_model_candidate_menu_gate.py`
- `s2t/results/s2t_v6_spectral_transition_new_model_candidate_menu_gate_results.json`