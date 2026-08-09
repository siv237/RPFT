# S2T Closure Roadmap

> Status: working
> Type: synthesis
> Updated: 2026-07-14

## Summary

This roadmap tracks what is already closed, what is partially closed, and what remains open in the S2T / spectral-closure direction. It is meant to connect claimed closures to concrete source files and to keep failed or incomplete checks visible instead of smoothing them into narrative agreement.

## Tome II Management Readout

- Tome II version II.A is not a blanket closure claim; it is a governed closure register with explicit no-go criteria.
- Successful II.A blocks: `S_geo`, `S_vac`, `m_tau`, and the Higgs EFT bridge.
- Partial II.A blocks: neutrino matrix and EW/QCD; both are promoted to II.B tasks rather than counted as failed predictions.
- The key project-control rule is that open gaps cannot be hidden inside successful numerical coincidences.

## Current S_vac Audit Update

- TeX source now reflects this conditional status: `S_vac` is marked as conditional success pending `kappa_Cas = 1/24`.
- A dedicated Tome II subsection now defines the `kappa_Cas` closure test rather than leaving it only as a wiki-side warning.
- `S_vac` remains a leading success, but its strict status depends on closing the conditional [[kappa-cas-one-over-24]] finite determinant/Casimir step.
- `K`, gauge Jacobian, basic geometry, `pi` holonomy, and `pi^4` volume-square support are stronger than before after cross-checking strict RPFT files.
- The next risk-reduction task is to make `kappa_Cas = 1/24` reproducible under the fixed zeta-determinant, spin-structure, zero-mode, and QED operator assumptions.

## Closure Status

- `S_vac` normalization — leading II.A success, numerically reproduced and structurally supported, but still conditional on the strict `1/24` finite determinant/Casimir step.
- `m_tau` channel — strong conditional numerical relation; uniqueness passes, but the seed and compact projection normalization remain open.
- Higgs EFT bridge — the potential and `lambda_H` remain constructive; absolute `v` and `M_H` inherit the conditional tau and `S_vac` scale.
- Neutrino Dirac chain — partially closed; the missing step is a strict overlap or holonomy lemma explaining the required `π + π^{-1}` factor from the Dirac/sector spectrum.
- EW/QCD threshold closure — open; the current small-log checks should not be treated as closure evidence without a dedicated threshold solver and physical-mass validation.

## Evidence Sources

- [[tome2-s2t-spectral-closure]] — primary S2T / spectral closure source page.
- [[tome2-proof-chain]] — derivation dependency map for Tome II closure claims.
- `tome2_s2t_spectral_closure.tex` — primary S2T / spectral closure source file.
- `technical_s2t_analysis.tex` — technical companion for the S2T reinterpretation layer.
- `s2t_tome2_results.json` — numerical audit record for the Tome 2 closure checks.
- `RPFT-main/rigorous/08_jacobian_derivation.md` — candidate source for strict Jacobian and normalization factors.
- `RPFT-main/rigorous/15_why_K.md` — candidate source for the choice and role of `K`.
- `RPFT-main/rigorous/16_radius_stabilization.md` — candidate source for radius and scale stabilization.
- `RPFT-main/rigorous/18_pi_term_rigorous.md` — candidate source for the rigorous `π` contribution.
- `RPFT-main/rigorous/30_qed_one_loop_proof.md` — candidate source for the QED one-loop anchor.
- `dirac_spin_holonomy_results.json`, `gauge_holonomy_results.json`, and `sector_attribution_results.json` — audit files to mine for overlap, holonomy, and sector-attribution constraints.

## Open Gaps

- Prove or reject the neutrino overlap identity `\mathcal{N}_\nu^2 = \pi + \pi^{-1}` from a defined Dirac/holonomy operator rather than fitting it as a residual factor; tracked in [[neutrino-overlap-lemma]].
- Derive the EW and QCD threshold phases from an explicit mass-spectrum model with enough degrees of freedom to match the physical scales; tracked in [[ew-qcd-threshold-closure]].
- Separate hard closures from bridge closures: distinguish exact spectral identities, EFT-level matches, and numerological or audit-only coincidences.
- Extract top-level metrics from JSON audits into stable wiki summaries so future arguments cite specific checks rather than filenames.

## Next Actions

- Ingest `tome2_s2t_spectral_closure.tex` into [[s2t-reinterpretation]] and this roadmap.
- Summarize `s2t_tome2_results.json` in [[numerical-audits]] with pass/fail status and relevant residuals.
- Create a focused threshold-audit script for EW/QCD closure that solves for admissible logarithmic thresholds and flags unphysical masses.
- Add a neutrino-overlap note under [[holonomy-and-dirac-sectors]] if the Dirac/spin/holonomy audits contain enough support for the `π + π^{-1}` factor.

## Links

- [[s2t-reinterpretation]] — concept page for the emerging S2T layer.
- [[spectral-correlational-source]] — candidate common object behind the closure program.
- [[holonomy-and-dirac-sectors]] — audit layer most relevant to the neutrino overlap gap.
- [[numerical-audits]] — source page for JSON audit outputs.
- [[research-catalog]] — broader map of strict and exploratory source files.

## 2026-07-10 EM Tower Status

The `4 -> 5` maturity step is now sharpened. The blocker is the full coexact tower, not only the constant `1/24` branch. See [[coexact-tower-delta]].

Research status:

- `RP^3` coexact tower computed: `T_coex^RP3 = 1.5227161455271536e-05`.
- Naive Maxwell--ghost--Dirac pairing tested and rejected as a direct cancellation mechanism.
- The most promising remaining leads are: derive determinant sign/prefactor, test whether the `pi^-4 S_geo^-2` term already summarizes this tower, or find a non-naive torsion/spin paired sector with exact spectral matching.

Roadmap update: `S_vac` should stay “conditional determinant success” until `Delta_tower^coex` is either absorbed by a derived existing term or explicitly included with a no-hidden-parameter normalization.


## 2026-07-14 C6 n=3 Gate Update

