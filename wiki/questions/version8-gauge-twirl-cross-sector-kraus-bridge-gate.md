# Gauge-твирлинг и межсекторный Kraus-мост

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Прямой gauge-синглетный оператор между quark- и lepton/vectorlike-
секторами отсутствует, но полный мультиплет уже существующих цветных
стрелок задаёт gauge-инвариантную квадратичную Kraus-сумму. Она сокращает
центральную `C^2` до скаляра без цветного вакуумного среднего.

## Key Points

- Межсекторная опора состоит из `QLYR` и `XLdR`: по три комплексных
  направления, всего 12 вещественных Kraus-направлений.
- Усреднение линейной стрелки по центру `SU3` равно нулю: линейного
  gauge-синглета нет.
- Сумма `-1/2 sum ad(D_e)^2` по ортонормированному базису не зависит от
  базиса и gauge-ковариантна.
- Максимальная невязка в 12 случайных `SU3 x SU2 x U1`-тестах — `4.75e-15`.
- На центральной `C^2` обе cross-семьи вместе дают спектр `{0,7/3}`;
  каждая отдельно уже оставляет только скаляр.
- Внутрисекторные `LLXR` и `YLeR` не снимают двухсекторность, что служит
  контрольным тестом.
- Качественный результат устойчив при независимых положительных скоростях
  от `1e-6` до `1e6`, но сама скорость и общий parent-action не выведены.

## Links

- [[version8-opening-contract]] — центральный тест Тома VIII.
- [[version8-markov-fixed-algebra-selector-gate]] — исходная `C^2`.
- [[version7-color-preserving-composite-cycle-parent-gate]] — прежняя
  попытка цветосохраняющего составного канала.
- [[version7-virtual-colored-bridge-schur-complement-gate]] — виртуальное
  чтение тех же цветных направлений.
- [[gauge-covariant-kraus-multiplet-literature-2026]] — внешний контекст.
- [[version8-kraus-bridge-parent-action-hessian-gate]] — проверка
  классического запуска и гессиана.
- [[version8-gauge-twirl-kraus-lcf-migration-gate]] — точная проверка,
  заменившая случайные gauge- и rate-тесты символическим сертификатом.

## Source Notes

- `s2t/gates/version8_gauge_twirl_cross_sector_kraus_bridge_gate.tex`
- `s2t/audits/s2t_v8_gauge_twirl_cross_sector_kraus_bridge_gate.py`
- `s2t/results/s2t_v8_gauge_twirl_cross_sector_kraus_bridge_gate_results.json`