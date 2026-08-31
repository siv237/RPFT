# Аудит кандидатов на энергию автономных часов

> Status: mature
> Type: question
> Updated: 2026-08-30

## Summary

Проверены шесть классов внутренних кандидатов: спектральное обрезание,
радиусы, щель шумового генератора, щель вакуумного родителя, энергия
компактона и наблюдаемые массы. Ни один не имеет выведенного отображения в
пару `(E_C,E_int)` часовой столкновительной модели.

## Key Points

- `Lambda` сохраняет орбиту профиль--обрезание.
- Физические радиусы не выведены.
- Обе щели зависят от выбранной безразмерной нормировки.
- Компактон фиксирует только `E L=pi hbar c`.
- Наблюдаемые массы остаются внешними или обучающими данными.
- Условная формула `Gamma=chi^2 E_C/hbar` сохраняется.

## Links

- [[version8-typed-clock-energy-to-noise-rate-anchor-gate]]
- [[version8-current-status-synchronization]]

## Source Notes

- `s2t/gates/version8_clock_energy_anchor_candidate_audit_gate.tex`
- `s2t/audits/s2t_v8_clock_energy_anchor_candidate_audit_gate.py`
- `s2t/results/s2t_v8_clock_energy_anchor_candidate_audit_gate_results.json`