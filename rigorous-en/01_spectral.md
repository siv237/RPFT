# §1. SPECTRAL GEOMETRY OF L(2,1)

## 1.1 Definitions

**Lens space** $L(p,q) = S^3 / \mathbb{Z}_p$, where $\mathbb{Z}_p$ acts on $S^3 \subset \mathbb{C}^2$:
$$(z_1, z_2) \mapsto (e^{2\pi i/p} z_1, e^{2\pi i q/p} z_2)$$

For $p=2, q=1$: $L(2,1) \cong \mathbb{RP}^3$ (projective space).

---

## 1.2 Spectrum of the scalar Laplacian

### Theorem (Ikeda 1979)

On $S^3$ of radius $R=1$ the scalar Laplacian $\Delta_0$ spectrum:

| $n$ | $\lambda_n$ | $d_n$ (multiplicity) |
|-----|-------------|----------------------|
| 0 | 0 | 1 |
| 1 | 3 | 4 |
| 2 | 8 | 9 |
| 3 | 15 | 16 |
| $n$ | $n(n+2)$ | $(n+1)^2$ |

**Formula:** $\lambda_n = n(n+2)$, $d_n = (n+1)^2$

### Projection to RP³

Antipodal map $\iota: (z_1, z_2) \mapsto (-z_1, -z_2)$ acts on spherical harmonics:
$$\iota Y_n^{(m)} = (-1)^n Y_n^{(m)}$$

**Consequence:** On $\mathbb{RP}^3 = S^3/\mathbb{Z}_2$ only **even** $n$ remain.

Multiplicity on $L(2,1)$:
$$d_n^{L(2,1)} = \tfrac{1}{2}(1 + (-1)^n)(n+1)^2 = \begin{cases} (n+1)^2, & n \text{ even} \\ 0, & n \text{ odd} \end{cases}$$

---

## 1.3 Zeta function of the scalar Laplacian on L(2,1)

### Definition
$$\zeta_{L(2,1)}(s) = \sum_{n=1}^{\infty} \frac{d_n^{L(2,1)}}{\lambda_n^s} = \sum_{k=1}^{\infty} \frac{(2k+1)^2}{[2k(2k+2)]^s}$$
(sum over even $n = 2k$)

### Simplification
$$\zeta_{L(2,1)}(s) = \frac{1}{4^s} \sum_{k=1}^{\infty} \frac{(2k+1)^2}{[k(k+1)]^s}$$

### Asymptotics (Weyl)
For large $n$: $\lambda_n \sim n^2$, $d_n \sim n^2$
$$\zeta_{L(2,1)}(s) \sim \int_1^\infty \frac{n^2}{n^{2s}} dn = \int_1^\infty n^{2-2s} dn$$
Converges for $\text{Re}(s) > 3/2$.

---

## 1.4 Zeta derivative at zero

### Theorem (regularization)
$$\zeta'(0) = \lim_{s \to 0} \frac{d}{ds} \zeta(s)$$
linked to the functional determinant:
$$\log \det(\Delta) = -\zeta'(0)$$

### Computation for L(2,1)
Heat-kernel expansion:
$$\text{Tr}(e^{-t\Delta}) = \sum_n d_n e^{-t\lambda_n} \sim \frac{\text{Vol}(M)}{(4\pi t)^{3/2}} + a_1 t^{-1/2} + a_2 t^{1/2} + \ldots$$
Coefficients $a_k$ are spectral invariants (Gilkey 1975).

**IMPORTANT: All formulas below assume $R = 1$ (Planck units).**

For lens space L(2,1) (d=3, R=1):
$$a_0 = \hat{V}_3 = \frac{\text{Vol}(L(2,1))}{R^3}\bigg|_{R=1} = \pi^2$$
$$a_1 = \frac{1}{6}\int_M R\, \frac{d\text{vol}}{R^3} = \frac{1}{6} \cdot 6 \cdot \pi^2 = \pi^2 \quad (R_{\text{scalar}}=6)$$

**Note on Seeley–DeWitt coefficients:**
$$K(t) \sim (4\pi t)^{-d/2} \sum_{k=0}^{\infty} a_{k/2} \, t^{k/2}$$
Coefficients $a_k$ are **dimensionless** at $R = 1$.

