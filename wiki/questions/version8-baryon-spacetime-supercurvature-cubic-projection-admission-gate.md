# Сдвинутая кривизна: формульный допуск и градуировочный запрет

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Единая центрально сдвинутая кривизна
`R_m(Z)=((m/2)I+Z)^2-(mI/2)^2=mZ+Z^2` даёт из одной положительной нормы

`Tr R_m(Z)^2=m^2 Tr Z^2+2m Tr Z^3+Tr Z^4`.

Поэтому форма коэффициентов уже не произвольна:
`alpha=m^2`, `lambda_3=2m`, `beta=1` и
`lambda_3^2/(alpha beta)=4`. Кубическая вариация точно пропорциональна
связному тензору `d_abc`, то есть воспроизводит операторную форму `W3`.

## Граница

Ненулевой центральный фон не принадлежит бесследовому 42-мерному кадру и
не является нечётным: для `Gamma=I11+(-I10)` выполнено
`Gamma M+M Gamma=m Gamma`. Его масштаб `m` текущим родителем также не
выведен. На точном луче действие равно
`38m^2t^2-6mt^3+134t^4` и при вещественном ненулевом `m` не имеет
ненулевой стационарной точки. Допущена алгебраическая форма взаимодействия,
но не её реализация настоящей градуированной суперкривизной, не абсолютный
коэффициент и не барионный вакуум.

## Связи

- [[version8-baryon-cubic-trace-connected-operator-gate]]
- [[version8-baryon-cubic-trace-parent-action-coefficient-origin-no-go-gate]]
- [[shifted-supercurvature-cubic-shape-literature-2026]]
- [[version8-gauge-closed-field-space-superconnection-gate]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.tex`
- `s2t/audits/s2t_v8_baryon_spacetime_supercurvature_cubic_projection_admission_gate.py`
- `s2t/results/s2t_v8_baryon_spacetime_supercurvature_cubic_projection_admission_gate_results.json`