The `S_vac` roadmap should now treat C6 as blocked at an explicit low-shell basis calculation, not at a vague “more determinant work” step. The master closure matrix status is `C6_master_closure_matrix_built_full_operator_rescue_gate`.

Immediate next action:

- Treat the explicit `n=3` projection as nonzero at audit level: trace `80.0`, rank `6`.
- Add the missing full one-form variation terms and Hilbert-metric variation.
- Assemble the second-order `1 <-> 3` determinant trace with the `lambda_3-lambda_1=12` denominator and sign convention.

Plain-language checkpoint: the program is not allowed to claim the `pi^-4` rank-10 theorem until the third-shell leak is either killed explicitly or absorbed by a derived identity with no fitted coefficient.


## 2026-07-14 n=3 Projection Result

The roadmap gate advanced: the explicit `n=3` coexact basis was built and the leaked vectors project nontrivially into it. This closes the “maybe basis projection kills it” escape route for the current conformal-slice audit.

Next roadmap state: C6 now requires a full-operator cancellation or a derived absorption identity. If neither appears, the `pi^-4` rank-10 determinant theorem is blocked even though the rank-10 pattern remains a strong structural compression.


## 2026-07-14 Full-Operator Rescue Roadmap

Roadmap state after the nonzero `n=3` projection: compute the full one-form operator terms, not more shell-selection tests. The concrete checklist is connection variation, Ricci/curvature variation, coexact-projector variation, Hilbert-metric variation, and `delta^2 Delta` locality/cancellation.

Go/no-go: if these terms do not cancel or absorb the trace-80 `1 <-> 3` contribution without a fitted coefficient, the clean rank-10 determinant theorem is blocked.


## 2026-07-14 Quotient-Parity Gate Closed

The explicit `n=3` projection is compatible with the `L(2,1)` quotient: cubic one-form representatives are antipodal-even. This means the roadmap cannot use RP3 parity or cover normalization to discard the low-shell obstruction.

Next roadmap state: compute or prove cancellation of the remaining full one-form terms. If that fails, the determinant-theorem status of `pi^-4` fails even though the structural compression remains strong.


## 2026-07-14 Local-Counterterm Escape Closed For n=3

The concrete low-shell trace `80.0` is not a local heat-kernel asymptotic term. The roadmap should not list local finite subtraction as a valid C6 rescue for this obstruction.

Next roadmap state: compute the missing full one-form terms or derive a no-fit absorption identity. Otherwise `pi^-4` remains structural compression.


## 2026-07-14 Small-Gap Rescue Closed For n=3

The `n=3` trace is too large to be treated as the small `N_need-10` residue. The roadmap should no longer list “tiny scheme gap” as a plausible explanation for this low-shell obstruction.

Next roadmap state: the only viable C6 rescue is a derived full-operator cancellation or absorption identity.


## 2026-07-14 Full-Operator Checklist Added

Roadmap update: the next C6 work item is not generic “mixed-trace derivation.” It is the five-block full-operator checklist: connection, Ricci, coexact-projector, Hilbert metric, and `delta^2 Delta`.

A roadmap pass requires all five blocks evaluated in the same quotient-normalized low-shell basis and a no-fit cancellation/absorption result.


## 2026-07-14 Connection Formula Substep

The first full-operator checklist substep is partially advanced: the conformal-slice connection variation formula is fixed. The roadmap now needs the evaluated `C_conn[1,3]` matrix, not another statement that connection terms exist.


## 2026-07-14 Ricci Formula Substep

The second full-operator checklist substep is partially advanced: the conformal-slice Ricci variation formula is fixed. The roadmap now needs the evaluated `C_Ric[1,3]` matrix and its combination with `C_conn[1,3]`, not another reminder that curvature exists.


## 2026-07-14 Projector Formula Substep

The third full-operator checklist substep is partially advanced: the moving coexact-projector formula is fixed. The roadmap now needs `C_proj[1,3]` and a self-adjointness check, not another fixed-slice projection.


## 2026-07-14 Hilbert Formula Substep

The fourth full-operator checklist substep is partially advanced: the one-form Hilbert inner-product variation is fixed. The roadmap now needs `C_Hilb[1,3]`, basis-normalization derivatives, and self-adjointness, not just fixed-metric Gram traces.


## 2026-07-14 Delta2 Delta Gate Substep

The fifth full-operator checklist substep is now explicit: `Tr(Delta^-1 delta^2 Delta)` cannot be silently discarded while the trace-square block is treated as a theorem. It must be proven local/subtracted or exactly compensated in the same Maxwell--ghost scheme, or evaluated as a finite low-shell block `C_delta2`.

Roadmap state: the master matrix should list `delta^2 Delta` as a blocking gate with three allowed outcomes only: local heat-kernel term fixed before fitting, exact compensation, or quotient-normalized finite block computation.

## 2026-07-14 Master Matrix Sync After Delta2 Gate

The master closure matrix now includes `delta2_delta_gate` as its own blocking node. The control-panel count is `24` nodes, with `9` blocking or failed nodes.

Plain-language status: the dashboard now matches the proof work. The fifth gate is no longer a footnote; it is a red light on the main board until `C_delta2` is computed or a no-fit locality/compensation proof is supplied.

## 2026-07-14 Delta2 Finite Block Spec

The roadmap now has a concrete fallback for the fifth full-operator gate. If locality or exact compensation fails, compute diagonal `C_delta2[1,1]` and `C_delta2[3,3]` over `55` symmetric deformation pairs after fixing the second-variation path.

Plain-language status: the work order is now measurable. The `delta2` gate is no longer “some second-order term”; it is a finite diagonal trace job with a path-choice warning.

## 2026-07-14 Master Matrix After Finite Delta2 Spec

After adding `delta2_finite_block_spec`, the master closure matrix has `25` nodes and `10` blocking or failed nodes.

Plain-language status: the board got one more red card, but that is progress: the missing calculation is now named, sized, and impossible to hide inside a caveat.

## 2026-07-14 Delta2 Path-Choice Gate

