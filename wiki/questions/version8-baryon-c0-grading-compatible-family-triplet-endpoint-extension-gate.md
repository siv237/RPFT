# Grading-совместимое endpoint-расширение семейной тройки

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Текущий charged-singlet target имеет grading-кратности `1_-+2_+`.
Сохранение старых знаков даёт две однородные семейные тройки: плюс-ветвь
требует одну новую линию, минус-ветвь — две. Поэтому единственная
минимальная архитектура расширяет `H23` до `H24`, завершает две старые
положительные линии одной новой и выбирает source `a0`.

Все три стрелки условной тройки нечётны; `SO(3)` коммутирует с grading и
гиперзарядом, а family-Hom равен `R I3`. Однако ковариантное endpoint-
замыкание равно полному `M3(C)`, а старый коннектор остаётся синглетом.
Полный тип `1+3` допускает два независимых rate-веса. Новое состояние,
`M3`-endpoint и ковариантный frame не выведены: ledger `0/3`.

## Связи

- [[version8-baryon-c0-so3-closed-environment-source-line-selector-gate]]
- [[version8-baryon-c0-minimal-neutral-endpoint-extension-gate]]
- [[version8-baryon-c0-family-to-multiplicity-intertwiner-admission-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate.py`
- `s2t/results/s2t_v8_baryon_c0_grading_compatible_family_triplet_endpoint_extension_gate_results.json`