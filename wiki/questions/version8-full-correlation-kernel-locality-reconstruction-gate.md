# Полное корреляционное ядро и возврат конечной локальности

> Status: mature
> Type: question
> Updated: 2026-08-28

## Summary

Inverse-spectral no-go Тома V остаётся верным для спектра и тепловых
следов, но не покрывает полный оператор корреляций в заданной алгебре
наблюдаемых. На той же коспектральной паре матричный логарифм полного ядра
точно возвращает генератор и различает связную и несвязную геометрии.

## Key Points

- Для `K_1,4` и `C4 + point` генераторы `H=3I-A` имеют общий спектр
  `(1,3,3,3,5)` и одинаковые скалярные спектральные функционалы.
- Полные ядра `C_tau=exp(-tau H)` различны даже с точностью до перестановки
  минимальных проекторов диагональной алгебры `C^5`.
- Формула `H=-log(C_tau)/tau` восстанавливает генератор с ошибкой меньше
  `2e-13`; отрицательная внедиагональная опора возвращает смежность.
- Для одной опоры неизвестный положительный масштаб `tau` не мешает:
  он лишь перемасштабирует генератор.
- Результат не предполагает полный спектральный тройной набор, но
  предполагает алгебру различимых наблюдаемых. Её происхождение пока не
  выведено.
- Пропущенный объект ранней программы — не «ещё один спектр», а пара
  `(observable algebra, full positive semigroup kernel)`.

## Links

- [[version5-reduction-triangle-cocycle-gate]] — исходный inverse-spectral
  запрет и та же конечная пара.
- [[spectral-correlational-source]] — ранняя гипотеза общего источника.
- [[full-heat-kernel-diffusion-geometry-reconstruction-2026]] —
  литературная граница восстановления геометрии из диффузии.
- [[version8-moving-kernel-second-fundamental-form-gate]] — закрытая
  локальная пространственная зацепка, после которой выполнена археология.

## Source Notes

- `s2t/gates/version8_full_correlation_kernel_locality_reconstruction_gate.tex`
- `s2t/audits/s2t_v8_full_correlation_kernel_locality_reconstruction_gate.py`
- `s2t/results/s2t_v8_full_correlation_kernel_locality_reconstruction_gate_results.json`
- `s2t/docs/toe_ugsm_common_shadow_bridge.tex`
- `s2t/gates/version5_reduction_triangle_cocycle_gate.tex`