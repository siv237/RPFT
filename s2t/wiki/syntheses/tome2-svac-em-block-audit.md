# Tome 2 Svac EM Block Audit

> Status: working
> Type: synthesis
> Updated: 2026-07-14

## Summary

This page audits the electromagnetic `S_vac` block of Tome II against the stricter RPFT derivation files. The research result is mixed but positive: the carrier and Jacobian pieces are strongly supported, the `pi` and `pi^4` structures have plausible geometric derivations, while the `1/24` Casimir/QED determinant contribution remains the main conditional proof point.

## Successes

- Carrier support is strong inside the minimal class: `K = RP^3 x S^1` is supported by compactness, spin admissibility, nontrivial `pi_1`, discrete flat `U(1)` connections, `Z_A = pi^2`, and phase step `pi`.
- Jacobian support is strong: `RPFT-main/rigorous/08_jacobian_derivation.md` derives `Z_A = pi^2` for the gauge sector and `Z_Psi = 4pi^3` for the spinor sector by separating gauge normalization from the spinor cover.
- Geometry support is strong for the basic volume facts: `RPFT-main/rigorous/31_geometry_proof.md` derives `Vol(S^3) = 2pi^2 R^3`, `Vol(RP^3) = pi^2 R^3`, and the nontrivial `RP^3` systole `pi R`.
- The `1/(pi^4 S_geo^2)` term has a credible geometric origin: `RPFT-main/rigorous/05_pi4_derivation.md` ties `pi^4` to the square of the dimensionless `RP^3` volume.
- The `pi` term is not just decorative: `RPFT-main/rigorous/18_pi_term_rigorous.md` and related Tome II language connect it to the nontrivial flat `Z_2` holonomy branch.
- Numerically, `s2t_tome2_results.json` reproduces `S_vac` against `alpha^{-1}` with residual around `-3.48e-9`.

## Failures And Risks

- Absolute uniqueness of `K` is not proven; the result is minimal-class uniqueness. A broader compact-space class could still challenge the choice if it passes the same no-hidden-parameter audit.
- The `1/24` contribution is the main weak point. `RPFT-main/rigorous/30_qed_one_loop_proof.md` explicitly says that a fully unconditional first-principles claim for `kappa_Cas = 1/24` may be too strong.
- The strict status of `1/24` is conditional on fixing the zeta-determinant scheme, scale subtraction rule, spin structure on `S^1`, zero-mode handling via `det'`, and the exact QED Maxwell--ghost/Hodge operator combination.
- The disappearance of the `log(mu)` ambiguity is encouraging but not enough: it removes a major scheme-dependence source, but still leaves the finite determinant constant to compute in the fixed scheme.
- The current `S_vac` success should therefore be reported as structurally strong but not yet mature until the finite determinant computation and alternative-regularization no-go are closed.

## TeX Source Alignment

- `tome2_s2t_spectral_closure.tex` now reflects this audit: `S_vac` is a conditional success until `kappa_Cas = 1/24` is closed.
- The new dedicated subsection defines the `kappa_Cas` working scheme and lists the exact closure protocol.

## Expected Research Result

If the remaining `1/24` condition is closed, the electromagnetic block becomes the strongest II.A result: `S_vac` would be supported by carrier selection, volume/Jacobian normalization, holonomy, zeta residue, and machine reproduction. If `1/24` fails or becomes scheme-dependent, `S_vac` must be downgraded from strict closure to conditional spectral fit even though the numerical residual is excellent.

## Compliance Check

- Tome II claim checked: `S_vac` is marked successful II.A closure in [[tome2-s2t-spectral-closure]].
- Proof-chain checked: [[tome2-proof-chain]] already flagged `1/24`, zeta residue, and QED finite part as risks.
- Strict RPFT files checked: `05_pi4_derivation.md`, `08_jacobian_derivation.md`, `15_why_K.md`, `18_pi_term_rigorous.md`, `30_qed_one_loop_proof.md`, and `31_geometry_proof.md`.
- Current status: strengthen `S_vac` as a leading success, but keep `1/24` as an unresolved proof risk.