The roadmap now has a gate before the finite `C_delta2` matrix: choose the second-variation path first. The preferred theorem route is `ambient_linear_embedding_strain`; `metric_geodesic_path` is allowed only if declared before numbers; `pure_conformal_test_path` is diagnostic unless a slice theorem is proven.

Plain-language status: the matrix job is not allowed to move the rails after seeing the train. The dashboard now has `26` nodes and `11` blocking or failed nodes.

## 2026-07-14 Ambient Delta2 Path Formula

The preferred path for the finite `C_delta2` theorem route is now fixed at metric level: `F_eps(x)=(I+eps A)x`, with `g'_A(u,v)=2<u,A v>` and `g''_A(u,v)=2<Au,Av>`.

Plain-language status: the rail choice is no longer open. The remaining job is harder but cleaner: derive `delta2 Delta_1,coex` on these rails and then compute the diagonal low-shell traces. The dashboard now has `27` nodes and `10` blocking or failed nodes.

## 2026-07-14 Delta2 Operator Decomposition

The roadmap now splits `delta2 Delta_1,coex` into six required formula blocks: principal second-symbol, second connection, second Ricci/curvature, second coexact-projector, second Hilbert/basis variation, and local-counterterm classification.

Plain-language status: the fifth gate is no longer a single black box. The dashboard now has `28` nodes and `11` blocking or failed nodes; the next advance must derive one of these six formulas or prove its finite projection is local/zero.

## 2026-07-14 Delta2 Principal Second-Symbol Formula

The first of the six `delta2 Delta_1,coex` subblocks is fixed at formula level: `delta2_principal_AB = -(partial_A partial_B g^{ij}) nabla_i nabla_j`, with `partial_A partial_B g^{-1}=h_A h_B+h_B h_A-k_AB`.

Plain-language status: one gear is shaped, but the machine is not assembled. The dashboard now has `29` nodes and `11` blocking or failed nodes; next work is either matrix traces for this gear or formulas for connection/Ricci/projector/Hilbert subblocks.

## 2026-07-14 Delta2 Second-Connection Skeleton

The second `delta2 Delta_1,coex` subblock is now scoped: `delta2 Gamma_AB`, inverse-metric times first-connection terms, covariant-derivative variation of `h_A`, and `delta Gamma_A delta Gamma_B` products.

Plain-language status: the second gear is located but not machined. The dashboard now has `30` nodes and `11` blocking or failed nodes; next work is full `delta2 Gamma_AB` expansion or diagonal trace evaluation after expansion.

## 2026-07-14 Delta2 Second-Ricci Skeleton

The third `delta2 Delta_1,coex` subblock is now scoped: `delta2 Ricci_AB`, mixed-index raising, first inverse-metric/first-Ricci products, and background-curvature terms from `partial_AB g^{-1}`.

Plain-language status: the curvature gear is located, but not machined. The dashboard now has `31` nodes and `11` blocking or failed nodes; next work is full `delta2 Ricci_AB` expansion or a move to projector/Hilbert skeletons.

## 2026-07-14 Delta2 Second-Projector Skeleton

The fourth `delta2 Delta_1,coex` subblock is now scoped: `delta2 Pi_coex`, scalar inverse-Laplacian second variation, codifferential second variation, side-projector terms, and cross terms with first operator variations.

Plain-language status: the moving doorway is mapped at second order, but not measured. The dashboard now has `32` nodes and `11` blocking or failed nodes; next work is full `delta2 Pi` expansion, self-adjointness, or the remaining Hilbert/local skeletons.

## 2026-07-14 Delta2 Second-Hilbert Skeleton

The fifth `delta2 Delta_1,coex` subblock is now scoped: second one-form inner product, second volume-form variation, basis transport, degenerate-shell rotations, and self-adjoint representation in the varied Hilbert metric.

Plain-language status: the second-order ruler is mapped, but not calibrated. The dashboard now has `33` nodes and `11` blocking or failed nodes; one skeleton remains: local-counterterm classification.

## 2026-07-14 Delta2 Local-Counterterm Classifier Skeleton

The sixth `delta2 Delta_1,coex` subblock is now scoped: local heat-kernel pieces, finite low-shell residuals, and same-scheme Maxwell--ghost compensation are separated.

Roadmap state: all six `delta2` skeleton gears are now named. The open work is no longer “maybe subtract something local”; it is either prove a predetermined local heat-kernel term, derive exact same-scheme compensation, or compute the finite `C_delta2` residual table.

Plain-language status: the sorter is installed, but the stones are not weighed. The dashboard now has `34` nodes and `11` blocking or failed nodes; next work is full formulas/traces, not post-hoc finite subtraction.

## 2026-07-14 Delta2 Skeleton Completion Gate

The `delta2 Delta_1,coex` skeleton phase is now complete as a scoping task. All six blocks are named: principal second-symbol, second connection, second Ricci/curvature, second coexact-projector, second Hilbert/basis, and local-counterterm classifier.

Roadmap state: the next phase is not another naming pass. It is trace work: expand the missing formulas, verify self-adjointness, prove locality/compensation if possible, or compute the finite diagonal `C_delta2[1,1]` and `C_delta2[3,3]` tables over the `55` symmetric deformation pairs.

Plain-language status: the map is complete, but the rooms are not measured. The dashboard now has `35` nodes and `11` blocking or failed nodes; C6 still cannot be upgraded.

## 2026-07-14 Delta2 Trace-Phase Priority

The trace phase now has a fixed first work order. Direct `Tr(Delta^-1 delta2 Delta)` evaluation must start with diagonal `C_delta2[1,1]` and `C_delta2[3,3]`, over the locked ambient path and `55` symmetric deformation pairs.

Roadmap state: `C_delta2[1,3]` and `C_delta2[3,1]` are archive/self-adjointness checks, not substitutes for the direct trace. The required diagonal workload is `936` entries per pair and `51480` entries before reductions.

Plain-language status: the first measuring order is fixed. Small diagonal box first, big diagonal box second, side boxes later. The dashboard now has `36` nodes and `11` blocking or failed nodes; C6 still waits for actual trace values or a locality/compensation proof.

