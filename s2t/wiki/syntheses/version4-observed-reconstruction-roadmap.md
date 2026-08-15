# Version IV.SM Observed Reconstruction Roadmap

> Opened: 2026-08-10

## Objective

Build an observed-sector architecture rather than reinterpret the frozen
hidden modes of Version III.H.

## Definition of Done

- derive or explicitly freeze the Standard Model representation ledger;
- cancel all local gauge and mixed gravitational anomalies;
- derive gauge, scalar and Yukawa normalizations from one measure;
- allow at most one dimensionful train input;
- run the complete RG and threshold pipeline;
- pass at least two preregistered dimensionless blind tests in independent
  sectors;
- preserve all failed observables in the scorecard.

## Gate Order

1. finite-algebra and representation classification;
2. anomaly cancellation;
3. spectral coupling normalization;
4. Higgs and Yukawa graph;
5. RG transport;
6. gauge-plus-matter blind test;
7. cross-tome functional bridge.

## Current Status

The representation, anomaly, gauge-normalization, Yukawa-map, flavour-menu,
Pfaffian, full-profile and base-K determinant gates have now been executed.
No observed-world numerical prediction is closed: the best blind Cabibbo
partial pass fails the remaining mass/CKM/CP tests, while the corrected
zero-mode and full radial profiles remain CP-even.

The base-K operator determinant is now assembled and reproduces the local
supertrace numerator `67`. Its nonlocal part is well defined after a discrete
spin/flat choice, but finite `R chi^2` and `chi^4` counterterms prevent a
parameter-free absolute vacuum.

The finite fermion branch difference scheme-independently ranks the
antiperiodic `S1` spin structure below the periodic one. The follow-up
[[version4-spin-sum-measure-gate]] closes the dynamic interpretation
negatively: the current Hilbert space and BV complex are defined for one
fixed spin structure and contain no sum or relative topological weights.
Thus the antiperiodic result is a conditional ranking, not a derived change
of background.

The follow-up [[version4-spin-branch-mass-stationarity-gate]] tests the last
scheme-independent fixed-`K` scale loophole. The exact derivative of the
periodic/AP determinant difference is strictly positive for every
`chi R3>0`; the ratio is monotone and has no nonzero stationary point. The
external gauge-mass objection is also resolved: the Goldstone is a separate
gauge-orbit mode, while the three listed scalars are physical quotient
coordinates.

## Immediate Next Decision

The minimal fixed-`K` determinant program is now exhausted even at the level
of scheme-independent branch ratios. Freeze one `S1` spin structure only if
the model is retained as an effective background theory. Physical reopening
requires either a new `Z2`/spin-TQFT or chiral measure, or the variational
carrier program below.

## Retrospective Carrier Decision

The source-level audit [[zero-prompt-toe-carrier-trace-2026-08-11]] shows
that `K=RP3 x S1` is not derived in `TOE.pdf`. TOE starts from a Gaussian
correlation operator on a general kernel domain `M x M`; `S3 x S1` enters
later as an UGSM-side diagnostic geometry, and the zero prompt adds the
central quotient, periodic circle and direct-product assumptions.

This creates a distinct reopening route: instead of adding another field to
the fixed-`K` parent action, define a normalized correlation functional over
a comparison class of carriers and test whether `K` is a stable minimizer.
This is a new architecture, but it is closer to the original TOE principle.

## First Post-K Candidate

The follow-up [[version4-toe-native-s4-carrier-candidate-gate]] abandons
`RP3 x S1` rather than decorating it. A coefficient-free lexicographic gate
requires a compact spin four-manifold, homogeneous positive-Einstein vacuum,
no unit-volume shape modulus, and then maximal continuous isometry. In the
declared menu, only round `S4` and equal-radius `S2 x S2` reach the last
filter; `S4` wins with isometry dimension `10` against `6`.

The new parent is almost-commutative over `S4`, with the observed finite
algebra `C + H + M3(C)` kept separate. This is a conditional minimal
candidate, not a derived vacuum: the next exact gate must compare `S4` and
`S2 x S2` under one preregistered Gaussian-correlation functional, prove a
positive second variation, and fix the common radius without observable
fitting.

## Correlation-Purity Ordering

