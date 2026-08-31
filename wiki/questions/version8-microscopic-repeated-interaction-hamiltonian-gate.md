# Микроскопический Hamiltonian повторных взаимодействий

> Status: working
> Type: question
> Updated: 2026-08-29

## Summary

Из двенадцати cross-arrow jump-операторов построен явный самосопряжённый
system--environment Hamiltonian на минимальном носителе `21*13=273`. Его
слабый repeated-interaction предел точно возвращает cross-arrow
GKSL-генератор. Однако две cross-семьи являются эквивалентными
gauge-копиями: полный коммутант связей имеет размерность `8` над `R`, а
симметричная rate-метрика, видимая генератором, — `4`. Все вещественные
элементы полного коммутанта дают самосопряжённые interaction-Hamiltonian.
Поэтому единичная звёздная связь естественна, но не уникальна.

## Problem

После no-go канонического unitary-продолжения требовалось найти
микроскопическое взаимодействие, которое не получается произвольным
логарифмированием Kraus-карты, и проверить, выбирают ли его существующие
симметрии однозначно.

## Search for solution

На среде

```text
C|0> direct_sum E_cross_C
```

проверен оператор

```text
H_int=sum_a D_a tensor (|a><0|+|0><a|).
```

LCF-аудит проверил его тип `End(C273)`, самосопряжённость, vacuum second
moment, gauge-ковариантность, GKSL-касательную и collision-limit. Отдельная
точная коммутантная система классифицировала допустимые матрицы связей.

## Expected result

- Явная unitary микродинамика должна давать `L_cross` в пределе `h=u/n`.
- Gauge-типизация не должна искусственно объявлять единичную связь
  единственной.
- Совпадение первой производной не должно выдаваться за равенство точного
  конечного Kraus-шага.

## Compliance check

- System/environment/ambient dimensions: `21/13/273`.
- Jump dimension: `12`.
- `H_int=H_int*`: точно.
- `<0|H_int^2|0>=G`: точно.
- GKSL tangent: точно.
- Full real gauge commutant: `8`.
- Real self-adjoint interaction couplings: `8`.
- Symmetric rate metrics `C^T C`: `4`.
- Finite-step mismatch: ненулевой коэффициент порядка `h^2`, свидетель
  `E_00`.
- Physical rate and fresh ancilla source: не выведены.
- LCF obligations: `9`.

## Status boundary

Микроскопическая реализация безразмерной cross-полугруппы получена.
Уникальный interaction-Hamiltonian, точная конечная карта, автономный
источник среды и размерное физическое время не получены.

## Links

- [[version8-microscopic-interaction-hamiltonian-search]] — поисковая
  постановка и литературная сверка.
- [[version8-canonical-autonomous-clock-unitary-extension-no-go-gate]] —
  предшествующий no-go.
- [[version8-minimal-covariant-stinespring-carrier-gate]] — минимальная
  среда `13`.
- [[version8-intrinsic-noise-clock-dilation-gate]] — collision-limit.
- [[version8-lcf-proofdsl-architecture-gate]] — реестр формальных
  обязательств.
- [[version8-trace-dual-cross-interaction-selector-gate]] — условный
  геометрический селектор четырёхмерной rate-свободы.

## Source Notes

- `s2t/gates/version8_microscopic_repeated_interaction_hamiltonian_gate.tex`
- `s2t/audits/s2t_v8_microscopic_repeated_interaction_hamiltonian_gate.py`
- `s2t/results/s2t_v8_microscopic_repeated_interaction_hamiltonian_gate_results.json`
- `s2t/proofdsl/examples/version8_microscopic_interaction_hamiltonian.py`