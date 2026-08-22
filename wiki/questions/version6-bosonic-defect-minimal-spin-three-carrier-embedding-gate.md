# Том VI: минимальное встраивание носителя спина три

> Status: working
> Type: question
> Updated: 2026-08-20

## Summary

Семикомпонентное тетраэдрическое поле канонически реализуется как
единственная часть спина три в `Hom(V1,V2)`, где `V1` — семейный триплет,
а `V2=Sym0^2(V1)` — уже существующая пятёрка параметра `Q`.
Квадрат соответствующей стрелки на триплетном углу точно воспроизводит
матричную кривизну `mu_T`.

## Carrier Pass

- `V2 tensor V1=V1+V2+V3`;
- казимир имеет спектр `2^3,6^5,12^7`;
- проектор `(C-2)(C-6)/60` имеет ранг семь;
- отображение симметричного бесследового тензора в матрицу `5x3`
  изометрично;
- новая калибровочная группа не требуется.

## Curvature Pass

Для стрелки `Z_T:V1 -> V2` выполнено

`Z_T^* Z_T = A(T)`,

поэтому триплетный угол равен

`Z_T^* Z_T-(v_T^2/3)I3=mu_T`.

На тетраэдрическом вакууме кривизна обращается в нуль, гессиан имеет три
орбитальных нуля и четыре положительные моды, а нормированный след на
`H45` совпадает с триплетным следом.

## Literal Block Failure

Самосопряжённый блок на `V1+V2` имеет размер восемь и ранг шесть. Из-за
прямоугольности `5x3` в пятёрке остаётся двумерное коядро. После усиления
физическим пакетом оно даёт тридцать нулевых направлений. Кроме того,
`Z_T Z_T^*` имеет два нулевых собственных значения, поэтому полный
двухугловой квадрат не может иметь нулевой изотропный вакуум.

## Verdict

Связанный бозонный носитель спина три и нужный угол кривизны получены.
Буквальное конечное дираковское встраивание закрыто. Следующий гейт должен
вывести односторонний угол из уже существующего коммутирующего квадрата,
градуировки или условного ожидания, а не вставлять его вручную.

Следующий гейт:
`version6_bosonic_defect_spin_three_corner_curvature_parent_gate`.

## Subsequent Result

[[version6-bosonic-defect-spin-three-corner-curvature-parent-gate]]
вывел нужный угол из модулярной высоты и единственного следа связывающего
контейнера. Два коядровых нуля не входят в физический спектр ветви
соответствия. При этом буквальная дираковская интерпретация не
переоткрывается, а полная контейнерная `M3` не калибруется.

## Links

- [[version6-bosonic-defect-tetrahedral-gauge-frame-branch-decision-gate]]
- [[spin-three-clebsch-gordan-carrier-literature-2026]]
- [[version6-bosonic-defect-tetrahedral-gauge-mass-parent-gate]]
- [[version5-commuting-square-readout-gate]]
- [[version5-graded-correspondence-superconnection-gate]]
- [[version6-matter-birth-program]]
- [[hilbert-module-modular-corner-curvature-literature-2026]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_minimal_spin_three_carrier_embedding_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_minimal_spin_three_carrier_embedding_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_minimal_spin_three_carrier_embedding_gate_results.json`
