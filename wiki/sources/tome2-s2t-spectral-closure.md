# Tome 2 S2T Spectral Closure

> Status: working
> Type: source
> Updated: 2026-07-09

## Summary

`s2t/docs/tome2_s2t_spectral_closure.tex` is the primary Tome II source for the S2T spectral-closure program. It fixes the allowed train inputs, compact carrier, normalization rules, no-go criteria, closed rows, and the remaining II.B tasks. Its central management value is that it separates successful closure claims from partial closures and explicitly forbids hiding open gaps inside numerical coincidences.

## Key Points

- Allowed train data are restricted to `alpha^{-1}`, `m_e`, and `m_mu`; all other quantities must be computed or used only for blind comparison.
- The working compact carrier is `K = RP^3 x S^1`, with `S^3 x S^1` used as the spinor cover or explicitly marked test geometry.
- The document now marks `S_geo` as the clean geometric result. `S_vac`, the tau relation, and the inherited absolute Higgs-scale bridge are conditional; `lambda_H` retains a separate spectral-normalization status.
- The neutrino sector is partial: the denominator `23 + pi^{-1}` is conditionally derived, but the Dirac insertion `m_D^(nu) = sqrt(pi + pi^{-1}) m_e^2 / m_mu` remains a II.B task.
- The unified parent-action gate is negative: the canonical metric preserves the neutrino denominator but does not preserve the raw tau seed or derive its loop coefficient.
- EW/QCD is partial: boundary normalizations, `v`, `lambda_H`, `M_H`, one-loop RG, and candidate `rho_S2T` are present, but GUT thresholds, KK tower structure, `Sigma_8/Sigma_3`, and two-loop RG remain open.
- The machine audit `s2t/audits/s2t_tome2_audit.py` reproduces the closed numerical rows into `s2t/results/s2t_tome2_results.json` and explicitly does not close EW/QCD thresholds or the neutrino Dirac insertion.

## Closure Register

- `K = RP^3 x S^1` — derived in the minimal class from the volume test `Z_A = pi^2`, phase step `pi`, and absence of continuous `U(1)` moduli.
- Spin shift `k + 1/2` — derived in the fermion sector from the antiperiodic spin structure on `S^1`.
- `pi` term in `S_geo` — derived in the EM sector from `Z_2` holonomy on the nontrivial flat branch of `RP^3`.
- `1/24` coefficient — conditionally derived in the EM sector from the finite part of the one-dimensional Maxwell--ghost branch; strict status requires fixing spin structure, `det'` handling, and finite subtraction scheme.
- `1/(pi^4 S^2)` term — derived from the fourth zeta residue and second-order scale suppression.
- QED shift `-alpha/3` — derived in the lepton sector from the finite part of a one-loop topological self-energy.
- Higgs bridge `v`, `lambda_H`, `M_H` — derived in the EFT sector without using `G_F`, `M_W`, `M_Z`, or `M_H` as inputs.
- `23 + pi^{-1}` neutrino denominator — conditionally derived from index count `24 - 1` and circle IR contribution; still needs full matrix phenomenology check.
- Neutrino Dirac insertion — II.B task, tracked in [[neutrino-overlap-lemma]].
- EW/QCD thresholds — II.B task, tracked in [[ew-qcd-threshold-closure]].

## Numerical Audit

- Train inputs: `alpha^{-1} = 137.035999177`, `m_e = 0.51099895069 MeV`, `m_mu = 105.6583755 MeV`.
- Closed rows: `S_geo = 137.036303775878`, `S_vac = 137.035999173522`, `m_tau = 1776.859428563 MeV`, `v_S2T = 245.993409261 GeV`, `lambda_H = 0.129221715985`, `M_H = 125.056486039 GeV`.
- Residuals: `S_vac - alpha^{-1} = -3.48e-9`; tau relative error is `-3.22e-7` against the control value.
- Open rows in the summary table include `sin^2 theta_W(M_Z)`, `alpha_s(M_Z)`, `M_W`, and `M_Z` because threshold closure is not yet derived.
- Conditional rows include neutrino mass splittings because their absolute scale still depends on the unclosed Dirac insertion.

## Source Update: Kappa_Cas Subsection

- The TeX source now contains a dedicated section `Проверка коэффициента kappa_Cas = 1/24`.
- This section defines the working `kappa_Cas` scheme, identifies the scalar `lambda_RP3 = 0` KK row as the dominant one-dimensional branch, records the quick numerical KK control, and lists the protocol needed for mature EM status.
- The document therefore no longer merely demotes `1/24`; it now contains an internal research program for closing or demoting the coefficient.

## Source Update: 1/24 Conditionalization

- The TeX source was updated so `S_vac` is no longer presented as an unconditional mature success.
- The coefficient `1/24` is now explicitly treated as a conditional EM-sector result depending on `kappa_Cas`, spin-structure choice, `det'` zero-mode handling, and finite subtraction scheme.
- The conclusion now lists three II.B tasks: close `kappa_Cas = 1/24`, build the EW/QCD threshold model, and derive the neutrino Dirac insertion.

## No-Go Criteria

- Any continuous coefficient introduced after inspecting blind observables and not derived from spectrum, normalization, topology, or EFT demotes the result to phenomenological fitting.
- If `S_vac`, `m_tau`, or the Higgs EFT bridge requires a hidden continuous parameter, that sector loses closure status.
- For the partial neutrino and EW/QCD blocks, no-go means the block remains II.B until the missing insertion or threshold model is derived.
- A physical unification claim additionally requires one prior action to pass at least two independent normalization-sensitive sectors; the current minimal action passes only the neutrino stiffness gate.

## Links

- [[tome2-proof-chain]] — proof-chain synthesis extracted from this source.
- [[tome2-svac-em-block-audit]] — focused audit of the `S_vac` electromagnetic closure claim.
- [[s2t-reinterpretation]] — concept page for the S2T layer.
- [[s2t-closure-roadmap]] — status map updated from this source.
- [[numerical-audits]] — JSON audit layer that reproduces the closed rows.
- [[neutrino-overlap-lemma]] — open II.B task for the neutrino Dirac insertion.
- [[ew-qcd-threshold-closure]] — open II.B task for threshold closure.
- [[holonomy-and-dirac-sectors]] — audit layer relevant to spin shift, holonomy, and overlap claims.

## Source Notes

- Source path: `s2t/docs/tome2_s2t_spectral_closure.tex`.
- Companion paths: `s2t/docs/technical_s2t_analysis.tex`, `s2t/audits/s2t_tome2_audit.py`, `s2t/results/s2t_tome2_results.json`.
- Ingested on 2026-07-09 at source-summary level; line-by-line proof extraction from the strict derivation sections remains a future pass.