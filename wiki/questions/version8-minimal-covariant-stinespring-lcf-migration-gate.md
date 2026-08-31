# Точная LCF-проверка минимальной Stinespring-дилатации

> Status: mature
> Type: question
> Updated: 2026-08-29

## Summary

Одношаговый cross-arrow канал перенесён из численного аудита в точный LCF-
слой. Окно `0<=p<=1/6`, Kraus/Choi-ранг `13`, инвариантность endpoint-
алгебры и калибровочная ковариантность теперь имеют символьные сертификаты.
Непрерывное физическое время по-прежнему не выведено.

## Problem

Отделить строгую конечномерную дилатацию от численных невязок и от ещё не
полученного автономного непрерывного шумового процесса.

## Search for solution

- Двенадцать jump-операторов восстановлены как точные SymPy-матрицы.
- Вычислены `Tr(Da Db)=2 delta_ab` и точный спектр `G=sum Da²`.
- В eDSL добавлен тип `KrausChannel`, который нельзя создать без точной
  Kraus-полноты.
- На `p=1/12` проверены прямая и двойственная полнота и все `221` endpoint-
  единицы.
- Символически доказаны внутренний ранг `13`, минимальность среды,
  ковариантность и GKSL-тангенс.
- Предъявлен точный контрпример закону конечной полугруппы.

## Expected result

Минимальный одношаговый носитель должен быть получен без нового физического
мультиплета, а параметр шага не должен автоматически превращаться во время.

## Compliance check

- `Spec(G)={0^9,1^6,2^3,3^2,6}` и `0<=p<=1/6` — точно.
- Kraus/Choi-ранг и минимальная размерность среды равны `13`.
- Среда: `C|0> direct_sum E_cross^C`.
- Endpoint-алгебра инвариантна на полном базисе.
- `K0'(0)=-G/2`; тангенс является исходным GKSL-генератором.
- `Phi_(1/50) o Phi_(3/100) != Phi_(1/20)` точно.

## Links

- [[version8-minimal-covariant-stinespring-carrier-gate]]
- [[version8-cross-arrow-covariance-lcf-migration-gate]]
- [[version8-intrinsic-noise-clock-dilation-gate]]
- [[version8-lcf-proofdsl-architecture-gate]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version8_minimal_covariant_stinespring_lcf_migration_gate.tex`
- `s2t/audits/s2t_v8_minimal_covariant_stinespring_lcf_migration_gate.py`
- `s2t/results/s2t_v8_minimal_covariant_stinespring_lcf_migration_gate_results.json`
- `s2t/proofdsl/channel.py`
- `s2t/proofdsl/examples/version8_stinespring.py`