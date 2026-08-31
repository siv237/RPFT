# Область действия электромагнитного зарядового тождества

> Status: mature
> Type: question
> Updated: 2026-08-30

## Итог

Тождество `A+C=Q_tot^2` подтверждено точно на всех 216 трёхкварковых
состояниях. На эпсилон-секторе оно даёт рисунок `(4,1,0,1)`.

Однако это алгебраическое тождество, а не вывод электромагнитной энергии.
Общий перестановочно-инвариантный оператор имеет вид
`H=(mu A+lambda C)/T` и сворачивается к `Q_tot^2/T` только в специальной
точке `mu=lambda=1`.

## Знак

Для протона и нейтрона

`E_n-E_p=-(mu+2lambda)/(3T)`.

Поэтому знак отрицателен на положительном электростатическом конусе, но не
является теоремой о полной разности масс: пространственные, дипольные и
магнитные члены в оператор не включены.

## Статус

- Зарядовое тождество: принято.
- Следовая норма `T`: принята как безразмерная норма.
- Универсальная электромагнитная формула энергии: отклонена.
- Физический знак полной разности масс: не выведен.

## Связи

- [[version8-baryon-common-environment-correlation-origin-gate]]
- [[version8-canonical-noise-frame-common-trace-gate]]
- [[version8-baryon-material-merge-review]]
- [[global-formula-atlas]]

## Исходники

- `s2t/gates/version8_baryon_em_total_charge_identity_scope_gate.tex`
- `s2t/audits/s2t_v8_baryon_em_total_charge_identity_scope_gate.py`
- `s2t/results/s2t_v8_baryon_em_total_charge_identity_scope_gate_results.json`