## Next Research Steps

1. Use [[kappa-cas-one-over-24]] to close or demote the exact assumptions behind `kappa_Cas = 1/24`.
2. Compare periodic versus antiperiodic `S^1` spin-structure choices and decide which one Tome II actually uses in the EM/QED block.
3. Run or inspect `RPFT-main/rigorous/02_zeta_compute.py` and `RPFT-main/rigorous/30_qed_one_loop_proof.md` together to see whether the finite determinant constant is reproducible.
4. Add an alternative-regularization no-go test: if another finite subtraction gives the same `S_vac` only by tuning, the current scheme is stronger; if many schemes work, the closure weakens.

## Links

- [[tome2-s2t-spectral-closure]] — source page for Tome II closure claims.
- [[tome2-proof-chain]] — proof-chain map for successful and partial II.A blocks.
- [[s2t-closure-roadmap]] — global closure status map.
- [[numerical-audits]] — machine reproduction of `S_vac` and other closed rows.
- [[kappa-cas-one-over-24]] — focused proof-risk page for the `1/24` coefficient.

## Source Notes

- Source paths: `tome2_s2t_spectral_closure.tex`, `RPFT-main/rigorous/05_pi4_derivation.md`, `RPFT-main/rigorous/08_jacobian_derivation.md`, `RPFT-main/rigorous/15_why_K.md`, `RPFT-main/rigorous/18_pi_term_rigorous.md`, `RPFT-main/rigorous/30_qed_one_loop_proof.md`, `RPFT-main/rigorous/31_geometry_proof.md`, `s2t_tome2_results.json`.

## 2026-07-10 Coexact Tower Update

The EM block has been downgraded from merely “`1/24` finite determinant risk” to a sharper tower question. The ordinary Maxwell--ghost/Hodge sector leaves a positive coexact Bessel tail on `RP^3 x S^1`; this is tracked in [[coexact-tower-delta]].

New computed facts:

- `s2t_coexact_tower_results.json` gives `T_coex^RP3 = 1.5227161455271536e-05`.
- The `RP^3` projection is not a simple half of `S^3`; it keeps odd coexact levels and projects out even ones, so the dominant `n=1` level survives.
- `T_coex^RP3/S_geo = 1.11e-7`, about `20.3%` of the existing `1/(pi^4 S_geo^2)` term.
- A naive Maxwell--ghost--Dirac cancellation was tested in `s2t_mgd_pairing_results.json` and rejected as a ready-made paired mechanism: required coefficients are non-natural (`0.1473`, `0.07364`, `2.9797`, or `1.4899` depending on the diagnostic Dirac tower).

Updated status: `S_vac` remains a conditional determinant success. The next proof target is not just `kappa_Cas = 1/24`; it is the full normalized determinant relation for `Delta_tower^coex`, including sign, radius factor, and whether the existing `pi^-4 S_geo^-2` residue already encodes the finite tower.

## 2026-07-10 Pi-Four Absorption Lead

A serious follow-up checked whether the existing `1/(pi^4 S_geo^2)` term could already encode the finite coexact tower. The best natural relation found is:

```text
1/(pi^4 S_geo^2) ≈ (pi^2/2) * T_coex^RP3 / S_geo.
```

The factor `1/2` matches the bosonic determinant prefactor, while `pi^2` is `Vol(RP3)`. Numerically, this candidate gives `5.483439627824377e-07` versus the existing `5.466750295392699e-07`, a `0.305%` overshoot.

Status: promising but not closed. This is now the primary route to saving the current formula without adding an independent `Delta_tower^coex`: derive the volume-weighted half-determinant normalization and explain the small residual without fitting.

## 2026-07-10 Residual Audit Update

The `pi^-4` absorption lead became stronger after testing the small residual. The raw volume-weighted tower formula overshoots by `0.3053%`, but multiplying it by a Casimir-mixing factor

```text
1 - 10/(24 S_geo)
```

matches the existing `1/(pi^4 S_geo^2)` term to relative error `3.04e-6`. This suggests a possible second-order mixing between the coexact tower residue and the already derived `1/24` determinant branch.