## 2026-07-14 Delta2 C11 Setup Gate

The first diagonal trace work package is now fixed: `C_delta2[1,1]` uses the six quotient-normalized `n=1` Killing/coexact states, the locked ambient path, and `55` symmetric deformation pairs.

Roadmap state: this is the first measurement package, not the measurement. It contains `36` entries per pair and `1980` raw entries before reductions. The remaining blockers are the full second-connection, second-Ricci, second-projector, Hilbert/basis, and local/compensation expansions in one convention.

Plain-language status: the small box is prepared but empty. The dashboard now has `37` nodes and `11` blocking or failed nodes; next progress must fill operator pieces or compute `C11` entries.

## 2026-07-14 Direction Re-Audit Gate

After re-reading the wiki and linked materials, the roadmap decision is: continue C6 only as a timeboxed, computation-facing sprint. The current direction is still justified by the structured `S_vac` spine, `P02` rank lead, `kappa_Cas`, volume/sign inputs, and localized blocker. It is not justified as open-ended scoping.

Roadmap rule: the next C6 step must either expand a missing operator piece toward `C_delta2[1,1]` / `C_delta2[3,3]`, prove same-scheme locality/compensation, or explicitly trigger fallback. Good fallback tracks are the external lens-space determinant gate and the neutrino overlap lemma; EW/QCD threshold closure is important but broader.

Plain-language status: do not abandon the mine, but stop wandering in tunnels. One more shaft toward real numbers; if it is fog, switch crew to the cleaner gates.

## 2026-07-14 C6 Timeboxed Operator Sprint Gate

The next allowed C6 move is now fixed: expand the second-connection piece `delta2 Gamma_AB` on the locked ambient path toward a `C_delta2[1,1]` insertion rule. This follows the direction re-audit: continue C6 only if it becomes computation-facing.

Roadmap rule: success means matrix-enabling operator content or same-scheme locality/compensation for the second-connection piece. Failure means trigger the prepared fallback tracks: external lens-space determinant gate and neutrino overlap lemma.

Plain-language status: the timer is on. The next dig must hit stone in the `C11` box, not draw another tunnel map. The dashboard now has `38` nodes and `11` blocking or failed nodes.

## 2026-07-14 Delta2 GammaAB Expansion Formula

The timeboxed C6 sprint produced its first operator content: an explicit mixed second-connection formula in background-`nabla` convention,
`Gamma_AB^k_ij = 1/2 [ g^{kl} C_AB_ijl + m_A^{kl} C_B_ijl + m_B^{kl} C_A_ijl ]`.

Roadmap state: this is real progress beyond label-only scoping, but it is not yet a `C11` value. The next required step is rough-Laplacian insertion: `Gamma_AB` terms, `Gamma_A Gamma_B` products, and inverse-metric/first-connection crosses must be reduced against the six `n=1` Killing states.

Plain-language status: one tooth of the connection gear is cut. It still has to be mounted in the machine before it can move the `C11` box. The dashboard now has `39` nodes and `11` blocking or failed nodes.

## 2026-07-14 Delta2 Connection Laplacian Insertion

The second-connection gear is now mounted into the rough one-form Laplacian at formula-slot level. The `C11` connection contribution splits into three slots: single `Gamma_AB`, inverse-metric/first-connection cross, and `Gamma_A Gamma_B` products.

Roadmap state: this is matrix-enabling structure, but not yet a matrix. The next required step is to fully expand the product terms and reduce the three slots against the six `n=1` Killing states.

Plain-language status: the tooth is now on the shaft, but the shaft has not turned the `C11` box. The dashboard now has `40` nodes and `11` blocking or failed nodes.

## 2026-07-14 Delta2 Connection Product Terms

The `Gamma_A Gamma_B` product slot is now decomposed into three families: derivative-index products, one-form-component products, and mixed-gradient products. Double-counting guardrails are fixed against principal, single-`Gamma_AB`, metric-cross, and extra A/B symmetrization terms.

Roadmap state: the dirty double-connection piece is now organized for reduction, but not integrated. Next work is exact index cleanup and reduction against the six `n=1` Killing states.

Plain-language status: the messy double gear is sorted into three baskets. The dashboard now has `41` nodes and `11` blocking or failed nodes; next step is counting teeth, not adding baskets.

## 2026-07-14 Delta2 Product Index Cleanup

The `Gamma_A Gamma_B` product slot has advanced from family sorting to an exact free-index operator table:

```text
P_AB(alpha)_c = -g^{ij}[Gamma_A^p_ij Gamma_B^d_pc
                         + Gamma_A^p_ic Gamma_B^d_jp
                         - Gamma_B^d_jc Gamma_A^p_id] alpha_d
                + A<->B.
```

Roadmap state: this is matrix-enabling cleanup for `C_conn2[1,1]`, not a computed matrix value. The next accepted move is explicit insertion of the ambient-path `Gamma_X` formulas and quotient integrals against the six `n=1` Killing one-forms.

Plain-language status: the three product teeth are now labelled by indices. The dashboard remains blocked until those teeth are integrated into the `C11` box.

## 2026-07-14 Delta2 Product Gamma Insertion

The product part of the second-connection block is now rewritten from abstract connection factors into first-strain tensors using `Gamma_X^k_ij = 1/2 g^{kl} C_X_ijl`. The matrix-enabling formula is:

```text
P_AB(alpha)_c = -1/4 g^{ij}[g^{pq} C_A_ijq g^{de} C_B_pce
                              + g^{pq} C_A_icq g^{de} C_B_jpe
                              - g^{de} C_B_jce g^{pq} C_A_idq] alpha_d
                + A<->B.
```

Roadmap state: this advances `C_conn2[1,1]` from index cleanup to an actual `C_A C_B` integrand template. The dashboard now has `42` nodes and still blocks on quotient integration and the remaining connection slots.

Plain-language status: the product teeth are now made from real strain material, but they have not touched the six Killing vectors yet.

## 2026-07-14 Delta2 Product Ambient Simplification

