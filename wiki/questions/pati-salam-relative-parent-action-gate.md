# Pati-Salam Relative Parent-Action Gate

> Status: working
> Research status: conditional pass
> Type: question
> Updated: 2026-08-14

## Result

The graph height generates a circle action with trace-preserving conditional
expectation `E_h` onto the block-diagonal fixed-point algebra. Eliminating a
fixed-point auxiliary curvature gives
`inf_C ||F-C||^2=||F-E_h(F)||^2`.

For even curvature `F=D_Delta^2`, this quotient norm equals
`||[h,F]/2||^2=4 det(Delta Delta^dagger)`. With overall relative-sector
weight `lambda_rel`, stability requires `lambda_rel>1/2`; one copy gives
`lambda_rel=1` and signature `(7,9,0)`.

## Verdict

The projector and internal normalization are fixed. The remaining question
is the carrier status, multiplicity and overall trace weight.

## Source Notes

- `s2t/gates/version4_pati_salam_relative_parent_action_gate.tex`
- `s2t/audits/s2t_v4_pati_salam_relative_parent_action_gate.py`
- `s2t/results/s2t_v4_pati_salam_relative_parent_action_gate_results.json`
- arXiv:1607.07143; arXiv:1710.02409; arXiv:1104.5199.