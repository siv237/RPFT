# KMS-канал выхода и граница детального баланса

> Status: working
> Type: question
> Updated: 2026-09-02

## Вопрос

Можно ли реализовать спектральную выходную долю `R_out=1/6` как точный
полностью положительный KMS-совместимый канал с ненулевым стационарным током?

## Результат

Построен двухуровневый Kraus-канал с `p_down=1/6` и `p_up=1/12`.
Отношение `p_up/p_down=1/2=exp(-log2)`, а состояние
`rho_KMS=diag(2/3,1/3)` стационарно. Потеря чистого возбуждённого состояния
точно равна `1/6`.

Однако в Gibbs-состоянии прямой и обратный потоки совпадают:
`J_down=J_up=1/18`, поэтому `J_net=0`. При нулевой температуре обратный
переход исчезает и остаётся выход `1/6`, но стационарным становится чистый
вакуум, а не верное конечное KMS-состояние.

## Статус

- условная архитектура: `10/10`;
- условное замыкание: `8/8`;
- точный CPTP KMS-канал: `1/1`;
- стационарный сквозной ток: `0/1`;
- происхождение привода и ванн: `0/2`;
- абсолютный масштаб: `0/1`;
- ProofDSL: `26/26`, registry `98/1150`.

Следующий вопрос — может ли двухрезервуарный неравновесный родитель создать
ненулевой стационарный ток без ручной подстановки его величины.

## Связи

- Предшественник: [[version10-cell-birth-four-volume-induced-newton-breathing-anomaly-k43-output-density-morphism-origin-gate]].
- Формулы: [[global-formula-atlas]].
- Реестр: [[global-theorem-and-no-go-ledger]].
- Исходники: `s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate.tex`, `s2t/audits/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate.py`, `s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_k43_kms_output_channel_parent_origin_gate_results.json`.