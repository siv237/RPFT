# Neutrino Overlap Lemma

> Status: draft
> Type: question
> Updated: 2026-08-03

## Question

Can the neutrino closure factor `\mathcal{N}_\nu^2 = \pi + \pi^{-1}` be derived from a specified Dirac, spin-holonomy, gauge-holonomy, or sector-overlap operator rather than inserted as a fitted residual?

## Why It Matters

The neutrino Dirac chain is the main partially closed S2T channel. If this overlap identity is derived from the operator spectrum, the neutrino row becomes a structural closure. If it fails, the row should remain an empirical bridge or be downgraded.

## Current Evidence

- `s2t/results/dirac_spin_holonomy_results.json` shows coefficient invariance across spin twists and identifies the antiperiodic sector with `theta = pi`.
- `s2t/results/gauge_holonomy_results.json` shows phase-branch motion under `beta` while preserving fitted heat coefficients.
- `s2t/results/sector_attribution_results.json` separates holonomy-phase control from mass/load control with a very large sector-separation ratio.
- None of these files alone proves the exact `\pi + \pi^{-1}` overlap identity.

## Needed Closure Test

- Define the relevant overlap space and inner product.
- Identify whether `\pi` and `\pi^{-1}` arise from dual compact cycles, reciprocal normalization, or a pair of spectral measures.
- Prove the identity analytically or produce a reproducible audit that rejects it as non-structural.

## 2026-08-03 First Operator Gate

The audit `s2t/audits/s2t_neutrino_overlap_first_gate_audit.py` tests the obvious no-fit routes.

### Negative result for holonomy alone

The antiperiodic spin structure fixes

```text
alpha=1/2,
theta=2*pi*alpha=pi,
U=exp(i theta)=-1.
```

However, a physical Wilson/spin holonomy is the unitary class `U`, not a preferred real logarithm `theta`. The expression

```text
theta + theta^{-1}
```

is not invariant under `theta -> theta+2*pi` and diverges at the periodic branch. Therefore `pi+pi^{-1}` cannot be derived from holonomy alone as a gauge-invariant class function.

The gauge-holonomy sweep reinforces this conclusion: phase branches move continuously with `beta`, while the local heat coefficients remain invariant. A reciprocal function of the raw phase angles would vary and becomes singular when one branch reaches zero.

### Reciprocal Gram candidate

There is one exact algebraic representation:

```text
Q_cycle = diag(g,g^{-1}),
det Q_cycle=1,
Tr Q_cycle = g+g^{-1}.
```

For `g=pi`, this gives the target exactly. This is potentially meaningful as a doubled primal/dual cycle metric. It is not yet a proof because the declared geometry has radius `R1=1` and circumference `2*pi`; neither standard choice yields `g=pi`. Antiperiodicity changes the spin transition function but does not geometrically quotient the circle to a half-length interval.

### Current verdict

- Holonomy-only derivation: failed.
- Standard full-circle or radius Gram norm: failed.
- Positive reciprocal cycle operator: viable conditional route.
- Absolute neutrino scale: still conditional.
- Dimensionless ratio `R_nu`: unchanged.

The next theorem-level object is no longer a scalar identity. It is a positive self-adjoint operator `Q_cycle` whose reciprocal eigenvalues are derived from geometry or spectral measure and whose square root enters the Dirac matrix element.

### Phenomenology control

Using the NuFIT 6.0 normal-ordering best fits, the current predicted solar splitting lies about `-0.70 sigma` from the central value, while the predicted splitting ratio is also compatible at sub-sigma level. Thus present data do not reject the factor, but they do not determine it exactly either. Numerical agreement cannot replace the missing operator.

## 2026-08-03 Construction of Qcycle

The second audit `s2t/audits/s2t_neutrino_qcycle_geodesic_gram_audit.py` constructs the positive operator rather than identifying it with a holonomy angle.

### Geometric carrier

Let `gamma=RP1` be a shortest noncontractible closed geodesic in unit round `RP3`. It lifts to a half great circle joining `x` to `-x` in `S3`, hence

```text
ell(gamma)=pi.
```

All projective lines are related by isometries, so the construction does not depend on a selected direction.

### Integral primal/dual basis

On the intrinsic circle `gamma`, choose