The comparison requested above is executed in
[[version4-s4-s2xs2-correlation-purity-gate]]. With equal four-volume and
the same scalar Gaussian operator, round `S4` has strictly larger Rényi-2
entropy at both analytic asymptotic ends and at every point of a converged
3001-point middle-profile audit. The difference peaks at approximately
`0.1810734` near `tau=0.1133942`.

This independently reinforces `S4`, but it does not yet derive the vacuum:
TOE must still determine whether its correlation principle maximizes or
minimizes this entropy, and the absolute radius remains unfixed.

## Gibbs Sign Completion

The sign problem is conditionally closed by
[[version4-gibbs-free-energy-carrier-gate]]. Normalizing the TOE heat
operator to a density state leads to the canonical Gibbs functional. Its
difference from the equilibrium free energy is relative entropy divided by
`tau`, so Klein positivity fixes the sign and uniquely selects the Gaussian
state.

The reduced carrier functional is `F=-log Z/tau`. Equal-volume spectral
audits give `F(S4)<F(S2 x S2)` at both analytic asymptotic ends and at every
point of the 3001-point middle grid. This makes `S4` the selected carrier in
the normalized correlation-state completion. The next gate must prove that
this Gibbs functional has the same carrier extrema as the original TOE
spectral action; otherwise it remains a mathematically canonical extension.

## Spectral/Gibbs Equivalence Verdict

The requested equivalence is tested in
[[version4-spectral-gibbs-equivalence-gate]] and closes negatively. The
literal primary formula `Tr f(Chat/Lambda^2)` is not trace class for a
standard cutoff with `f(0)>0`, because compact correlation eigenvalues
accumulate at zero. Moreover, trace functionals are additive on direct sums,
whereas Gibbs free energy contains an outer logarithm and is nonadditive.

The corrected architecture recovers the unbounded generator
`H_C=-log(Chat)/tau=Delta`. Local EFT dynamics use
`Tr f(H_C/Lambda^2)`, while global carrier selection uses
`-log Tr Chat/tau`. These are sequential readings of one operator, not one
identical action and not an arbitrarily weighted sum.

## Absolute-Radius No-Go

The volume constraint is released in [[version4-s4-radius-boundary-no-go]].
For round `S4_a`, Gibbs free energy has strictly negative radius derivative
and decompactifies. Any positive decreasing cutoff spectral action has
strictly positive radius derivative and minimizes at collapse. Neither
functional has a finite stationary radius.

An arbitrary weighted sum can balance the two trends, but the resulting
radius is directly encoded by the relative coefficient. The next admissible
scale mechanism must derive a volume, pressure, mean-energy or relative
normalization constraint from one correlation-operator measure before
comparison with physical scales.

## Correlation-Cell Reopening

The first coefficient-free intensive candidate is tested in
[[version4-correlation-cell-free-energy-density-gate]]. The dimensionless
free energy per four-dimensional correlation cell has a strict minimum on
round `S4` at `a/sigma=1.3513921957`. Its stationarity condition is
equivalent to `p=-epsilon`.

Equal-radius `S2 x S2`, optimized at its own scale, has a higher minimum
density. Thus `S4` remains selected and the scale gate is conditionally
reopened at the ratio level. The absolute value of `sigma` is still open and
must be derived from the corrected gravitational normalization before any
comparison with measured scales.

## Absolute-Scale Self-Consistency

The gravitational matching is tested in
[[version4-absolute-scale-eft-validity-gate]]. With the Gaussian moment
`f2=1`, it formally gives `sigma=0.16287 l_P` and
`a=0.22010 l_P`. However, the selected vacuum has
`R/Lambda^2=6.5708` and `a Lambda=1.3514`, outside the large-cutoff regime
needed for the local Seeley-DeWitt derivation.

The failure is independent of `f2`. Therefore `a/sigma` remains the current
positive result, while absolute matching through the local gravitational
coefficient is frozen as uncontrolled. Reopening requires either a derived
EFT/correlation scale hierarchy or an exact nonlocal response calculation.

## Hybrid Inheritance Experiment

The old carrier's exact ledger is tested in
[[version4-s4-rp3-hybrid-experiment-gate]]. A separate metric `RP3` density
has a strict minimum near `b=2 sigma`, but not exactly at it. The honest
`S4 x RP3` product density is unbounded below when either factor collapses,
and the internal scalar KK towers begin at order the correlation cutoff.