Caution: the integer `10` is not yet derived. Until it is identified as a multiplicity, index, or determinant cross-term coefficient, this remains a strong hypothesis rather than a closure.

## 2026-07-10 Integer 10 Candidate

The previously unexplained `10` in the Casimir-mixing factor now has a plausible spectral origin: the scalar/ghost even sector on `RP^3` has degeneracies `1` for `ell=0` and `9` for the first nonzero even shell `ell=2`, giving `1+9=10`.

This is relevant because the `1/24` branch is scalar/periodic in the Maxwell--ghost determinant, and exact one-form modes inherit scalar eigenvalues. The hypothesis is now:

```text
pi^-4 residue ≈ (Vol(RP3)/2) * T_coex/S_geo * (1 - (1+9)/(24S_geo)).
```

Status: promising; proof requires deriving this as a second-order cross-term, not merely observing the multiplicity.

## 2026-07-10 Determinant Trace-Rank Test

The follow-up script `s2t_determinant_casmix_audit.py` tested the explicit second-order form:

```text
1/(pi^4 S_geo^2) ?= (pi^2/2) * T_coex^RP3/S_geo * (1 - N/(24 S_geo)).
```

Solving this equation for the required effective trace-rank gives:

```text
N_need = 10.0099700224.
```

The nearest integer is `10`, exactly the candidate scalar/ghost cumulative rank `d_0+d_2=1+9`. With `N=10`, the relative error against the existing `pi^-4` term is `3.04e-6`.

Updated status: this is stronger than a naked integer fit because the required determinant trace-rank is almost integral and points to the first two even scalar shells on `RP^3`. It is still not a proof: closure requires an explicit gauge-fixed mixed-trace calculation with the correct second-order sign.


## 2026-07-10 `P_0,2` Quadratic Projector Candidate

A stronger candidate for the missing finite-rank selection rule was added in `s2t_p02_projector_audit.py`.

Instead of taking `ell=0,2` from the full scalar/exact tower, the candidate identifies `P_0,2` with the space of ambient quadratic even functions on `S^3 ⊂ R^4` descending to `RP^3`:

```text
q_A(x) = A_ab x^a x^b,  A_ab=A_ba.
```

This space has dimension:

```text
dim Sym^2(R^4) = 4*5/2 = 10.
```

It decomposes as trace plus traceless symmetric quadratics:

```text
Sym^2(R^4) = R δ_ab ⊕ Sym^2_0(R^4),  10 = 1 + 9.
```

On scalar harmonics this is exactly `ell=0` plus `ell=2`. In this interpretation higher shells `ell=4,6,...` are excluded because they are higher-than-quadratic ambient deformations, not because of an arbitrary cutoff.

Updated status: this is the best current proof target. It explains the finite rank representation-theoretically, but it still requires the determinant-level derivation that the Maxwell--ghost mixed operator `B` couples specifically to this quadratic strain sector rather than to the full scalar tower.

## 2026-07-10 Metric-Variation Coupling Lemma

A conditional derivation was added via `s2t_metric_variation_p02_audit.py` and inserted into Tome II.

The logic is:

```text
δ log det Δ = Tr(Δ^{-1} δ_g Δ).
```

Therefore the mixed perturbation `B` is determined by the allowed metric strain `h`. If the `pi^-4` mixed term is restricted to first ambient linear deformations of `S^3 ⊂ R^4`, then:

```text
x -> (I + εA)x.
```

The antisymmetric part of `A` is an `SO(4)` rotation/isometry and produces no strain. The symmetric part gives:

```text
q_A(x)=A_ab x^a x^b.
```

These functions are even under `x -> -x`, so they descend to `RP^3`. Their space is `Sym^2(R^4)`, with rank `10 = 1 + 9` from trace plus traceless parts. Thus, under the first-ambient-strain assumption, `B` couples to `P_0,2` rather than the full scalar tower.

Status: conditional derivation. The remaining proof obligation is to justify that the S2T `pi^-4` mixed term uses only first ambient metric strain, not arbitrary internal metric perturbations.