The locked ambient strain path collapses the product subslot. For `h_A(Y,Z)=2<Y,A Z>`, the connection tensor is `C_A(X,Y,Z)=-4<X,Y><Z,A x>`, hence `Gamma_A^p_ij=-2 g_ij a_A^p` with `a_A=(A x)^T`. The A/B-symmetrized product operator becomes:

```text
P_AB(alpha)_c = -12 [ a_A_c <a_B,alpha> + a_B_c <a_A,alpha> ].
```

Roadmap state: this is a real simplification of the product part of `C_conn2[1,1]`. The next task is no longer a full Christoffel-product contraction; it is finite moment integration of pairings `<E_ij,a_A>` over `L(2,1)`. The dashboard now has `43` nodes and still no `C11` number.

Plain-language status: the product gear shrank from a box of teeth to two arrows `a_A`, `a_B`. Now we have to measure how those arrows overlap the six Killing rulers.

## 2026-07-14 Delta2 Product C11 Moment Table

The simplified product operator has now been integrated against the six `n=1` Killing states in a raw `Sym^2(R4)` strain basis. The moment identity is:

```text
Integral <E_r,a_A><a_B,E_s> dV = Tr(sym(Omega_r^T A) sym(Omega_s^T B))/6,
C_rs(A,B) = -12 [M(r,A;s,B) + M(r,B;s,A)].
```

Roadmap state: this is the first real `C11` subslot table. All `55` symmetric strain pairs are nonzero for the `Gamma_A Gamma_B` product piece, with ranks from `1` to `5`. Therefore product terms cannot be dismissed; any final cancellation must come from the single-`Gamma_AB`, metric-cross, Ricci, projector, Hilbert/basis, or compensation pieces. The dashboard now has `44` nodes.

Plain-language status: one gear finally touched the six rulers, and it moved in every direction. We still need the other gears before saying whether the whole machine cancels.

## 2026-07-14 Delta2 Single GammaAB Ambient Simplification

The neighboring connection gear, single `Gamma_AB`, now also collapses on the locked ambient path. The mixed connection has the form:

```text
Gamma_AB^k_ij = g_ij w_AB^k,
w_AB = -((AB+BA)x)^T + 4 A_T a_B + 4 B_T a_A,
with a_A=(Ax)^T and a_B=(Bx)^T.
```

Equivalently, preserving the tangent-endomorphism notation, `w_AB=-ell_AB+4 A_T a_B+4 B_T a_A`. The resulting rough-Laplacian slot is:

```text
L_single_GammaAB(alpha)_c = (nabla_c w_AB^d) alpha_d
                            + 2 w_AB^d nabla_c alpha_d
                            + 3 w_AB^d nabla_d alpha_c.
```

Roadmap state: this is the formula gate for the second connection's non-product slot. The product slot already has a nonzero `C11` moment table; this single-`Gamma_AB` slot is now ready for its own moment table. The dashboard now has `45` nodes.

Plain-language status: the second gear is now a single arrow `w_AB`. It has not touched the six rulers yet, but it is no longer a bulky tensor.

## 2026-07-15 Delta2 Single GammaAB C11 Moment Table

The single `Gamma_AB` slot has now been measured against the six `n=1` Killing states. The finite table uses

```text
C_rs(A,B)=Integral <e_r,L_single(e_s)> dV_g,
L_single(alpha)_c=(nabla_c w_AB^d)alpha_d+2w_AB^d nabla_c alpha_d+3w_AB^d nabla_d alpha_c.
```

Roadmap state: this is the second real connection `C11` subslot table. It is nonzero for `52/55` raw symmetric strain pairs, with rank distribution `0:3`, `2:12`, `4:36`, `6:4`. Since the product subslot was nonzero for all `55` and had a different rank distribution, there is no cheap proportional cancellation. The dashboard now has `46` nodes.

Plain-language status: the second gear also touched the six rulers. It moves in most directions, but not exactly like the first gear. The full connection block still needs the metric-cross gear.

## 2026-07-15 Delta2 Metric-Cross Ambient Formula

The remaining connection slot, inverse-metric / first-connection cross, now has an ambient-path operator formula. With `S_A=P_TAP_T`, `a_A=(Ax)^T`, and `tau_A=Tr_T(S_A)`,

```text
L_cross[A|B](alpha)_c
  = 4 (S_A)^i_c (nabla_i a_B^d) alpha_d
    + 8 (S_A)^i_c a_B^d nabla_i alpha_d
    + 4 tau_A a_B^d nabla_d alpha_c,
L_metric_cross_AB=L_cross[A|B]+L_cross[B|A].
```

Roadmap state: the second-connection `C11` block now has all three subslot formulas: product, single `Gamma_AB`, and metric-cross. Two of them already have finite moment tables; the third is formula-ready but not measured. The dashboard now has `47` nodes.

Plain-language status: all three connection gears are now shaped. Two have touched the six rulers; the third is ready to touch them next.

## 2026-07-15 Delta2 Metric-Cross C11 Moment Table

The third second-connection subslot has now been measured. The metric-cross table uses

```text
C_rs(A,B)=Integral <e_r,L_metric_cross_AB(e_s)> dV_g.
```

Roadmap state: all three connection subslot tables are now available in the same raw strain basis. Metric-cross is nonzero for all `55` symmetric strain pairs, with rank distribution `4:39`, `6:16`. Product was nonzero for all `55`; single `Gamma_AB` was nonzero for `52/55`. The dashboard now has `48` nodes.

Plain-language status: the third gear also moves. Now the connection machine can finally be assembled by adding the three gear tables.

## 2026-07-15 Delta2 Full Connection C11 Assembly

The three connection subslot tables have now been added:

```text
C_conn2[1,1]=C_product+C_single_GammaAB+C_metric_cross.
```

Roadmap state: the assembled second-connection block is nonzero for all `55` raw symmetric strain pairs. Its rank distribution is `2:6`, `4:39`, `6:10`. Therefore internal cancellation inside the connection block is ruled out. The dashboard now has `49` nodes.

