# Том VI: минимальные требования к новой модели спектрального рождения

> Status: mature
> Type: question
> Updated: 2026-08-21

## Problem

После остановки неизменённой архитектуры задан единый контракт, по которому
будут сравниваться любые новые модели.

## Search for solution

Сформулированы семь обязательных тестов `R0--R6`: физический носитель,
единый функционал, эндогенный запуск, скорость, устойчивый endpoint,
слепое численное предсказание и заранее заданные сертификаты провала.

## Expected result

Кандидат считается допустимым только при совместном прохождении всех
тестов. Контракт необходим, но сам по себе ещё не доказывает модель.

## Compliance check

Версия VI имеет часть `R0` и методически выполняет `R6`, но не проходит
`R1--R5`. Поэтому она остаётся строгим классификационно-кинематическим
основанием, но не допущена как динамическая теория рождения.

Автоматически отвергаются: ручная вставка ранга, скрытый портал, внешний
quench, топология вместо вероятности и неустойчивое седло вместо материи.

## Следующий гейт

[[version6-spectral-transition-new-model-candidate-menu-gate]] сравнит
минимальные архитектуры по одному и тому же контракту.

## Links

- [[version6-spectral-transition-dynamic-closure-status-gate]]
- [[version6-spectral-transition-componentwise-creation-observable-gate]]
- [[version6-matter-birth-program]]
- [[spectral-transition-primitive-literature-2026]]

## Source Notes

- `s2t/gates/version6_spectral_transition_new_model_minimal_requirements_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_new_model_minimal_requirements_gate.py`
- `s2t/results/s2t_v6_spectral_transition_new_model_minimal_requirements_gate_results.json`
- S. Coleman, *The Fate of the False Vacuum. I* (1977).
- C. G. Callan, S. Coleman, *The Fate of the False Vacuum. II* (1977).
- F. R. Klinkhamer, N. S. Manton, *A Saddle-Point Solution in the Weinberg--Salam Theory* (1984).