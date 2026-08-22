# Том VI: скрученный спектр полного стационарного вихря

> Status: stale
> Type: question
> Updated: 2026-08-20

## Краткий вывод

На полном стационарном фоне `(K,a,b,q)` найдены две сопряжённые отрицательные
пары в нетривиальных характерах остаточной `Z3`.

- основной экстраполированный кандидат: `-0.02386058`;
- второй кандидат: `-0.01112057`;
- сопряжённые сектора совпадают с остатком `1.77e-11`;
- эрмитов остаток не превышает `2.21e-14`.

Отрицательные уровни усиливаются при сгущении сетки и не были сняты
стационаризацией поля `Q`.

## Последующий результат

[[version6-bosonic-defect-full-tensor-translation-calibration-gate]] выявил
несогласованный знак материального члена фоновой калибровки. После его
исправления перенос сошёлся к нулю, а обе отрицательные пары поднялись до
`3.68989479` и `3.72136029`. Поэтому вывод этой страницы сохраняется только
как историческая диагностика некалиброванного оператора.

## Историческая незакрытая калибровка

Переносный блок `c=0`, `j=±1` остаётся положительным. Его уровни на сетках
`70,100,140,200,280` равны
`0.00996187, 0.00802057, 0.00715253, 0.00669883, 0.00648619`, а формальная
экстраполяция даёт `0.00626629` вместо точного нуля.

На момент этого расчёта отрицательная пара считалась сильным кандидатом, но
не физическим сертификатом. Последующий гейт выполнил требуемую калибровку и
снял этот кандидат.

## Исторически следующий вопрос

Этот вопрос закрыт страницей
[[version6-bosonic-defect-full-tensor-translation-calibration-gate]].

## Связи

- [[version6-bosonic-defect-full-tensor-stationary-background-gate]]
- [[version6-bosonic-defect-full-tensor-translation-calibration-gate]]
- [[version6-bosonic-defect-full-tensor-polar-hessian-gate]]
- [[version6-bosonic-defect-polar-angular-sturm-liouville-gate]]
- [[version6-matter-birth-program]]

## Исходные материалы

- `s2t/gates/version6_bosonic_defect_full_tensor_stationary_twisted_spectrum_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_full_tensor_stationary_twisted_spectrum_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_full_tensor_stationary_twisted_spectrum_gate_results.json`