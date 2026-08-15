# Coexact Tower Delta

> Status: open
> Type: question
> Updated: 2026-07-14

## Question

Does the full coexact Maxwell tower on `RP^3 x S^1` vanish by a hidden paired mechanism, get absorbed into an already present `pi^-4 S_geo^-2` residue, or require an explicit correction `Delta_tower^coex` to `S_vac`?

## Current Result

The tower is not zero in the ordinary Maxwell--ghost/Hodge sector. A direct `RP^3` parity projection was implemented in `s2t/audits/s2t_coexact_tower_audit.py` and recorded in `s2t/results/s2t_coexact_tower_results.json`.

Key numbers:

- `T_coex^S3 = 1.531916808400627e-05`.
- `T_coex^RP3 = 1.5227161455271536e-05`.
- `T_coex^RP3 / T_coex^S3 = 0.9939940192424161`.
- The first surviving `RP^3` level contributes `0.9999756862947792` of the projected tower.

The `RP^3` quotient keeps odd coexact levels with full `S^3` multiplicity and projects out even levels. Since the dominant level is `n=1`, the projected tower is almost the same as the full `S^3` value rather than half of it.

## Rejected Shortcuts

- Simple half-projection is wrong for the finite Bessel tail because the dominant `n=1` level survives.
- Hodge cancellation only pairs exact one-forms with scalar ghosts; it does not remove coexact transverse modes.
- Local heat-kernel counterterms can remove local divergences but not the finite nonlocal winding/Bessel part.
- A radius rescue would require roughly `R1/R3 >= 1.285` to push `T_coex/S_geo` below the current `alpha^-1` residual, conflicting with the current `R=1` normalization unless independently derived.

## Live Leads

1. **Determinant normalization:** derive the precise sign and prefactor connecting `T_coex` to `Delta_tower^coex` in `S_vac`.
2. **Existing `pi^-4` residue:** check whether `1/(pi^4 S_geo^2)` is already an effective summary of the finite tower rather than an independent correction.
3. **Non-naive paired sector:** a special torsion/spin/Dirac companion could still work only if its squared spectrum matches `rho_n = n + 1` and gives opposite signed multiplicities without a fitted coefficient.

## Maxwell--Ghost--Dirac Check

The old Maxwell--ghost--Dirac trace was tested in `s2t_mgd_pairing_audit.py` with results in `s2t_mgd_pairing_results.json`.

Naive pairing fails:

- Coexact `RP^3` starts at `rho = 2` with degeneracy `6`.
- The round Dirac tower starts at `rho = 3/2` for periodic spinors, or uses a different shifted tower for antiperiodic-style tests.
- Cancellation would require coefficients `0.1473`, `0.07364`, `2.9797`, or `1.4899` depending on the diagnostic Dirac case, none of which is a natural ghost/topological factor.

Therefore the old Maxwell--ghost--Dirac wording remains useful for the full QED determinant and `zeta_tot(0)` scale-cancellation question, but it is not a ready-made cancellation of `Delta_tower^coex`.

## Source Notes

- `s2t/docs/tome2_s2t_spectral_closure.tex` — main text; now includes the coexact tower protocol and Maxwell--ghost--Dirac audit.
- `s2t/audits/s2t_coexact_tower_audit.py` and `s2t/results/s2t_coexact_tower_results.json` — `RP^3` coexact tower computation.
- `s2t_mgd_pairing_audit.py` and `s2t_mgd_pairing_results.json` — diagnostic Maxwell--ghost--Dirac pairing test.
- External references checked 2026-07-10: Ikeda--Yamamoto on three-dimensional lens-space spectra; Lauret / Lauret--Miatello--Rossetti on lens-space `p`-spectra via congruence lattices; Nash--O'Connor on determinants of Laplacians on lens spaces; Schwarz/Ray--Singer on gauge determinant and analytic torsion bookkeeping. See [[external-literature-spectral-determinants]].
- [[tome2-svac-em-block-audit]] — EM block audit consuming this result.
- [[kappa-cas-one-over-24]] — original `1/24` determinant proof-risk page.

## 2026-07-10 Literature Gate Update

The external literature check supports the conservative conclusion: the coexact sector is a real determinant sector to be treated with lens-space `p`-form technology, not a disposable artifact of the internal script.

However, the literature check does **not** yet prove the S2T absorption identity. In particular:

- lens-space spectra literature is the right place to verify `RP^3 = L(2,1)` exact/coexact multiplicities;
- determinant-on-lens-space literature is the right place to verify finite determinant normalization;
- analytic torsion/gauge-functional literature requires scalar ghosts, exact forms, coexact forms, and zero modes to be tracked together;
- no checked external source yet derives the S2T factor `1 - 10/(24 S_geo)` or the finite `P_0,2` trace rank inside the Maxwell--ghost determinant.

Updated status: the viable route remains absorption of the coexact finite tower into the existing `pi^-4` term, but this is a strong hypothesis rather than a literature-backed theorem until the `L(2,1)` `p`-form determinant calculation is written explicitly.

## 2026-07-10 Pi-Four Tower Hypothesis Audit

The most serious absorption hypothesis is now:

```text
1/(pi^4 S_geo^2)  ?=  (Vol(RP3)/2) * T_coex^RP3 / S_geo
                 =  (pi^2/2) * T_coex^RP3 / S_geo
```

This was tested in `s2t/audits/s2t_pi4_tower_hypothesis_audit.py` with results in `s2t/results/s2t_pi4_tower_hypothesis_results.json`.

Key numbers:

- `1/(pi^4 S_geo^2) = 5.466750295392699e-07`.
- `T_coex^RP3 / S_geo = 1.1111771870449321e-07`.
- Required direct prefactor: `4.919782694541265`, close to `pi^2/2 = 4.934802200544679`.
- Equivalently, with the bosonic `1/2 log det` factor exposed, required prefactor is `9.83956538908253`, close to `Vol(RP3) = pi^2 = 9.869604401089358`.
- The natural candidate `(pi^2/2) T/S` gives `5.483439627824377e-07`, overshooting the existing `pi^-4` term by `0.30528799615638967%`.

Interpretation: this is the strongest current lead. It suggests the `pi^-4` term may be a volume-weighted half-determinant summary of the finite coexact tower. However, it is not an exact identity at the current normalization: the residual is `1.6689332431677886e-09`, comparable to the present `alpha^-1` residual. A proof would need to derive the `Vol(RP3)` factor and explain the `0.305%` mismatch as either a legitimate local finite subtraction, a missing sector, or a sign/normalization convention.

