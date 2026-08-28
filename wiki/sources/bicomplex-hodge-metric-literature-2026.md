# Бикомплексы, полная степень и зависимость Hodge-метрики

> Status: working
> Type: source
> Updated: 2026-08-28

## Summary

Первичная литература подтверждает ключевое различие текущего гейта:
двойной комплекс задаётся bigrading и двумя антикоммутирующими
дифференциалами, тогда как сопряжённые операторы, лапласианы и Hodge-звезда
требуют отдельно выбранной эрмитовой метрики. Поэтому total-degree сам по
себе не является теоремой единственности относительной нормы.

## Key Points

- Структурная теорема Йонаса Штельцига описывает конечные двойные комплексы
  алгебраически через квадраты и зигзаги. В эту классификацию не входит
  канонический положительный вес направлений.
- Тардини и Томассини явно рассматривают параметризованные комбинации
  дифференциалов, квадрат которых равен нулю. Hodge-лапласиан вводится после
  отдельной фиксации эрмитовой метрики.
- Поповичи, Штельциг и Угарте также формулируют метрические условия только
  после выбора эрмитовой метрики. Это подтверждает, что bigrading и метрика
  являются различными входами.
- Литература поддерживает no-go общей схемы, но не содержит проектного
  утверждения о дефекте `54-42=12`. Связь этого дефекта с `E_aff` является
  новой локальной гипотезой проекта.

Последующий аудит закрыл эту локальную гипотезу. Число `42` относится к
полному трёхступенному контейнеру, но кривизна нулевая на его средней
21-мерной ступени. Минимальная endpoint-опора имеет размерность `21`, а
нулевое дополнение может произвольно менять полную размерность, не меняя
след. Поэтому совпадение `54-42=12` не является инвариантом двойного
комплекса или конечной спектральной тройки.

## Project Reading

Явный квадратный контроль проекта показывает

```text
d_h²=d_v²=d_h d_v+d_v d_h=0
```

после любого перескалирования `d_v -> c d_v`. Одновременно семейство
`G_eta=P_E+eta P_L` совместимо с полной степенью, Real-сопряжением и
подходящей изометрической Hodge-инволюцией. Поэтому значение `eta=1` нельзя
приписывать одной структуре бикомплекса.

## Links

- [[version7-bicomplex-total-degree-hodge-metric-gate]]
- [[version7-affine-defect-bicomplex-completion-gate]]
- [[version7-minimal-curvature-support-trace-gate]]
- [[version7-common-chain-number-hodge-relative-trace-gate]]
- [[clifford-form-degree-normalization-literature-2026]]
- [[polar-transfer-linking-expectation-literature-2026]]

## Source Notes

- J. Stelzig, “On the Structure of Double Complexes”, J. London Math. Soc.
  104 (2021), 956–988; arXiv:1812.00865.
- N. Tardini, A. Tomassini, “Differential operators on almost-Hermitian
  manifolds and harmonic forms”, Complex Manifolds 7 (2020), 106–128;
  arXiv:1909.06569.
- D. Popovici, J. Stelzig, L. Ugarte, “Higher-Page Bott–Chern and Aeppli
  Cohomologies and Applications”, J. Reine Angew. Math. 777 (2021),
  157–194; arXiv:2007.03320.
- `s2t/gates/version7_bicomplex_total_degree_hodge_metric_gate.tex`
- `s2t/results/s2t_v7_bicomplex_total_degree_hodge_metric_gate_results.json`