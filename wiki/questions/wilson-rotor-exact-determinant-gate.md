# Wilson Rotor Exact Determinant Gate
> Status: working
> Type: question
> Updated: 2026-08-15

## Result

The full weight determinant rejects the previous `2 V_(1/2) + 3 V_(3/2)`
completion. Its charge planes have multiplicities `q=1:5` and `q=3:3`,
producing an extra angle-dependent term `2 log|1+2 cos(theta)|`.

The simple exact logarithmic pattern is eight equal unit-charge real planes,
corresponding to four complex `SU2` doublets of real dimension 16.

## Remaining Mismatch

With the same normalized triplet trace, the inverse term requires mean charge
norm squared 6. Canonical axial and full doubled-Casimir norms give 1 and 3;
the latter produces inverse coefficient 4 instead of 8.

## Verdict

The Casimir-level candidate is closed as an exact determinant completion.
The fundamental-only candidate survives only if a doubled fixed-charge sector
is derived from the action.

## Evidence

- `s2t/audits/s2t_wilson_rotor_exact_determinant_audit.py`
- `s2t/results/s2t_wilson_rotor_exact_determinant_results.json`
- `s2t/gates/wilson_rotor_exact_determinant_gate.tex`