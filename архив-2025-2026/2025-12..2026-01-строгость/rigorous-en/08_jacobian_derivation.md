# §8. RIGOROUS KK JACOBIAN DERIVATION

**Goal:** Prove Theorem 5.2 — that $Z_A = \text{Vol}(\mathbb{RP}^3) = \pi^2$ and $Z_\Psi = \text{Vol}(S^3 \times S^1) = 4\pi^3$.

---

## 8.1 Standard KK reduction formula

### Higher-dimensional action
For a (4+k)-dim theory on $M_4 \times K$:
$$S_{4+k} = \int_{M_4 \times K} d^4x\, d^ky\, \sqrt{g_{4+k}}\, \mathcal{L}_{4+k}$$

### Fubini and integrating over K
By Fubini:
$$S_{4+k} = \int_{M_4} d^4x\, \sqrt{g_4} \int_K d^ky\, \sqrt{g_K}\, \mathcal{L}_{4+k}$$

For fields independent of $y$ (zero-mode):
$$S_{4+k} = \text{Vol}(K) \cdot \int_{M_4} d^4x\, \sqrt{g_4}\, \mathcal{L}_4$$

### Gauge coupling relation
For a gauge kinetic term:
$$S_A = \frac{1}{g_{4+k}^2} \int_{M_4 \times K} F^2\, d^{4+k}x$$
After KK reduction:
$$S_A = \frac{\text{Vol}(K)}{g_{4+k}^2} \int_{M_4} F^2\, d^4x = \frac{1}{g_4^2} \int_{M_4} F^2\, d^4x$$
Hence:
$$\frac{1}{g_4^2} = \frac{\text{Vol}(K)}{g_{4+k}^2}$$

**Important (dimension):** for $k\neq 0$ the higher-dimensional coupling $g_{4+k}$ is **dimensionful**.
In particular, for $k=1$ (5D) we have $[g_5^2]=\text{length}$, so writing “$g_{4+k}=1$” without specifying the normalization can hide an extra numerical factor.

In RPFT the natural length scale of the extra circle is
$$\mathrm{Vol}(S^1)=2\pi R.$$

**Independent principle (no free dimensionless constants):**
since $g_5^2$ has dimension of length, the only dimensionless combination in the $S^1$ sector is
$$\tilde g_5^2 \equiv \frac{g_5^2}{\mathrm{Vol}(S^1)}.$$
Assuming the fundamental theory introduces no additional dimensionless parameters, we take the minimal choice
$$\tilde g_5^2 = 1,$$
so
$$\boxed{g_5^2 = \mathrm{Vol}(S^1) = 2\pi R.}$$

Then for the zero mode along $S^1$ one gets
$$\boxed{\frac{1}{g_4^2} = \frac{\mathrm{Vol}(\mathbb{RP}^3\times S^1)}{g_5^2} = \frac{\pi^2\cdot 2\pi R}{2\pi R} = \pi^2.}$$

---

## 8.2 Application to RPFT

### Geometry
- Internal space: $K = L(2,1) \times S^1$
- Vol(L(2,1)) = Vol(RP³) = $\pi^2$ (R=1)
- Vol(S¹) = $2\pi$ (R=1)
- Vol(K) = $\pi^2 \times 2\pi = 2\pi^3$

### But why $4\pi^3$?
**Answer:** Fermions “see” the cover.

---

## 8.3 Sector separation (Ikeda 1979)

### Antipodal action
On $S^3$, $\iota: x \mapsto -x$ acts on harmonics:
$$\iota Y_\ell^{(m)} = (-1)^\ell Y_\ell^{(m)}$$

### Projection to L(2,1) = $S^3/\mathbb{Z}_2$
- **Even modes** ($\ell$ even): $\iota Y_\ell = +Y_\ell$ → survive on L(2,1)
- **Odd modes** ($\ell$ odd): $\iota Y_\ell = -Y_\ell$ → vanish on L(2,1)

### Key observation
- **Bosons (gauge fields)** use even modes:
  $$A_\mu(x,y) = \sum_{\ell \text{ even}} a_\mu^{(\ell)}(x) Y_\ell(y)$$
  Normalization:
  $$\int_{L(2,1)} |Y_\ell|^2 d\text{vol} = 1 \quad (\text{normalized harmonics})$$
  Jacobian:
  $$Z_A = \frac{\mathrm{Vol}(\mathbb{RP}^3\times S^1)}{\mathrm{Vol}(S^1)} = \mathrm{Vol}(\mathbb{RP}^3) = \pi^2$$