## 2026-07-10 S2T First-Strain Selection

The script `s2t_first_strain_selection_audit.py` formalizes why the `pi^-4` mixed term should use first ambient strain rather than arbitrary internal metric perturbations.

S2T criteria used:

- the carrier `K=RP^3 x S^1` and radii are fixed in II.A;
- arbitrary `h_ij(y)` would introduce an infinite-dimensional new metric sector;
- arbitrary metric perturbations leave the minimal constant-curvature carrier class;
- ordinary scalar/exact inheritance gives the full scalar tower, not `ell=0,2`;
- manual `ell=0,2` cutoff is forbidden;
- first ambient linear strain is canonical under the `S^3` cover and `SO(4)`.

Result: within II.A, the unique minimal admissible finite-rank metric-strain channel is `Sym^2(R^4)`, hence `P_0,2`. Higher ambient polynomial strains are not forbidden forever, but they constitute a new model sector and require recomputing the `pi^-4` residue.

## 2026-07-10 Full Coexact Delta Audit

`s2t_full_coexact_delta_audit.py` tested the two `4 -> 5` routes directly.

Result:

- No standard paired sector was found: Hodge exact/scalar ghosts do not cancel coexact transverse modes; `RP^3` projection leaves the dominant `n=1` mode; Dirac/spin-cover cancellation is not a pure Maxwell coexact pairing.
- The full projected tower is nonzero and dominated by the first mode.
- If treated as a new independent `Delta_tower^coex`, even the smallest simple normalization worsens the `alpha^-1` match by about `15x`.
- The `P_0,2` volume-weighted mixed normalization is essentially the existing `pi^-4` residue, so it is viable only as an absorption interpretation, not as an extra term.

Status: `4 -> 5` is still not achieved. The next proof target is no longer “compute whether the tower exists”; it exists. The target is to prove the absorption identity or find a genuinely new paired sector.

## 2026-07-10 External Literature Gate

An immediate literature pass was recorded in [[external-literature-spectral-determinants]]. The checked anchor set is:

- Ikeda--Yamamoto for spectra of three-dimensional lens spaces;
- Lauret / Lauret--Miatello--Rossetti for modern lens-space `p`-spectra via congruence lattices;
- Nash--O'Connor for determinants of Laplacians on lens spaces;
- Schwarz and Ray--Singer for gauge-functional, zero-mode, and analytic-torsion determinant bookkeeping.

Audit consequence: the absorption route is compatible with the correct literature domain, but not proven by it. The internal `P_0,2` rank-10 explanation remains the best finite-strain candidate; nevertheless, Tome II must keep the EM closure conditional until an explicit `L(2,1)` exact/coexact determinant derivation shows the sign, determinant power, zero-mode subtraction, and the finite projector rank.
## Каноническая хронология C6

Полная хронология шагов от поглощения башни до разложения
максвелловско-духового определителя теперь поддерживается только на
странице [[coexact-tower-delta]]. Единая таблица формульных подблоков и их
матричного состояния находится в [[c6-second-variation-checklist]].

Синтетический вывод: геометрические ранг и объёмная нормировка остаются
условно мотивированными, но полная вторая вариация и вклад духов не
вычислены. Поэтому C6 не закрыт, а коэффициент остаётся структурным
сжатием, а не доказанным следствием определителя.
## 2026-07-13 Scalar FP Bookkeeping Audit

The audit `s2t_c6_scalar_fp_bookkeeping_audit.py` turns the FP residual warning into a determinant-power check. Bare standard FP gives:

```text
Gamma_std = 1/2 log det' Delta_1,coex - 1/2 log det' Delta_0 + zero/gauge/local.
```

If the residual scalar half-determinant has the same first-strain `P02` trace-square, the simplified C6 rank flow is no longer `10`; it is `10/2=5`. Numerically this changes the suppression factor from `0.9969594432` to `0.9984797216`, producing a relative mismatch of about `1.53e-3` against `1/(pi^4 S_geo^2)`. Therefore C6 can only proceed by proving scalar half-power cancellation or proving zero `P02` projection of the scalar residual.