## 2026-07-10 Residual Audit: Casimir-Mixing Lead

A follow-up residual audit in `s2t/audits/s2t_pi4_residual_audit.py` found a surprisingly strong candidate for the remaining `0.3053%` mismatch. The needed multiplier is:

```text
M_needed = 0.9969564117480219
epsilon_needed = 1 - M_needed = 0.0030435882519781465
```

The closest structurally meaningful candidate found is not `alpha/pi` but a Casimir-mixing factor:

```text
epsilon_CasMix = 10/(24 S_geo) = 0.003040556810026934
M_CasMix = 1 - 10/(24 S_geo)
```

Using it gives:

```text
(pi^2/2) * T_coex^RP3/S_geo * (1 - 10/(24 S_geo))
= 5.466766918121624e-07
```

versus

```text
1/(pi^4 S_geo^2) = 5.466750295392699e-07
```

The relative mismatch is only `3.04e-6` of the `pi^-4` term. This is much stronger than the raw `0.3053%` mismatch, but it introduces a new integer `10`. This is acceptable only if `10` can be derived as a multiplicity or cross-term coefficient, not fitted after the fact.

Current best formula-candidate:

```text
1/(pi^4 S_geo^2) ≈ (pi^2/2) * T_coex^RP3/S_geo * (1 - 10/(24 S_geo))
```

Status: strongest lead, not closed. The next proof target is to derive or reject the integer `10`.

## 2026-07-10 Integer 10 Origin Candidate

The integer `10` in the Casimir-mixing lead now has a concrete spectral candidate, tested in `s2t/audits/s2t_integer10_origin_audit.py` with results in `s2t/results/s2t_integer10_origin_results.json`.

On `RP^3`, scalar harmonics descending from `S^3` are even `ell`. The relevant early scalar/ghost shells are:

- `ell = 0`: constant scalar shell, degeneracy `1`; this is the branch behind the periodic `1/24` Casimir residue after removing only the true `(0,0)` zero mode.
- `ell = 2`: first nonzero even scalar shell, degeneracy `(2+1)^2 = 9`; exact one-form modes inherit this scalar spectrum.

Therefore:

```text
1 + 9 = 10
```

This gives a non-arbitrary source for the factor in

```text
1 - 10/(24 S_geo).
```

Numerically:

- `epsilon_needed = 0.0030435882519781465`.
- `10/(24S_geo) = 0.003040556810026934`.
- Relative error in epsilon: `-9.960092168322969e-04`.
- Resulting `pi^-4` term mismatch: `3.040696579678917e-06` relative to the target.

Status: upgraded from naked numerology to a concrete spectral candidate. Still not a proof: the second-order determinant expansion must show why the constant scalar branch and first even scalar/exact shell enter exactly as the multiplicity `10`, with the shown sign.


## 2026-07-10 Full Delta Audit

The script `s2t/audits/s2t_full_coexact_delta_audit.py` computed normalization variants for treating the coexact tower as an independent correction to the current `S_vac` formula.

Key results:

- `T_coex^RP3 = 1.5227161455271536e-05`.
- The first surviving transverse mode contributes `0.9999756863` of the tower.
- Adding even the smallest simple independent correction, `0.5*T_coex/S_geo`, worsens the current `alpha^-1` error by about `15x`.
- The volume-weighted half determinant with `P_0,2`/Casimir mixing is essentially the existing `pi^-4` term; if added again as an independent correction it worsens the fit by about `156x`.

Updated conclusion: the tower is real and nonzero, but it cannot be added on top of the current `pi^-4` term. The only viable closure route is an absorption scheme: prove that the existing `1/(pi^4 S_geo^2)` term is already the normalized coexact tower residue with `P_0,2` mixing. Otherwise `S_vac` remains a truncation/conditional determinant result.
## 2026-07-10 Lens P-Form Absorption Gate

The dedicated audit `s2t/audits/s2t_lens_pform_absorption_audit.py` tested the best current route:

```text
Delta_abs^P02 = (pi^2/2) * T_coex^RP3/S_geo * (1 - 10/(24 S_geo)).
```

Main numbers:

- `T_coex^RP3 = 1.5227161455e-05`.
- `N_need = 10.0099700224`.
- `N_P02 = dim Sym^2(R^4) = 10`.
- `P02` relative mismatch against `1/(pi^4 S_geo^2)` is `3.04e-6`.
- Including the next even scalar shell would give `1+9+25=35`, so the finite rank depends essentially on the first ambient-strain selection rule, not on generic scalar/exact inheritance.

Verdict: option A is the best route but not a theorem. The external lens-space literature validates the spectral/determinant framework; it does not supply the missing S2T mixed-trace derivation. Tome II should keep `S_vac` at conditional determinant success until the `L(2,1)` Maxwell--ghost mixed trace derives the volume factor, sign, `det'` convention, and rank-10 projector.
## 2026-07-10 Mixed-Trace Closure Matrix

The audit `s2t/audits/s2t_mixed_trace_closure_matrix.py` separates numerical support from theorem requirements.

Decision matrix:

- `C1`: lens-space `p`-form framework — pass as framework.
- `C2`: ordinary Hodge/ghost cancellation — fails as a full coexact cancellation.
- `C3`: `pi^2/2` volume-half normalization — numerically strong, not derived.
- `C4`: `P02` rank selection — conditional pass inside first ambient strain.
- `C5`: exact rank identity — fails as exact identity because `N_need=10.0099700224`, not exactly `10`.
- `C6`: Maxwell--ghost mixed trace — first blocking gap and the next real proof target.

Practical consequence: continue route A only by computing the explicit `L(2,1) x S^1` mixed trace with sign, volume factor, `det'` convention, zero modes, and finite `P02` rank. New numerical improvements around `N≈10` do not raise `S_vac` above conditional determinant success.
## 2026-07-10 C6 Operator-Trace Skeleton

The audit `s2t/audits/s2t_c6_operator_trace_skeleton.py` localizes the remaining C6 proof gap. It is no longer useful to search for new nearby integers; the missing work is an explicit second variation of the gauge-fixed Maxwell--ghost determinant under first ambient strain.

Operator blocks required by the absorption identity:

- coexact transverse Maxwell determinant supplies the nonzero `T_coex^RP3` tower;
- exact/longitudinal Maxwell and Faddeev--Popov scalar ghost implement ordinary Hodge cancellation and `det'` bookkeeping;
- periodic scalar/ghost branch supplies the already isolated `1/(24 S_geo)` Casimir factor;
- first ambient strain insertion supplies `P02` with `Tr P02 = 10`.

Conditional passes:

- `P02` rank `10` is representation-theoretically natural inside first ambient strain;
- `ell >= 4` is excluded inside II.A because it is a higher ambient strain sector, not because of an arbitrary scalar-shell cutoff.

Open C6 tests:

- derive the sign of the full Maxwell--ghost second variation, not just the formal `log det` sign;
- derive the volume normalization `Vol(RP3)/2 = pi^2/2` from normalized modes and measure;
- explain `N_need - Tr(P02) = 0.0099700224` as a finite scheme residue, a subleading determinant term, or a downgrade trigger.

Verdict: C6 is narrowed but not closed. The next proof attempt must compute `delta_g^2 Gamma_Maxwell+ghost |_{P02}`; otherwise `pi^-4` remains a strong structural compression rather than a mature theorem.
## 2026-07-10 P02 Volume-Normalization Audit

The audit `s2t/audits/s2t_p02_volume_normalization_audit.py` checks whether the prefactor `pi^2/2` is fitted or geometrically forced.

Result:

- Unit `S^3` has volume `2 pi^2`; `RP^3=S^3/Z2` has volume `pi^2`.
- For uniform `x in S^3 subset R^4`, the moments are `E[x_a x_b]=delta_ab/4` and `E[x_a x_b x_c x_d]=(delta_ab delta_cd + delta_ac delta_bd + delta_ad delta_bc)/24`.
- For `q_A=x^T A x`, the `RP^3` inner product is `Vol(RP3)*((Tr A)(Tr B)+2Tr(AB))/(4*6)`.
- This orthogonally splits `Sym^2(R4)=R I plus Sym^2_0(R4)`, giving rank `1+9=10`.
- Since `q_A` is even under `x -> -x`, it descends to `RP^3`; the bosonic determinant contributes the standard `1/2`, so the natural prefactor is `Vol(RP3)/2 = pi^2/2 = 4.9348022005`.

Verdict: the volume-factor subtest of C6 is conditionally passed. The condition is important: `T_coex^RP3` must be normalized as a determinant density over `RP^3`. This does not close C6 because the full Maxwell--ghost second-variation sign and the `N_need-10=0.0099700224` scheme gap remain open.
## 2026-07-10 C6 Second-Variation Sign Audit

The audit `s2t/audits/s2t_c6_second_variation_sign_audit.py` checks whether the sign in

```text
1 - Tr(P02)/(24 S_geo)
```

is compatible with a gauge-fixed determinant expansion.

Result:

- For a determinant block `c log det(A + eps B)`, ignoring or locally subtracting `delta^2 A` terms gives the quadratic trace-square term `-(c/2) Tr((A^-1 B)^2)`.
- For the real bosonic coexact Maxwell block, `c=1/2`, hence the trace-square sign is negative: `-1/4 Tr((A^-1 B)^2)`.
- The required factor is a suppression, `1 - 10/(24 S_geo) = 0.9969594432 < 1`, so the coexact bosonic sign has the correct direction.

Verdict: the sign subtest conditionally passes for the coexact bosonic block.

Caveats:

- A Faddeev--Popov ghost determinant has the opposite quadratic sign if the same `P02` insertion acts as an independent ghost trace-square.
- A true Laplacian variation contains `delta^2 Delta` terms; these must be local/subtracted or canceled in the same scheme.

Consequence: the next C6 proof must show that `P02` belongs to the coexact bosonic mixed block while the ghost/exact branch leaves only the finite `1/24` Casimir factor, and that `Tr(Delta^-1 delta^2 Delta)` does not add a finite nonlocal correction.
## 2026-07-10 C6 Ghost/Exact Isolation Audit

The audit `s2t/audits/s2t_c6_ghost_exact_isolation_audit.py` checks the main caveat left by the sign audit: whether the same `P02` trace-square leaks into the ghost determinant with the opposite Grassmann sign.

Scenarios:

- Desired route: `P02` is a coexact bosonic metric-strain insertion and does not appear as an independent ghost trace-square. Then the suppression factor remains `1 - 10/(24 S_geo) = 0.9969594432`.
- Failure route 1: the same `P02` appears in both coexact bosonic and ghost trace-squares. The opposite ghost sign cancels the suppression in the simplified sign model, giving `factor=1`.
- Failure route 2: ghost/exact leakage includes the ordinary scalar tower through `ell=4`, with rank `1+9+25=35`. Then the net factor is `1 - (10-35)/(24 S_geo) = 1.0076013920`, an enhancement rather than the required suppression.

Verdict: C6 now requires a precise isolation lemma. The ordinary exact/scalar ghost tower must cancel before the finite `P02` coexact trace is counted, and the constant scalar branch must enter only through the already isolated `kappa_Cas=1/24` finite factor. Without that lemma, the `P02` rank remains geometrically natural but not a determinant proof of the `pi^-4` term.
## 2026-07-13 Formal Gamma Maxwell-Ghost Decomposition

The audit `s2t/audits/s2t_c6_formal_gamma_audit.py` writes the formal C6 functional and classifies the requested proof obligations.

Working decomposition:

```text
Gamma_M+gh^(1)[g]
  = 1/2 log det' Delta_1,coex[g]
    + Gamma_exact[g]
    - log det' Delta_0[g]
    + Gamma_zero/gauge[g]
    + Gamma_local.counterterms[g].
```

Sector meaning:

- `Delta_1,coex` is the transverse/coexact Maxwell block and the source of the nonzero coexact tower.
- `Gamma_exact` is the longitudinal/exact gauge-fixed sector.
- `-log det' Delta_0` is the Faddeev--Popov scalar ghost.
- `Gamma_zero/gauge` handles gauge volume, the removed true scalar zero mode, and the absence of harmonic one-forms because `b1(RP3)=0`.
- `Gamma_local.counterterms` contains local heat-kernel subtractions.

Proof-obligation status:

- `P02` in coexact bosonic metric-strain insertion — conditional lemma: `P02=Sym^2(R4)=1+9` under first ambient strain.
- Exact/scalar ghost tower cancels before finite `P02` counting — required isolation lemma, not fully proven.
- Constant scalar branch enters only through `kappa_Cas=1/24` — conditional scheme statement with `det'` removing the true `(0,0)` mode.
- `delta^2 Delta` terms are local/subtracted/compensated — open required subtraction lemma.
- `N_need-10=0.0099700224` — downgrade trigger unless derived as finite scheme residue or subleading determinant contribution.

Verdict: the formal `Gamma_Maxwell+ghost[g]` decomposition can be written, and it makes C6 precise. It does not close C6 as a theorem. `S_vac` remains conditional determinant success until ghost isolation, `delta^2 Delta` locality/compensation, and the gap are resolved inside the same functional.