```text
e0=1 in H0(gamma;Z),
e1=ds/ell in H1(gamma;Z),  integral_gamma e1=1.
```

Their Hodge `L2` norms are

```text
||e0||^2=ell,
||e1||^2=ell^{-1}.
```

Therefore

```text
Qcycle=diag(ell,ell^{-1}),
det Qcycle=1.
```

At `ell=pi`, this is exactly

```text
Qcycle=diag(pi,pi^{-1}).
```

### Selection of the neutrino vector

The integral lattice is `Z e0 direct_sum Z e1`. The primal/dual involution acts by `J(a,b)=(b,a)`. Its only primitive nonzero invariant vectors are `plus/minus(1,1)`. Thus the self-dual neutrino vector is fixed up to an irrelevant sign:

```text
v_nu=e0+e1.
```

Its squared norm is

```text
||v_nu||^2_Q=pi+pi^{-1}.
```

Consequently the desired scalar can be written as the genuine operator norm

```text
sqrt(pi+pi^{-1})=||Qcycle^(1/2) v_nu||.
```

### Status

This constructs `Qcycle` and removes the earlier holonomy branch problem. It does not yet close the neutrino mass theorem. The one-form generator is intrinsic to `gamma`; since `H1(RP3;R)=0`, it is not a global harmonic one-form on the ambient carrier. The remaining proof is to construct a restriction or defect map from ambient neutrino spinors to the cycle complex and derive a self-dual EFT vertex selecting `v_nu`.

Current status: operator constructed, Dirac embedding open.

## 2026-08-03 Minimal Seesaw Embedding

The next audit `s2t/audits/s2t_neutrino_qcycle_seesaw_embedding_audit.py` shows that the factor can enter the seesaw matrix without first being declared as a standalone scalar mass.

In the orthonormal two-channel cycle basis define

```text
mD_cycle = y v_nu^T Qcycle^(1/2),
v_nu=(1,1),
MR_cycle=M0 I2.
```

Then

```text
-mD_cycle MR_cycle^{-1} mD_cycle^T
=-(y^2/M0) v_nu^T Qcycle v_nu
=-(y^2/M0)(pi+pi^{-1}).
```

With

```text
y=m_e^2/m_mu,
M0=(23+pi^{-1})m_mu,
```

this reproduces the stated light-neutrino scale.

### Why the factor survives normalization

The vector `v_nu` is treated as a primitive integral coupling/charge vector, not as an internal wavefunction. The physical cycle-channel fields have canonical kinetic terms in the orthonormal basis; the coupling components are obtained by applying the metric vielbein `Qcycle^(1/2)` to the integral vector. Dividing `v_nu` by its `Qcycle` norm would define a different model and erase the topological coupling strength.

### Invariance

Under an orthogonal change of cycle-channel basis,

```text
mD -> mD O^T,
MR -> O MR O^T,
```

the seesaw contraction is unchanged. Numerical rotation tests agree to machine precision.

### Remaining gap

The matrix algebra is now closed. The remaining task is representation-theoretic:

1. embed the two cycle channels inside the already counted eight-real-dimensional Majorana module;
2. derive the defect/restriction Yukawa vertex from the ambient Dirac action;
3. prove that charge conjugation or another exact symmetry selects `v_nu=(1,1)`;
4. prove that the heavy cycle block is proportional to `I2` rather than carrying a new adjustable matrix.

Status: minimal seesaw embedding constructed; ambient representation and vertex proof remain open.

## 2026-08-03 Majorana Dimension Gate

Attempting the requested representation embedding exposed a more basic inconsistency in the current denominator proof.

The text counts

```text
3 generations * 8 real components - 1 = 23
```

and identifies the removed direction with the generation-singlet field

```text
N_tr=(N_R1+N_R2+N_R3)/sqrt(3).
```

But `N_tr` is still a complete internal spinor. If the internal module has real dimension `d`, the generation-singlet projector is

```text
P_tr tensor I_d
```

and has rank `d`. The generation-traceless subspace has rank `2d`, not `3d-1`.

Therefore:

```text
d=8  -> 24-8=16,
d=4  -> 12-4=8.
```

The number `23` can be retained only through a different construction: remove one explicitly derived vector from the full `R24` module. That requires a canonical rank-one projector `|u><u|`; it is not the same operation as removing a generation-singlet spinor field.

