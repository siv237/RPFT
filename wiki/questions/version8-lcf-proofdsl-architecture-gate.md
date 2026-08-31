# LCF-ядро строгой типизации и шаблон машинного гейта

> Status: mature
> Type: question
> Updated: 2026-08-30

## Summary

В архитектуру проекта введён исполняемый шаблон `GateSpec`: гейт получает
статус `lcf-checked` только после возврата настоящего `Theorem` каждым
обязательством. Проверены двадцать три результата: no-go коннектора `21 -> 20`,
спинодальный порог `21/2`, неподвижная алгебра `C^2`, linking-GKSL с
`dim Fix=41`, gauge-twirl Kraus-мост, его parent-action и полярная
cross-ковариация, минимальная Stinespring-дилатация и безразмерное шумовое
время, полный примитивный Markov-генератор, KMS-no-go, history/clock-
граница, микроскопический interaction-Hamiltonian, следово-двойственный
cross-rate селектор, no-go его происхождения из старого parent-action и
точный no-go абсолютного масштаба времени полного 42-jump процесса и
Toeplitz-конвейер свежих 43-мерных ancilla.

## Problem

Превратить первый proof eDSL из одиночного примера в повторно используемый
механизм проверки проектных гейтов.

## Search for solution

- Добавлены обязательства, спецификация гейта, агрегатор и JSON-сертификат.
- Созданы реестр, CLI и копируемый шаблон миграции.
- Перенесены теория представлений Тома VIII и независимое точное
  дифференциальное утверждение.
- Добавлены негативные контроли незаконных состояний.

## Expected result

Ни булево значение, ни численное приближение, ни ответ внешнего решателя не
должны самостоятельно повышаться до статуса теоремы.

## Compliance check

- Зарегистрированных результатов: `26`.
- Обязательств: `165`.
- Негативных контролей: `5/5`.
- Тестов пакета: `33 passed`.
- No-go: `dim Hom_G=13`, `max rank=9<20`.
- Спинодальный порог: точно `beta=21/2`.
- Неподвижная алгебра: точно `13 -> 2`, проекторы `12+9`.
- Linking-QMS: `441` trace-тестов, `221` corner-тест, `dim Fix=41`.
- Gauge-twirl: `12` jump-направлений, `12` gauge-генераторов, линейное
  ядро `0`, центральное ядро `1` при всех положительных скоростях.
- Parent-action: гессиан `7 I12/18`, сигнатуры сохраняются для всех
  неотрицательных весов, древесные Kraus-веса при `z=0` равны нулю.
- Cross-ковариация: точное поле степени 6, шесть одинаковых положительных
  пар, нулевой блок `12x15` и общая ось при всех `eta>0`.
- Stinespring: `0<=p<=1/6`, Kraus/Choi-ранг `13`, `221` endpoint-проверка,
  точный GKSL-тангенс и точный no-go конечной полугруппы.
- Noise clock: полный спектр размерности `221`, ядро `46`, щель `1/2`,
  модульный no-go и точный collision-limit.
- Full QMS: `25` jump-операторов, `Fix=C I21`, примитивность для всего
  положительного конуса и no-go следового выбора весов.
- KMS: единственная плотность `I21/21`, transfer-следы `13,6,6` и условное
  отношение `exp(-beta_Delta)` без выбранного разрыва.
- History-мост: clock-срезы `0,1,2` точно дают `Phi_*^n`; дополнение полного
  унитария имеет размерность `252`.
- Clock-unitary: ковариантное `U(1)`-семейство сохраняет канал; после
  Real-чётной редукции остаются `z=±1`.
- Z3 отсутствует и не входит в доверенную границу.

## Links

- [[lcf-proof-edsl]]
- [[formal-verification-and-palomar-roadmap]]
- [[version8-bimodule-common-curvature-relative-weight-gate]]
- [[version8-markov-fixed-algebra-lcf-migration-gate]]
- [[version8-linking-qms-gksl-lcf-migration-gate]]
- [[version8-gauge-twirl-kraus-lcf-migration-gate]]
- [[version8-kraus-bridge-parent-action-lcf-migration-gate]]
- [[version8-cross-arrow-covariance-lcf-migration-gate]]
- [[version8-minimal-covariant-stinespring-lcf-migration-gate]]
- [[version8-intrinsic-noise-clock-lcf-migration-gate]]
- [[version8-full-primitive-markov-generator-lcf-migration-gate]]
- [[version8-page-wootters-stinespring-history-gate]]
- [[version8-canonical-autonomous-clock-unitary-extension-no-go-gate]]
- [[version8-microscopic-repeated-interaction-hamiltonian-gate]]
- [[version8-trace-dual-cross-interaction-selector-gate]]
- [[version8-metric-dual-environment-parent-action-origin-gate]]
- [[version8-full-noise-cotangent-carrier-admission-gate]]
- [[version8-full-noise-trace-frame-metric-gate]]
- [[version8-full-noise-42-jump-gksl-fixed-algebra-gate]]
- [[version8-full-noise-repeated-interaction-hamiltonian-gate]]
- [[version8-full-noise-physical-time-scale-no-go-gate]]
- [[version8-full-noise-toeplitz-ancilla-chain-dilation-gate]]

## Source Notes

- `s2t/gates/version8_lcf_proofdsl_architecture_gate.tex`
- `s2t/audits/s2t_v8_lcf_proofdsl_architecture_gate.py`
- `s2t/results/s2t_v8_lcf_proofdsl_architecture_gate_results.json`
- `s2t/proofdsl/templates/gate_template.py`
- `s2t/proofdsl/registry.py`
- `s2t/proofdsl/verify.py`