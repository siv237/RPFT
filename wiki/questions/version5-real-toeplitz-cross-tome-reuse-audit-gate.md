# Ретроспективный аудит обменного KO6-каркаса

> Status: mature
> Type: question
> Updated: 2026-08-17

## Summary

Перечтение доказанных блоков Томов III–V показало, что алгебраический
каркас обменной Real-формы уже многократно построен: две сопряжённые копии,
противоположные градуировки, обмен через `J` и точное правило
`J d J^-1 = d*`.

## Reusable Results

- Новое конечномерное KO6-удвоение не требуется.
- Полный след и Pfaffian-сокращение не являются вычислением `KO6`-класса.
- `J` не выбирает ориентацию; она должна приходить из `L/L*` и символов
  Тёплица `z/z^-1`.
- Аффинная KO6-цепь уже даёт точный конечномерный образ обмена
  `d <-> d*`.

## Negative Controls

- Все старые KO6-модули конечномерны и потому не дают ненулевой
  фредгольмов индекс.
- Архивная строгая RPFT-попытка `theta:0->pi` сама получает нулевой
  спектральный поток и нулевой индекс семейства.
- Добавлять Clifford-стабилизацию как новые физические состояния нельзя.

## Verdict

Следующий гейт сужен. Сначала нужно вычислить отображение
`KO6(C_R) -> K0(C direct_sum C)`. Последующий гейт получил точную формулу
`c6(n)=(-n,n)`, поэтому умножение на проектор ранга 15 действительно даёт
пару `(-15,+15)` и доказывает вещественный класс 15.

## Links

- [[version5-real-toeplitz-kr-classification-gate]]
- [[version3-real-bimodule-square-gate]]
- [[version3-orbit-measure-pfaffian-gate]]
- [[version4-pfaffian-eta-orientation-gate]]
- [[version5-oriented-height-hodge-ko6-gate]]
- [[version5-affine-ko6-reference-corner-gate]]
- [[version5-real-toeplitz-bott-comparison-map-gate]]

## Source Notes

- `s2t/gates/version5_real_toeplitz_cross_tome_reuse_audit_gate.tex`
- `s2t/audits/s2t_v5_real_toeplitz_cross_tome_reuse_audit_gate.py`
- `s2t/results/s2t_v5_real_toeplitz_cross_tome_reuse_audit_gate_results.json`
- `архив-2025-2026/2025-12..2026-01-строгость/rigorous/21_pi_coefficient_derivation.md`
- `архив-2025-2026/2025-12..2026-01-строгость/rigorous/22_spectral_flow_derivation.py`