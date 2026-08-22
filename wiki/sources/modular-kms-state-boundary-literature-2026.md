# Модулярные, КМС- и информационные веса у границы состояний

> Status: working
> Type: source
> Updated: 2026-08-19

## Summary

Для верной матрицы плотности `rho` конечномерный модулярный оператор
действует как `Delta_rho(X)=rho X rho^{-1}`. Обратная матрица поэтому
входит в модулярную кинематику. Однако стандартные GNS-, KMS- и
монотонные информационные метрики образуют целое семейство конструкций;
само существование `Delta_rho` не выбирает энергетический потенциал
`Tr(rho^{-1}X*X)`.

При потере ранга модулярный оператор становится сингулярным, а некоторые
информационные метрики или относительные энтропии расходятся. Такие
сингулярности могут ограничивать пространство верных состояний, но их
использование как физического объёмного потенциала требует отдельного
принципа.

## Primary Sources

- R. Longo, *The emergence of time*, `arXiv:1910.13926` — модулярный
  поток, связанный с верным нормальным состоянием.
- D. Petz, *Introduction to quantum Fisher information*,
  `arXiv:1008.2417` — монотонные квантовые метрики и ковариации.
- D. Petz, *From f-divergence to quantum quasi-entropies and their use*,
  `arXiv:0909.3647` — относительные энтропии и квазииэнтропии.
- F. M. Ciaglia et al., *Monotone metric tensors in Quantum Information
  Geometry*, `arXiv:2203.10857` — геометрия многообразия верных матриц
  плотности.
- D. Šafránek, *Discontinuities of the quantum Fisher information and
  the Bures metric*, `arXiv:1906.06185` — особенности при изменении ранга
  статистической модели.

## Project Consequence

Том V использует `rho_beta` для ориентации модулярных частот, но
кривизновое действие нормирует обычным матричным следом. Поэтому
`R^{-1}` нельзя без нового постулата переносить из модулярного оператора в
энергию моста. Каноническая относительная энтропия к `I3/3` даёт барьер
`1/3`, который стабилизирует изотропное состояние и закрывает
самозапуск.

## Links

- [[version6-modular-dual-weight-bridge-coercivity-gate]]
- [[version5-modular-commutant-parent-correspondence-gate]]
- [[relational-modular-internal-time-literature-2026]]
- [[version6-real-qutrit-purification-transition-gate]]

## Source Notes

- Литературная проверка выполнена 2026-08-19 по первичным источникам.