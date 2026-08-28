# Version VII: полный product-коэффициент шестого цикла

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Проверить, сохраняется ли формальный коэффициент шестикромочного цикла после
раскрытия слабых и цветовых интертвинеров полного product-оператора.

## Search for Solution

В стандартном слабом кадре

$$H=(0,1)^T,\qquad \widetilde H=(1,0)^T.$$

Исходный цикл через `uR` содержит множитель
`H_tilde^dagger H=0`. Явная блочная матрица подтверждает отсутствие
билинейного члена между `QL-YR` и `XL-uR` в полном `Tr Phi^6`.

Исчерпывающий перебор 14 простых шестикромочных циклов нашёл ровно три,
которые квадратичны по тяжёлым полям около singlet-вакуума:

1. исходная up-пара — коэффициент `0`;
2. down-пара `(QL-YR,XL-dR)` — коэффициент `12`;
3. слабая пара `(LL-XR,YL-eR)` — коэффициент `12` для параллельных слабых
   компонент.

Gaussian-множитель `-1/6` превращает два выживших билинейных коэффициента в
`-2`.

## Expected Result

Исходный виртуальный цикл строго закрыт: прежний determinant-блок имел
ненулевой `kappa` только в редуцированной скалярной смежности. Полный
оператор переносит возможную цветную связь на down-ребро `XL-dR` и
одновременно открывает слабую конкурирующую пару. Следующий тест обязан
рассматривать их совместно в точном Gaussian-гессиане.

Следующий гейт — [[version7-weak-aligned-cycle-competition-gate]].

## Compliance Check

- Явные блочные матрицы воспроизводят коэффициенты `0,12,12`.
- Ортогональный контроль слабой пары даёт нулевой билинейный коэффициент.
- Перебор полного графа даёт `14` простых циклов и ровно `3` локально
  квадратичные ветви.
- Статус: `original cycle no-go; down and weak competition open`.

## Links

- [[version7-full-product-a6-project-intuition-search]]
- [[product-a6-spectral-action-literature-2026]]
- [[version7-common-spectral-profile-singlet-virtual-ratio-gate]]
- [[version7-common-higgs-degree-two-cross-edge-gate]]
- [[version7-weak-aligned-cycle-competition-gate]]

## Source Notes

- `s2t/gates/version7_full_product_a6_cycle_coefficient_gate.tex`
- `s2t/audits/s2t_v7_full_product_a6_cycle_coefficient_gate.py`
- `s2t/results/s2t_v7_full_product_a6_cycle_coefficient_gate_results.json`