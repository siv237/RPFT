# Том VI: статус динамического замыкания спектрального рождения

> Status: mature
> Type: question
> Updated: 2026-08-21

## Problem

Сведён полный ledger ветви: какие уровни действительно закрыты, а где
неизменённая архитектура должна остановиться.

## Search for solution

Проверены семь уровней: KO6/Toeplitz-классификация, смена ранга,
переходное седло, новый observable, trigger, скорость и endpoint.

## Expected result

Классификационное замыкание не должно выдаваться за физическую теорию
рождения. Продолжение допустимо только через явно новую модель.

## Compliance check

- закрыты классификация и кинематика смены ранга;
- сфалерон остаётся контрольным седлом, а не проектным endpoint;
- selection rules являются частичным observable;
- trigger, скорость и устойчивый endpoint открыты;
- итог: `2` закрытых, `2` частичных и `3` открытых уровня;
- неизменённая архитектура остановлена.

## Следующий гейт

[[version6-spectral-transition-new-model-minimal-requirements-gate]]
формализует обязательный контракт новой модели.

## Links

- [[version6-spectral-transition-componentwise-creation-observable-gate]]
- [[version6-spectral-transition-sphaleron-spectral-flow-gate]]
- [[version6-matter-birth-program]]
- [[spectral-transition-primitive-literature-2026]]

## Source Notes

- `s2t/gates/version6_spectral_transition_dynamic_closure_status_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_dynamic_closure_status_gate.py`
- `s2t/results/s2t_v6_spectral_transition_dynamic_closure_status_gate_results.json`
- S. Coleman, *The Fate of the False Vacuum. I* (1977).
- C. G. Callan, S. Coleman, *The Fate of the False Vacuum. II* (1977).
- F. R. Klinkhamer, N. S. Manton, *A Saddle-Point Solution in the Weinberg--Salam Theory* (1984).