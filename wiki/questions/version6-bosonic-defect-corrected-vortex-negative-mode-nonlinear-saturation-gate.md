# Том VI: нелинейная проверка отрицательной моды вихря

> Status: working
> Type: question
> Updated: 2026-08-20

## Краткий вывод

Прежняя отрицательная мода вычислялась около непрерывного профиля,
выбранного на сетке, но не являвшегося точной стационарной точкой
дискретной энергии. Нелинейная релаксация показала, что двойная яма
соответствует перемещению центра вихря между положениями относительно
узлов сетки.

После закрепления нуля поля в центре, полной дискретной релаксации и
повторного вычисления гессиана отрицательные моды исчезают:

- сетка `25`: `lambda_min=0.0120226`;
- сетка `33`: `lambda_min=0.0008661`;
- сетка `41`: `lambda_min=0.0004727`.

## Статус

- отрицательная мода предыдущего гейта не является физическим
  сертификатом;
- нелинейный срез не дал нового конечного дефекта;
- диагностирован барьер Пайерлса--Набарро дискретного перемещения;
- эффективная центрированная подсистема не содержит найденной
  отрицательной моды;
- полная устойчивость `Q+T+B` остаётся открытой.

## Связи

- [[version6-bosonic-defect-corrected-vortex-covariant-zero-mode-resolution-gate]]
- [[version6-bosonic-defect-corrected-vortex-nonradial-stability-gate]]
- [[discrete-vortex-peierls-nabarro-literature-2026]]
- [[version6-bosonic-defect-translation-covariant-discretization-gate]]
- [[version6-matter-birth-program]]

## Исходные материалы

- `s2t/gates/version6_bosonic_defect_corrected_vortex_negative_mode_nonlinear_saturation_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_negative_mode_nonlinear_saturation_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_corrected_vortex_negative_mode_nonlinear_saturation_gate_results.json`