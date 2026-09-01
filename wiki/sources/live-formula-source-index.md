# Обратный индекс формул живого корпуса

> Status: working
> Type: source
> Updated: 2026-09-01

## Summary

Полный механический индекс формул из `s2t/docs/`, `s2t/gates/` и `corpus/`. Каждая запись хранит точный путь, строки и исходный LaTeX-блок. Доказательный статус задают [[global-formula-atlas]] и [[global-theorem-and-no-go-ledger]].

## Итог

| Слой | Файлов | Формул | Страницы |
|---|---:|---:|---|
| Документы и сборки Томов I–VII | 26 | 944 | [[live-formulas-docs-01]], [[live-formulas-docs-02]], [[live-formulas-docs-03]], [[live-formulas-docs-04]], [[live-formulas-docs-05]], [[live-formulas-docs-06]], [[live-formulas-docs-07]], [[live-formulas-docs-08]], [[live-formulas-docs-09]] |
| Гейты Version 3 | 27 | 322 | [[live-formulas-gates-version3-01]], [[live-formulas-gates-version3-02]], [[live-formulas-gates-version3-03]] |
| Гейты Version 4 | 115 | 1101 | [[live-formulas-gates-version4-01]], [[live-formulas-gates-version4-02]], [[live-formulas-gates-version4-03]], [[live-formulas-gates-version4-04]], [[live-formulas-gates-version4-05]], [[live-formulas-gates-version4-06]], [[live-formulas-gates-version4-07]], [[live-formulas-gates-version4-08]], [[live-formulas-gates-version4-09]], [[live-formulas-gates-version4-10]] |
| Гейты Version 5 | 78 | 810 | [[live-formulas-gates-version5-01]], [[live-formulas-gates-version5-02]], [[live-formulas-gates-version5-03]], [[live-formulas-gates-version5-04]], [[live-formulas-gates-version5-05]], [[live-formulas-gates-version5-06]], [[live-formulas-gates-version5-07]], [[live-formulas-gates-version5-correction-01]] |
| Гейты Version 6 | 112 | 1033 | [[live-formulas-gates-version6-01]], [[live-formulas-gates-version6-02]], [[live-formulas-gates-version6-03]], [[live-formulas-gates-version6-04]], [[live-formulas-gates-version6-05]], [[live-formulas-gates-version6-06]], [[live-formulas-gates-version6-07]], [[live-formulas-gates-version6-08]], [[live-formulas-gates-version6-09]] |
| Гейты Version 7 | 39 | 439 | [[live-formulas-gates-version7-01]], [[live-formulas-gates-version7-02]], [[live-formulas-gates-version7-03]], [[live-formulas-gates-version7-04]], [[live-formulas-gates-version7-05]], [[live-formulas-gates-version7-06]], [[live-formulas-gates-version7-07]], [[live-formulas-gates-version7-08]], [[live-formulas-gates-version7-09]], [[live-formulas-gates-version7-10]], [[live-formulas-gates-version7-11]], [[live-formulas-gates-version7-12]], [[live-formulas-gates-version7-13]], [[live-formulas-gates-version7-14]], [[live-formulas-gates-version7-15]], [[live-formulas-gates-version7-16]], [[live-formulas-gates-version7-17]], [[live-formulas-gates-version7-18]], [[live-formulas-gates-version7-19]], [[live-formulas-gates-version7-20]], [[live-formulas-gates-version7-21]], [[live-formulas-gates-version7-22]], [[live-formulas-gates-version7-23]], [[live-formulas-gates-version7-24]], [[live-formulas-gates-version7-25]], [[live-formulas-gates-version7-26]], [[live-formulas-gates-version7-27]], [[live-formulas-gates-version7-28]], [[live-formulas-gates-version7-29]], [[live-formulas-gates-version7-30]], [[live-formulas-gates-version7-31]], [[live-formulas-gates-version7-32]], [[live-formulas-gates-version7-33]], [[live-formulas-gates-version7-34]], [[live-formulas-gates-version7-35]], [[live-formulas-gates-version7-36]], [[live-formulas-gates-version7-37]], [[live-formulas-gates-version7-38]], [[live-formulas-gates-version7-39]] |
| Гейты Version 7 — продолжение | 1 | 6 | [[live-formulas-gates-version7-40]] |
| Гейты Version 7 — корневая стационарность | 1 | 6 | [[live-formulas-gates-version7-41]] |
| Гейты Version 7 — индексный суперслед | 1 | 7 | [[live-formulas-gates-version7-42]] |
| Гейты Version 7 — положительная относительная норма | 1 | 6 | [[live-formulas-gates-version7-43]] |
| Гейты Version 7 — Real-полуследовой вес | 1 | 7 | [[live-formulas-gates-version7-44]] |
| Гейты Version 7 — степень формы и клиффордов след | 1 | 6 | [[live-formulas-gates-version7-45]] |
| Гейты Version 7 — кратности общего следа | 1 | 9 | [[live-formulas-gates-version7-46]] |
| Гейты Version 7 — полярный инцидентный перенос | 1 | 12 | [[live-formulas-gates-version7-47]] |
| Гейты Version 7 — метрика редуцированного quotient | 1 | 10 | [[live-formulas-gates-version7-48]] |
| Тематические гейты | 60 | 479 | [[live-formulas-gates-thematic-01]], [[live-formulas-gates-thematic-02]], [[live-formulas-gates-thematic-03]], [[live-formulas-gates-thematic-04]] |
| Финальный corpus | 1 | 19 | [[live-formulas-corpus-01]] |

