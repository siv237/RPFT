# Том VI: переносная калибровка полного тензорного вихря

> Status: working
> Type: question
> Updated: 2026-08-20

## Краткий вывод

В полном полярном операторе найден единственный несогласованный знак:
переменная связности равна минус физической вариации `delta A`, поэтому
материальный член фоновой калибровки должен иметь знак плюс.

После исправления:

- переносный уровень экстраполируется к `7.49e-6`, то есть к нулю;
- аналитическая касательная имеет предел Рэлея `-1.84e-5`;
- её перекрытие с нижней модой на сетке `280` равно `0.99999986`;
- прежние отрицательные пары поднялись до `3.68989479` и `3.72136029`.

Следовательно, отрицательные значения предыдущего гейта были артефактом
знака фоновой калибровки, а не физической неустойчивостью прямой нити.

## Что остаётся открытым

Проверено окно `c=-1,0,1`, `-3<=j<=3` и целевое сгущение критических блоков.
Полный высокоугловой хвост тензорного оператора ещё не закрыт. Поэтому
линейная устойчивость прямой нити и рождение материи пока не доказаны.

## Последующий результат

[[version6-bosonic-defect-full-tensor-high-angular-coercivity-gate]] проверил
плотным решателем мост `4<=|j|<=139` и закрыл остаток при `|j|>=140`
коэрцитивной оценкой. Отрицательных внутренних мод не осталось; открыта
только точная континуальная величина внутренней щели.

## Следующий вопрос

Построить прямой конечный мост по `|j|` и аналитическую коэрцитивную оценку
остатка для всех трёх скрученных характеров.

## Связи

- [[version6-bosonic-defect-full-tensor-stationary-twisted-spectrum-gate]]
- [[version6-bosonic-defect-full-tensor-high-angular-coercivity-gate]]
- [[version6-bosonic-defect-full-tensor-stationary-background-gate]]
- [[version6-bosonic-defect-polar-high-angular-coercivity-gate]]
- [[vortex-collective-coordinate-zero-mode-literature-2026]]
- [[version6-matter-birth-program]]

## Исходные материалы

- `s2t/gates/version6_bosonic_defect_full_tensor_translation_calibration_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_full_tensor_translation_calibration_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_full_tensor_translation_calibration_gate_results.json`