Thus the full metric pi-ledger cannot be inherited without new continuous
physics. The clean surviving content is the discrete `Z2` topological core:
torsion holonomy and linking data. The next hybrid mechanism must realize
this core as a genuine finite/topological sector with a derived measure.

## Full-Corpus Retrospective Decision

The RPFT, UGSM, TOE and tractate corpus is re-audited in
[[version4-project-retrospective-entropy-measure-gate]]. The source history
separates maximum kernel entropy, normalized-state entropy and minimum
spectral complexity. These are different variational problems, so the
conditional `S4` Gibbs ordering cannot be promoted directly to the archived
topology postulate.

Mean spectral energy for unit-volume `S4` and `S2 x S2` crosses at
`tau=0.09576644817`; it is not a scale-free selector. The most natural
factorized cell measure is a weighted average of sector densities and
collapses to the lower `RP3` boundary, rather than stabilizing a hybrid.

The only materially unexecuted source-level route is the TOE 6.5 variation
of spectral density with a fluctuation determinant and information entropy.
The corrected next program uses `H_C=-log(Chat)/tau` and varies normalized
state and carrier jointly. It must derive one common measure and pass a
positive joint-Hessian test before any observable matching.

## Negative-Space Correction

The assumption-level follow-up
[[version4-negative-space-bundle-fluctuation-gate]] recovers the nontrivial
circle bundle over `RP3`, modeled by `U(2)`. Its scalar spectrum obeys the
coupled rule `ell+m` even, so projective parity and KK momentum are no longer
independent. This is a genuine forgotten mechanism, but its scalar
correlation density still collapses when the base shrinks.

The major surviving omission is the full renormalized field fluctuation
action on `S4` and `S2 x S2`. Previous carrier gates use only a positive
scalar heat state. The physical parent ledger adds three scalars, a massive
vector with ghosts and two Dirac pairs. Their signed determinant cannot be
replaced by the flat supertrace inside an entropy formula. The next exact
calculation is therefore `Gamma_fluc`, in one frozen counterterm scheme,
followed by the joint geometry Hessian.

## Full-Field Counterterm Obstruction

The prerequisite is executed in
[[version4-full-field-carrier-counterterm-gate]]. At unit four-volume the
carrier difference has nonzero components

```text
Delta integral R   = 11.2969093903,
Delta integral W2  = -256 pi^2/3,
Delta integral E4  = -64 pi^2.
```

Therefore finite Einstein, Weyl-squared and Euler coefficients can reverse
any finite nonlocal determinant ordering. In particular, the Euler coupling
changes relative topology weights without affecting local equations inside
one topology. Minimal subtraction defines a reproducible number but not a
derived physical carrier measure.

The corrected immediate task is now parent derivation of these finite
coefficients, scalar nonminimal couplings and the vector-mass completion.
Only after that should the nonlocal scalar-vector-ghost-Dirac determinant and
joint Hessian be computed.

## Gaussian Bare Topology Measure

The first concrete coefficient-fixing mechanism is tested in
[[version4-gaussian-bare-spectral-topology-gate]]. The Gaussian spectral
action is interpreted as the fundamental bare Wilsonian action at the
cutoff, fixing its moments and the Weyl-squared-to-Euler ratio.

The exact unit-volume spin-Dirac heat traces have one crossing at
`t=0.12415316994`. Below it the positive spectral action favours `S4`; above
it `S2 x S2` wins. The earlier correlation-cell scale maps to
`t=0.10673403996`, inside the `S4` window, where the independent Dirac trace
difference is `-0.03458179886`.

For a constant almost-commutative vacuum the heat trace factorizes into a
spacetime trace and a positive finite-space factor, so the finite algebra
does not change this ordering. The reopening remains conditional because
`Lambda sigma=1`, quantum RG shifts and the massive-vector completion are
not yet derived.

## Final Visual Status Tree

The complete branch structure is rendered in
[[project-success-tree-2026-08-11]]. It separates the surviving mathematical
core from closed Tome II/III implementations and shows the final full-shape,
topology-prior and vector/RG kill-gates without subjective probabilities.