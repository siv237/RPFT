# GNVW/ALPU-барьер локальной генерации ancilla-сдвига

> Status: mature
> Type: source
> Updated: 2026-08-30

## Summary

Два первичных источника дают точный внешний контроль для главы Тома VIII.
GNVW-индекс одномерного QCA равен размерности клетки для одноклеточного
сдвига и единице для локально реализуемых автоматов. Расширение на ALPU
показывает, что конечновременная Hamiltonian-эволюция с Lieb--Robinson
локальностью имеет тривиальный индекс; трансляция с нетривиальным индексом
таким Hamiltonian не генерируется.

## Sources

- D. Gross, V. Nesme, H. Vogts, R. F. Werner, *Index theory of one
  dimensional quantum walks and cellular automata*, `arXiv:0910.3675`.
- D. Ranard, M. Walter, F. Witteveen, *A converse to Lieb--Robinson bounds
  in one dimension using index theory*, `arXiv:2012.00741`.

## Project consequence

Для клетки размерности `43` имеем `ind(S)=43`. Локальный system--cell
collision является конечным дефектом с индексом `1`, поэтому полный шаг
`V=S U_col` также имеет индекс `43`. Product-vacuum может иметь локальный
parent, но точный conveyor не может происходить из локального Hamiltonian-
пути от тождества.

## Links

- [[version8-vacuum-chain-parent-state-and-local-hamiltonian-origin-gate]]
- [[version8-full-noise-toeplitz-ancilla-chain-dilation-gate]]