# Tome 2 Proof Chain

> Status: working
> Type: synthesis
> Updated: 2026-07-09

## Summary

This page extracts the main proof chain from `s2t/docs/tome2_s2t_spectral_closure.tex`. It records which Tome II claims have an explicit derivation path, what each derivation depends on, and what would invalidate it. The purpose is to support management-level review of Tome II without confusing numerical reproduction with proof.

## Proof Chain Map

- Compact carrier `K = RP^3 x S^1` — derived in the minimal S2T carrier class from `Z_A = pi^2`, phase step `pi`, and absence of continuous `U(1)` moduli.
- Spin shift `k + 1/2` — derived from the nontrivial spin structure on `S^1`, equivalent to antiperiodic spinor boundary conditions.
- `pi` term in `S_geo` — attributed to the nontrivial `Z_2` flat holonomy branch on `RP^3`.
- `1/24` coefficient — formerly attributed to a one-dimensional Maxwell--ghost--Dirac combination; after the 2026-07-10 audit, the safe statement is narrower: the constant periodic Maxwell--ghost branch supports `1/24`, while a naive Maxwell--ghost--Dirac cancellation of the coexact tower is rejected. See [[coexact-tower-delta]].
- `1/(pi^4 S^2)` term — attributed to a fourth zeta residue and second-order scale suppression.
- QED shift `-alpha/3` — conditional normalization claim. The compact loop is finite, but the displayed sum does not yield `1/3` without an uncomputed `RP3` projection factor.
- Tau formula — numerically unique in the frozen low-complexity grammar, but the seed `pi^2 + 2pi + 2/3` is currently a premise rather than an operator eigenvalue.
- Higgs EFT bridge — derives `v_S2T`, `lambda_H`, and `M_H` from a minimal effective potential `U(H, chi)` without using `G_F`, `M_W`, `M_Z`, or `M_H` as train inputs.

## Expected Result

If the proof chain is correct, Tome II version II.A has a restricted but real closure result:

- electromagnetic vacuum closure is not merely numeric because the carrier, holonomy, zeta, and subtraction terms are assigned structural roles;
- the charged-lepton relation is not a trivial dense rational fit inside the tested grammar, but its operator derivation remains conditional;
- the Higgs row is an EFT bridge closure because it follows from the potential minimum and fixed spectral residues;
- the remaining neutrino and EW/QCD gaps stay outside the successful closure set.

## Compliance Checks

- Machine reproduction is delegated to `s2t/audits/s2t_tome2_audit.py` and `s2t/results/s2t_tome2_results.json`.
- Numerical rows remain reproducible, but `m_tau`, `v_S2T`, and `M_H` now carry conditional derivation status; only `lambda_H` retains its independent spectral-normalization status inside this chain.
- The audit explicitly does not close the neutrino Dirac insertion or EW/QCD thresholds.
- The Tome II no-go criteria require demotion if any closed block needs a hidden continuous parameter or post-hoc fitted coefficient.

## TeX Source Alignment

- TeX source now reflects this conditional status: the conclusion marks `S_vac` as conditional success, not unconditional mature closure.

## Remaining Proof Risks

- The carrier derivation is minimal-class uniqueness, not absolute uniqueness among all compact spaces.
- The `1/24`, zeta-residue, and QED finite-part assignments should be cross-checked against the stricter RPFT derivation files before being marked mature.
- The Higgs EFT bridge is a bridge closure; it should not be advertised as a full microscopic electroweak derivation.
- The neutrino matrix remains partial until `m_D^(nu) = sqrt(pi + pi^{-1}) m_e^2 / m_mu` is derived from a defined Lagrangian or operator overlap.
- EW/QCD remains II.B until threshold masses, KK tower structure, `Sigma_8/Sigma_3`, and two-loop RG are derived without hidden fitting.

## Management Status

- Problem: Tome II needs proof-level organization, not only a source summary.
- Search for solution: extracted the main derivation nodes from the carrier, spin, zeta/vacuum, QED, tau, and Higgs sections.
- Expected result: readers can see why II.A is partially successful and exactly where II.B begins.
- Compliance check: each proof node is paired with its dependency and demotion risk.

## Links

- [[tome2-s2t-spectral-closure]] — primary source page for Tome II.
- [[s2t-closure-roadmap]] — closure status map consuming this proof chain.
- [[tome2-svac-em-block-audit]] — focused audit of the strongest electromagnetic closure block.
- [[kappa-cas-one-over-24]] — focused proof-risk page for the finite determinant coefficient.
- [[numerical-audits]] — machine evidence for closed numerical rows.
- [[neutrino-overlap-lemma]] — open proof target outside the II.A success set.
- [[ew-qcd-threshold-closure]] — open threshold target outside the II.A success set.

## Source Notes

- Source path: `s2t/docs/tome2_s2t_spectral_closure.tex`.
- Key source sections: compact carrier, gauge normalization, Dirac/spin structures, zeta regularization, final vacuum scalar, tau mass, one-loop QED shift, Higgs scale and self-coupling.
- This page is a synthesis layer; source-level equations remain in the TeX file.