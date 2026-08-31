# Минимальные новые данные спектрального якоря

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Нормированная однополюсная форма требует двух независимых данных:
выбранного масштаба базы `a>0` и выбранной безразмерной карты `c>0`, после
чего `m²=ca`. Полное ядро дополнительно требует амплитуды `lambda_3`.

Точные свидетели `1/2` против `2/3` показывают, что удаление `a` или `c`
возвращает неединственность. Деление на статическое значение удаляет
`lambda_3`, поэтому амплитуда не выбирает форму.

## Вердикт

Минимальный контракт получен, но не реализован. Следующий узел должен
строить внутренний селектор пары `(a,c)`.

## Связи
- [[version8-baryon-spectral-scale-anchor-candidate-audit-gate]]
- [[version8-baryon-nonlocal-kernel-spectral-measure-parent-origin-gate]]
- [[global-theorem-and-no-go-ledger]]

## Исходники
- `s2t/gates/version8_baryon_spectral_scale_anchor_minimal_new_data_gate.tex`
- `s2t/audits/s2t_v8_baryon_spectral_scale_anchor_minimal_new_data_gate.py`
- `s2t/results/s2t_v8_baryon_spectral_scale_anchor_minimal_new_data_gate_results.json`