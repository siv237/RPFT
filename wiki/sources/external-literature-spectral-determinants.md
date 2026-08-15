# External Literature: Spectral Determinants

> Status: literature gate
> Type: source
> Updated: 2026-07-10

## Purpose

This page records the external literature that must constrain the S2T electromagnetic determinant program, especially the proposed mixed-trace origin of the integer `10` in the `pi^-4` residue.

## Why This Gate Is Needed

The internal S2T audit found:

```text
N_need = 10.0099700224 ≈ 10 = d_0 + d_2 = 1 + 9
```

where `d_0` and `d_2` are the first two even scalar degeneracies on `RP^3`. This is strong internal evidence, but it is not enough. A mature claim must be checked against the standard literature on:

- spectra of functions and `p`-forms on lens spaces;
- Hodge decomposition and exact/coexact modes;
- Ray-Singer analytic torsion;
- gauge-fixed Maxwell/Faddeev-Popov determinant bookkeeping;
- zero-mode and `det'` conventions.

## Source Clusters

### Ray-Singer Analytic Torsion

Relevant authors: D. B. Ray, I. M. Singer.

Why it matters:

- Analytic torsion is built from zeta-regularized determinants of Laplacians on forms.
- It gives the classical determinant language for comparing scalar, exact, coexact, and harmonic sectors.
- Any S2T claim about determinant residues or torsion-like finite parts should be compatible with this framework.

Key external anchor:

- Ray and Singer's 1971/1973 analytic torsion program, including `R`-torsion and Laplacian determinants.

### Schwarz Gauge-Functional / Partition-Function Line

Relevant author: A. S. Schwarz.

Why it matters:

- Degenerate quadratic gauge functionals require gauge fixing and determinant normalization.
- Schwarz-type arguments connect gauge partition functions, zero modes, and Ray-Singer torsion.
- The S2T Maxwell--ghost branch should not choose determinant factors independently of this tradition.

Key external anchor:

- Schwarz's work on degenerate quadratic functionals and Ray-Singer invariants.

### Lens-Space Spectra on `p`-Forms

Relevant authors: A. Ikeda, Y. Yamamoto, E. Lauret, R. J. Miatello, J. P. Rossetti.

Why it matters:

- `RP^3` is `L(2,1)`, so lens-space spectra are the direct mathematical reference class.
- The literature studies Laplace spectra on functions and forms, including `p`-spectra and isospectrality.
- The S2T exact/coexact/scalar degeneracy bookkeeping must be compared to these formulas, not only to inherited `S^3` intuition.

Key external anchors:

- Ikeda--Yamamoto on spectra of three-dimensional lens spaces.
- Lauret--Miatello--Rossetti on `p`-form spectra of lens spaces and congruence-lattice descriptions.

### Faddeev-Popov / BRST Ghost Determinants

Relevant authors: L. D. Faddeev, V. N. Popov, later BRST literature.

Why it matters:

- Gauge-fixed Maxwell theory introduces scalar ghost determinants.
- The sign and determinant exponent depend on bosonic/fermionic Gaussian integration and gauge choice.
- The S2T mixed-trace claim must prove that ghost/exact cancellations leave the proposed finite scalar rank rather than removing it.

## What The Literature Supports

The external literature supports the following background assumptions:

- It is legitimate to decompose gauge-field determinants into Hodge sectors.
- Scalar, exact, coexact, and harmonic sectors must be tracked separately.
- Lens-space `p`-form spectra are a known, nontrivial subject and should constrain `RP^3` claims.
- Analytic torsion is the standard invariant language for determinant combinations of Laplacians on forms.
- Gauge fixing and ghosts can change determinant powers and signs, so they cannot be treated heuristically.

## What The Literature Does Not Yet Prove For S2T

The literature gate does **not** by itself prove:

- that the S2T mixed trace equals `d_0+d_2`;
- that only the `ell=0,2` scalar/even shells enter;
- that higher even shells `ell=4,6,...` are excluded by a valid operator selection rule;
- that the sign is exactly the S2T sign after ghost and `det'` conventions;
- that the remaining `3.04e-6` mismatch is a legitimate finite local-scheme residue.

## Required Next Proof Obligations

Before the `10` can be upgraded from strong candidate to theorem, S2T must provide:

1. A gauge-fixed Maxwell--ghost determinant formula on `RP^3 x S^1`.
2. A precise Hodge decomposition into harmonic, exact, coexact, and scalar/ghost sectors.
3. A lens-space p-form multiplicity table for `L(2,1)` checked against external formulas.
4. A second-order mixed-trace derivation showing the sign and rank.
5. A selection rule explaining why the trace rank is `1+9`, not `1`, `9`, `1+9+25`, or another allowed integer.
6. A no-go statement: if external p-form spectra or ghost normalization contradict the selection rule, the `10` remains numerological compression.

## Relation To Tome II

Tome II now contains an external-literature gate for the electromagnetic determinant block. The gate protects the model from treating an internally successful audit as a literature-backed theorem too early.