Первичная таблица выше сохраняет разбиение исходного прохода. Повторный
полный проход 2026-08-31 по тому же правилу извлечения с последующими
инкрементами новых гейтов дал **657** формулосодержащих файлов и **7030**
блочные формулы. Прежние числа
`467/5216` считаются устаревшим снимком, а не текущим итогом.

## Инкрементальная синхронизация 2026-08-30

Ранее не индексированные пути вынесены в дополнительные страницы:

- документы: [[live-formulas-docs-10]] — 17 формул из 3 файлов;
  [[live-formulas-docs-11]] — 7 формул заключения Тома VIII;
  [[live-formulas-docs-12]] — 4 формулы введения Тома IX;
- поздние гейты Version 7: [[live-formulas-gates-version7-49]],
  [[live-formulas-gates-version7-50]], [[live-formulas-gates-version7-51]],
  [[live-formulas-gates-version7-52]];
- гейты Version 8: [[live-formulas-gates-version8-01]],
  [[live-formulas-gates-version8-02]], [[live-formulas-gates-version8-03]],
  [[live-formulas-gates-version8-04]], [[live-formulas-gates-version8-05]],
  [[live-formulas-gates-version8-06]], [[live-formulas-gates-version8-07]],
  [[live-formulas-gates-version8-08]], [[live-formulas-gates-version8-09]],
  [[live-formulas-gates-version8-10]], [[live-formulas-gates-version8-11]],
  [[live-formulas-gates-version8-12]], [[live-formulas-gates-version8-13]],
  [[live-formulas-gates-version8-14]], [[live-formulas-gates-version8-15]],
  [[live-formulas-gates-version8-16]], [[live-formulas-gates-version8-17]],
  [[live-formulas-gates-version8-18]],
  [[live-formulas-gates-version8-19]],
  [[live-formulas-gates-version8-20]],
  [[live-formulas-gates-version8-21]],
  [[live-formulas-gates-version8-22]],
  [[live-formulas-gates-version8-23]],
  [[live-formulas-gates-version8-24]],
  [[live-formulas-gates-version8-25]],
  [[live-formulas-gates-version8-26]],
  [[live-formulas-gates-version8-27]],
  [[live-formulas-gates-version8-28]],
  [[live-formulas-gates-version8-29]],
  [[live-formulas-gates-version8-30]],
  [[live-formulas-gates-version8-31]],
  [[live-formulas-gates-version8-32]], [[live-formulas-gates-version8-33]],
  [[live-formulas-gates-version8-34]], [[live-formulas-gates-version8-35]],
  [[live-formulas-gates-version8-36]], [[live-formulas-gates-version8-37]],
  [[live-formulas-gates-version8-38]], [[live-formulas-gates-version8-39]],
  [[live-formulas-gates-version8-40]], [[live-formulas-gates-version8-41]],
  [[live-formulas-gates-version8-42]], [[live-formulas-gates-version8-43]],
  [[live-formulas-gates-version8-44]], [[live-formulas-gates-version8-45]],
  [[live-formulas-gates-version8-46]], [[live-formulas-gates-version8-47]],
  [[live-formulas-gates-version8-48]], [[live-formulas-gates-version8-49]],
  [[live-formulas-gates-version8-50]], [[live-formulas-gates-version8-51]],
  [[live-formulas-gates-version8-52]], [[live-formulas-gates-version8-53]],
  [[live-formulas-gates-version8-54]], [[live-formulas-gates-version8-55]],
  [[live-formulas-gates-version8-56]], [[live-formulas-gates-version8-57]],
  [[live-formulas-gates-version8-58]], [[live-formulas-gates-version8-59]],
  [[live-formulas-gates-version8-60]], [[live-formulas-gates-version8-61]],
  [[live-formulas-gates-version8-62]], [[live-formulas-gates-version8-63]],
  [[live-formulas-gates-version8-64]], [[live-formulas-gates-version8-65]],
  [[live-formulas-gates-version8-66]], [[live-formulas-gates-version8-67]],
  [[live-formulas-gates-version8-68]], [[live-formulas-gates-version8-69]],
  [[live-formulas-gates-version8-70]], [[live-formulas-gates-version8-71]],
  [[live-formulas-gates-version8-72]], [[live-formulas-gates-version8-73]],
  [[live-formulas-gates-version8-74]], [[live-formulas-gates-version8-75]],
  [[live-formulas-gates-version8-76]], [[live-formulas-gates-version8-77]],
  [[live-formulas-gates-version8-78]], [[live-formulas-gates-version8-79]],
  [[live-formulas-gates-version8-80]], [[live-formulas-gates-version8-81]],
  [[live-formulas-gates-version8-82]], [[live-formulas-gates-version8-83]],
  [[live-formulas-gates-version8-84]], [[live-formulas-gates-version8-85]],
  [[live-formulas-gates-version8-86]];
