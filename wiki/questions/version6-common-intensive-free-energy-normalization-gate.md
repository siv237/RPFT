# Version VI: единая интенсивная нормировка свободной энергии

> Status: working
> Type: question
> Updated: 2026-08-19

## Summary

Проверены все естественные способы превратить обычный пфаффиановый
показатель `15` в интенсивный вес `1/20` без выборочной подгонки.

- Общее деление всей эффективной энергии на `300` не меняет знак
  гессиана: вакуум остаётся устойчивым после включения полного пфаффиана.
- В большеразмерном интенсивном пределе один коллективный мостовой цикл
  подавляется как `1/300`, а фермионный вклад имеет кратность `15/300`.
  Итоговая кривизна равна `5763/2240>0`.
- Отрицательная мода сохраняется только если делить на `300` один
  фермионный член, оставляя мостовой детерминант ненормированным. Это
  запрещённая секторная нормировка.

## Main Result

Для восстановления неустойчивости в едином интенсивном пределе
потребовалось бы не менее 276 независимых копий мостового поля. В проекте
имеется одна общая матрица `B`; кратность представления не создаёт новых
интегрируемых коллективных полей.

Стандартная детерминантная ветвь насыщения закрыта. Это не опровергает
фазовую картину мира-кристалла, но требует другого стабилизатора.

## Next Test

Тест выполнен в
[[version6-nongaussian-spatial-stiffness-saturation-gate]]. Производная
жёсткость не видит однородную долину потери ранга и потому не насыщает
рождение фазы. Она сохраняется только как возможный стабилизатор размера
уже созданного дефекта.

## Links

- [[version6-product-ko2-family-pfaffian-operator-gate]]
- [[version6-nongaussian-spatial-stiffness-saturation-gate]]
- [[large-rank-intensive-effective-action-literature-2026]]
- [[version6-state-weighted-bridge-nonperturbative-saturation-gate]]
- [[version5-spatial-extension-derrick-balance-gate]]
- [[version5-superconnection-skyrme-coefficient-gate]]
- [[version6-matter-birth-program]]

## Source Notes

- `s2t/gates/version6_common_intensive_free_energy_normalization_gate.tex`
- `s2t/audits/s2t_v6_common_intensive_free_energy_normalization_gate.py`
- `s2t/results/s2t_v6_common_intensive_free_energy_normalization_gate_results.json`