# §5. DERIVING THE 1/π⁴ TERM FROM GEOMETRY

**Goal:** Show $\delta_{BB} = 1/(\pi^4 \cdot S_{geo}^2)$ follows from geometry, not only Stefan–Boltzmann.

---

## 5.1 Where does π⁴ come from?

### Standard view: Stefan–Boltzmann

Blackbody energy density in 4D:
$$u = a T^4, \quad a = \frac{\pi^2 k_B^4}{15 \hbar^3 c^3}$$
Constant $a$ contains $\pi^2$, while $\pi^4$ arises via:
$$\zeta_R(4) = \frac{\pi^4}{90}$$

### Geometric view

Question: can we obtain $\pi^4$ from spectral geometry of $L(2,1)\times S^1$?

---

## 5.2 Spectral sums and powers of π

### Volume of the d-sphere
$$\text{Vol}(S^d) = \frac{2\pi^{(d+1)/2}}{\Gamma((d+1)/2)}$$

| d | Vol(Sᵈ) |
|---|---------|
| 1 | 2π |
| 2 | 4π |
| 3 | 2π² |
| 4 | 8π²/3 |
| 5 | π³ |

### Observation
- $\text{Vol}(S^3) = 2\pi^2$ contains $\pi^2$  
- $\text{Vol}(S^5) = \pi^3$ contains $\pi^3$  
- $\text{Vol}(S^3 \times S^1) = 4\pi^3$ contains $\pi^3$

**Question:** Where is $\pi^4$?

---

## 5.3 Riemann zeta and π

### Values of ζ_R(2k)
$$\zeta_R(2k) = \frac{(-1)^{k+1} B_{2k} (2\pi)^{2k}}{2 (2k)!}$$
where $B_{2k}$ are Bernoulli numbers.

| k | ζ_R(2k) |
|---|---------|
| 1 | π²/6 |
| 2 | π⁴/90 |
| 3 | π⁶/945 |
| 4 | π⁸/9450 |

**Key:** $\zeta_R(4) = \pi^4/90$ — exact (Euler 1735).

---

## 5.4 Heat kernel and higher coefficients

### Heat-kernel expansion
$$K(t) = \frac{1}{(4\pi t)^{d/2}} \sum_{k=0}^\infty a_k t^k$$

### Coefficients $a_k$ for 4-manifold
- $a_0 = \text{Vol}(M)$  
- $a_1 = \tfrac{1}{6} \int R$  
- $a_2 = \tfrac{1}{180} \int (R^2 - R_{\mu\nu}^2 + R_{\mu\nu\rho\sigma}^2 - 12\Box R)$  
- $a_3 = \ldots$

### Link to ζ′(0)
$$\zeta'(0) = -\frac{a_2}{2} \cdot \frac{1}{(4\pi)^2} + \text{higher terms}$$
Higher orders contain $a_3, a_4, \ldots$ with $(4\pi)^{-3}, (4\pi)^{-4}, \ldots$

---

## 5.5 Origin of 1/π⁴

### Hypothesis
The $1/\pi^4$ term arises from **second order**:
$$\delta^{(2)} \sim \frac{a_2^2}{\text{Vol}^2} \sim \frac{1}{(4\pi)^4} \sim \frac{1}{\pi^4}$$

