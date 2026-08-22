# Том VI: внутренняя щель полного прямого вихря

> Status: working
> Type: question
> Updated: 2026-08-20

## Краткий вывод

После удаления двух переносных нулей полный поперечный оператор прямой нити
имеет строго положительную континуальную щель

`Delta_int = 3.61933633`.

Минимум находится в сопряжённых блоках `(c,j)=(1,1),(-1,-1)`. Сходимость
имеет порядок `2.00564`. Ближайший конкурент стремится к `3.66499002`,
поэтому первый внутренний уровень отделён запасом `0.04565369`.

Это закрывает полную поперечную линейную устойчивость бесконечной прямой
нити: ни тензорные, ни калибровочные, ни высокоугловые возмущения не дают
направления распада.

## Физическая граница

Щель не доказывает существование локализованной частицы. Для этого нужно
изогнуть нить и вывести энергию кривизны, а затем проверить конечный минимум
энергии замкнутого кольца.

## Последующий результат

[[version6-bosonic-defect-curved-string-effective-action-gate]] вывел
ведущее действие Намбу—Гото и показал, что спокойное кольцо монотонно
сжимается. Для возможной стабилизации требуется ответ массивных мод или
отдельный сохраняющийся продольный/топологический заряд.

## Следующий вопрос

Вывести низкоэнергетическое действие медленно изогнутой нити из полного
стационарного профиля и разрешённого поперечного гессиана.

## Связи

- [[version6-bosonic-defect-full-tensor-high-angular-coercivity-gate]]
- [[version6-bosonic-defect-curved-string-effective-action-gate]]
- [[version6-bosonic-defect-full-tensor-translation-calibration-gate]]
- [[version6-bosonic-defect-full-tensor-stationary-background-gate]]
- [[vortex-angular-fourier-block-literature-2026]]
- [[version6-matter-birth-program]]

## Исходные материалы

- `s2t/gates/version6_bosonic_defect_full_tensor_internal_gap_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_full_tensor_internal_gap_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_full_tensor_internal_gap_gate_results.json`