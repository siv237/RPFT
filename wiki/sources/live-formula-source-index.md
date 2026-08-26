# Обратный индекс формул живого корпуса

> Status: working
> Type: source
> Updated: 2026-08-26

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
| Гейты Version 7 | 8 | 96 | [[live-formulas-gates-version7-01]], [[live-formulas-gates-version7-02]], [[live-formulas-gates-version7-03]], [[live-formulas-gates-version7-04]], [[live-formulas-gates-version7-05]], [[live-formulas-gates-version7-06]], [[live-formulas-gates-version7-07]], [[live-formulas-gates-version7-08]] |
| Тематические гейты | 60 | 479 | [[live-formulas-gates-thematic-01]], [[live-formulas-gates-thematic-02]], [[live-formulas-gates-thematic-03]], [[live-formulas-gates-thematic-04]] |
| Финальный corpus | 1 | 19 | [[live-formulas-corpus-01]] |

Всего: **427** формулосодержащих файлов и **4804** блочные формулы. После нормализации пробелов: **4715** различных блоков и **89** повторных вхождений.

## Правило извлечения

Учитываются парные `$$...$$`, `\[...\]` и внешние окружения `equation`, `align`, `gather`, `multline`, `displaymath`, `eqnarray` со звёздными вариантами. Табличные и внутристочные формулы требуют отдельного прохода.

## Links

- [[pre-tome-formula-source-index]]
- [[pre-tome-formula-genealogy]]
- [[global-formula-atlas]]
- [[formula-equivalence-and-status-index]]
- [[global-theorem-and-no-go-ledger]]