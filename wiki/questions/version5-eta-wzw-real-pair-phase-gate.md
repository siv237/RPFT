# Эта-фаза и WZW-ориентация Real-пары

> Status: working
> Type: question
> Updated: 2026-08-18

## Summary

Явная обменная пара имеет winding и трёхмерные Bott-заряды `+15/-15`.
На исходной окружности кубическая WZW-форма отсутствует по размерности;
там существует только первая нечётная форма.

При целочисленном уровне экспоненцированная комплексная фаза класса 15
равна единице. Одна ориентированная вещественная ветвь условно имеет
Pfaffian-паритет `(-1)^15=-1`, но сопряжённая ветвь также нечётна, поэтому
полный KO6-Pfaffian даёт `+1`.

Проект не вывел ориентацию Pfaffian line и правило, по которому физическая
мера считает только одну ветвь в фазе. Поэтому эта/WZW-фаза не выбирает
сектор 15 относительно нулевого сектора. Неизбежность дефекта внутри уже
заданного класса сохраняется.

## Links

- [[version5-closure-deficit-induced-vacuum-response-gate]]
- [[version5-real-toeplitz-ko7-unitary-representative-gate]]
- [[version4-pfaffian-eta-orientation-gate]]
- [[version4-determinant-line-inflow-gate]]
- [[eta-wzw-pfaffian-phase-literature-2026]]

## Source Notes

- `s2t/gates/version5_eta_wzw_real_pair_phase_gate.tex`
- `s2t/audits/s2t_v5_eta_wzw_real_pair_phase_gate.py`
- `s2t/results/s2t_v5_eta_wzw_real_pair_phase_gate_results.json`