- гейты Version 9: [[live-formulas-gates-version9-01]] — 7 формул первого
  admission-гейта; [[live-formulas-gates-version9-02]] — 12 формул общего
  carrier; [[live-formulas-gates-version9-03]] — 13 формул bounded
  functional; [[live-formulas-gates-version9-04]] — 11 формул selector-origin;
  [[live-formulas-gates-version9-05]] — 11 формул raw endpoint-origin;
  [[live-formulas-gates-version9-06]] — 14 формул finite-module architecture;
  [[live-formulas-gates-version9-07]] — 18 формул fixed-parent module-origin;
  [[live-formulas-gates-version9-08]] — 17 формул finite-geometry configuration space;
  [[live-formulas-gates-version9-09]] — 17 формул typed creation-frame;
  [[live-formulas-gates-version9-10]] — 18 формул creation source/rate origin;
  [[live-formulas-gates-version9-11]] — 16 формул bidirectional KMS completion;
  [[live-formulas-gates-version9-12]] — 16 формул KMS parameter-origin;
  [[live-formulas-gates-version9-13]] — 15 формул общего KMS source-parent;
  [[live-formulas-gates-version9-14]] — 18 формул four-slot origin двух
  source-covectors; [[live-formulas-gates-version9-15]] — 19 формул
  minimal relative-shape selector; [[live-formulas-gates-version9-16]] —
  16 формул parent-origin его четырёх sources;
  [[live-formulas-gates-version9-17]] — 18 формул minimal invariant
  logdet parent; [[live-formulas-gates-version9-18]] — 18 формул
  measure-origin logdet parent; [[live-formulas-gates-version9-19]] —
  20 формул auxiliary fermion module admission;
  [[live-formulas-gates-version9-20]] — 17 формул statistics parent-origin;
  [[live-formulas-gates-version9-21]] — 21 формула minimal BRST complex;
  [[live-formulas-gates-version9-22]] — 18 формул BRST shift-origin;
  [[live-formulas-gates-version9-23]] — 20 формул Stückelberg parent;
  [[live-formulas-gates-version9-24]] — 19 формул physical fermion-loop
  origin-аудита; [[live-formulas-gates-version9-25]] — 20 формул minimal
  fermion-bath architecture; [[live-formulas-gates-version9-26]] — 22
  формулы normalized KMS--Keldysh influence-functional admission;
  [[live-formulas-gates-version9-27]] — 20 формул reservoir spectral-density
  parent-origin; [[live-formulas-gates-version9-28]] — 14 формул reservoir
  measure-anomaly parent-origin; [[live-formulas-gates-version9-29]] — 14
  формул minimal new parent axiom admission; [[live-formulas-gates-version9-30]] —
  12 формул axiom-augmented common-parent closure.
  [[live-formulas-gates-version9-31]] — 10 формул axiom-augmented blind
  dimensionless prediction.
  [[live-formulas-gates-version9-32]] — 8 формул conditional program status.
  [[live-formulas-gates-version9-33]] — 7 формул physical-origin reopening
  criterion.
  [[live-formulas-gates-version9-34]] — 9 формул common-origin covariance
  carrier admission.
  [[live-formulas-gates-version9-35]] — 9 формул Gaussian reference-state
  parent-origin.
  [[live-formulas-gates-version9-36]] — 7 формул physical reference-scale
  parent-origin.
  [[live-formulas-gates-version9-37]] — 6 формул финального статуса Тома IX
  и программы Тома X.

Новые страницы индексируют 174 дополнительных пути относительно исходного
снимка. Текущий сводный счёт `671/7207` получен повторным полным проходом и
последующими точными инкрементами; он имеет приоритет над суммой
исторических страничных снимков, часть которых отражает более ранние
состояния файлов.

## Правило извлечения

Учитываются парные `$$...$$`, `\[...\]` и внешние окружения `equation`, `align`, `gather`, `multline`, `displaymath`, `eqnarray` со звёздными вариантами. Табличные и внутристочные формулы требуют отдельного прохода.

## Links

- [[pre-tome-formula-source-index]]
- [[pre-tome-formula-genealogy]]
- [[global-formula-atlas]]
- [[formula-equivalence-and-status-index]]
- [[global-theorem-and-no-go-ledger]]