### Spinor convention warning

- A physical four-dimensional Minkowski Majorana spinor has four real components.
- A complex four-component Euclidean internal Dirac spinor has eight real components only after realification.
- An eight-real symplectic-Majorana interpretation is possible but requires an explicit doublet and reality condition.

The cycle doublet constructed above could participate in such a symplectic structure, but it does not by itself select a single vector in the full generation--spinor module.

### Updated status

- `Qcycle`: constructed.
- Minimal cycle-channel seesaw contraction: algebraically valid.
- `23+pi^{-1}` denominator: downgraded to an unproved rank-one-projector hypothesis.
- Absolute neutrino scale: open.
- Dimensionless `R_nu`: also returns to conditional status because it contains `23`.

The next task is to construct the full representation and either derive a symmetry-protected rank-one vector or replace `23` by the generation-covariant rank.

## 2026-08-03 Rank-One Selector No-Go

The full minimal module factorizes as

```text
R3_generation tensor R4_lowest-RP3-spinor tensor R2_cycle.
```

The available exact selections have ranks `1`, `4`, and `1`, respectively: the `S3` generation singlet, the lowest `RP3` Dirac eigenspace, and the self-dual cycle branch. Their joint canonical projector therefore has real rank `1*4*1=4`, not rank one.

The two spin structures on `RP3` exchange which sign of the lowest eigenvalue `|lambda|=3/2` survives, but the surviving eigenspace has complex multiplicity `2`, hence real rank `4`. A finite exact obstruction gives the same result: the quaternion subgroup `Q8` acting on the lowest-spinor module forbids an invariant real line, and averaging any rank-one spinor projector over `Q8` gives `I4/4` with support rank four.

Under the symmetries already declared in the theory, a symmetry-protected rank-one projector therefore does not exist. Retaining `23` requires genuinely new structure selecting a spinor polarization: a defect boundary condition, condensate, preferred Killing spinor, or explicit symmetry breaking.

The representation-consistent alternatives are

```text
remove generation-singlet x self-dual-cycle x lowest-spinor block: 24-4=20,
remove the complete generation-singlet internal module:             24-8=16.
```

Neither number is yet a physical denominator. Status: `23` is ruled out under the present exact symmetry package; `Qcycle` and its seesaw contraction remain valid.

## 2026-08-03 Twisted Majorana Defect Route

There is one concrete way around the no-go that does not choose a spinor by hand. Put an odd-winding real class-D Majorana mass defect on the systolic core `gamma=RP1`. Its minimal radial operator

```text
A_perp=d/dx+tanh(x)
```

has the unique normalized real zero mode `sech(x)/sqrt(2)`, while the adjoint zero solution is non-normalizable. The transverse mod-two index is therefore one.

The core channel also sees two existing signs:

```text
antiperiodic spin holonomy = -1,
nontrivial RP3 Z2 flat-line holonomy = -1.
```

Their product is `+1`, so the single real Majorana channel is periodic around `gamma` and has one longitudinal constant zero mode. Multiplying the ranks of the generation singlet, transverse zero mode, longitudinal zero mode and self-dual cycle line gives `1*1*1*1=1`.

This reopens `24-1=23` conditionally and remains compatible with `Qcycle`: the defect selects the ambient spinor line, while `Qcycle` still supplies the reciprocal cycle norm `pi+pi^-1`.

The price is explicit and nontrivial. The current S2T action does not yet contain the required two-component real mass order parameter or prove odd winding around `gamma`. The restriction map, state counting in the Majorana/BdG formulation, and the identification of the unique zero branch with the removed heavy direction remain open.

Status: a mathematically explicit completion route exists; it is a new structural hypothesis, not yet a theorem of the current model.

## 2026-08-03 Torsion Square-Root Origin

The odd winding is not forced by the smooth ambient `Z2` line alone. If `y` generates the solid-torus complement of the systolic core, the filling relation is `mu_core=2y`. Thus the ambient torsion character has `chi_L(y)=-1` but `chi_L(mu_core)=+1`; locally it carries no meridian pi flux.

The complement nevertheless has a canonical square-root pair:

```text
chi_S(y)^2=-1,
chi_S(y)=+i or -i,
chi_S(mu_core)=chi_S(2y)=-1.
```