## Links

- [[tome2-svac-em-block-audit]] — internal EM block audit.
- [[coexact-tower-delta]] — open coexact tower problem.
- [[kappa-cas-one-over-24]] — `1/24` determinant branch.
- [[tome2-s2t-spectral-closure]] — main Tome II source.

## Source Notes

- Source paths: `s2t/results/external_literature_spectral_determinants_results.json`, `s2t/results/s2t_determinant_casmix_results.json`, `s2t/results/s2t_integer10_origin_results.json`.
- External anchors checked 2026-07-10:
  - A. Ikeda and Y. Yamamoto, “On the spectra of 3-dimensional lens spaces”, Osaka J. Math. 16 (1979), PDF: `https://projecteuclid.org/journals/osaka-journal-of-mathematics/volume-16/issue-2/On-the-spectra-of-3-dimensional-lens-spaces/ojm/1200772263.pdf`.
  - E. Lauret, “Spectra of lens spaces from 1-norm spectra of congruence lattices”, arXiv: `https://arxiv.org/abs/1604.02471`.
  - E. Lauret, R. J. Miatello, J. P. Rossetti, “Spectra of lens spaces from 1-norm spectra of congruence lattices”, journal/arXiv cluster; use as the modern lens-space `p`-spectrum reference line.
  - C. Nash and D. J. O'Connor, “Determinants of Laplacians on lens spaces”, arXiv: `https://arxiv.org/abs/hep-th/9212022`.
  - A. S. Schwarz, “The partition function of degenerate quadratic functional and Ray-Singer invariants”, Lett. Math. Phys. 2 (1978), DOI page: `https://doi.org/10.1007/BF00406412`.

## 2026-07-10 External Literature Verification Audit

Immediate literature check result: the project may keep the absorption route as a live hypothesis, but it must not be marked as a theorem yet.

### What is externally supported

- `RP^3` is the lens space `L(2,1)`, so the correct reference class is lens-space spectra, not only informal `S^3` mode counting.
- Ikeda--Yamamoto is a primary source for spectra of three-dimensional lens spaces. This supports treating `L(2,1)`/`RP^3` multiplicities as a literature-constrained object.
- Lauret / Lauret--Miatello--Rossetti give a modern congruence-lattice formulation for lens-space spectra, including `p`-form spectra. This is the right external framework for verifying coexact/exact one-form multiplicities.
- Nash--O'Connor explicitly treat determinants of Laplacians on lens spaces. This supports checking the S2T finite determinant branch against actual lens-space determinant technology rather than a purely local heat-kernel argument.
- Schwarz and Ray--Singer support the general rule that gauge determinants, zero modes, and analytic torsion must be handled together; ghost factors cannot be assigned independently of the Hodge complex.

### What is not externally proven yet

- No checked external formula in this pass proves that the S2T `pi^-4` term equals the finite Bessel/coexact tower on `RP^3 x S^1`.
- No checked external formula in this pass proves the specific Casimir-mixing multiplier `1 - 10/(24 S_geo)`.
- No checked external formula in this pass proves that the determinant cross-term rank is exactly the finite projector `P_0,2 = ell=0 ⊕ ell=2` rather than the full scalar/exact tower.
- The scalar count `1+9=10` remains representation-theoretically natural for ambient quadratic functions on `S^3/RP^3`, but the Maxwell--ghost determinant must still be shown to couple exactly to this sector.

### Consequence for Tome II status

The literature gate strengthens the caution, not the closure. The safe status is:

```text
coexact tower: externally plausible/nonzero sector;
pi^-4 absorption: strong internal numerical and representation-theoretic hypothesis;
P_0,2 rank 10: natural finite-strain candidate;
theorem status: not yet achieved without an explicit lens-space p-form determinant derivation.
```

Practical next proof obligation: extract the `L(2,1)` one-form multiplicity formulas from Ikeda--Yamamoto or Lauret--Miatello--Rossetti, separate exact/coexact parts, and compare the determinant expansion with the S2T `P_0,2` mixed-strain ansatz.

## 2026-08-03 Independent L(2,1) Reproduction

The requested external gate is now carried out in [[external-l21-spectrum-determinant-reproduction]]. The audit does not import the project's multiplicities. It starts from the `Z_2` central-character projection of the standard `S^3` scalar and coexact one-form representations.

For the untwisted bundle required by ordinary Maxwell theory, it reproduces

```text
scalar:   n even, lambda=n(n+2), multiplicity=(n+1)^2;
coexact1: n odd,  lambda=(n+1)^2, multiplicity=2n(n+2).
```

Thus the first coexact multiplicities are `6,0,30,0,70`, matching the internal table exactly. The minimally coupled scalar determinant with the zero mode removed gives

```text
zeta'_0(0)=-0.6951703617566010,
```

reproducing Dowker's published projective-space value `-0.695171` within rounding.

The audit also identifies a convention hazard. Nash--O'Connor's explicit `p=2` formulas use the nontrivial flat character. That twisted sector selects the parity opposite to the untwisted Maxwell bundle, so its determinant values are controls, not direct Maxwell inputs.

