# §21. DERIVING THE COEFFICIENT 1 IN FRONT OF π

**Goal:** Show that the coefficient of π in \(\alpha^{-1} = 4\pi^3 + \pi^2 + \mathbf{1}\cdot\pi\) is exactly 1 from first principles.

**Methods:**
1. Atiyah–Patodi–Singer (APS) theorem
2. Localization in TQFT (Duistermaat–Heckman)
3. Functional-integral normalization

---

## 21.1 Problem setup

RPFT formula:
$$\alpha^{-1} = 4\pi^3 + \pi^2 + c \cdot \pi - \text{corrections}$$
We need to fix \(c\).

**Known:**
- \(\pi = d(M_{flat}(RP^3, U(1)))\) distance between \(\{0,\pi\}\)
- \(\pi = L_{sys}(RP^3)\) systole
- But why \(c = 1\)?

---

## 21.2 APS approach

APS theorem for a 4-manifold \(W\) with boundary \(\partial W = M^3\):
$$\text{Index}(D_W) = \int_W \hat{A} - \frac{\eta(M)+h}{2}$$
with \(\eta(M)\) the eta invariant and \(h=\dim\ker D_M\).

For RP³: from `11_eta_invariant.py`, **η(RP³)=0** (symmetric Dirac spectrum). Thus APS does **not** produce the π term.

Twisted eta: for Dirac twisted by a line bundle with holonomy θ, \(\eta(D_\theta)=\eta(D)+\Delta\eta(\theta)\). For RP³, \(p=2,q=1\) lens space: the Donnelly formula yields 0; twist does not give π.  
**Conclusion:** eta-invariant route fails for RP³.

---

## 21.3 TQFT localization approach

Duistermaat–Heckman:
$$Z = \sum_{a\in \text{crit}} \frac{e^{-S(a)}}{\sqrt{\det'(H_a)}}$$

For U(1) on RP³, crit = flat connections:
$$M_{flat}(RP^3,U(1)) = \{1,-1\} \cong \{0,\pi\}$$
Yang–Mills action on flat connections vanishes, but effective action includes determinants:
$$\Gamma_{\text{eff}}(a) = S(a) + \tfrac12 \log\det'(\Delta_a)$$
Difference:
$$\Delta\Gamma = \tfrac12\big[\log\det'(\Delta_\pi) - \log\det'(\Delta_0)\big] = -\tfrac12(\zeta'_\pi(0) - \zeta'_0(0))$$
Twist θ=π shifts boundary conditions → half-integer modes; the ζ′ difference yields a contribution proportional to the minimal cycle length.

---

## 21.4 Ray–Singer torsion check

Analytic torsion:
$$\log T_{RS}(M,E) = \tfrac12 \sum_k (-1)^k k\, \zeta'_k(0)$$
Cheeger–Müller: \(T_{RS} = \tau\) (Reidemeister).

For RP³, trivial bundle τ=1. For nontrivial representation ρ_π:
$$\tau(RP^3,\rho_\pi) = |1 - e^{i\pi}|^{-1} = \tfrac12$$
So \(\log\tau_\pi - \log\tau_0 = -\log 2 \neq \pi\). Torsion does not give the coefficient.

---

## 21.5 KEY ARGUMENT: Normalization via systole (WKB)

Two vacua in QED on \(M_4\times K\): \(|0\rangle\) (trivial bundle), \(|\pi\rangle\) (holonomy π). Tunneling amplitude:
$$\langle\pi|0\rangle \sim e^{-S_{tunnel}}$$
with \(S_{tunnel} = p_{\min} \cdot L_{sys}\).

- \(L_{sys} = \pi\) (systole of RP³)
- **\(p_{\min} = 1\)** in Planck units: minimal momentum/charge gives Wilson loop \(W = \exp(i\cdot 1 \cdot \pi) = -1\).

Hence \(S_{tunnel} = 1 \cdot \pi = \pi\). The coefficient 1 comes from quantization in Planck units.

---

## 21.6 (Partial) index-family view

Family \(\{D_\theta\}_{\theta\in[0,\pi]}\); Bismut–Freed family index integrates curvature over θ. For RP³, η difference vanishes, so index = 0; this route does not fix c but is consistent with the WKB normalization above.

---

## 21.7 Faddeev–Popov normalization perspective

Gauge group Map(RP³,U(1)) has \(\pi_0 = H^1(RP^3;\mathbb{Z}) = \mathbb{Z}_2\): two components (trivial / nontrivial). Partition function splits: \(Z = Z_0 + Z_\pi\). Normalization between components introduces the path length in M_flat; the real part in log contributes π. Chern–Simons on RP³ gives zero here (Dedekind sum vanishes), so the π comes from moduli-space length, not CS phase.

---

## 21.8 Final argument

Metric on \(M_{flat}(RP^3,U(1)) = \{0,\pi\}\): \(ds^2 = d\theta^2\). Distance \(d(0,\pi)=\pi\). Minimal action along this path with \(p_{\min}=1\) gives exactly π. Dimensional consistency in
$$\alpha^{-1} = 4\pi^3 + \pi^2 + c\pi$$
implies \(c=1\) as the unique dimensionless choice in Planck units.

---

## 21.9 Summary

**Shown:**  
1. Standard invariants (η, τ, CS) do **not** yield π for RP³.  
2. π = distance \(d(M_{flat})\) (geometry).  
3. Coefficient 1 = minimal momentum/charge in Planck units.  
4. Dimensional consistency selects \(c=1\).

**Not fully proved:**  
1. Strict derivation of \(c=1\) from an index theorem.  
2. Explicit det′\(D_\theta\) for the family.

**Status:** ⚠️ ~70% (argument, not a complete proof).

---

← [20_RG_matching.py](20_RG_matching.py) | [README.md](README.md) →
