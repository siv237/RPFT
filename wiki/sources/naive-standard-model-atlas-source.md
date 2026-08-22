# Наивный атлас Стандартной модели

> Status: working
> Type: source
> Updated: 2026-08-19

## Summary

Архивный `atlas.md` и связанные `standart_model*.md` фиксируют раннюю
фазу проекта, когда массы, связи и космологические доли подбирались как
короткие выражения из `pi`, `S_vac`, массы электрона и массы протона.
Тексты содержат несколько очень точных и простых совпадений, но также
чрезмерные заявления `FINAL VERIFIED`, смешение базовых величин с
предсказаниями и заметный дрейф формул между версиями.

## Preserved Short Formulas

Особый интерес сохраняют строки:

- `alpha_s=1/(6+pi^2/4)`;
- `sin^2(thetaW)=(8-3/(4pi))/(21+4pi)`;
- `mb/mp=pi+4/3`;
- `(ms/mp)^-1=pi^2+1/3`;
- `md/me=pi^2-1`, `mu/me=pi+1`;
- `(mtau/mmu)_core=pi^2+2pi+2/3`;
- `Vcb=1/(24-pi^-1)`;
- `OmegaLambda=1-pi^-1`, `OmegaDM=pi^-1-(2pi^2)^-1`,
  `OmegaB=(2pi^2)^-1`.

Предыдущие аудиты установили общую Laurent-алгебру
`Z[1/24][Pi,Pi^-1]`, коллективную компрессию одиннадцати строк и точную
SU(5)-rank реконструкцию коэффициентов gauge-формул. Но общий selector и
родительское действие не были выведены.

## New Reading

Том VI независимо получил точный контрольный спектр
`(2/3,1/6,1/6)`. Это позволяет читать часть дробей атласа как спектр и
щель параметра порядка. Подробный результат сохранён в
[[atlas-projective-order-parameter-bridge]] и
[[version6-naive-atlas-order-parameter-rank-bridge-gate]].

## Source Notes

- `архив-2025-2026/2026-02-проработка/Проработка/atlas.md`
- `архив-2025-2026/2026-02-проработка/Проработка/standart_model.md`
- `архив-2025-2026/2026-02-проработка/Проработка/standart_model2.md`
- `архив-2025-2026/2025-12-истоки/base/26-stparam.md`
- `s2t/results/s2t_rpft_pi_atlas_results.json`
- `s2t/results/s2t_collective_pi_atlas_base_results.json`
- `s2t/results/s2t_pi_spectral_address_operator_results.json`
- `s2t/results/s2t_su5_rank_selector_results.json`

## Links

- [[pi-spectral-address-operator-gate]]
- [[collective-pi-atlas-base-gate]]
- [[su5-rank-selector-gate]]
- [[atlas-projective-order-parameter-bridge]]