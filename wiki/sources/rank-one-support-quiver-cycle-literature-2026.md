# Ранговые опоры матриц и циклическая динамика колчанов

> Status: working
> Type: source
> Updated: 2026-08-27

## Summary

Литература подтверждает разграничение, возникшее в Томе VII: условие малого
ранга задаётся определительными соотношениями и жёстко ограничивает рисунок
ненулевых элементов, тогда как выбор устойчивой циклической конфигурации
колчана относится к действию на всём пространстве его представлений.

## Primary Sources

- F. J. Király, L. Theran, R. Tomioka, *The Algebraic Combinatorial
  Approach for Low-Rank Matrix Completion*, `arXiv:1211.4116`: допустимость
  низкорангового заполнения зависит от комбинаторного рисунка известных
  матричных элементов и определительных соотношений.
- M. Tsakiris, *Results on the algebraic matroid of the determinantal
  variety*, `arXiv:2002.05082`: зависимости между матричными координатами
  кодируются алгебраическим матроидом определительного многообразия.
- M. Harada, G. Wilkin, *Morse theory of the moment map for representations
  of quivers*, `arXiv:0807.4734`: квадрат нормы отображения момента задаёт
  стратификацию и градиентную динамику на полном пространстве представлений
  колчана.

## Consequence for Tome VII

Опора ненулевой матрицы ранга один является декартовым произведением опор
левого и правого векторов. Поэтому маска

$$
\begin{pmatrix}1&0&1\\0&0&1\end{pmatrix}
$$

не может быть точной опорой ранга один: требуемый минор равен произведению
двух ненулевых амплитуд. Этот локальный определительный запрет нельзя снять
добавлением плоских переменных вне прямоугольника.

Следующий осмысленный класс моделей — действие на полном представлении
колчана с relations или циклической кривизной. Оно должно быть
предзарегистрировано до подстановки целевого шестирёберного цикла.

## Links

- [[version7-edge-coherence-full-graph-competition-gate]]
- [[version7-edge-coherence-field-space-superconnection-gate]]
- [[kernel-grassmannian-quiver-stability-literature-2026]]
- [[version7-four-vertex-vectorlike-selector-gate]]

## Source Notes

- `s2t/gates/version7_edge_coherence_full_graph_competition_gate.tex`
- `s2t/results/s2t_v7_edge_coherence_full_graph_competition_gate_results.json`