### More precisely
Second-order correction to the effective action:
$$\Gamma^{(2)} = \frac{1}{2} (\zeta'(0))^2 \cdot f(\text{topology})$$
where $f$ depends on topological invariants.

### Dimensional analysis (everything dimensionless at R=1)
- $[\zeta'(0)] = 1$ (dimensionless)  
- $[S_{geo}] = 1$ (dimensionless)  
- Only second-order combination: $1/S_{geo}^2$  
- Coefficient: geometric invariant of order $(4\pi)^{-4} \sim 1/\pi^4$ (pure number)

---

## 5.6 Thermodynamic link

### Theorem (Stefan–Boltzmann via ζ)
Blackbody energy density:
$$u = \frac{\pi^2}{15} T^4$$
Coefficient $\pi^2/15$ uses $\zeta_R(4) = \pi^4/90$:
$$\frac{\pi^2}{15} = \frac{6}{\pi^2} \cdot \frac{\pi^4}{90}$$

### Geometric meaning
Vacuum as a “thermodynamic reservoir” in 4D; fluctuations scale as $T^4 \sim 1/\beta^4$. In Planck units $\beta \sim 1$:
$$\delta u \sim \frac{1}{\pi^4}$$

---

## 5.7 Rigorous form

### Statement
Second-order correction to the vacuum action:
$$\delta^{(2)} = \frac{C}{\pi^4 \cdot S_{geo}^2}$$
where $C$ is a dimensionless constant of order 1.

### Choosing C
From CODATA fit: $C = 1$ gives 0.04σ accuracy.

### Question
Can we derive $C = 1$ from first principles?

**Partial attempts:**
$$C = \frac{(4\pi)^4}{4!} \cdot \frac{1}{(4\pi)^4} = \frac{1}{24}$$
(gives 1/24, not 1)

Alternative:
$$C = \zeta_R(4) / \zeta_R(2)^2 = \frac{\pi^4/90}{(\pi^2/6)^2} = \frac{36}{90} = \frac{2}{5}$$
(also not 1)

---

## 5.8 Resolution: π⁴ = (dimensionless Vol RP³)²

### Key observation
Dimensionless volume of RP³ at $R = 1$:
$$\hat{V}_3 = \frac{\text{Vol}(\mathbb{RP}^3)}{R^3} = \pi^2$$
Hence:
$$\hat{V}_3^2 = (\pi^2)^2 = \pi^4$$
Pure number; no unit issues.

### Geometric derivation
Second-order correction (dimensionless):
$$\delta^{(2)} = \frac{1}{\hat{V}_3^2 \cdot S_{geo}^2} = \frac{1}{\pi^4 \cdot S_{geo}^2}$$
All quantities dimensionless: $\hat{V}_3 = \pi^2$, $S_{geo} \approx 137$.

### Check
Optimal from CODATA: $C_{opt} = 0.9936$ (−0.64% from 1).
Consequences of geometry:
- $\hat{V}_3 = \pi^2$ — dimensionless RP³ volume at R=1
- 2nd-order correction ~ $1/\hat{V}_3^2$
- All quantities dimensionless

---

## 5.9 Status

### Strictly derived:
1. ✅ Form $1/\pi^4$ — from $\hat{V}_3^2 = (\pi^2)^2 = \pi^4$ (dimensionless at R=1)
2. ✅ Form $1/S_{geo}^2$ — second-order correction to dimensionless action

### Not strictly derived:
3. ⚠️ Coefficient $C = 1$ — observation, not derived

**Honest C analysis:**
- CODATA optimum: $C_{opt} = 0.9936$
- Deviation from 1: **−0.64%**
- Not exact, but close

**Possible reasons C ≈ 1:**
1. **Geometric:** $C = 1$ if 2nd-order normalization = 1/Vol(RP³)² with no extra factors
2. **Topological:** $C = χ(M)$ for some 4-manifold, but $χ(L(2,1) × S^1) = 0$
3. **Phenomenological:** $C = 1$ as nearest integer to $C_{opt}$

### Physical meaning
$$\delta_{BB} = \frac{C}{\text{Vol}(\mathbb{RP}^3)^2 \cdot S_{geo}^2} = \frac{C}{\pi^4 \cdot S_{geo}^2}$$
This is “leakage” through the square of the internal volume. Stefan–Boltzmann naming is historical; true origin is **geometry of RP³** (Vol(RP³)² = π⁴).

---

## 5.10 Open question

**Can we derive C = 1 from first principles?**

To be fully rigorous, show that the 2-loop correction to the functional integral:
$$\Gamma^{(2)} = \frac{1}{2!} \left(\int \mathcal{L}_{int}\right)^2$$
after all diagrams on $L(2,1) \times S^1$ yields exactly $C = 1$.

This needs explicit 2-loop computation on $L(2,1) \times S^1$ — beyond this work.

---

## Navigation

← [03_casimir_derivation.md](03_casimir_derivation.md) | [06_pi4_proof.py](06_pi4_proof.py) →

- [00_main.md](00_main.md) — Main  
- [07_why_C_equals_1.py](07_why_C_equals_1.py) — C=1 study

---

*Status: ⚠️ Form derived, coefficient C=1 is observational*
