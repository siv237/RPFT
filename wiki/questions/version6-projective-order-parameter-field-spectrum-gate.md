# Version VI: поле проекторного параметра порядка

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Переход к полям начат без нового постулата. Первое выведенное бозонное
поле — `Q(x)=R(x)-I3/3`, вещественная симметричная бесследовая матрица с
пятью локальными компонентами.

## Field Spectrum

На ordered-фоне при `beta_c=1.542669540860...`:

- спектр `R*=(0.9121666003...,0.04391669984...,0.04391669984...)`;
- вакуумная орбита `SO(3)/O(2)=RP2`;
- одна амплитудная мода с кривизной `4.5081528...`;
- две вырожденные двухосные моды с кривизной `17.8845270...`;
- две директорные моды Голдстоуна с нулевой кривизной.

## Matter Candidates

Топология `RP2` даёт:

- `pi1=Z2` — линейные дисклинации;
- `pi2=Z` — точечные ежи;
- `pi3=Z` — хопфовы текстуры.

Это первые строгие кандидаты на материю как дефекты поля порядка. Пока не
доказаны их конечная энергия, радиус, статистика и соответствие
наблюдаемым частицам.

## Boundary

Две нулевые директорные моды ещё не являются калибровочными бозонами.
Нужно вывести локальную `SO(3)`-связность и физический quotient. Для
частиц необходимо вернуть пространственную жёсткость, баланс Деррика,
spin-cover и спектр фермионных нулевых мод.

## Next Test — completed

Энергетический тест выполнен в
[[version6-spatial-projective-defect-energy-spectrum-gate]]. Прямая линия
логарифмически нелокальна, глобальный ёж линейно расходится, а хопфова
текстура требует положительного баланса `E2+E4`. Классы `+15/-15`
сохраняются у ежа, но конечная энергия требует gauge-завершения.

Последующая цепочка вывела составную конечную связность, закрыла
spin-cover fermion-carrier и идентифицировала строгий остаток как
SM-нейтральное бозонное поле семейного spin `j=2`. См.
[[version6-bosonic-defect-field-identification-gate]].

## Links

- [[version6-two-copy-affine-dilation-gate]]
- [[projective-order-parameter-fields-and-defects-literature-2026]]
- [[version5-projective-hedgehog-point-defect-gate]]
- [[version5-hopf-twisted-defect-superconnection-energy-index-gate]]
- [[version6-nongaussian-spatial-stiffness-saturation-gate]]
- [[version6-matter-birth-program]]
- [[version6-spatial-projective-defect-energy-spectrum-gate]]
- [[version6-bosonic-defect-field-identification-gate]]

## Source Notes

- `s2t/gates/version6_projective_order_parameter_field_spectrum_gate.tex`
- `s2t/audits/s2t_v6_projective_order_parameter_field_spectrum_gate.py`
- `s2t/results/s2t_v6_projective_order_parameter_field_spectrum_gate_results.json`