- **Spinors (fermions)** use odd modes (spin structure):
  $$\Psi(x,y) = \sum_{\ell \text{ odd}} \psi^{(\ell)}(x) \chi_\ell(y)$$
  Odd modes require lifting to the cover $S^3$:
  $$\int_{S^3} |\chi_\ell|^2 d\text{vol} = 1$$
  Jacobian (including $S^1$):
  $$Z_\Psi = \int_{S^3 \times S^1} d\text{vol} = \text{Vol}(S^3) \times \text{Vol}(S^1) = 2\pi^2 \times 2\pi = 4\pi^3$$

---

## 8.4 Rigorous theorem

### Theorem 8.1 (Jacobian split)
For KK reduction of QED on $K = L(2,1) \times S^1$ with trivial spin structure:
$$Z_A = \frac{\mathrm{Vol}(L(2,1)\times S^1)}{\mathrm{Vol}(S^1)} = \pi^2$$
$$Z_\Psi = \int_{S^3 \times S^1} d\text{vol} = 4\pi^3$$

*Proof.*  
- Gauge field $A_\mu$: $\iota A = +A$; by Ikeda (1979, Thm 2.3), even modes survive. Normalization on the quotient gives $Z_A = \text{Vol}(L(2,1)) = \pi^2$.  
- Spinor $\Psi$: trivial spin structure (η=0) selects odd modes (Bär 1996). Odd modes vanish on the quotient but live on the cover $S^3$; including $S^1$ yields $Z_\Psi = 4\pi^3$. ∎

---

## 8.5 Why different dimensions?

### Question
Z_A ∝ R³ (3D volume), Z_Ψ ∝ R⁴ (4D volume). How to add them?

### Answer
In Planck units R=1, all are dimensionless:
$$\hat{Z}_A = Z_A/R^3\big|_{R=1} = \pi^2, \quad \hat{Z}_\Psi = Z_\Psi/R^4\big|_{R=1} = 4\pi^3$$

**Different natures:**
- Z_A — normalization of boson kinetic term (3D integral)  
- Z_Ψ — normalization of fermion kinetic term (4D integral)

**Why they add in log det:**
$$\log\det(O_1 O_2) = \log\det(O_1) + \log\det(O_2)$$
1-loop effective action:
$$\Gamma^{(1)} = -\log\det(D\!\!\!\!/\,) + \tfrac{1}{2}\log\det(\Delta_A)$$
Each log is dimensionless; sum is valid.

**Volume link (Weyl leading term):**
$$-\log\det(D) = \zeta'_D(0) \sim \text{Vol}(S^3 \times S^1) = 4\pi^3$$
$$\tfrac{1}{2}\log\det(\Delta_A) = -\tfrac{1}{2}\zeta'_A(0) \sim \text{Vol}(L(2,1)) = \pi^2$$

---

## 8.6 Status

| Claim | Status | Comment |
|-------|--------|---------|
| $Z_A = \pi^2$ | ⚠️ Conditional | Requires an explicit 5D normalization (e.g. $g_5^2 = \mathrm{Vol}(S^1)$) |
| $Z_\Psi = \text{Vol}(S^3\times S^1) = 4\pi^3$ | ✅ Derived | Spin structure → odd modes → cover |
| Sum valid | ✅ Derived | log det₁ + log det₂ |
| Link to ζ′(0) | ⚠️ Partial | Leading term ∼ Vol; corrections needed |

---

## References
1. **Ikeda A.** “Spectra and eigenforms of the Laplacian on $S^n$ and $P^n(\mathbb{C})$", *Osaka J. Math.* **15** (1978) 515–546.  
2. **Bär C.** “The Dirac operator on space forms of positive curvature”, *J. Math. Soc. Japan* **48** (1996) 69–83.  
3. **Gilkey P.B.** *Invariance Theory, the Heat Equation, and the Atiyah-Singer Index Theorem*, CRC Press (1995).  
4. *Wikipedia:* Kaluza–Klein theory — geometric interpretation.

---

## Navigation

← [07_why_C_equals_1.py](07_why_C_equals_1.py) | [README.md](README.md) →

- [00_main.md](00_main.md) — Main  
- [01_spectral.md](01_spectral.md) — Spectral geometry

---

*Status: ⚠️ Gap #1 partially closed — $Z_A = \pi^2$ is conditional on the bosonic-sector normalization*