## 2026-07-14 L21 Quotient Normalization Update

The audit `s2t/audits/s2t_c6_l21_normalization_audit.py` fixes the quotient-normalization convention needed before evaluating the coexact mixed trace.

Result:

- For an antipodal-invariant coexact one-form normalized on `S3`, the descended raw norm on `L(2,1)` is smaller by `1/2`.
- The quotient-orthonormal representative is therefore multiplied by `sqrt(2)`.
- In bilinear matrix elements, the two external `sqrt(2)` factors cancel the quotient integral factor `1/2`, giving net cover factor `1`.
- The final coexact trace must not be globally multiplied by `2` or `1/2` once quotient-orthonormal states are used.
- Evaluating integrals on the cover does not restore projected-out even shells; the state space remains the `L(2,1)` state space.

Consequence: the next C6 calculation should compute `<n,i|delta_A Delta_1|m,j>` on invariant lifts with this normalization fixed. Any remaining discrepancy cannot be blamed on a global cover-volume factor.

## 2026-07-14 Shell-Selection Update

The audit `s2t/audits/s2t_c6_l21_shell_selection_audit.py` rules out a too-simple C6 rescue: `P_0,2` shell selection alone does not truncate the coexact tower.

Result:

- The quadratic insertion is even, so it preserves the `RP3/L(2,1)` parity sector.
- For surviving odd coexact shells, the necessary representation-level channels are `n -> n` and `n -> n±2`.
- Hence infinitely many odd-shell channels remain allowed before coefficient-level cancellations are considered.

Consequence: the open question becomes sharper. The remaining possible rescues are not “selection by parity” but one of: exact coefficient cancellation after the full one-form Laplacian variation, locality/subtraction of all tower channels, or a physical transverse quotient normalization that absorbs them without adding a fitted parameter.

## 2026-07-14 Coexact Locality Gate Update

The audit `s2t/audits/s2t_c6_l21_coexact_locality_gate_audit.py` rules out another over-simple rescue: not every allowed coexact shell channel can be declared local.

Result:

- UV/asymptotic pieces may be handled by predetermined local heat-kernel counterterms.
- Low-shell finite pieces and off-diagonal trace-square channels are global determinant data.
- Finite postfactum subtraction is forbidden unless derived from the already fixed normalization scheme.

Consequence: the coexact-tower question is now reduced to a finite-part problem. Either the finite nonlocal coexact mixed trace equals the existing `pi^-4` residue with `P_0,2` rank, or `S_vac` must retain conditional/structural-compression status.

## 2026-07-14 Low-Shell Block Specification

The audit `s2t/audits/s2t_c6_l21_low_shell_block_spec_audit.py` specifies the first finite block that must be computed to decide the coexact absorption route.

Minimum block:

- `M_11`: `6 x 6`, trace-square weight `1/16`.
- `M_13`: `6 x 30`, trace-square weight `1/64`.
- `M_31`: `30 x 6`, trace-square weight `1/64`.

This is `396` entries per deformation direction, or `3960` across the ten directions of `Sym^2(R4)` before exploiting symmetry.

Consequence: the coexact-tower problem is now operational. The next result must be a real vector-harmonic matrix-element calculation for the one-form operator, not another selection-rule audit.

## 2026-07-14 n=1 Killing-Overlap Update

The audit `s2t/audits/s2t_c6_l21_n1_killing_overlap_audit.py` gives the first concrete low-shell warning.

Result:

- The `n=1` coexact shell is the six-dimensional Killing-form shell.
- A traceless `P_0,2` deformation has nonzero diagonal overlap on this shell.
- The normalized overlap matrix has rank `4` and eigenvalues `-1/6,-1/6,0,0,1/6,1/6`.

Consequence: the `1 -> 1` channel is not symmetry-zero. If C6 survives, the cancellation must come from the full one-form Laplacian variation and coexact projection, not from parity or representation selection alone.

## 2026-07-14 n=1 Principal-Symbol Update

The audit `s2t/audits/s2t_c6_l21_n1_principal_symbol_audit.py` checks the first actual operator term on the `n=1` Killing shell.

Result:

- In the conformal slice `h=2qg`, the principal-symbol variation is `-4` times the nonzero `q_A` overlap matrix.
- The weighted trace-square of this principal piece is `1/9`.

Consequence: the obstruction is no longer only an overlap warning. A full C6 rescue must exhibit an explicit cancellation from the remaining one-form terms or an exact absorption identity for the finite part.

## 2026-07-14 n=1 Toy Trace-Square Update

The audit `s2t_c6_l21_n1_toy_tracesquare_audit.py` computes the diagnostic trace-square from the nonzero Killing overlap.

Result:

- `Tr(M^2)=1/9` for the traceless `P_0,2` test direction.
- Multiplying by `lambda_1^-2=1/16` gives `1/144`.

Consequence: the first shell gives a finite warning-scale response in the toy overlap model. The coexact route now depends on showing that the full `delta_A Delta_1` operator cancels or absorbs this response, not merely that representation selection is favorable.

## 2026-07-14 update: leakage into the cubic shell

The conformal `n=1 -> n=1` cancellation does not mean the perturbation vanishes. A new leakage audit shows zero projection back to the Killing shell, but a nonzero cubic tangent-polynomial image with normalized Gram trace `96` and eigenvalues `12,16,16,16,16,20`. Plainly: the first floor is quiet, but the signal has moved to the third floor. The next task is the actual coexact `n=3` projection and the second-order `1 <-> 3` determinant contribution.

## 2026-07-14 update: coexact gate is not yet passed

The cubic leakage audit has a new caution flag. The raw ambient image is nonzero and divergence-free, but it is not tangent: `x·V` has max coefficient `16`. Plainly: we see a strong third-floor shadow, but part of it points out of the building. Before calling it a physical coexact `n=3` contribution, the next step must remove the normal component by intrinsic tangent projection and only then test co-closedness and spectral projection.

## 2026-07-14 update: tangent projection leaves a signal

The normal part of the cubic leakage was removed on the unit sphere: the tangency norm becomes `0.0`. But the signal does not disappear. The tangent-projected Gram trace is `85.3333`, with eigenvalues `12,14.6667,14.6667,14.6667,14.6667,14.6667`. Plainly: after scraping off the outward shadow, there is still a real tangent pattern on the sphere. It is not yet a coexact determinant contribution, because the divergence/co-closed projection remains to be done.

## 2026-07-14 update: tangent signal fails coexact passport

