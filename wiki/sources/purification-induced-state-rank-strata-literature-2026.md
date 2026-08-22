# Очищение, индуцированное состояние и ранговые страты

> Status: working
> Type: source
> Updated: 2026-08-19

## Summary

Матрица амплитуд `B` канонически задаёт нормированное состояние
`rho=B B*/Tr(B B*)`. Левый и правый редуцированные квадраты имеют
одинаковые ненулевые собственные значения. Ранг состояния равен рангу
амплитуды, а пространство матриц плотности естественно стратифицировано
по рангу.

При случайной или равномерной мере на амплитудах индуцированная мера на
состояниях имеет Wishart-тип. Такая мера обычно поддерживает полный ранг;
чистые состояния требуют ограничения размерности окружения или явного
рангового условия.

## Primary Sources

- A. Uhlmann, *The transition probability in the state space of a
  *-algebra*, Rep. Math. Phys. 9 (1976) 273 — амплитуды и очищения
  состояний.
- K. Życzkowski, H.-J. Sommers, *Induced measures in the space of mixed
  quantum states*, `arXiv:quant-ph/0012101` — редуцированные состояния,
  индуцированные меры и нормированные Wishart-матрицы.
- D. Viennot, *Purification of quantum states and gauge structures*,
  `arXiv:1508.02279` — геометрия очищений и стратификация пространства
  матриц плотности.
- I. Bengtsson, K. Życzkowski, *Geometry of Quantum States*, Cambridge
  University Press, 2006 — геометрия орбит фиксированного ранга.

## Project Consequence

Отождествление `R=B^T B/Tr(B^T B)` устраняет невозможную комбинацию
чистого состояния с произвольным полноранговым поперечным блоком. Однако
трёхмерная амплитуда допускает ранги 1, 2 и 3; стандартная индуцированная
мера не выбирает чистую страту. Поэтому purification-кинематика решает
коэрцитивность, но не выводит материальный сектор.

## Links

- [[version6-self-consistent-state-bridge-purification-gate]]
- [[version6-real-qutrit-purification-transition-gate]]
- [[polar-wishart-bv-measure-literature-2026]]
- [[modular-kms-state-boundary-literature-2026]]

## Source Notes

- Литературная проверка выполнена 2026-08-19 по первичным источникам.