Plain-language status: the three connection gears were assembled into one machine. The machine still moves in every direction. If C6 cancels, the cancellation must come from other machines: Ricci, projector, Hilbert/basis, principal, or compensation.

## 2026-07-15 Tome II Status Sync

The main manuscript `tome2_s2t_spectral_closure.tex` now includes the latest C6/C11 status in its conclusion. It states that `C_conn2[1,1]` has been assembled from product, single-`GammaAB`, and metric-cross tables, is nonzero for all `55` raw symmetric strain pairs, and has rank distribution `2:6`, `4:39`, `6:10`.

Plain-language status: the book no longer lags behind the wiki on the connection block. It now says clearly: connection does not cancel itself, so any C6 rescue must come from the other blocks.

## 2026-07-15 Delta2 Principal C11 Moment Table

The principal second-symbol block has now been measured on the same six `n=1` Killing states. The computation uses

```text
L_pr(K)=tr_T(H_AB)K-H_ABK,
H_AB=4(S_A S_B+S_B S_A)-P_T(AB+BA)P_T.
```

Roadmap state: this is the first non-connection `C11` table. It is nonzero for all `55` raw symmetric strain pairs, with rank distribution `4:39`, `6:16`. The dashboard now has `50` nodes.

Plain-language status: the principal gear also moves in every direction. Next we must add it to the connection machine; only then can we see whether those two large blocks cancel or reinforce.

## 2026-07-15 Delta2 Principal Plus Connection C11 Assembly

The principal and assembled connection `C11` tables have now been added:

```text
C_principal_plus_connection[1,1]=C_principal[1,1]+C_conn2[1,1].
```

Roadmap state: the combined block is nonzero for all `55` raw symmetric strain pairs, with rank distribution `4:39`, `6:16`. Principal does not cancel connection. The dashboard now has `51` nodes.

Plain-language status: two big machines are now bolted together, and the combined machine still moves in every direction. The rescue must come from Ricci, projector, Hilbert/basis, or compensation.

## 2026-07-15 C11 Table Reverification

A separate verifier recomputed representative entries directly from the product, single-`GammaAB`, metric-cross, and principal formulas, then checked every stored assembly. The verification passed: `56` direct sample entries matched, all `55` connection sums matched, and all `55` principal-plus-connection sums matched.

Plain-language status: the arithmetic did not fall apart under recheck. The current nonzero conclusions for connection and principal+connection survive this sanity pass.

## 2026-07-15 Finite Spectral Residue Gap Scan

An A--E controlled side scan has been filed as [[finite-spectral-residue-gap]]. It checks whether missing mosaic pieces for the `pi^-4` route are more likely to come from new physics or from determinant bookkeeping.

Roadmap state: the scan does not close C6. It identifies the most promising next proof-risk target as the small gap `N_need-10=0.0099700224`, with candidate sources in same-scheme `det'`, Hodge-Jacobian, gauge-volume, zero-mode, scalar ghost, projector, and Hilbert/basis normalization. This supports continuing the C6 work through projector/Hilbert/compensation checks before inventing a new sector.

Plain-language status: we found the likely missing screw is in the measuring apparatus, not in a new machine. The next job is to test the ruler, gauge volume, and projector bookkeeping.

## 2026-07-15 Finite Gap Source Audit

The focused source audit [[finite-gap-source-audit]] now ranks candidate explanations for the gap. It keeps `det'`, Hodge/Jacobian, and gauge volume as required same-scheme bookkeeping, but does not treat them as sufficient by themselves. Scalar ghost half-power leakage is classified as a downgrade trigger because it changes the effective rank from `10` toward `5`. The best live rescue components are coexact-projector variation, Hilbert/basis transport, and a pre-fixed local/finite subtraction convention.

Roadmap state: next C6 work should prioritize projector and Hilbert/basis blocks over broad new-sector searches. Ricci remains required, but the audit marks it as less likely to explain the small scheme gap by itself.

Plain-language status: the table says which screws are still worth turning. The dangerous loose screw is scalar ghost leakage; the useful screws are projector and Hilbert/basis transport.

## 2026-07-15 Projector Hilbert Rescue Sprint

The next computation-facing sprint is now filed as [[projector-hilbert-rescue-sprint]]. It translates the two best live rescue components into pass/fail gates: expand `delta2 Pi_coex`, fix scalar `det'` inverse conventions, verify self-adjointness in the varied Hilbert metric, choose a canonical basis transport, compute Gram corrections, and prioritize diagonal `C_delta2[1,1]` / `C_delta2[3,3]` traces.

Roadmap state: C6 should now proceed through projector first, then Hilbert/basis transport. The sprint succeeds only by producing a finite contribution, a same-scheme locality/subtraction proof, or a clean downgrade trigger. It does not succeed by adding labels or nearby integers.

Plain-language status: the next job is to test the moving doorway and the moving ruler. If they do not move the obstruction, `pi^-4` likely stays structural compression rather than theorem.

## 2026-07-15 Delta2 Projector Expansion Gate

The second coexact-projector variation has been expanded as a formula gate in [[delta2-projector-expansion-gate]]. With `D=delta_g`, `L=Delta_0`, and `G=L^{-1}_{det'}` on zero-mean scalar modes,

```text
G_AB = G L_A G L_B G + G L_B G L_A G - G L_AB G,
Pi_AB = -d[ G_AB D + G_A D_B + G_B D_A + G D_AB ].
```

Roadmap state: this advances projector work from skeleton to explicit expansion identity. It is still not a matrix result: the ambient-path formulas for `D_A`, `D_AB`, `L_A`, and `L_AB` must be expanded before quotient integrals can be trusted.

Plain-language status: the moving doorway now has named hinges. We still need to measure how far those hinges move.

## 2026-07-15 Scalar Codifferential Ambient Gate

The ambient-path formula slots needed by `Pi_AB` are now filed in [[scalar-codifferential-ambient-gate]]. With the positive scalar Laplacian `L f=-g^{ij}nabla_i nabla_j f` and codifferential `D alpha=-g^{ij}nabla_i alpha_j`, the first variations are

