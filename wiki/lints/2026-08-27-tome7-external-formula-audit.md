# Проверка внешнего формульного аудита Тома VII

> Status: mature
> Type: lint
> Updated: 2026-08-27

## Summary

Пять замечаний внешнего аудита проверены по актуальным LaTeX-гейтам,
вычислительным аудитам и JSON-сертификатам. Три предполагаемые формульные
ошибки относятся к устаревшему, OCR-повреждённому или неполному отображению:
в текущем корпусе формулы уже записаны правильно. Два замечания о конвенциях
приняты как полезные редакционные уточнения.

## Проверенные утверждения

- Формула сингулярных чисел уже имеет правильный вид
  `1/15 [1 + 2 sum_j (1-sigma_j^2)^2]` в
  `s2t/gates/version7_chiral_hodge_index_instability_gate.tex`.
- Сырой спектр относительного гессиана полностью читаем и совпадает с
  `s2t/results/s2t_v7_corrected_vacuum_relative_edge_hessian_gate_results.json`:
  кратности равны `27, 6, 12, 9, 18`, а физический спектр содержит уровни
  `0`, `4/45` и `16/45` с кратностями `27, 18, 27`.
- Оператор укоренения уже записан двумя эйлеровыми производными в
  `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex`;
  коэффициент единственного монома `12` подтверждён сертификатом.
- Коэффициент плоского гессиана `8/7` независимо проверяется конечными
  разностями на всех 24 вещественных координатах. В гейт добавлено явное
  соглашение о нормированном следе и координатах.
- Сигнатуры `(12,0,10)` и `(108,0,90)` подтверждены машинно. В гейт добавлено
  уточнение, что они считаются в пространстве комплексных рёберных и
  семейных блоков, а раскрытие калибровочного мультиплета меняет кратности,
  но не знаки.

## Вердикт

Внешний аудит не обнаружил новой ошибки, меняющей математический статус
Тома VII. Он оказался полезен как независимая проверка отображения формул и
выявил два места, где конвенции следовало сделать явными. Главные no-go и
положительные вердикты гейтов не пересматривались.

## Links

- [[version7-rank-changing-superconnection-admission-gate]] — конвенция
  плоского гессиана.
- [[version7-corrected-vacuum-relative-edge-hessian-gate]] — сырой и
  обобщённый спектры.
- [[version7-baseline-rooted-primitive-cycle-admission-gate]] — оператор
  укоренения и единственный цикл.
- [[version7-rooted-cycle-isotypic-edge-projector-gate]] — уровень подсчёта
  сигнатур.
- [[global-theorem-and-no-go-ledger]] — граница строгих статусов Тома VII.

## Source Notes

- `s2t/gates/version7_chiral_hodge_index_instability_gate.tex`
- `s2t/gates/version7_corrected_vacuum_relative_edge_hessian_gate.tex`
- `s2t/gates/version7_baseline_rooted_primitive_cycle_admission_gate.tex`
- `s2t/gates/version7_rank_changing_superconnection_admission_gate.tex`
- `s2t/gates/version7_rooted_cycle_isotypic_edge_projector_gate.tex`
- соответствующие файлы `s2t/audits/s2t_v7_*.py` и
  `s2t/results/s2t_v7_*_results.json`