For a **3-manifold without boundary** (d=3):
- $a_0 = \hat{V}_3$ — dimensionless volume  
- $a_{1/2} = 0$ (no boundary)  
- $a_1 = \tfrac{1}{6}\int_M R\, d\hat{V}$ — first correction  
- $a_{3/2}$ contains $\nabla R$ and boundary terms

For the **4-manifold** $M^4 = L(2,1) \times S^1$ (R=1):
- $a_0 = \hat{V}_4 = 2\pi^3$ (dimensionless volume)  
- $a_1 = \tfrac{1}{6}\int_{M^4} R\, d\hat{V}$  
- $a_2 = \tfrac{1}{180}\int_{M^4} (c_1 R^2 + c_2 R_{\mu\nu}^2 + c_3 R_{\mu\nu\rho\sigma}^2)\, d\hat{V}$

where $c_1, c_2, c_3$ depend on the field type, and $d\hat{V} = d\text{vol}/R^4$ is the dimensionless volume element.

---

## 1.5 Formula for ζ′(0) via heat kernel

$$\zeta'(0) = -\gamma a_0^{(D)} + \text{FP}\int_0^\infty t^{-1} \big[\text{Tr}(e^{-t\Delta}) - a_0 t^{-D/2} - \ldots\big] dt$$
where FP is the finite part, $\gamma$ is the Euler constant.

### Numerical result (mpmath)
```python
from mpmath import mp, nsum, diff, log, pi, inf
mp.dps = 50

def zeta_L21(s):
    """Zeta function for scalars on L(2,1)"""
    def term(k):
        n = 2*k  # even n
        d = (n+1)**2
        lam = n*(n+2)
        return d / lam**s
    return nsum(term, [1, inf])

# Derivative at s=0
zeta_prime_0 = diff(zeta_L21, 0)
print(f\"ζ'_L(2,1)(0) = {zeta_prime_0}\")
```

---

## 1.6 Link to 1/24

### Casimir energy on a circle

For a free scalar on $S^1$ of period $L$:
$$E_{Casimir} = -\frac{\pi}{6L} \cdot \frac{1}{24} = -\frac{\pi}{144 L}$$
Coefficient $1/24$ is $\zeta_R(-1)$ (Riemann zeta):
$$\zeta_R(-1) = 1 + 2 + 3 + \ldots = -\frac{1}{12}$$
and $-\tfrac{1}{2}\zeta_R(-1) = \tfrac{1}{24}$.

### Extension to L(2,1)

**Hypothesis:** For L(2,1) the Casimir coefficient has the form:
$$\kappa_{L(2,1)} = 1 \cdot \frac{1}{24} + O(\text{topology})$$
where “1” is the “effective dimension” in the IR limit.

**TODO:** Strict computation of $\kappa$ from the spectral sum.

---

## 1.7 Spectrum tables for L(2,1)

| Field | $\lambda_n$ | $d_n$ on $S^3$ | $d_n$ on $L(2,1)$ | Parity |
|-------|-------------|----------------|-------------------|--------|
| Scalar | $n(n+2)$ | $(n+1)^2$ | $(n+1)^2$ (even) | even n |
| Vector | $(n+1)^2$ | $2n(n+2)$ | $2n(n+2)$ (even) | even n |
| Spinor | $(n+3/2)^2$ | $2(n+1)(n+2)$ | $2(n+1)(n+2)$ (odd) | odd n |

### 1.8 Spin structures on L(2,1)

**Theorem (Bär 1996):** L(2,1) = RP³ admits exactly **two** inequivalent spin structures.

Spin structure is classified by $\eta \in H^1(M; \mathbb{Z}_2) \cong \mathbb{Z}_2$.

| Spin structure | η | Dirac spectrum |
|----------------|---|----------------|
| Trivial | 0 | $\pm(n+3/2)$, n odd |
| Nontrivial | 1 | $\pm(n+3/2)$, n even |

**RPFT choice:** use the **trivial** spin structure (η = 0), where fermions “see” odd modes — antipodally antisymmetric.

*Ref:* Bär C., "The Dirac operator on space forms of positive curvature", J. Math. Soc. Japan **48** (1996) 69–83.

---

## Navigation

← [00_main.md](00_main.md) | [02_zeta_compute.py](02_zeta_compute.py) →

- [03_casimir_derivation.md](03_casimir_derivation.md) — 1/24 derivation  
- [05_pi4_derivation.md](05_pi4_derivation.md) — 1/π⁴ derivation