```text
L_A f = h_A^{ij} nabla_i nabla_j f + C_A^k nabla_k f,
D_A alpha = h_A^{ij} nabla_i alpha_j + C_A^k alpha_k,
C_A^k = g^{ij} Gamma_A^k_ij.
```

The mixed variations are expressed through `p_AB=partial_AB g^{-1}` and `Gamma_AB`:

```text
L_AB f = -p_AB^{ij} Hess_ij(f) + p_A^{ij} Gamma_B^k_ij nabla_k f
       + p_B^{ij} Gamma_A^k_ij nabla_k f + g^{ij} Gamma_AB^k_ij nabla_k f,
D_AB a = -p_AB^{ij} nabla_i a_j + p_A^{ij} Gamma_B^k_ij a_k
       + p_B^{ij} Gamma_A^k_ij a_k + g^{ij} Gamma_AB^k_ij a_k.
```

Roadmap state: projector work has moved from naming `Pi_AB` to identifying the four operator slots that enter it. No quotient matrix has been computed yet.

Plain-language status: the doorway hinges now have motion formulas. Next we substitute the ambient simplifications and measure them against the low-shell bases.

## 2026-07-15 Projector Ambient Substitution Gate

The ambient substitution for the projector slots is now filed in [[projector-ambient-substitution-gate]]. The first variations reduce to

```text
L_A f = 2 S_A^{ij} nabla_i nabla_j f - 6 a_A^k nabla_k f,
D_A alpha = 2 S_A^{ij} nabla_i alpha_j - 6 a_A^k alpha_k.
```

The mixed second variations reduce to

```text
L_AB f = -p_AB^{ij} Hess_ij(f) + b_AB^k nabla_k f,
D_AB alpha = -p_AB^{ij} nabla_i alpha_j + b_AB^k alpha_k,
b_AB = 4 tau_A a_B + 4 tau_B a_A + 3 w_AB.
```

Roadmap state: projector work now uses the same ambient building blocks as the connection block: `a_A`, `S_A`, `tau_A`, `w_AB`, and `p_AB`. The next obstacle is scalar Green-chain reduction, not tensor naming.

Plain-language status: the door hinges are now made from the same parts as the gears we already measured. Next we need the Green-chain moments.

## 2026-07-15 Projector Green Chain Reduction Gate

The scalar Green-chain reduction protocol is now filed in [[projector-green-chain-reduction-gate]]. It separates the deformation-space rank `P02=1+9` from the scalar Green inverse `G=Delta_0^{-1}_{det'}`: `ell=0` is part of the deformation trace direction but is excluded from `G`, while nonzero even shells `ell=2,4,6,...` must be handled honestly.

Roadmap state: projector work has reached the spectral accounting gate. The next accepted output is a shell-transition table for `L_A` and `L_AB`, showing whether higher even shells leak into the projector contribution or are removed by a same-scheme locality/subtraction rule.

Plain-language status: we cannot just keep `ell=0,2` by hand. The next job is to prove whether the Green chains stay in the small box or leak upward.

## 2026-07-15 Projector Shell Transition Table

The first projector shell-leakage table is now filed in [[projector-shell-transition-table]]. Selection rules give

```text
L_A:  ell -> ell-2, ell, ell+2,
L_AB: ell -> ell-4, ell-2, ell, ell+2, ell+4,
```

within the even `RP^3` scalar sector. Thus `ell=2` can leak to `ell=4` under `L_A`, and to `ell=4,6` under `L_AB` or double `L_A G L_B` chains.

Roadmap state: representation selection alone does not close projector Green chains to the `P02=1+9` window. The next accepted output is either explicit coefficient vanishing for the relevant quotient contractions, a same-scheme locality/subtraction theorem for higher shells, or a downgrade of rank-10 projector theorem status.

Plain-language status: the door can swing to higher floors. We now need to prove those floors do not count, or count them honestly.

## 2026-07-15 Projector Higher Shell Witness

The higher-shell warning has an explicit witness in [[projector-higher-shell-witness]]. Taking the `ell=2` harmonic `q=x1^2-x2^2`, the degree-4 harmonic projection of `q^2` is nonzero. Equivalently, `ell=2 x ell=2` contains a genuine `ell=4` component on `S^3`, descending compatibly to the even `RP^3` scalar sector.

Roadmap state: higher-shell leakage is no longer just “allowed by selection rules”; it is explicitly present at the scalar harmonic level. The next C6 projector step must test whether the relevant quotient contractions vanish or whether a same-scheme locality/subtraction theorem removes the higher shells.

Plain-language status: the higher floor exists. Now we must prove it is empty in this determinant problem, or include it.

## 2026-07-15 Projector Coefficient Test Protocol

The concrete coefficient tests are now filed in [[projector-coefficient-test-protocol]]. The first dangerous families are

```text
T1 = <ell=4 | L_A | ell=2>,
T2 = <ell=4 | L_AB | ell=0>,
T3 = <ell=4 | L_AB | ell=2>,
T4 = <ell=6 | L_A G L_B | ell=2>,
T5 = low one-form quotient contraction of the dangerous scalar pieces.
```

Roadmap state: the next accepted projector output is no longer another selection-rule page. It is a coefficient witness or cancellation theorem for T1--T5. Nonzero coefficients that survive quotient contraction force higher-shell inclusion or downgrade; structural vanishing keeps projector rescue alive.

Plain-language status: now we have five door-sensor tests. If any sensor fires and reaches the low one-form room, rank-10 projector closure is in trouble.

## 2026-07-15 Projector T1 Coefficient Witness

The first coefficient sensor has fired in [[projector-t1-coefficient-witness]]. For `A=diag(1,-1,0,0)` and `q=x1^2-x2^2`, the quartic part of `L_A q` on `S^3` contains `20(x1^2-x2^2)^2`, whose degree-4 harmonic projection is nonzero. Hence

```text
<ell=4 | L_A | ell=2> != 0
```

at symbolic witness level.

Roadmap state: `G L_A G` is not rank-10-closed by coefficient structure. Projector rescue now depends on T5-style low one-form quotient contraction vanishing, a same-scheme locality/subtraction theorem, or inclusion of higher scalar shells.

