# Совместный гессиан изотипической relative-кривизны

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Гладкий изотипический член безопасно дополняет переход Тома VII, но не
замыкает полный parent action. Полное gauge-замыкание превращает запусковую
область в пятимерный комплексный incidence-модуль, поэтому естественный
индекс становится `10 real`, а не `7 real`. Переход
`(10,0,20) -> (0,0,30)` существует, но зависит от двух невыведенных масс.

## Problem

Совместить новый гладкий relative-член с ранее проверенным гессианом и
проверить переход на полном 30-мерном вещественном transfer-модуле.

## Search for solution

- Добавлен вакуумный гессиан `S_B` к старому 27D переходу.
- Полный transfer-модуль разложен на gauge-инвариантные подмодули
  `I_5 + H_10`.
- Построен проектор на incidence-орбиту.
- Проверено, поднимает ли `H_B` две нулевые Gram-моды.
- Просканировано двухмассовое gauge-инвариантное продолжение edge-Hodge
  гессиана.

## Expected result

Успех требовал сохранения старого перехода и получения строго устойчивого
полного вакуума без свободного продолжения массовой метрики.

## Compliance check

- Старый переход сохраняется для `kappa=0..10^6`.
- Полная incidence-орбита: `5 complex = 10 real`.
- Тяжёлый модуль: `10 complex = 20 real`.
- Gauge-дефект проектора: `<1.74e-15`.
- `H_B` имеет ранг `12`, но равен нулю на двумерном Gram-ядре.
- Представитель `(m_I,m_H)=(4,3.6)` даёт
  `(10,0,20) -> (0,0,30)` и вакуумную щель `5.53437`.
- Другие веса дают иные исходные сигнатуры.
- Два запуска дали одинаковый SHA-256
  `1b6ab1042ea258d2be9b419b40112c7aad9c04b64c8a82cf2c2c0713994fe41d`.

## Key Points

- Новый relative-член не разрушает достигнутое.
- Gauge-замыкание естественно меняет число запусковых мод с 7 на 10.
- Полный качественный переход существует как класс, но пока не как
  единственное действие.
- Открытая проблема локализована в происхождении двух edge-Hodge масс или в
  отдельном Real-quotient, если требуется нечётный индекс.

## Links

- [[version8-smooth-relative-background-order-parameter-gate]]
- [[version8-gauge-closed-noise-parent-hessian-gate]]
- [[version8-gauge-closed-field-space-superconnection-gate]]
- [[version7-qualitative-parent-mass-metric-freeze-gate]]

## Source Notes

- `s2t/gates/version8_isotypic_relative_curvature_parent_hessian_gate.tex`
- `s2t/audits/s2t_v8_isotypic_relative_curvature_parent_hessian_gate.py`
- `s2t/results/s2t_v8_isotypic_relative_curvature_parent_hessian_gate_results.json`