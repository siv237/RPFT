# Эйлеров цикл, перестановочная сшивка и изотопия узла

> Status: working
> Type: source
> Updated: 2026-08-21

## Краткий вывод

Локальное равенство числа входов и выходов необходимо для непрерывного
потока, но не гарантирует единственную глобальную компоненту. Для
детерминированной сшивки конечного набора проходов требуются биекция и
один цикл перестановки. Сохранение типа узла требует отдельного запрета
разрезания, склейки и прохождения нити через саму себя.

## Первичные источники

- L. Euler, *Solutio problematis ad geometriam situs pertinentis*,
  Commentarii Academiae Scientiarum Imperialis Petropolitanae 8 (1741),
  128–140 — исходная постановка обхода всех рёбер и условий замкнутого
  маршрута.
- G. Birkhoff, *Tres observaciones sobre el algebra lineal*, Universidad
  Nacional de Tucumán, Revista, Serie A 5 (1946), 147–151 — разложение
  сохраняющих поток стохастических правил по перестановочным каналам.
- K. Reidemeister, *Elementare Begründung der Knotentheorie*,
  Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 5
  (1927), 24–32 — локальные движения, сохраняющие тип узла без разрезания
  и склейки.

## Значение для проекта

Текущие поля `Q` и `T` задают локальные моменты проходов, но не матрицу их
сшивки. Унитарность сохраняет норму, а топологический заряд — сектор, но
ни одно из этих условий не выделяет одну циклическую компоненту.

Перебор четырёх меток показывает, что правильная тетраэдральная группа
`A4` не содержит четырёхцикла. Поэтому следующий допустимый маршрут —
подвеска уже существующего фазового `C4` над тетраэдральными проходами.

## Связи

- [[version6-single-thread-global-cycle-sewing-gate]]
- [[version6-single-thread-connectivity-weighted-moment-parent-gate]]
- [[version5-order-four-resonant-loop-transport-gate]]
- [[version5-local-defect-transfer-operator-gate]]

## Исходные материалы

- `s2t/gates/version6_single_thread_global_cycle_sewing_gate.tex`
- `s2t/audits/s2t_v6_single_thread_global_cycle_sewing_gate.py`
- `s2t/results/s2t_v6_single_thread_global_cycle_sewing_gate_results.json`
