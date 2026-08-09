# Kappa Cas One Over 24

> Status: working
> Type: question
> Updated: 2026-07-09

## Question

Is the Tome II coefficient `kappa_Cas = 1/24` a strict spectral consequence of the compact QED/Maxwell--ghost sector on `RP^3 x S^1`, or is it a conditional value that depends on the chosen zeta-determinant scheme, spin structure, zero-mode handling, and subtraction convention?

## TeX Integration

- `tome2_s2t_spectral_closure.tex` now includes the dedicated section `Проверка коэффициента kappa_Cas = 1/24`.
- The section turns this page from an external wiki warning into an explicit internal checkpoint of Tome II.

## Current Answer

The current research status is conditional success. The value `1/24` is strongly supported by the one-dimensional zeta/Casimir residue and by a KK prototype, but the strict RPFT source itself warns that an unconditional first-principles claim may be too strong. Therefore `1/24` should be treated as the main proof risk inside the otherwise strong `S_vac` electromagnetic block.

## Successes

- The Abel/heat-kernel check converges to `-zeta_R(-1)/2 = 1/24`.
- A direct quick reproduction gives `0.041666658333334656` at Abel regulator `t = 0.002`, within about `8.33e-9` of `1/24`.
- The KK gauge prototype on `RP^3 x S^1` gives `0.04166667555480416`, within about `8.89e-9` of `1/24` for the tested truncation.
- Removing the `lambda_RP3 = 0` scalar KK level leaves only the small massive residual `8.88813749e-9`, so the dominant contribution is exactly the constant scalar KK row expected in the Maxwell--ghost combination.
- The `log(mu)` ambiguity appears reduced on the product background because local conformal-anomaly terms and determinant zero-mode shifts are argued to cancel in the relevant operator combination.

## Failures And Risks

- The result is not yet an unconditional theorem: it depends on a fixed zeta-determinant scheme and finite subtraction convention.
- The spin-structure choice is delicate. Tome II uses the antiperiodic branch for several `S^1` residues, while the strict RPFT QED discussion distinguishes spatial KK periodic spin structure from thermal/KMS antiperiodic structure.
- Zero-mode treatment is essential: the result depends on using `det'` and retaining the nonzero KK row above the `RP^3` scalar constant mode.
- The QED operator combination must be exactly Maxwell--ghost/Hodge as assumed; a different operator package could shift the finite determinant constant.
- The small massive residual is numerically tiny in the prototype, but the proof still needs a clean analytic statement showing why it is negligible, cancelled, or outside the normalized finite part.

## Expected Result

If this coefficient is closed, the `S_vac` block can be promoted from strong conditional success to mature spectral closure. If the coefficient remains scheme-dependent, then Tome II should keep `S_vac` as a numerically excellent but conditional closure claim.

## Compliance Check

- Checked source: `RPFT-main/rigorous/30_qed_one_loop_proof.md` explicitly lists what still needs proof for `kappa_Cas = 1/24`.
- Checked prototype: formulas from `RPFT-main/rigorous/02_zeta_compute.py` reproduce `1/24` to roughly `1e-8` in a quick focused run.
- Checked Tome II: `tome2_s2t_spectral_closure.tex` now treats `1/24` as a conditional coefficient and includes a protocol for closing the `kappa_Cas` no-go.

## Next Research Steps

1. Decide and document whether the EM/QED `S^1` branch in Tome II is spatial periodic, antiperiodic, or sector-dependent.
2. Write the analytic decomposition of Maxwell--ghost determinants into the scalar `lambda_RP3 = 0` KK row plus massive residual.
3. Prove whether the massive residual cancels, is exponentially suppressed under the accepted normalization, or must be retained.
4. Run an alternative-regularization comparison to test whether `1/24` is stable without fitting `S_vac` after the fact.

## Links

- [[tome2-svac-em-block-audit]] — broader audit where this coefficient is the main risk.
- [[tome2-proof-chain]] — proof-chain page that flags this as a conditional node.
- [[tome2-s2t-spectral-closure]] — source page for Tome II claims.
- [[s2t-closure-roadmap]] — global closure status map.

## Source Notes

- Source paths: `RPFT-main/rigorous/30_qed_one_loop_proof.md`, `RPFT-main/rigorous/02_zeta_compute.py`, `tome2_s2t_spectral_closure.tex`.
- Quick reproduction command used an inline Python extraction of the Abel and KK formulas from `02_zeta_compute.py`; no project source files were modified by the calculation.

## 2026-07-10 Coexact-Tower Complication

The `1/24` question is now separated from the full EM determinant question. The periodic scalar/constant branch still supports `kappa_Cas = -zeta_R(-1)/2 = 1/24`, but the full coexact Maxwell tower adds a finite nonlocal Bessel issue tracked in [[coexact-tower-delta]].

Current audit results:

- `T_coex^RP3 = 1.5227161455271536e-05` in the unit-radius projected coexact tower.
- The dominant `n=1` coexact mode survives the `RP^3` parity projection.
- Local heat-kernel subtraction and `det'` zero-mode handling do not by themselves remove this finite positive tail.
- The old Maxwell--ghost--Dirac wording does not provide a naive level-by-level cancellation; diagnostic Dirac towers require non-natural prefactors.

Implication: closing `kappa_Cas = 1/24` is necessary but no longer sufficient for full EM closure. A mature result also needs either a derived paired sector or a normalized formula for `Delta_tower^coex`.
