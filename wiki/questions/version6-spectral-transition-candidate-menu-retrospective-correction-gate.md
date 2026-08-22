# Том VI: ретроспективная коррекция меню моделей

> Status: mature
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, был ли выбранный динамический `D_F(x)` действительно новым
кандидатом либо повторял закрытые исследования Тома V.

## Search for solution

Сопоставлены гейты самопорождающегося дефекта, проекторного сокращения
кратности, общего масштаба суперсвязности, спектральной жёсткости,
фермионной спектральной меры и индуцированного детерминантом действия.

## Expected result

Новый кандидат должен содержать механизм, отсутствующий в прошлых гейтах,
а не переименовывать уже проверенный операторнозначный дефект.

## Compliance check

- kink и дираковская нулевая мода уже были построены;
- полный носитель давал кратность `300`;
- условная цепочка проекторов `300→45→15→2→1` уже известна;
- единый функционал, амплитуда и масштаб не выведены;
- спектральное действие и фермионный детерминант не фиксируют коэффициенты;
- выбор динамического `D_F(x)` как новой архитектуры отменён;
- полностью допущенной модели нет;
- непостроенным остаётся точный нелинейный дискретный родитель.

## Следующий гейт

[[version6-spectral-transition-discrete-nonlinear-parent-reopening-gate]]
проверит, может ли одно локальное дискретное правило породить нелинейность,
дефект, масштаб и физическое сокращение кратности.

## Links

- [[version6-spectral-transition-new-model-candidate-menu-gate]]
- [[version5-self-generated-transition-defect-gate]]
- [[version5-holonomy-projector-defect-multiplicity-gate]]
- [[version5-defect-transport-part-conclusion-gate]]
- [[version5-fermionic-determinant-induced-skyrme-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_spectral_transition_candidate_menu_retrospective_correction_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_candidate_menu_retrospective_correction_gate.py`
- `s2t/results/s2t_v6_spectral_transition_candidate_menu_retrospective_correction_gate_results.json`