The tangent cubic signal is real, but it is not yet a physical coexact mode. Its tangent Gram trace is `85.3333`, while the divergence Gram trace is `170.6667`. Plainly: after removing the outward shadow, the pattern remains on the sphere, but it still has a longitudinal/exact component. The next necessary step is the Hodge coexact projector, not a determinant conclusion.

## 2026-07-14 update: Hodge proxy leaves coexact residue

A trace-level Hodge projection proxy now removes the exact/gradient part from the tangent cubic signal. The tangent trace is `85.3333`; the exact part removed is `21.3333`; the leftover coexact trace proxy is `64.0`. Plainly: after removing the “flowing” part, a strong “vortical” part remains. This is the first serious `1 <-> 3` obstruction candidate, but it is still proxy-level until an explicit orthonormal coexact `n=3` projection is performed.

## 2026-07-14 update: proxy obstruction is large

The Hodge-proxy residue is not a small leak. Its coexact trace is `64.0`, which is `6.4` times the rank-10 `P02` route. Plainly: if this survives the explicit `n=3` coexact-basis projection, C6 cannot stay a clean rank-10 absorption story without a new cancellation or paired sector.

## 2026-07-14 update: explicit `n=3` basis is the gate

The next C6 step is now sharply defined. The `n=3` coexact shell has degeneracy `30`, while the leakage image from the six Killing forms has dimension at most `6`. The proxy trace `64` must be confirmed or killed by projecting those six images into the explicit quotient-normalized coexact `n=3` basis. Plainly: the model has reached a turnstile, not a fog bank.


## 2026-07-14 update: explicit `n=3` projection is nonzero

The explicit basis audit has now passed the construction part. The cubic coexact `n=3` space was built directly as homogeneous cubic vector polynomials in `R4` satisfying three linear gates: tangency `x·V=0`, divergence-free condition, and component harmonicity. The linear algebra gives ambient dimension `80`, constraint rank `50`, and nullity `30`, exactly the expected `n=3` coexact degeneracy.

Projecting the six leaked Killing-shell images into this quotient-normalized basis does not kill the signal. In the modelled conformal slice the projected Gram trace is `80.0`, rank is `6`, and eigenvalues are `12,12,14,14,14,14`. Plainly: the third-floor turnstile was built, and the signal goes through it. This is still not the final C6 determinant coefficient, because the full one-form variation, Hilbert-metric terms, sign, and tower bookkeeping remain open. But the old hope “maybe the explicit `n=3` basis kills the leak” is now a failed route for this slice.


## 2026-07-14 update: full-operator rescue gate

After the explicit `n=3` projection came out nonzero, the next blocker is no longer “build the basis.” The basis exists. The new gate is the full one-form operator. Five term classes still have to be derived and tested together: connection variation, Ricci/curvature variation, coexact-projector variation, Hilbert inner-product variation, and genuine `delta^2 Delta` terms.

Plainly: the signal reached the third floor. Now only the full building wiring can turn it off. If those five term classes do not cancel or absorb the trace `80.0` by a no-fit identity, the clean rank-10 `pi^-4` determinant theorem is blocked.


## 2026-07-14 update: quotient parity does not kill the n=3 leak

A separate parity/descent audit checks whether the explicit cubic `n=3` one-form basis is accidentally living only on the `S3` cover. It is not. Under the antipodal map `x -> -x`, cubic vector coefficients change sign and `dx` also changes sign, so the one-form product is invariant. Plainly: the third-floor signal is allowed inside `RP3`; the quotient door does not close on it.

The same audit confirms that the projection used the quotient volume normalization already, so the trace `80.0` should not be multiplied by an extra `2` or `1/2`. This closes a normalization escape route, not the full C6 problem.


## 2026-07-14 update: local counterterms cannot erase the n=3 low note

A new finite-counterterm gate checks whether the concrete `n=1 <-> n=3` trace can simply be called local and subtracted. It cannot. The projected trace `80.0` is finite low-shell spectral data, not a large-`n` heat-kernel asymptotic coefficient. Plainly: this is a low musical note, not high-frequency hiss. Local counterterms can clean up the hiss; they do not let us erase this specific note after hearing it.

The only honest rescue routes left are unchanged but sharper: the complete one-form operator must cancel the term, or a derived no-fit absorption identity must absorb it. A finite counterterm chosen after seeing the alpha target is forbidden.


## 2026-07-14 update: the n=3 obstruction is not a tiny gap

A scale audit compares the explicit projected trace with the rank-10 story and the small `N_need-10` mismatch. The trace is `80.0`, which is `8` times the rank-10 count. Even using the conservative denominator-squared proxy, `trace/(lambda_3-lambda_1)^2 = 0.5556`, which is about `55.7` times larger than the small `N_need-10 = 0.0099700224` gap.

Plainly: this is not a rounding scratch. It is a large low-shell block. If C6 survives, it must survive by a real full-operator cancellation or a no-fit absorption identity, not by calling the term a tiny scheme residue.


## 2026-07-14 update: full-operator checklist is fixed

The remaining C6 rescue is now a checklist, not a slogan. Five blocks must be written and evaluated in the same quotient-normalized `n=1` and `n=3` bases: connection variation, Ricci/curvature variation, coexact-projector variation, Hilbert inner-product variation, and direct `delta^2 Delta` terms.

Plainly: the third-floor fire is real and large. The next step is not to say “full operator may cancel it”; the next step is to use all five extinguishers and show the numbers. If any extinguisher is only waved at, C6 is still open.


## 2026-07-14 update: first extinguisher formula fixed

The first full-operator block, connection variation, is now fixed at formula level for the conformal strain slice `h_ab=2qg_ab`. The Levi-Civita variation is

```text
delta Gamma^k_ij = delta^k_j nabla_i q + delta^k_i nabla_j q - g_ij nabla^k q.
```

Plainly: we have picked up the first extinguisher and written its nozzle shape. It has not yet sprayed the fire. The next needed output is the actual `C_conn[1,3]` matrix in the quotient-normalized `n=1` and `n=3` bases, then its interference with the trace-80 block.


## 2026-07-14 update: second extinguisher formula fixed

The Ricci/curvature block is now fixed at formula level for the conformal strain slice. In dimension `3`, for `h_ab=2qg_ab`,

```text
delta Ric_ab = - nabla_a nabla_b q - g_ab nabla^2 q,
```

and the mixed Ricci operator also has the index-raising piece `-4q alpha_a` on the unit background. Plainly: the second extinguisher has a formula too, but it has not yet sprayed the fire. The next needed output is `C_Ric[1,3]` in the same quotient-normalized bases.


