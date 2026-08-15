# Pati-Salam BV Multiplicity Fork Gate

> Status: architecture fork
> Type: question
> Updated: 2026-08-14

## Result

The chain `4bar -> 2_R -> 4` is not a submodule of the standard KO6
Pati-Salam fermionic space. Standard contractible BV gauge-fixing pairs
cannot change the classical vacuum or generate the determinant selector.

The physical vectorlike branch is anomaly-safe and shifts beta coefficients
by `(-2/3,0,-4/3)`, but misses the one-percent frozen-scale gate. The
non-propagating mapping-cone branch leaves running unchanged and gives
`lambda_rel=1` for one copy, whose multiplicity is not yet derived.

## Verdict

Choose one architecture branch, then compute its mixed Hessian and RG ledger.

## Source Notes

- `s2t/gates/version4_pati_salam_bv_multiplicity_fork_gate.tex`
- `s2t/audits/s2t_v4_pati_salam_bv_multiplicity_fork_gate.py`
- `s2t/results/s2t_v4_pati_salam_bv_multiplicity_fork_gate_results.json`