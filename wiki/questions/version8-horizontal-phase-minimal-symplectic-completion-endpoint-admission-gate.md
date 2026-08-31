# Концевой допуск минимальной симплектической достройки

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Абстрактное сбалансированное представление
`4 H_plus + 4 H_minus + C_plus + C_minus + 4 S_zero` имеет комплексную
размерность `26` и допускает инвариантную симплектическую форму полного
ранга с определителем `1`. Пространство инвариантных кососимметрических
форм имеет размерность `23`, поэтому калибровочная симметрия не выбирает
каноническую поляризацию.

Два независимых поля дают ненулевую свёртку, но одно поле по-прежнему имеет
нулевую самосвёртку. Главное препятствие — концевое происхождение: текущий
носитель содержит одну копию `H_plus`, а требуется четыре. Три недостающие
копии дают шесть новых комплексных направлений, отсутствующих в образе
нынешних внутренних флуктуаций.

Итак, формальное котангенциальное завершение допущено, но его реализация
существующим конечным родителем отклонена. Новые фермионы не обязательны для
внешнего бозонного удвоения; при концевой реализации их статус и аномалии
потребуют нового гейта.

## Следующий вопрос

Можно ли вывести удвоенный колчан и его отображение момента из одного
положительного родительского действия, не объявляя шесть направлений и
поляризацию внешними данными?

## Связи

- [[version8-horizontal-phase-complex-symplectic-polarization-admission-gate]]
- [[version5-derived-moment-map-minimal-data-gate]]
- [[version3-bf-aksz-pairing-gate]]
- [[version7-four-vertex-vectorlike-selector-gate]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate.tex`
- `s2t/audits/s2t_v8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate.py`
- `s2t/results/s2t_v8_horizontal_phase_minimal_symplectic_completion_endpoint_admission_gate_results.json`
- `s2t/proofdsl/examples/version8_horizontal_phase_minimal_symplectic_completion_endpoint_admission.py`