## 2026-07-14 update: third extinguisher is the moving doorway

The coexact-projector block is now fixed as an operator obligation. The physical transverse space is not a fixed room: it moves when the metric changes. With no harmonic one-forms on `L(2,1)`, the projector is

```text
Pi_coex = I - d Delta_0^{-1} delta,
```

so `delta Pi_coex` must enter the reduced operator `delta(Pi Delta_1 Pi)`. Plainly: the third extinguisher is the moving doorway itself. We have written how the doorway moves, but the actual `C_proj[1,3]` matrix still has to be computed.


## 2026-07-14 update: fourth extinguisher is the ruler

The Hilbert inner-product block is now fixed at formula level. For one-forms,

```text
delta <alpha,beta> = integral [(-h^{ab} + 1/2 tr(h) g^{ab}) alpha_a beta_b] dvol.
```

In the conformal three-dimensional slice `h=2qg`, this reduces to `integral q <alpha,beta> dvol` for fixed components. Plainly: the fourth extinguisher is the ruler itself. When the metric changes, the way we measure overlaps changes. The ruler formula is written, but the trace-80 fire has not yet been remeasured with it.


## 2026-07-14 update: fifth extinguisher is `delta^2 Delta`

The final checklist block is now formalized as a gate. For the determinant,

```text
delta^2 log det Delta = Tr(Delta^-1 delta^2 Delta) - Tr(Delta^-1 delta Delta Delta^-1 delta Delta).
```

Therefore the trace-square suppression cannot become a theorem unless the first term is handled in the same scheme. There are only three acceptable outcomes: prove it is purely local heat-kernel data with no finite `P02` low-shell projection, prove exact compensation against another Maxwell--ghost block, or compute the finite quotient-normalized `C_delta2` block and include it in the master matrix.

Plainly: the fifth extinguisher is the acceleration of the operator itself. It may be harmless local smoke, but after trace `80.0` it must either be proven smoke or measured as another flame.

## 2026-07-14 update: `C_delta2` finite block is scoped

The `delta^2 Delta` fallback is now not just “compute something.” For the direct trace term `Tr(Delta^-1 delta^2 Delta)`, the first required finite data are diagonal shell traces:

```text
C_delta2[1,1] and C_delta2[3,3].
```

Because `delta^2` is bilinear in deformation directions, there are `55` symmetric deformation pairs in `Sym^2(R4)`. Before trace reductions this means `36 + 900 = 936` diagonal entries per pair, or `51480` raw diagonal entries. Off-diagonal `C_delta2[1,3]` and `C_delta2[3,1]` should be archived for self-adjointness, but they are not the direct trace term.

Plainly: the fifth extinguisher mostly changes the heat on each floor. First measure the `n=1` and `n=3` floors themselves; cross-floor sprays are consistency checks, not the main trace.

## 2026-07-14 update: `delta2` path choice is a gate

The `C_delta2` finite block now has a scheme gate before any matrix number is meaningful. The term `delta^2 Delta` depends on the chosen one-parameter path, not only on the tangent strain `h_A`.

Allowed routes are:

```text
ambient_linear_embedding_strain
metric_geodesic_path
pure_conformal_test_path
```

The preferred theorem route is the same ambient linear embedding strain used by the first-strain audits, with its induced second derivative written explicitly. The conformal path remains useful as a diagnostic, but it cannot prove the full ambient `P02` theorem unless a slice theorem is supplied.

Plainly: before measuring the fifth extinguisher, choose the track it rolls on. If the track is chosen after seeing whether the fire goes out, that is a hidden fit.

## 2026-07-14 update: ambient `delta2` path formula fixed

The preferred theorem path is now fixed, not merely named. Use the raw ambient pullback path

```text
F_eps(x)=(I+eps A)x,
g_eps=F_eps^*<.,.>_R4.
```

For tangent vectors `u,v` on `S3/RP3`, this gives

```text
g'_A(u,v)=2 <u,A v>,
g''_A(u,v)=2 <A u,A v>,
partial_A partial_B g(u,v)=<A u,B v>+<B u,A v>.
```

Plainly: the rails are now nailed down. We still have not run the train: the actual `delta2 Delta_1,coex` operator and the finite `C_delta2` traces remain uncomputed.

## 2026-07-14 update: `delta2 Delta_1` parts are named

The fifth extinguisher now has a parts list. On the fixed ambient path, `delta2 Delta_1,coex` must be built from six subblocks:

```text
principal_second_symbol
second_connection_terms
second_ricci_curvature_terms
coexact_projector_second_variation
hilbert_basis_second_variation
local_counterterm_classifier
```

Plainly: we have named the machine parts. None of the parts has been machined yet, so this does not put out the trace-80 fire. It only prevents us from pretending that `delta2 Delta` is one vague object.

## 2026-07-14 update: principal second-symbol formula fixed

The first of the six `delta2 Delta_1` parts is now fixed at formula level. For the ambient path,

```text
partial_A partial_B g^{ij}
  = h_A^i_k h_B^{kj} + h_B^i_k h_A^{kj} - k_AB^{ij},

delta2_principal_AB(Delta_1) alpha
  = - (partial_A partial_B g^{ij}) nabla_i nabla_j alpha.
```

Here `h_A=partial_A g` and `k_AB=partial_A partial_B g`. This is only the principal second-symbol piece; connection, Ricci, projector, Hilbert, and local-classifier pieces are separate.

Plainly: one gear of the fifth extinguisher is shaped. It is not installed yet, and no `C_delta2` trace has been computed from it.

## 2026-07-14 update: second-connection skeleton fixed

The second `delta2 Delta_1` gear is now located. It consists of the second connection acceleration and connection-product terms in the rough one-form Laplacian:

```text
delta2 Gamma_AB,
partial_B g^{-1} * delta_A Gamma + A<->B,
delta_B[nabla h_A] + A<->B,
delta Gamma_A * delta Gamma_B products.
```

This block is separate from the principal second-symbol block. Plainly: we now know where the connection gear sits, but the teeth are not cut yet. The full `delta2 Gamma_AB` tensor and `C_delta2` diagonal traces are still missing.

## 2026-07-14 update: second-Ricci skeleton fixed

The third `delta2 Delta_1` gear is now located: curvature. It contains

```text
delta2 Ricci_AB,
partial_AB(g^{-1} Ric),
partial_A g^{-1} * partial_B Ric + A<->B,
background-curvature terms from partial_AB g^{-1}.
```