This line cannot extend through the core and therefore defines a discrete quarter-holonomy defect. For a charge-two Majorana pairing channel, meridian phase `pi` forces pair-field phase change `2pi`, hence vortex winding `1` and odd mod-two index.

The construction is already visible in the existing gauge audit: `beta=1/4` produces the conjugate holonomies `-i,+i`, both squaring to the nontrivial `Z2` branch. No continuous phase is fitted.

Updated status: the required odd winding now has a concrete non-parametric origin. The remaining gate is to derive this singular square-root line and its core boundary condition from the S2T action and prove that the transverse zero mode inherits the periodic longitudinal channel.

## 2026-08-03 Core Gluing Majorana Line

The remaining local gluing problem can be solved in a minimal Nambu model. With particle--hole involution `C=tau_x K`, choose

```text
v(theta)=(exp(i theta/2),exp(-i theta/2))/sqrt(2).
```

This vector is Majorana-real: `C v=v`. A square-root transition changes the pair phase by `pi` and acts as

```text
G_1/4=diag(i,-i),
v(theta+pi)=G_1/4 v(theta).
```

Thus the quarter-holonomy transports the local zero-mode basis itself. The coefficient line only sees the two real signs

```text
h_spin=-1,
h_Z2=-1,
h_coefficient=h_spin*h_Z2=+1.
```

The core Majorana coefficient is periodic and has one constant real zero mode. Removing the ambient torsion line gives the control result `h=-1` and removes the zero mode.

There is no physical Nambu doubling. For a `C`-fixed vector, `a v` remains `C`-fixed only when `a` is real, so the kernel is one real line. Inside the conditional defect model this gives complement rank `24-1=23`.

Status at this stage: the local topology, odd index, core gluing and real state count are mutually consistent. The next gate is global action embedding; the later parent-superconnection audit below closes its geometric tubular restriction and isolates the stronger spectral-kernel question.

## 2026-08-03 Global Action Denominator Gate

A global tubular EFT candidate can be written:

```text
S_tube=(1/2) integral <Psi,B_Phi Psi>,
B_Phi=Dirac_Sroot+Phi_1 Gamma_1+Phi_2 Gamma_2,
```

with the existing `Qcycle` row attached through the normalized core restriction map. The unique defect kernel defines `P_H=I-|u0><u0|` with rank `23`.

However, the action audit exposes a crucial distinction. For the symmetry-covariant mass `M_H=M0 P_H`, a normalized coupling gives `w^T M_H^+ w=1/M0`, independent of rank. Equal unnormalized couplings give `23/M0`, placing `23` in the numerator. The Gaussian determinant contains `23 log(M0)`. None of these standard operations produces a tree-level denominator `23 M0`.

The desired operator

```text
M_target=M0*(Tr(P_H)+pi^{-1})*P_H
```

works algebraically, but using it as a definition would merely insert the answer. Its scalar coefficient must be derived as a spectral trace, loop self-energy, or collective stiffness in the same action.

Updated status: the global defect EFT, rank-one kernel and rank-23 quotient are consistent. The numerical denominator `23+pi^{-1}` remains conditional at action level.

## 2026-08-03 Collective Stiffness Normalization

The action-level no-go can be respected rather than bypassed. Do not interpret `23` as a heavy fermion mass eigenvalue. Instead define the single collective pairing tangent

```text
Xi=(P_H,e1_dual)
```

in `End(R24) direct_sum Omega1(gamma)`. Its canonical product norm is

```text
||Xi||^2=Tr(P_H^2)+||e1||^2=23+pi^{-1}.
```

For an auxiliary collective amplitude

```text
S[a]=(M_*/2)||Xi||^2 a^2+y_cycle a J_nu,
```

integrating out `a` gives `-y_cycle^2 J_nu^2/(2 M_* ||Xi||^2)`. The rank therefore enters through canonical normalization of one collective deformation, not through a manually enlarged mass or an unnormalized sum over propagators.

The result is invariant under rescaling the auxiliary coordinate. With the existing `Qcycle` vertex and `M_*=m_mu`, it reproduces the stated neutrino scale exactly.

The remaining gate is the relative product metric. A general metric gives `alpha*23+beta/pi`; exact `D_nu` requires `alpha=beta=1`. These equal weights must come from one spectral-action or superconnection trace, not from the neutrino data.

