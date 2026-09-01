# Минимальный Stückelberg shift-parent

> Status: mature
> Type: question
> Updated: 2026-09-01

## Problem

Построить nontrivial bounded parent с rank-ten shift orbit и проверить,
сохраняется ли требуемый ghost logdet после quotient reduction.

## Search for solution

- Введены две even copies `E_x,E_y`, total dimension `20`.
- Gauge transformation: `x->x+epsilon`, `y->y+epsilon`.
- Invariant combination `z=x-y` и parent
  `S=(x-y)^T D_aux (x-y)/2`.
- Hessian имеет rank/nullity `10/10`; kernel совпадает с gauge orbit.
- Gauge condition `F=D_aux x` даёт FP determinant
  `det R_theta det R_kappa`.
- Проверены quotient dimension и combined boson/ghost determinant.

## Expected result

Stückelberg parent должен дать настоящую gauge orbit без spectator flatness;
одновременно требуется отсутствие новых quotient modes и сохранение target
logdet.

## Compliance check

- Gauge architecture `10/10`, nontrivial rank-ten orbit `1/1`.
- Isotropic Hessian spectrum `{0^(10),2^(10)}`.
- Gauge-invariant quotient dimension `10`.
- Complex boson factor `1/det D_aux` отменяет ghost factor
  `det D_aux`; combined factor `1`.
- No-new-quotient-modes `0/1`, uncancelled logdet `0/1`.
- ProofDSL `10/10`, registry `55/432`.
- Physical four-slot parent остаётся `0/1`.
- Следующий гейт:
  `version9_endpoint_creation_kms_logdet_physical_fermion_loop_parent_origin_gate`.

## Links

- [[version9-endpoint-creation-kms-logdet-brst-shift-symmetry-parent-origin-gate]]
- [[kms-stueckelberg-shift-parent-sources-2026]]
- [[lcf-proof-edsl]]

## Source Notes

- `s2t/gates/version9_endpoint_creation_kms_logdet_minimal_stueckelberg_shift_parent_architecture_gate.tex`
- `s2t/audits/s2t_v9_endpoint_creation_kms_logdet_minimal_stueckelberg_shift_parent_architecture_gate.py`
- `s2t/results/s2t_v9_endpoint_creation_kms_logdet_minimal_stueckelberg_shift_parent_architecture_gate_results.json`
- `s2t/proofdsl/examples/version9_kms_minimal_stueckelberg_shift_parent.py`