This is separate from the principal and connection gears. Plainly: RP3 is curved, so this gear cannot be thrown away. We know its slot, but the actual `delta2 Ricci_AB` tensor and `C_delta2` traces are still missing.

## 2026-07-14 update: second-projector skeleton fixed

The fourth `delta2 Delta_1` gear is the moving coexact doorway at second order. The required pieces are

```text
delta2 Pi_coex,
delta2(Delta_0^{-1}),
delta2(delta_g),
(delta Pi_A) Delta_1 (delta Pi_B),
(delta Pi_A)(delta_B Delta_1) + A<->B,
side-projector terms in delta2(Pi Delta Pi).
```

Plainly: we now know every hinge of the moving doorway that can move twice or cross-move with the operator. But the hinge motion has not been measured, self-adjointness has not been checked, and no `C_delta2` trace has been computed.

## 2026-07-14 update: second-Hilbert skeleton fixed

The fifth `delta2 Delta_1` gear is the ruler at second order. It includes

```text
second variation of g^{ab} alpha_a beta_b,
second variation of dvol_g,
cross terms between g^{-1} and dvol_g variations,
basis transport to keep quotient bases orthonormal,
degenerate-shell rotations,
self-adjoint representation in the varied Hilbert metric.
```

Plainly: the ruler can stretch twice, and now we know which marks can move. But the ruler has not been recalibrated: no basis transport, Gram correction, self-adjointness check, or `C_delta2` trace is done.

## 2026-07-14 update: delta2 local-counterterm classifier

The last `delta2 Delta_1,coex` skeleton is now explicit: local-counterterm classification. It separates three buckets:

- predetermined local heat-kernel data, removable only by a declared scheme;
- finite low-shell spectral data, especially future `C_delta2[1,1]` and `C_delta2[3,3]` entries;
- possible exact compensation inside the same Maxwell--ghost determinant scheme.

Plainly: this is the trash sorter. Dust fixed by the rules may be swept away before looking at the data. Stones found in the low shells cannot be swept away after we see them. If the local/nonlocal split is not proven, the finite `C_delta2` table must be computed and kept in the master matrix.

## 2026-07-14 update: delta2 skeleton phase complete

A new completion gate checks the six `delta2 Delta_1,coex` rooms together. The result is deliberately mixed:

- complete: principal second-symbol, second connection, second Ricci/curvature, second coexact-projector, second Hilbert/basis, and local-counterterm classifier are all named;
- open: full formulas, self-adjoint reduction, locality or same-scheme compensation, and diagonal `C_delta2[1,1]`, `C_delta2[3,3]` traces.

Plainly: the map is complete, but the rooms have not been measured. This prevents a fake upgrade: C6 cannot improve just because the missing pieces now have names.

## 2026-07-14 update: delta2 trace priority

After skeleton completion, the first measurement order is now fixed. Direct `Tr(Delta^-1 delta2 Delta)` work starts with diagonal blocks:

- first: `C_delta2[1,1]`, a `6 x 6` block per symmetric deformation pair, weight `1/4`;
- second: `C_delta2[3,3]`, a `30 x 30` block per symmetric deformation pair, weight `1/16`;
- archive later: `C_delta2[1,3]` and `C_delta2[3,1]`, useful for self-adjointness but not a replacement for the direct trace.

Plainly: weigh the two boxes sitting on the scale first. The side boxes may tell us whether the setup is symmetric, but they do not replace the main weight.

## 2026-07-14 update: C11 setup gate

The first `delta2` trace block is now packaged as a concrete job:

- target: `C_delta2[1,1]`;
- basis: six quotient-normalized `n=1` Killing one-forms on `L(2,1)`;
- workload: `36` entries per symmetric deformation pair, `55` pairs, `1980` raw entries before reductions;
- convention: no extra cover factor and no path change after numbers.

Plainly: the small box is now on the bench with labels attached. But it is still empty: connection, Ricci, projector, Hilbert/basis, and local/compensation pieces must be expanded before the numbers can be filled in.

## 2026-07-14 update: direction re-audit

The wiki/material pass does not support a full switch away from C6 yet. The `pi^-4`/`P02`/`kappa_Cas` spine remains too structured, and the blocker is now sharply localized. But it also does not support more open-ended C6 scoping.

Plainly: this cave is still worth one more serious dig, but only toward stone, not another map. The next C6 move must produce matrix-enabling operator content or a same-scheme locality/compensation proof. If not, the better switch targets are external determinant literature and the neutrino overlap lemma.

## 2026-07-14 update: timeboxed C6 operator sprint

The next C6 step is no longer open-ended. The selected sprint target is the second-connection operator piece: expand `delta2 Gamma_AB` enough that it can feed the `C_delta2[1,1]` work package or be proven local/compensated in the same scheme.

Plainly: one tool must now touch the small box. If it cannot, the cave does not get another map; the work should pivot to the external determinant gate and neutrino overlap lemma.

## 2026-07-14 update: GammaAB tooth cut

The sprint has produced actual operator content: the mixed second-connection tensor is now explicit in a background-`nabla` convention,
`Gamma_AB = 1/2(g^{-1} C_AB + m_A C_B + m_B C_A)`.

Plainly: one tooth of the gear is cut. But the gear is not mounted yet. The next step is to insert this tensor, the `Gamma_A Gamma_B` products, and inverse-metric/first-connection crosses into the rough one-form Laplacian and see whether it can feed `C11`.

## 2026-07-14 update: connection gear mounted

The second-connection tensor is now inserted into rough-Laplacian slot structure. The `C11` connection block has three pieces:

- single `Gamma_AB` insertion;
- inverse-metric / first-connection cross;
- `Gamma_A Gamma_B` products.

Plainly: the tooth is now on the shaft. The remaining job is to turn it against the six `n=1` Killing vectors and see whether it produces cancellation, reinforcement, or a finite residual.

## 2026-07-14 update: product gear sorted

The `Gamma_A Gamma_B` part of connection2 is now split into three bins:

- derivative-index products;
- one-form-component products;
- mixed-gradient products.

Plainly: the dirtiest double-gear piece is no longer a blob. It is sorted, but not counted. The next step is exact index cleanup and integration against the six `C11` basis vectors.

## 2026-07-14 update: product gear index cleanup

The `Gamma_A Gamma_B` product slot now has a fixed free-index operator table for the rough one-form Laplacian convention `L alpha_c = -g^{ij} nabla_i nabla_j alpha_c`:

```text
P_AB(alpha)_c = -g^{ij}[Gamma_A^p_ij Gamma_B^d_pc
                         + Gamma_A^p_ic Gamma_B^d_jp
                         - Gamma_B^d_jc Gamma_A^p_id] alpha_d
                + A<->B.
```

