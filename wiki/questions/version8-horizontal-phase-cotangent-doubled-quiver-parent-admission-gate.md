# Допуск котангенциального удвоенного колчанного родителя

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Ретроспектива показала, что новый носитель действительно продвигает старую
задачу. Том III имел симплектическую скобку без выбранной положительной
метрики, а Том V — предпроективное выражение без совместимой физической
поляризации. На нынешнем 26-мерном носителе матрицы
`K_a=Omega rho(X_a)` симметричны и задают ненулевое отображение момента.

Из четырнадцати компонент независимы тринадцать; одна центральная
комбинация тождественно исчезает. Слабая котангенциальная пара даёт явный
ненулевой свидетель `(-1,0,...,0,-1/2)`.

Но каноническая волоконная фаза `q -> z q`, `p -> z^-1 p` сохраняет
симплектическую форму, коммутирует с калибровочной группой и оставляет все
компоненты момента неизменными. Поэтому любой родитель вида
`F(mu)`, включая `lambda ||mu-zeta||^2`, остаётся фазонезависимым.
Параметры `lambda`, `zeta` и положительная метрика также не выбраны.

## Следующий вопрос

Может ли уже существующая следовая метрика выбрать совместимую комплексную
структуру `J`, положительную форму `g=Omega J` и взаимодействие, которое
нарушает котангенциальный `U(1)` без ручного фазового члена?

## Связи

- [[version8-horizontal-phase-minimal-symplectic-completion-endpoint-admission-gate]]
- [[version3-bf-aksz-pairing-gate]]
- [[version5-derived-moment-map-minimal-data-gate]]
- [[version8-full-noise-cotangent-carrier-admission-gate]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate.tex`
- `s2t/audits/s2t_v8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate.py`
- `s2t/results/s2t_v8_horizontal_phase_cotangent_doubled_quiver_parent_admission_gate_results.json`
- `s2t/proofdsl/examples/version8_horizontal_phase_cotangent_doubled_quiver_parent_admission.py`