# B-L Root Condensate Consistency Gate

> Status: working
> Research status: промежуточный результат; заменён трилеммой root--mass--condensate
> Type: question
> Updated: 2026-08-06

## Supersession

Этот этап проверял только голономию самого поля спаривания. Последующий аудит `root-mass-condensate-trilemma-gate` показал, что торсионная скрутка переносит знак в отображение Юкавы и не является полным решением.

## Question

Can the order-four sterile B-L root holonomy coexist with a nonzero ordinary charge-two pairing condensate on the entire core complement?

## Results

- The complement is a solid torus with generator `y` and core meridian `mu=2y`.
- Sterile holonomy `+i` on `y` makes an ordinary charge-minus-two scalar see holonomy `-1`.
- A nonzero covariantly constant ordinary scalar therefore cannot exist globally on the complement, although its meridian holonomy is trivial.
- A charge-two VEV leaves only `Z2`; a charge-four VEV preserves the order-four element but does not allow a linear `Phi N_c N_c` coupling.
- Twisting the charge-minus-two pairing field by the existing ambient torsion line multiplies the two minus signs to `+1` and restores a globally compatible section.

## Verdict

The simple B-L Higgs interpretation is rejected. The twisted bundle solves only the condensate-holonomy subproblem and is superseded as a complete rescue by the later trilemma.

## Evidence

- `s2t/audits/s2t_bl_root_condensate_consistency_audit.py`
- `s2t/results/s2t_bl_root_condensate_consistency_results.json`
- `s2t/gates/bl_root_condensate_consistency_gate.tex`