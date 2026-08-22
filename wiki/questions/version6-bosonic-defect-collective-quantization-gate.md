# Version VI: коллективное квантование бозонного дефекта

> Status: working
> Type: question
> Updated: 2026-08-20

## Summary

Формальная ориентационная орбита ежа равна `SO(3)`, но не является
локальной коллективной координатой: её момент инерции расходится как
`L^3`. Диагональное вращение — стабилизатор, а не мода.

## Results

- fit ориентационной инерции дал степень `3.002412...`;
- коэффициент `L^3` совпал с `(16 pi/9) Delta^2`;
- локализованными остаются три переноса;
- масштаб имеет положительную кривизну и даёт massive breathing-моду;
- отсутствует стабилизаторная gauge-фаза `S1`, поэтому нет dyon-заряда;
- нормируемое пространство модулей в текущем приближении равно `R3` и не
  несёт `Z2`-петли для FR-знака;
- минимальное квантование даёт нейтральное состояние спина ноль.

## Boundary

Полный configuration-space аудит ещё может потребовать отдельной
топологической линии, но текущие WZW/Pfaffian данные её не выводят.
Абсолютные масса, радиус и breathing-частота остаются ненормированными.

Проверка выполнена в [[version6-bosonic-defect-mass-portal-parent-gate]]:
безразмерный профиль замкнут, но две абсолютные единицы не выведены, а
портал формы к Хиггсу имеет нулевой коэффициент в минимальном родителе.

## Links

- [[version6-bosonic-defect-field-identification-gate]]
- [[bosonic-defect-collective-quantization-literature-2026]]
- [[version6-gauged-projective-spin-cover-parent-gate]]
- [[version5-eta-wzw-real-pair-phase-gate]]
- [[version6-matter-birth-program]]
- [[version6-bosonic-defect-mass-portal-parent-gate]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_collective_quantization_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_collective_quantization_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_collective_quantization_gate_results.json`