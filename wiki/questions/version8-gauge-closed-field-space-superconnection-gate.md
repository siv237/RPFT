# Gauge-замкнутое пространство полей и суперсвязностная развилка

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Type-mismatch предыдущего гейта устранён: 15 complex transfer-полей и 12
real gauge-связностей образуют один замкнутый ассоциированный field space.
Но полного действия пока нет: фиксированный полярный фон сохраняет только
стабилизатор, а производный движущийся polar скачком меняется в rank-zero.

## Problem

Построить единое поле до BV quotient и проверить, содержатся ли gauge-
кинетика, transfer-кинетика и relative-селектор в одной ковариантной
суперсвязности.

## Search for solution

- Построено представление gauge-алгебры на 15D transfer-модуле.
- Построено присоединённое действие на 12 gauge-связностях.
- Проверена индуцированная связность на `Hom(C11,C10)`.
- Проверены endpoint-, Gram- и ковариантно-производные блоки кривизны.
- Сравнены фиксированная и движущаяся полярные ветви.
- Проверена эквивариантность polar decomposition и её rank-zero предел.

## Expected result

Успех требовал одного gauge-замкнутого field space без новых частиц и
гладкой relative-компоненты, определённой как в нуле, так и в вакууме.

## Compliance check

- Field space: `15 complex transfer + 12 real gauge = 42 real`.
- Новых gauge-генераторов и endpoint-фермионов: `0`.
- Остаток transfer-замыкания: `6.12e-16`.
- Остаток gauge-adjoint замыкания: `1.49e-15`.
- Ковариантность стандартной кривизны: остатки `<6.31e-15`.
- Fixed-polar полный gauge-дефект: от `2.0831` до `21.3772`.
- Moving-polar остаток: `<1.31e-14`.
- Скачок polar при rank-zero: `sqrt(10)`.

## Key Points

- Общий полевой носитель действительно существует.
- Полярная relative-кривизна полностью ковариантна только вместе с
  движущимся фоном.
- Производный polar корректен на страте постоянного ранга, но негладок в
  исходном нуле.
- Следующий шаг должен искать гладкий относительный order parameter, а не
  сразу вычислять BV-гессиан.

## Links

- [[version8-unified-field-space-project-intuition-search]]
- [[version8-gauge-closed-noise-parent-hessian-gate]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[version7-real-linking-superconnection-assembly-gate]]
- [[superconnection-curvature-and-polar-strata-literature-2026]]

## Source Notes

- `s2t/gates/version8_gauge_closed_field_space_superconnection_gate.tex`
- `s2t/audits/s2t_v8_gauge_closed_field_space_superconnection_gate.py`
- `s2t/results/s2t_v8_gauge_closed_field_space_superconnection_gate_results.json`