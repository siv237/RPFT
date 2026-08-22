# Том VI: допустимость характерного C4-селектора компакттона

> Status: working
> Type: question
> Updated: 2026-08-21

## Problem

Проверено, может ли уже существующий четырёхтактный характер выделить
компакттонные ветви `±i`, а аффинный сток — превратить это выделение в
динамический захват без ручного проектора или нового резервуара.

## Search for solution

Редуцированный компакттонный шаг разложен по характерам `±i`. Затем
перебраны все `24` аффинные перестановки, все шесть четырёхциклов и три
подгруппы `C4`; вычислены полный коммутант и коммутант на `P3`-триплете.
Отдельно проверена минимальная когерентная связь со стоком.

## Expected result

Положительный результат требовал одновременно канонического назначения
`C4` аффинному носителю и эволюции, уменьшающей смесь двух характеров до
одной Real-сопряжённой ветви.

## Compliance check

- на точном компакттонном многообразии построен
  `D_chi=1-|<Psi,F(Psi)>|^2=4*w_+*w_-`;
- его нуль состоит ровно из состояний `F Psi=±i Psi`;
- условие также фиксирует равные узловые нормы, фазу `±pi/2` и
  коллинеарность внутренних векторов;
- выбранный четырёхцикл разлагает аффинный `P3` на `i,-1,-i`;
- в полном `S4` имеются шесть ориентированных четырёхциклов и три разные
  подгруппы `C4`, поэтому выбор не каноничен;
- коммутант полного аффинного триплета одномерен, так что связь `rho V`
  остаётся изотропной;
- любая линейная `C4`-эквивариантная унитарная динамика сохраняет веса
  `w_±` и сам `D_chi`;
- конечный когерентный сток рекуррентен, а не контрактен;
- точный селектор найден, но trigger, скорость и захват не выведены.

## Verdict

Зацепка сохраняется как коэффициент-свободный диагностический функционал
для будущей открытой модели. В неизменённом родителе она не становится
механизмом рождения: для этого пришлось бы вручную выбрать
`S4 -> C4` и добавить диссипативную или измерительную динамику.

## Следующий гейт

[[version6-spectral-transition-discrete-compacton-c4-boundary-eta-dissipation-gate]]
проверяет усиленную гипотезу с явной `S4→C4`-границей и слабой
эта/Pfaffian-диссипацией. После неё статус ветви замораживается.

## Links

- [[version6-spectral-transition-discrete-compacton-dynamical-capture-gate]]
- [[version6-existing-multiplicity-resonant-sink-gate]]
- [[version6-single-thread-global-cycle-sewing-gate]]
- [[version5-transition-primitive-scientific-language-gate]]
- [[version6-matter-birth-program]]
- [[version6-spectral-transition-discrete-compacton-c4-boundary-eta-dissipation-gate]]

## Source Notes

- `s2t/gates/version6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.tex`
- `s2t/audits/s2t_v6_spectral_transition_compacton_c4_affine_selector_admissibility_gate.py`
- `s2t/results/s2t_v6_spectral_transition_compacton_c4_affine_selector_admissibility_gate_results.json`