This keeps three teeth visible: derivative-index products, one-form-component products, and mixed component/gradient products. The cleanup also adds a guardrail: the one-form-component and mixed-gradient terms may merge under final dummy-index canonicalization and `A,B` symmetrization, so they must not be counted as independent integrals until the six-basis contraction is performed.

Plainly: the double gear now has labelled teeth. It still has not been turned against the six quotient-normalized `n=1` Killing vectors, so no `C_conn2[1,1]` number is claimed.

## 2026-07-14 update: product Gamma insertion

The `Gamma_A Gamma_B` product gear has been rewritten in first-strain tensor language. Using `Gamma_X^k_ij = 1/2 g^{kl} C_X_ijl`, the product operator becomes:

```text
P_AB(alpha)_c = -1/4 g^{ij}[g^{pq} C_A_ijq g^{de} C_B_pce
                              + g^{pq} C_A_icq g^{de} C_B_jpe
                              - g^{de} C_B_jce g^{pq} C_A_idq] alpha_d
                + A<->B.
```

This is now ready to be paired with the `C11` basis template `Integral e_r^c P_AB(e_s)_c dV_g`, but the integral has not been done.

Plainly: the gear teeth are no longer abstract labels; they are made out of the strain tensors `C_A` and `C_B`. The six Killing vectors still have not been used as the measuring ruler.

## 2026-07-14 update: product ambient simplification

The product subslot has a new simplification on the locked ambient path. The first strain `h_A(Y,Z)=2<Y,A Z>` gives

```text
C_A(X,Y,Z) = -4 <X,Y><Z,A x>,
Gamma_A^p_ij = -2 g_ij a_A^p,
where a_A=(A x)^T.
```

After A/B symmetrization,

```text
P_AB(alpha)_c = -12 [ a_A_c <a_B,alpha> + a_B_c <a_A,alpha> ].
```

Plainly: the dirty product gear is now just two tangent arrows. The next actual calculation is to integrate their overlaps with the six Killing one-forms.

## 2026-07-14 update: product C11 moment table

The product subslot has now been actually measured against the six Killing vectors. In the raw ambient strain basis,

```text
Integral <E_r,a_A><a_B,E_s> dV = Tr(sym(Omega_r^T A) sym(Omega_s^T B))/6,
C_rs(A,B) = -12 [M(r,A;s,B) + M(r,B;s,A)].
```

Result: all `55` symmetric strain-pair matrices are nonzero. Their ranks are distributed as `1:6`, `2:12`, `3:4`, `4:27`, `5:6`.

Plainly: the product gear is not fake; it gives a real nonzero table. But it is only one gear, so the next question is whether the other connection pieces cancel it or reinforce it.

## 2026-07-14 update: single GammaAB ambient simplification

After the product subslot table, the single `Gamma_AB` slot has also simplified. On the locked ambient path,

```text
Gamma_AB^k_ij = g_ij w_AB^k,
w_AB = -ell_AB + 4 A_T a_B + 4 B_T a_A,
ell_AB=((AB+BA)x)^T.
```

The corresponding rough-Laplacian piece is

```text
L_single_GammaAB(alpha)_c
  = (nabla_c w_AB^d) alpha_d
    + 2 w_AB^d nabla_c alpha_d
    + 3 w_AB^d nabla_d alpha_c.
```

Plainly: the next connection gear is now just one arrow plus its derivative. The next calculation should measure this arrow against the six Killing forms, just as we did for the product gear.

## 2026-07-15 update: single GammaAB C11 moment table

The single `Gamma_AB` gear has now been measured. In the raw strain basis, the finite table is nonzero for `52` of `55` symmetric strain pairs. The quiet pairs are `S01,S23`, `S02,S13`, and `S03,S12`; ranks are distributed as `0:3`, `2:12`, `4:36`, `6:4`.

Plainly: the second gear is real too, but it is not just the first gear with another coefficient. We cannot declare cancellation by eye; the remaining metric-cross gear must be computed and then all connection pieces must be added.

## 2026-07-15 update: metric-cross formula

The last connection subslot has been reduced to a usable ambient formula:

```text
L_cross[A|B](alpha)_c
  = 4 (S_A)^i_c (nabla_i a_B^d) alpha_d
    + 8 (S_A)^i_c a_B^d nabla_i alpha_d
    + 4 tau_A a_B^d nabla_d alpha_c,
L_metric_cross_AB=L_cross[A|B]+L_cross[B|A].
```

Plainly: the third gear is now cut. It still has not been tested against the six Killing vectors, but the full connection block is no longer missing a formula slot.

## 2026-07-15 update: metric-cross C11 moment table

The third connection gear has now been measured. Metric-cross is nonzero for all `55` raw symmetric strain pairs, with ranks `4:39` and `6:16`.

Plainly: all three connection gears now have tables. The next step is not guessing cancellation; it is adding product + single `Gamma_AB` + metric-cross into the full `C_conn2[1,1]` block.

## 2026-07-15 update: full connection C11 assembly

The three connection tables have been added into `C_conn2[1,1]`. Result: no internal cancellation. The full connection block is nonzero for all `55` raw symmetric strain pairs, with ranks `2:6`, `4:39`, `6:10`.

Plainly: the connection machine does not shut itself off. Any final cancellation has to come from outside connection: Ricci, projector, Hilbert/basis, principal, or compensation terms.

## 2026-07-15 update: principal C11 moment table

The principal second-symbol block has now been measured against the six Killing vectors. It is nonzero for all `55` raw symmetric strain pairs, with ranks `4:39`, `6:16`.

Plainly: the first non-connection gear is real too. The next honest step is to add principal + connection, not to guess cancellation by rank similarity.

## 2026-07-15 update: principal plus connection assembly

The principal table has been added to the assembled connection table. Result: no cancellation. The combined block is nonzero for all `55` raw symmetric strain pairs, with ranks `4:39`, `6:16`.

Plainly: principal does not switch off connection. If C6 is rescued, the rescue has to come from curvature/Ricci, coexact projector, Hilbert/basis, or compensation terms.

## 2026-07-15 update: C11 table recheck

A separate sanity verifier recomputed `56` formula entries directly and checked every `55`-pair assembly. No mismatch was found. The connection block remains nonzero with ranks `2:6`, `4:39`, `6:10`; the principal+connection block remains nonzero with ranks `4:39`, `6:16`.

Plainly: this does not prove the theorem, but it says the current tables are internally consistent and not obviously broken by arithmetic or copy/sign mistakes.

