# Version VI: идентификация бозонного дефектного поля

> Status: working
> Type: question
> Updated: 2026-08-20

## Summary

После закрытия spin-cover fermion-ветви точно идентифицирован строгий
остаток: `Q` — лоренц-скалярная внутренняя пятёрка `SO(3)fam` и singlet
`(1,1,0)` калибровочной группы Стандартной модели.

## Results

- семейный Casimir равен `j(j+1)=6`, то есть `j=2`;
- все коммутаторы `Q tensor I15` с двенадцатью SM-генераторами равны нулю;
- линейный `SO(3)`-инвариант отсутствует из-за `Tr Q=0`;
- портал `Tr(Q^2) H†H` разрешён, но его коэффициент не выведен;
- прямая фермионная связь имеет не менее пяти независимых видовых
  коэффициентов и не выбрана родителем;
- `P(n)=P(-n)`, поэтому знак ориентированного заряда не принадлежит
  непомеченному полю `Q`;
- электрический, цветовой, слабый, барионный и лептонный заряды не
  получены;
- WZW/Pfaffian-фаза полной Real-пары равна `+1`, фермионная статистика не
  выведена.

## Verdict

Текущий материальный объект — нейтральный бозонный топологический кандидат
семейного скрытого сектора, а не установленная частица Стандартной модели.
Следующий тест должен квантовать его коллективные координаты и проверить
возможные ограничения Финкельштейна--Рубинштейна.

Тест выполнен: ориентационный ротор ненормируем, dyon-фаза отсутствует,
а минимальное коллективное квантование даёт спин ноль. См.
[[version6-bosonic-defect-collective-quantization-gate]].

## Links

- [[version6-two-copy-spin-cover-multiplicity-gate]]
- [[bosonic-projective-defect-identification-literature-2026]]
- [[version6-projective-order-parameter-field-spectrum-gate]]
- [[version6-gauged-projective-spin-cover-parent-gate]]
- [[version5-eta-wzw-real-pair-phase-gate]]
- [[version6-matter-birth-program]]
- [[version6-bosonic-defect-collective-quantization-gate]]

## Source Notes

- `s2t/gates/version6_bosonic_defect_field_identification_gate.tex`
- `s2t/audits/s2t_v6_bosonic_defect_field_identification_gate.py`
- `s2t/results/s2t_v6_bosonic_defect_field_identification_gate_results.json`