Most importantly, the external untwisted reconstruction gives

```text
Gamma_FP,nonzero = 1/2 log det Delta_1^coex - 1/2 log det' Delta_0.
```

Therefore the scalar half-determinant residual is independently confirmed. The external gate strengthens the lens-space spectral foundation but does not reopen exact `pi^-4` absorption.

## 2026-08-03 RP3 x S1 Winding Functional Audit

The next external calculation is recorded in [[external-rp3xs1-winding-determinant-audit]]. It independently reproduces the internal positive Bessel sum

```text
T_coex^RP3=1.5227161455271526e-5
```

with an absolute difference of about `1.0e-20` from the stored value.

The audit then separates two functionals that had previously been discussed too closely:

```text
Casimir-energy continuation:
E_nonlocal=-T_coex/pi=-4.846956029729683e-6;

Euclidean determinant winding part:
logdet_winding=-4.184891094335807e-5;
Gamma_boson,winding=-2.0924455471679034e-5.
```

The `K_1` sum follows from the zeta continuation of `1/2 sum (m^2+rho^2)^(1/2-s)`. The compact-circle log determinant instead follows from `det(-d_tau^2+rho^2)=4sinh^2(pi rho)` and has a finite part `2log(1-exp(-2pi rho))`.

External-gate consequence: the nonzero coexact global contribution is real and the old Bessel number is numerically correct, but identifying it with a four-dimensional determinant residue requires an additional functional, dimensional and normalization derivation.
## 2026-07-10 Quadratic Projector Candidate

The standard Hodge/Faddeev--Popov route failed to select `ell=0,2` by itself. A better candidate is the representation-theoretic projector onto ambient quadratic strains:

```text
P_0,2 : q_A(x)=A_ab x^a x^b on S^3/RP^3.
```

Because `A_ab` is symmetric in four ambient coordinates, the rank is `dim Sym^2(R^4)=10`, decomposing as the trace `ell=0` mode plus the nine traceless `ell=2` modes.

This candidate is literature-compatible with the representation theory of spherical harmonics, but it is not yet a Maxwell determinant theorem. The remaining external check is whether the gauge-fixed mixed perturbation naturally reduces to ambient quadratic metric/volume strain.
## 2026-07-10 Metric-Variation Coupling Gate

The new audit `s2t/audits/s2t_metric_variation_p02_audit.py` refines the `P_0,2` candidate into a conditional lemma.

External-standard ingredient:

```text
δ log det Δ = Tr(Δ^{-1} δ_g Δ).
```

If the metric variation `δ_g` is restricted to first ambient strains of `S^3 ⊂ R^4`, the perturbation space is `Sym^2(R^4)`, not the full scalar tower. This is compatible with the representation theory of spherical harmonics: trace is `ell=0`, traceless symmetric quadratics are `ell=2`.

The literature gate now asks a sharper question: is the S2T `pi^-4` residue really the first ambient-strain mixed term? If yes, the `P_0,2` selection rule is natural. If no, the full scalar tower problem returns.
## 2026-07-10 S2T Selection Rule

The internal S2T selection audit `s2t/audits/s2t_first_strain_selection_audit.py` adds a model-building criterion on top of the external determinant literature.

It does not claim that general QED forbids arbitrary metric perturbations. Instead, it says that Tome II.A has already fixed a minimal constant-curvature carrier. Within that closure scheme, arbitrary `h_ij(y)` would be a new sector and would reintroduce an infinite metric tower. Therefore the `pi^-4` mixed term, if it is to remain an II.A closed residue, must use the first canonical ambient strain channel.

This sharpens the external question: not “are arbitrary metric perturbations possible in physics?”, but “is the II.A residue defined as the first ambient-strain determinant residue?”
## Каноническая хронология C6

Подробная последовательность внутренних проверок C6 хранится только на
странице [[coexact-tower-delta]]. Сводная ведомость шестнадцати подблоков
второй вариации находится в [[c6-second-variation-checklist]].

Локальный вывод этой страницы остаётся прежним: внешняя литература
подтверждает применимость спектров форм и теории определителей на линзовых
пространствах, но не доказывает требуемое S2T-тождество поглощения, знак
полного определителя или конечный ранг проекции.
## 2026-08-03 Decisive Functional Bridge Verdict

The reproduced winding calculation distinguishes two objects that had previously been used as if they supplied one residue:

```text
T_coex = sum d rho sum_q K1(2 pi q rho)/q,
Gamma_wind = sum d log(1-exp(-2 pi rho)).
```

The first controls the nonlocal Casimir-energy continuation; the second is the Euclidean log determinant. Numerically they are not related by the declared Maxwell normalization: `T_coex=1.5227161455e-5`, while the bosonic winding action is `-2.0924455472e-5`.

Combined with the nonzero geometric C11 table and scalar half-residual, this closes the present C6 route negatively. The literature gate strengthens the spectrum but does not supply the missing functional identity.
