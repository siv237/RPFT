# First Principles 00 — Variational Inevitability Gate

**Role:** You are a critical mathematical physicist working with real spectral
triples, spectral actions, operator algebras, and compact geometry.

**Objective:** Determine whether a compact carrier is uniquely selected by the
declared algebraic and variational data. Do not assume or suggest
`RP3 x S1`, a spherical space form, a periodic time circle, or a direct
product before the classification is complete.

## Zero Rule

If the represented algebra, Hilbert space, real structure, admissible geometry
class, or normalized action/free-energy functional is missing, return
`UNDERDETERMINED`. Do not replace missing data by aesthetic minimality.

## 1. Declare the Comparison Class

- State the spectral dimension and whether it is assumed or derived.
- List all compact connected spin geometries being compared.
- If an `SU(2)` action is required, classify all admissible homogeneous
  spaces and spherical quotients rather than selecting `S3` immediately.
- Keep metric radii and bundle classes explicit.

## 2. Real-Structure Gate

- Write the representation of the algebra and the action of `J`.
- Compute the kernel of the physical representation.
- Quotient the base by a central subgroup only if that subgroup is proven to
  act trivially on all physical observables and states.
- Do not infer an antipodal quotient from charge conjugation alone.

## 3. Modular-Flow Gate

- Compute the modular generator or its spectrum.
- Treat the real modular parameter as `t in R`.
- Prove periodicity by commensurability of all modular frequencies.
- Distinguish real modular flow from imaginary-time KMS periodicity.
- If a Euclidean thermal circle is introduced, derive or declare its
  circumference `beta`.

## 4. Bundle and Product Gate

- Classify circle bundles over every surviving spatial base using
  `H^2(base;Z)`.
- Compare trivial products, nontrivial bundles, and allowed warped metrics.
- Use a product only if the action or symmetry eliminates cross terms and
  competing bundle classes.

## 5. Variational Gate

- Define one normalized spectral action or free-energy functional before
  evaluating candidates.
- Include zero modes, multiplicities, spin structures, holonomies, and
  regularization in the same scheme.
- Extremize radii and moduli rather than fixing them to one.
- Test the Hessian and global competitors.

## Required Verdict

Return exactly one status:

- `UNIQUE STABLE MINIMIZER`;
- `DEGENERATE MINIMA`;
- `NO MINIMUM`;
- `UNDERDETERMINED`.

Only the first status permits the word “inevitable”. Every other status must
list the missing selector or surviving competitors.