Updated status: `D_nu` has a non-tautological collective-stiffness derivation candidate. Its final theorem status depends only on deriving the common unweighted metric.

## 2026-08-03 Superconnection Metric Closure

The relative metric can also be fixed without introducing `alpha/beta`. Put the two pieces into one graded superconnection tangent:

```text
bold Xi=P_H tensor e0_hat + P_kernel tensor e1,
e0_hat=1/sqrt(pi),
e1=ds/pi.
```

The zero-form is a dynamical field mode and is canonically `L2` normalized. The one-form is a quantized holonomy generator and retains unit period. A single trace--Hodge norm gives

```text
||bold Xi||^2
=Tr(P_H^2)||e0_hat||^2+Tr(P_kernel^2)||e1||^2
=23+pi^{-1}.
```

The cross term vanishes twice: zero-forms and one-forms are orthogonal in the graded metric, and `P_H P_kernel=0` internally.

This normalization rule is the same field-versus-integral-vector distinction already required by `Qcycle`; it is not selected from neutrino data.

Status at this stage: the denominator is closed inside the minimal graded-superconnection model with no relative continuous weight. The following parent audit supplies the ambient tubular embedding; what remains is justification of the canonical metric itself or a special spectral-kernel identity.

## 2026-08-03 Parent Superconnection Embedding

The ambient restriction can be constructed explicitly on

```text
H_parent=L2(RP3 x S1,S) tensor R24 tensor H_Nambu,
D_parent=D_K tensor I+Gamma_K tensor D_F.
```

In the tubular defect sector use

```text
delta A=a rho(r)(P_H tensor e0_hat+P_kernel tensor e1).
```

The radial profile and spectator compact-circle mode are canonically normalized. Integrating them out gives exactly the core tangent `a bold Xi`; the ambient and restricted norms agree with zero error and equal `a^2(23+pi^{-1})`.

This closes the geometric parent-to-tube restriction. It does not make the result kernel-independent. A control expansion of `Tr f((D0+a delta A)^2)` for linear, exponential and rational kernels shows that a generic spectral Hessian weights the massive heavy sector and zero-mode connection sector differently. Only the linear/quadratic configuration metric preserves equality automatically in the reduced test.

Updated status: the denominator is a theorem of the canonical superconnection configuration metric. It is not yet a universal theorem of an arbitrary bosonic spectral kernel. The parent theory must either make that metric primary or derive a special kernel/background identity.

## 2026-08-04 Spectral Metric Uniqueness Gate

The remaining kernel question has an analytic answer in the reduced commuting control. The two Hessian weights are

```text
w0=2 f'(0),
wM=2 f'(M^2)+4 M^2 f''(M^2).
```

Requiring equality smoothly for every nonzero background gives `f'(0)=f'(x)+2x f''(x)`. Its only solution smooth at the origin is `f(x)=A+B x`. Thus the background-independent route uniquely returns the affine kernel, equivalently the canonical quadratic configuration metric.

The standard positive heat-kernel class fails more strongly. For `f(x)=integral exp(-t x) dmu(t)` with positive nonzero measure, `wM-w0` is strictly positive for every `x>0`. No nonconstant positive heat mixture closes the gate.

At one fixed mass, non-affine solutions can be tuned because equality imposes only one scalar constraint. Such a choice cannot count as a no-fit derivation unless an independent principle fixes the kernel before the neutrino target is used.

Final status: `23+pi^-1` is rigorous inside the explicitly declared affine/canonical configuration-metric model. It remains conditional for an unspecified bosonic spectral action.

## Links

- [[tome2-s2t-spectral-closure]] — Tome II source defining this as a II.B task.

- [[s2t-closure-roadmap]] — roadmap where this is the main partial closure.
- [[holonomy-and-dirac-sectors]] — audit layer most likely to contain the needed structure.
- [[numerical-audits]] — JSON source cluster for current evidence.
- [[formalize-common-source]] — broader formalization problem.

## Source Notes

- Source paths: `s2t/results/dirac_spin_holonomy_results.json`, `s2t/results/gauge_holonomy_results.json`, `s2t/results/sector_attribution_results.json`, `s2t/docs/tome2_s2t_spectral_closure.tex`, `s2t/results/s2t_tome2_results.json`.