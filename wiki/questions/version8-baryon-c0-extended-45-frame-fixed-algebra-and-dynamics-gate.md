# Неподвижная алгебра и динамика расширенного 45-кадра

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Расширенный кадр задаёт корректный унитальный сохраняющий след
GKSL-генератор, однако новый паулиевский `M2`-блок изолирован от старого
`H21`. Совместный коммутант и неподвижная алгебра равны
`C P21 direct_sum C Pn`, поэтому процесс на `H23` не примитивен.

Три новые бесследовые моды затухают с собственным значением `-4`;
старо-новые когерентности также затухают, поскольку `Q42=sum F_a^2`
положительно определён. Центральные популяции двух компонент сохраняются.

## Граница

Внутренний мост `E=|s0><a0|` не является динамическим мостом между новым
блоком и прежним 42-носителем. Для физического статуса условного `c0=4`
нужен gauge-ковариантный оператор с ненулевым старо-новым блоком.

## Связи

- [[version8-baryon-c0-minimal-neutral-endpoint-extension-gate]]
- [[version8-full-noise-42-jump-gksl-fixed-algebra-gate]]
- [[version8-baryon-c0-existing-42-carrier-linking-bridge-classification-gate]]

## Исходники

- `s2t/gates/version8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate.tex`
- `s2t/audits/s2t_v8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate.py`
- `s2t/results/s2t_v8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate_results.json`