## 2026-07-14 Scalar P02 Projection Audit

The audit `s2t_c6_scalar_p02_projection_audit.py` gives a partial positive result. The retained scalar row responsible for `kappa_Cas=1/24` is constant on `RP3`; therefore an `RP3` first ambient strain has no traceless `ell=2/P02` scalar-Laplacian insertion on that row. This supports the claim that `1/24` is not itself a ghost `P02` trace-square.

However, this does not close C6. The trace rank-1 direction still needs volume/gauge normalization, and the nonzero scalar half-determinant left by bare standard FP remains dangerous: nonconstant scalar modes have nonzero `RP3` gradients and can couple to the first ambient strain. Therefore the standard-FP obstruction is now localized to the nonzero scalar residual tower, not to the constant `1/24` row.


## 2026-07-14 Scalar Variation P02 Audit

The audit `s2t_c6_scalar_variation_p02_audit.py` tests the hoped-for symmetry no-go for scalar `P02` leakage. It fails: `RP3` scalar modes are even `ell`, the first nonzero shell is `ell=2` with multiplicity `9`, and an `ell=2` traceless first ambient strain can couple by the usual selection rule `ell -> ell, ell±2`. Thus the nonzero scalar residual tower has an allowed `P02` leakage channel.

This is a downgrade for the standard covariant FP route. C6 can still survive if the scalar trace-square is proven local/subtracted or cancelled by zero/gauge/Jacobian factors, but it is no longer credible to claim that the nonzero scalar tower vanishes by symmetry. The physical transverse quotient remains the clean conditional route.


## 2026-07-14 Standard FP Rescue Routes Audit

The audit `s2t_c6_scalar_rescue_routes_audit.py` checks whether the standard-FP scalar obstruction can be rescued by locality/subtraction or by zero/gauge/Jacobian cancellation. Both fail as theorem-level claims in the current model.

Local subtraction removes heat-kernel/UV pieces only; it does not remove the finite nonlocal Bessel/winding part associated with positive scalar eigenvalues. Zero/gauge/Jacobian factors remove zero modes and set determinant powers, but they do not provide an opposite nonzero scalar tower cancelling the residual `-1/2 log det' Delta0`. Thus standard covariant FP cannot currently deliver the rank-10 C6 determinant theorem.

Operational verdict: either adopt/derive the physical transverse quotient as the defining EM determinant scheme, or keep `pi^-4` as structural compression rather than mature determinant residue.

## 2026-07-14 L(2,1) Coexact Normalization Audit

The audit `s2t_c6_l21_normalization_audit.py` closes a small but important normalization layer before the explicit coexact mixed-trace calculation.

Result:

- The covering map `S3 -> L(2,1)=S3/{±1}` has degree `2`, so `Vol(L(2,1)) = Vol(S3)/2 = pi^2` at unit radius.
- If an antipodal-invariant coexact one-form lift has `Integral_S3 |alpha|^2 = 1`, its descended raw norm on `L(2,1)` is `1/2`.
- The quotient-orthonormal state is therefore `sqrt(2)` times the descended state.
- In a bilinear variation matrix element, the two external `sqrt(2)` factors cancel the quotient integral factor `1/2`; the net cover factor is `1`.
- Therefore matrix elements may be computed on `S3` using invariant lifts, but the final mixed trace must not be multiplied again by `2` or `1/2`.
- The quotient still controls the state space: even coexact shells remain projected out even when integrals are evaluated on the cover.

Verdict: this normalization sublayer is fixed. It does not close C6, but it removes a common factor-of-two ambiguity from the next proof target: the explicit matrix elements `<n,i|delta_A Delta_1|m,j>` and the associated coexact trace-square on `L(2,1)`.

## 2026-07-14 L(2,1) Shell-Selection Audit

The audit `s2t_c6_l21_shell_selection_audit.py` tests whether the finite rank `10` can be derived from representation-level shell selection alone.

Result:

- The first ambient strain is quadratic and even: `P_0,2 = ell=0 plus ell=2`.
- Evenness preserves the `L(2,1)` parity sector, so odd coexact shells remain in the allowed state space.
- The necessary channel rule permits surviving odd shells to connect as `n -> m` with `|n-m| in {0,2}`.
- Thus `n=1` can connect to `1,3`; `n=3` can connect to `1,3,5`; and the pattern continues through the odd tower.
- Therefore `rank 10 = dim Sym^2(R4)` is not an operator-trace rank derived from shell selection alone.

Verdict: this is a sharpening negative result, not a collapse of the whole program. C6 now requires a coefficient-level theorem: the full one-form Laplacian variation plus coexact projection must cancel, localize/subtract, or physically absorb the infinite allowed coexact channels. If that theorem fails, `pi^-4` must be downgraded from determinant theorem to structural compression.

## 2026-07-14 Coexact Locality Gate Audit

The audit `s2t_c6_l21_coexact_locality_gate_audit.py` tests whether the infinite allowed coexact shell channels can be dismissed as local counterterms.

Result:

- Local counterterms can remove UV/heat-kernel asymptotic pieces only.
- The allowed shell channels include low-spectrum and finite off-diagonal trace-square data such as `1 -> 1`, `1 -> 3`, and `3 -> 1`.
- These finite low-shell pieces are global spectral determinant data, not local heat-kernel coefficients.
- A finite subtraction chosen to force the observed `alpha` value would violate the no-hidden-parameter rule.
- The physical quotient remains viable only as a primary determinant-domain theorem; it does not automatically prove finite tower absorption.

Verdict: local subtraction alone cannot rescue C6. The next proof must split the mixed trace into local/asymptotic and finite/nonlocal parts, then derive that the finite coexact part either vanishes/cancels or equals the existing `pi^-4/P_0,2` residue without an added coefficient.

## 2026-07-14 Low-Shell Block Specification

The audit `s2t_c6_l21_low_shell_block_spec_audit.py` converts the next C6 step into a concrete finite calculation.

Required channels:

- `1 -> 1`, with matrix shape `6 x 6` and weight `1/16`.
- `1 -> 3`, with matrix shape `6 x 30` and weight `1/64`.
- `3 -> 1`, with matrix shape `30 x 6` and weight `1/64`.

The required low block has `396` entries per deformation direction before symmetry reduction. Across the full `Sym^2(R4)` deformation space this is `3960` raw entries.

Verdict: C6 now has an explicit next computation rather than a vague proof gap. The calculation must use the full one-form Laplacian variation, coexact projection, and inner-product variation. If this low-shell block is nonzero and independent, `pi^-4` cannot be promoted to determinant theorem. If it vanishes or matches the absorption identity, the route remains viable but still needs extension to the odd tower.

## 2026-07-14 n=1 Killing-Overlap Audit

The audit `s2t_c6_l21_n1_killing_overlap_audit.py` tests whether the lowest diagonal channel `1 -> 1` can be dismissed by parity or representation symmetry.

Result:

- The first coexact shell is represented by six Killing one-forms from `so(4)` antisymmetric generators.
- For the traceless `P_0,2` deformation `A=diag(1,-1,0,0)`, the normalized overlap matrix of `q_A <alpha_i,alpha_j>` on `L(2,1)` is nonzero.
- Numeric rank of this overlap is `4`; max absolute entry is `1/6`; eigenvalues are `-1/6,-1/6,0,0,1/6,1/6`.

Verdict: the `1 -> 1` low-shell channel is not killed by simple symmetry at the Killing-overlap level. C6 can still survive only if the full one-form operator variation produces an explicit cancellation or absorption when principal-symbol, connection, Ricci, coexact-projection, and inner-product terms are all included.

## 2026-07-14 n=1 Principal-Symbol Warning

The audit `s2t_c6_l21_n1_principal_symbol_audit.py` evaluates the principal-symbol part of the full one-form operator variation on the `n=1` Killing shell in the reduced conformal slice `h=2qg`.

Result:

- On the unit `S3` Killing shell, `Delta_1 alpha=4 alpha`, `Ric(alpha)=2 alpha`, hence `nabla^2 alpha=-2 alpha`.
- With `delta g^{ab}=-2qg^{ab}`, the principal-symbol variation gives `-delta g^{ab} nabla_a nabla_b = -4q` on this shell.
- Thus the nonzero `q_A` overlap matrix is multiplied by `-4`.
- The resulting weighted principal trace-square for the traceless test direction is `1/9`.

Verdict: the principal-symbol term is already nonzero and larger than the toy overlap warning. C6 can still survive only if the remaining one-form terms cancel or absorb this matrix explicitly.

## 2026-07-14 n=1 Toy Trace-Square Warning

The audit `s2t_c6_l21_n1_toy_tracesquare_audit.py` turns the nonzero Killing overlap into a diagnostic trace-square scale.

Result:

- For the traceless test direction, the normalized overlap has `Tr(M^2)=1/9`.
- With `lambda_1=4`, the toy trace-square is `lambda_1^-2 Tr(M^2)=1/144`.
- This is `1/6` of the one-rank `1/24` scale and `1/60` of the rank-ten `10/24` scale.

Verdict: this is not the C6 coefficient, because the full one-form operator variation has derivative, connection, Ricci, projection, and Hilbert-metric terms. But it quantifies the warning: the first coexact shell has a finite response unless the full operator produces an explicit cancellation or absorption.


## 2026-07-14 Master C6 Closure-Matrix Update

The master closure matrix now records the new C6 status as `C6_master_closure_matrix_built_full_operator_rescue_gate`. This supersedes the older wording where the main blocker was only “standard FP scalar residual” or “generic mixed-trace computation.” Those remain real issues, but the physical coexact-quotient route has acquired a sharper low-shell gate.

New low-shell picture:

- The `n=1 -> n=1` Hodge-filtered conformal projection cancels.
- The operator does not vanish: six Killing-shell images leak into cubic content.
- Tangent projection removes the normal piece, but a tangent signal remains.
- Hodge-proxy filtering removes the exact/gradient part and leaves coexact proxy trace `64.0`.
- The true test is now projection into the explicit quotient-normalized `n=3` coexact basis of dimension `30`.

Plainly: C6 has reached a turnstile. We must build the third-shell coexact basis and see whether the leaked signal passes through. If it passes, rank-10 absorption is not a clean theorem without a new cancellation or derived absorption identity. If it dies there, the route reopens but still has to be checked against the higher odd tower.


## 2026-07-14 Explicit n=3 Projection Audit

The hard `n=3` basis gate has been partially passed in the negative direction for the clean rank-10 route. A new audit constructs the 30-dimensional quotient-normalized cubic coexact basis from tangency, divergence-free, and harmonicity constraints. Projection of the six leaked `n=1` images into this basis is nonzero: projected trace `80.0`, projected rank `6`, eigenvalues `12,12,14,14,14,14`.

Verdict: the leak is not an artifact of lacking an explicit basis. It is now a concrete low-shell obstruction candidate. C6 can still survive only if the complete one-form Laplacian variation, connection/Ricci terms, Hilbert inner-product variation, or a no-fit absorption identity cancels this contribution. Without that, `pi^-4` must remain structural compression rather than mature determinant theorem.


## 2026-07-14 Full-Operator Rescue Gate

The nonzero explicit `n=3` projection does not by itself prove C6 failure, but it moves the burden of proof. The next required theorem is not another basis construction. It is a complete one-form operator calculation showing that connection, Ricci, coexact-projector, Hilbert-metric, or `delta^2 Delta` terms cancel/absorb the rank-6 trace-80 low-shell contribution.

Verdict: C6 is still open, but the rescue space is now narrow. A scalar shortcut, local finite subtraction, or post-hoc counterterm is not acceptable. The cancellation must be written at operator level or `pi^-4` must be downgraded.


## 2026-07-14 n=3 Quotient-Parity Descent Check

The explicit `n=3` obstruction candidate also passes the `L(2,1)` descent gate. For a one-form `alpha=sum_i V_i(x) dx_i` with cubic coefficients, the antipodal map gives `V_i(-x)=-V_i(x)` and `d(-x_i)=-dx_i`, hence `a^* alpha=alpha`. Therefore the cubic coexact one-forms are allowed on `RP3`.