Plain-language status: the first door sensor fired. The leak reaches `ell=4`; now we must see whether it reaches the one-form room.


## 2026-07-15 Projector T2/T3 Coefficient Witness

The next coefficient page [[projector-t2-t3-coefficient-witness]] separates the constant and first nonzero scalar inputs for the mixed second projector slot. `T2=<ell=4|L_AB|ell=0>` vanishes because `L_AB(1)=0`. But for `A=B=diag(1,-1,0,0)` and `q=x1^2-x2^2`, the quartic part of `L_AA q` has a nonzero degree-4 harmonic projection, so

```text
T3=<ell=4|L_AB|ell=2> != 0
```

at symbolic witness level.

Roadmap state: both first-order and mixed-second projector scalar slots can leak from `ell=2` to `ell=4`. The trace scalar input is safe for `L_AB`, but this does not rescue rank-10 closure. The next decisive check is T5: whether these scalar leaks survive the low one-form quotient contraction.

Plain-language status: one sensor is quiet, one more sensor fired. The leak is not just in the first hinge; the second hinge can leak too.

## 2026-08-02 Consolidated Decision Roadmap

The success/failure audit and the next project phases are consolidated in [[research-roadmap-2026-08-02]]. The immediate `C6` decision gate is `T5`: pair the nonzero `T1/T3` scalar leakage with the quotient-normalized low one-form states through the relevant `dG` projector terms.

Roadmap state: if the dangerous contractions vanish structurally, continue to `T4`, full `C_delta2[1,1]`, and same-scheme determinant assembly. If a contraction survives, either include the required higher shells or downgrade exact `pi^-4` absorption; do not continue nearby-integer searches.

Plain-language status: we now have a finish line. First test whether the leak reaches the physical room; then either complete the machine or honestly lower the claim.

## 2026-08-02 Projector T5 Quotient Table

The direct T5 calculation is filed in [[projector-t5-quotient-contraction-table]]. It uses the complete `ell=4` scalar shell (`25` columns) and the quotient-normalized low coexact one-form basis (`6` `n=1` plus `30` `n=3` rows). The `36 x 25` table has maximum raw entry `2.77e-16` and numerical rank `0`.

Roadmap state: the pure outer-`dG` `Pi_AB` leakage is removed exactly by `<beta_coex,dG phi>=<delta beta_coex,G phi>=0`. This also means a direct `T4` higher-shell scalar in the same outer-`dG` position cannot reach the coexact matrix. The remaining projector bottleneck is the cross-return term `Pi Delta_{1,A} Pi_B + A<->B`, where the varied one-form operator acts before final projection.

Plain-language status: the leak reaches the hallway but not the physical room. We must now test whether the moving one-form operator can carry it back through another door.

## 2026-08-02 Cross Return And Hilbert Similarity Verdict

The cross-return channel closes structurally because `Delta_1(g)d=dDelta_0(g)`: exact forms remain exact under the Hodge Laplacian and its metric variation.

The first Hilbert calculation gives `M_31=-12H_31` and changes the visible self-adjoint cross norm squared from `80` to `180`. Carrying the similarity representation through second order shows that this apparent worsening is exactly compensated:

```text
raw determinant trace-square             = 5.0,
self-adjoint representation trace-square = 5.625,
second similarity trace                  = 0.625,
raw logdet Hessian                        = -5.0,
self-adjoint logdet Hessian               = -5.0.
```

Direct finite differences give zero Hessian difference. This is required by `det(G^(1/2)L G^(-1/2))=det(L)`.

Roadmap state: projector and Hilbert/basis transport neither rescue nor worsen C6 at determinant level. The active gate is now the genuine mixed second Hodge operator `L_AB`, especially the Ricci/curvature block and its combination with the already nonzero principal+connection C11 table.

Plain-language status: the doorway and measuring ruler are now understood. They change the appearance of the obstacle but not its determinant weight. The next calculation must target the real second-order physics.

## 2026-08-02 Ricci C11 Gauss Table

The curvature block is now computed in [[ricci-c11-gauss-table]] using the exact Gauss equation for the linearly deformed sphere. The Ricci table has rank distribution `0:12`, `4:27`, `6:16`. Its pure-scaling control gives `delta2 Ric#=12I` exactly, and independent pointwise finite differences agree to about `1.6e-6`.

After adding Ricci to the existing principal-plus-connection table, every one of the `55` strain pairs remains nonzero, with rank distribution `4:39`, `6:16`. For `A=diag(1,-1,0,0)`, the combined matrix is

```text
diag(44/3,22/3,22/3,22/3,22/3,12).
```

Roadmap state: geometric C11 cancellation has failed. Projector is closed, Hilbert is determinant-neutral, and Ricci reinforces rather than cancels the principal+connection block. The next and final live C6 rescue class is same-scheme determinant bookkeeping; without a mandatory compensation, exact `pi^-4` absorption must be downgraded.

Plain-language status: all geometric gears are now assembled, and the machine still moves in every direction. Only the determinant accounting can still stop it; otherwise this rescue route ends.

## 2026-08-02 Final Same-Scheme Determinant Verdict

The final determinant accounting is filed in [[c6-final-same-scheme-verdict]]. No mandatory compensation is found in the declared scheme:

- standard covariant FP leaves the nonzero scalar half-determinant;
- `det'`, zero modes, gauge volume and the Hodge Jacobian do not create an opposite nonzero tower;
- projector and Hilbert/basis transport are neutral at determinant level;
- local counterterms cannot erase finite low-shell spectral data;
- no mandatory same-spectrum paired sector is present;
- the physical transverse quotient is a conditional primary definition, not a derived cancellation.

Roadmap state: `C6` is no longer an active rescue gate. The exact `pi^-4` determinant theorem is downgraded to structural compression, `S_vac` stays conditional, and the primary proof vector moves to the neutrino overlap lemma plus external reproducibility.

Plain-language status: this tunnel ends here. The project continues through a different tunnel, with the failed claim clearly marked rather than hidden.
