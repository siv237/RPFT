# §10. COMPUTING THE a₂ COEFFICIENT AND THE ORIGIN OF 1/24

**Goal:** Explicitly compute the Seeley–DeWitt coefficient a₂ for \(M = L(2,1) \times S^1\) and show the link to 1/24.

---

## 10.1 Gilkey formula for a₂

### General formula (Gilkey 1975, Thm 4.1.6)
For the Laplacian on a d-dimensional Riemannian manifold without boundary:
$$a_2 = \frac{1}{(4\pi)^{d/2}} \int_M \frac{R^2 - 3R_{ij}R^{ij} + R_{ijkl}R^{ijkl}}{180} \, d\text{vol}$$

Scalar-field coefficients:
- \(c_1 = 1\) (R²)
- \(c_2 = -3\) (Ricci²)
- \(c_3 = 1\) (Riemann²)

### For spinors
$$a_2^{spinor} = \frac{1}{(4\pi)^{d/2}} \int_M \left( \frac{-R^2}{30} + \frac{R_{ij}R^{ij}}{12} + \frac{R_{ijkl}R^{ijkl}}{180} \right) d\text{vol}$$

---

## 10.2 Curvature of S³

Unit S³ metric:
$$ds^2 = d\chi^2 + \sin^2\chi (d\theta^2 + \sin^2\theta \, d\phi^2)$$

Constant curvature \(K = 1/R^2\); for \(R=1\):
$$R_{ijkl} = g_{ik}g_{jl} - g_{il}g_{jk}$$

Scalar invariants for S³:
- Scalar curvature: \(R = d(d-1)K = 6\)
- Ricci: \(R_{ij} = 2 g_{ij}\)
- Ricci²: \(R_{ij}R^{ij} = 12\)
- Riemann²: \(R_{ijkl}R^{ijkl} = 12\)

---

## 10.3 Curvature of RP³ = L(2,1)

RP³ = S³/Z₂, locally isometric to S³. Thus locally the same invariants:
- \(R = 6\)
- \(R_{ij}R^{ij} = 12\)
- \(R_{ijkl}R^{ijkl} = 12\)

Volume: Vol(RP³) = Vol(S³)/2 = \(\pi^2\).

---

## 10.4 Curvature of S¹

S¹ is flat:
- \(R = 0\)
- \(R_{ij} = 0\)
- \(R_{ijkl} = 0\)

Volume: Vol(S¹) = \(2\pi\) (R=1).

---

## 10.5 Curvature of the product \(L(2,1) \times S^1\)

For \(M \times N\):
- \(R(M\times N) = R(M) + R(N) = 6 + 0 = 6\)
- Ricci, Riemann block-diagonal

Integrals on \(M = L(2,1) \times S^1\):
$$\int_M R \, d\text{vol} = 6 \cdot \pi^2 \cdot 2\pi = 12\pi^3$$
$$\int_M R_{ij}R^{ij} \, d\text{vol} = 12 \cdot 2\pi^3 = 24\pi^3$$
$$\int_M R_{ijkl}R^{ijkl} \, d\text{vol} = 12 \cdot 2\pi^3 = 24\pi^3$$

---

## 10.6 Computing a₂ for \(M = L(2,1) \times S^1\)

### Scalar (d = 4)
$$a_2^{scalar} = \frac{1}{(4\pi)^2} \cdot \frac{1}{180} \left[ R^2 - 3 R_{ij}R^{ij} + R_{ijkl}R^{ijkl} \right] \cdot \text{Vol}$$
Plugging in:
$$a_2^{scalar} = \frac{1}{16\pi^2} \cdot \frac{1}{180} (36 - 36 + 12) \cdot 2\pi^3 = \frac{\pi}{120}$$

### Spinor (d = 4)
Different coefficients; structure similar (not expanded here).

---

## 10.7 Link to \(\zeta'(0)\) and Casimir

Formula:
$$\zeta'(0) = -\frac{1}{2} a_2 \cdot (\text{log factor})$$
For 4D:
$$-\zeta'(0) = a_2 + O(\text{finite})$$

**Where does 1/24 come from?**  
From \(\zeta_R(-1) = -1/12\):  
Casimir on S¹: \(E_{Cas}(S^1) = \frac{1}{2}\zeta(-1/2) = \zeta_R(-1) = -1/12\).  
For 4D normalization: \(\delta_{Cas} = -\tfrac{1}{2}(-1/12) = 1/24\).

### Alternative route
For \(M^3 \times S^1\):
$$a_2(M \times S^1) = a_2(M) \cdot L_{S^1} + a_{3/2}(M)a_{1/2}(S^1) + a_1(M)a_1(S^1) + \ldots$$
With \(L_{S^1} = 2\pi\) and \(a_k(S^1) = 0\) for \(k>0\):
$$a_2(M \times S^1) = 2\pi \cdot a_2(M)$$

For RP³:
$$a_2(RP^3) = \frac{1}{(4\pi)^{3/2}} \cdot \frac{R_{3D}}{6} \cdot \text{Vol}(RP^3) = \frac{\pi^{1/2}}{8}$$
*Note:* normalization is delicate; careful bookkeeping needed.

---

## 10.8 Numerical check

```python
from mpmath import mp, pi
mp.dps = 50

# Curvature invariants for RP³
R = 6
Rij2 = 12
Rijkl2 = 12
Vol_RP3_S1 = pi**2 * 2*pi  # = 2π³

# a₂ for scalar in 4D
a2_integrand = (R**2 - 3*Rij2 + Rijkl2) / 180  # (36 -36 +12)/180 = 1/15
a2 = a2_integrand * Vol_RP3_S1 / (4*pi)**2    # (1/15)*2π³ /16π² = π/120

print(f"a₂ = {float(a2):.10f}")
print(f"a₂ / Vol = {float(a2 / Vol_RP3_S1):.10f}")
```

---

## 10.9 Status of the 1/24 derivation

| Step | Status | Comment |
|------|--------|---------|
| Gilkey formula | ✅ | Standard |
| Curvature of RP³ | ✅ | K=1, R=6 |
| a₂ computation | ✅ | Direct |
| **Link \(a_2 \leftrightarrow 1/24\)** | ⚠️ | Needs careful normalization |

**Honest take:** 1/24 arises from:
1. \(\zeta_R(-1) = -1/12\) (S¹ Casimir)  
2. Factor 1/2 from regularization  
→ \(1/(2 \times 12) = 1/24\)

Gilkey gives the **structure** of a₂; the exact 1/24 comes from the 1D Casimir via \(\zeta_R(-1)\), not yet from a completed 4D explicit evaluation.

---

## 10.10 Recommendations

1. Compute a₂ for the specific spinor operator on RP³ × S¹.  
2. Check \(a_2\)–\(\zeta'(0)\) link via heat-kernel asymptotics.  
3. Compare with known lens-space results (Dowker 1977).

---

## Navigation

← [09_topological_term.md](09_topological_term.md) | [README.md](README.md) →

---

*Status: ⚠️ Structure correct; exact 1/24 needs further validation*