Verdict: the nonzero projected trace is not removed by quotient parity and is not a cover-factor artifact. C6 now has to be rescued, if at all, by the full one-form operator or a derived no-fit absorption identity.


## 2026-07-14 n=3 Finite-Counterterm Gate

The nonzero `n=1 <-> n=3` projected trace cannot be dismissed as a local subtraction term. It is a finite low-shell matrix contribution on `L(2,1)`, not a UV heat-kernel asymptotic coefficient. Therefore a finite counterterm chosen to erase trace `80.0` would be a forbidden post-hoc scheme choice.

Verdict: the local-counterterm rescue route is closed for this concrete obstruction candidate. The only remaining C6 rescue routes are explicit full-operator cancellation or a derived no-fit absorption identity.


## 2026-07-14 n=3 Obstruction Scale Check

The explicit `n=3` projected trace is not small on the internal C6 scale. It is `80.0`, eight times the rank-10 count, and the denominator-squared bookkeeping proxy is `0.5556`, about `55.7` times the `N_need-10` gap.

Verdict: the nonzero `n=3` block cannot be explained as the tiny finite scheme mismatch between `N_need=10.0099700224` and `10`. A successful C6 proof now needs a genuine full-operator cancellation or a no-fit absorption identity.


## 2026-07-14 Full-Operator Rescue Checklist

The C6 rescue condition has been converted into five auditable computations. The nonzero `n=3` trace can be rescued only if the connection, Ricci, coexact-projector, Hilbert-metric, and direct `delta^2 Delta` blocks cancel it or map it into a derived no-fit absorption identity.

Verdict: the phrase “full one-form variation may cancel it” is no longer sufficient. The next proof must produce the five matrix blocks with signs and quotient normalization. Until then, `pi^-4` remains structural compression rather than mature determinant theorem.


## 2026-07-14 Connection-Variation Formula Gate

The connection-variation block has been fixed at formula level for the conformal first-strain slice `h=2qg`: `delta Gamma^k_ij = delta^k_j nabla_i q + delta^k_i nabla_j q - g_ij nabla^k q`. This is the first concrete component of the full one-form operator rescue checklist.

Verdict: this is progress but not a C6 rescue. The required next output is the actual `n=1 <-> n=3` connection matrix block and its contribution to the trace-80 obstruction.


## 2026-07-14 Ricci-Variation Formula Gate

The Ricci/curvature block has been fixed at formula level for the conformal first-strain slice. In dimension `3`, `delta Ric_ab = -nabla_a nabla_b q - g_ab nabla^2 q`, and the mixed Ricci operator includes the index-raising contribution `-4q alpha_a` on the unit background.

Verdict: this is the second concrete component of the full one-form operator rescue checklist. It is not yet a cancellation: the required next output is the actual `n=1 <-> n=3` Ricci matrix block.


## 2026-07-14 Coexact-Projector Formula Gate

The coexact-projector block has been fixed as an explicit moving-slice obligation. Since `Pi_coex = I - d Delta_0^{-1} delta` on non-harmonic one-forms, `delta Pi_coex` contributes to `delta(Pi Delta_1 Pi)`.

Verdict: this is the third concrete component of the full one-form operator checklist. It is not yet a cancellation: the required next output is the actual `n=1 <-> n=3` projector-variation matrix block and a self-adjointness check of the reduced operator.


## 2026-07-14 Hilbert Inner-Product Formula Gate

The Hilbert inner-product block has been fixed at formula level. The one-form overlap varies by `delta <alpha,beta> = integral [(-h^{ab}+1/2 tr(h)g^{ab}) alpha_a beta_b] dvol`; in the conformal three-dimensional slice this reduces to a `q`-weighted overlap for fixed components.

Verdict: this is the fourth concrete component of the full one-form operator checklist. It is not yet a cancellation: the required next output is the actual `n=1 <-> n=3` Hilbert/basis-normalization matrix block and a self-adjointness check.
