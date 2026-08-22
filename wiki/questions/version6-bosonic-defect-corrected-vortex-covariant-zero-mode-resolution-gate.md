# Том VI: ковариантная фиксация выявила отрицательную моду вихря

> Status: working
> Type: question
> Updated: 2026-08-20

## Краткий вывод

В предыдущей фоновой калибровке был выбран неверный знак, оставлявший
оператор Фаддеева--Попова типа `Delta+m^2`. После перехода к
эллиптическому оператору `-Delta+m^2` искусственный мягкий кластер
перестал скрывать физическую отрицательную моду.

На сетках `32,40,48` нижнее значение равно соответственно
`-0.10338`, `-0.20170`, `-0.18905`. Знак сохраняется при изменении
радиуса области от `8` до `12`.

## Физический смысл

- прямая каноническая вихревая нить линейно неустойчива;
- отрицательная мода смешивает заряженное ядро и связность примерно
  поровну;
- неустойчива продольная полоса `|k_z|<0.4348`;
- это возможный механизм деформации нити, но ещё не доказанное замыкание
  в хопфову петлю и не рождение частицы;
- следующий вопрос — нелинейно продолжить отрицательный собственный
  вектор и найти конечный исход.

## Последующая коррекция

[[version6-bosonic-defect-corrected-vortex-negative-mode-nonlinear-saturation-gate]]
показал, что sampled-профиль не был точной стационарной точкой дискретной
энергии. Отрицательное направление перемещало центр вихря относительно
узлов сетки. После центрированной дискретной релаксации отрицательные
моды исчезли, поэтому утверждение о физической неустойчивости прямой нити
снято.

## Связи

- [[version6-bosonic-defect-corrected-vortex-nonradial-stability-gate]]
- [[version6-bosonic-defect-corrected-vortex-negative-mode-nonlinear-saturation-gate]]
- [[version6-bosonic-defect-q-stiffness-parent-normalization-gate]]
- [[so3-z3-vortex-profile-and-stability-literature-2026]]
- [[version6-matter-birth-program]]

## Исходные материалы

- `s2t/gates/version6_bosonic_defect_corrected_vortex_covariant_zero_mode_resolution_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_corrected_vortex_covariant_zero_mode_resolution_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_corrected_vortex_covariant_zero_mode_resolution_gate_results.json`