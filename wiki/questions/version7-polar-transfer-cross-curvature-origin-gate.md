# Version VII: смешанная полярно-передаточная кривизна

> Status: mature
> Type: question
> Updated: 2026-08-28

## Problem

Наследуемая метрика двух согласованных Gram-углов сохраняет полный вес и
проваливает селективный запуск. Нужно заменить вопрос о ручной половине
вопросом о канонической кривизне связывающего бимодуля.

## Search for Solution

Для полярной коизометрии `U:C11 -> C10` построена кривизна
`R_U=C_t U-U C_s`. Знак минус фиксирован правым правилом Лейбница.
Переплетение фоновых Gram-операторов даёт `R_U(0)=0`, а переменная часть
начинается квадратично. Поэтому квадрат `R_U` имеет нулевой гессиан в
начале. В целевом вакууме его линеаризация даёт положительную
полуопределённую добавку ранга `22`.

Самосопряжённое завершение удовлетворяет
`1/4 ||[[0,R_U],[R_U*,0]]||² = 1/2 ||R_U||²`. Эта половина удаляет две
ориентации одного внедиагонального блока и не является секторным весом.

## Expected Result

- Нулевой гессиан имеет сигнатуру `(7,0,20)` и тяжёлую щель `18/5`.
- Целевой вакуум имеет сигнатуру `(0,0,27)` и минимальную моду
  `3.9368554658...`.
- Ручной вес `beta=1/2` для запуска больше не требуется.
- Знак суммы `C_t U+U C_s` даёт провал `(27,0,0)`.
- Количественная нормировка масс ещё не выведена.

Следующий гейт должен собрать рёберную Hodge-кривизну и `R_U` в одной
Real-связывающей суперсвязности с единым следом.

## Links

- [[version7-index-defect-reduced-linking-quotient-gate]]
- [[version7-incidence-transfer-markov-weight-gate]]
- [[version5-morita-linking-parent-gate]]
- [[version6-spectral-transition-morita-two-step-connector-gate]]
- [[version7-real-linking-superconnection-assembly-gate]]

## Source Notes

- `s2t/gates/version7_polar_transfer_cross_curvature_origin_gate.tex`
- `s2t/audits/s2t_v7_polar_transfer_cross_curvature_origin_gate.py`
- `s2t/results/s2t_v7_polar_transfer_cross_curvature_origin_gate_results.json`
