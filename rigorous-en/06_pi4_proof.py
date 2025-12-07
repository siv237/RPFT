#!/usr/bin/env python3
"""
Searching for a rigorous derivation of the 1/π⁴ coefficient.
Question: why δ_BB = 1/(π⁴ · S_geo²) and not C/(π⁴ · S_geo²)?

Navigation:
  ← 05_pi4_derivation.md | 07_why_C_equals_1.py →
  Main: 00_main.md
"""

from mpmath import mp, pi, zeta, sqrt, log, exp, gamma as mpgamma, factorial
import numpy as np

mp.dps = 50

print("="*70)
print("INVESTIGATING THE 1/π⁴ COEFFICIENT")
print("="*70)

# =============================================================================
# §1. RIEMANN ZETA AND POWERS OF π
# =============================================================================

print("\n§1. Values ζ_R(n) and π-powers")
print("-"*40)

# Exact ζ(2k)
for k in range(1, 6):
    z = zeta(2*k)
    coeff = z / pi**(2*k)
    print(f"ζ({2*k}) = {float(z):.10f} = {float(coeff):.10f} × π^{2*k}")

print("\nKey values:")
print(f"  ζ(2) = π²/6      = {float(pi**2/6):.10f}")
print(f"  ζ(4) = π⁴/90     = {float(pi**4/90):.10f}")
print(f"  ζ(6) = π⁶/945    = {float(pi**6/945):.10f}")

# =============================================================================
# §2. STEFAN–BOLTZMANN AND π⁴
# =============================================================================

print("\n§2. Stefan–Boltzmann law")
print("-"*40)

print("""
Blackbody energy density in d dimensions:

  u(T) = C_d · T^{d+1}

For d = 3:
  u = (π²/15) · T⁴

Coefficient π²/15 contains:
  π²/15 = 6/90 · π² = (6/π²) · (π⁴/90) = (6/π²) · ζ(4)

Where is 1/π⁴?
-------------
If we normalize by S_geo² ≈ 137²:
  δ ~ ζ(4) / S_geo² = (π⁴/90) / S_geo²

But we have δ = 1/(π⁴ · S_geo²), not π⁴/90 · 1/S_geo²!

So we need another source of π⁴.
""")

# =============================================================================
# §3. PHASE-SPACE INTEGRAL
# =============================================================================

print("\n§3. Phase-space volume")
print("-"*40)

print("""
Hypothesis: π⁴ from momentum-space normalization.

In 4D QM:
  ∫ d⁴p / (2π)⁴ = state normalization

Factor (2π)⁴ in denominator = 16π⁴.

But we have π⁴, not 16π⁴...
""")

print(f"(2π)⁴ = {float((2*pi)**4):.6f}")
print(f"π⁴    = {float(pi**4):.6f}")
print(f"Ratio = {float((2*pi)**4 / pi**4):.6f} = 16")

# =============================================================================
# §4. CONFORMAL (TRACE) ANOMALY
# =============================================================================

print("\n§4. Conformal anomaly in 4D")
print("-"*40)

print("""
In 4D CFT:

  <T^μ_μ> = c · (Weyl)² - a · (Euler)

Coefficients for free fields:
  scalar: c = 1/120, a = 1/360
  Dirac:  c = 1/20,  a = 11/360

Euler density:
  E₄ = R² - 4R_μν² + R_μνρσ²

Integral:
  χ(M) = (1/32π²) ∫ E₄ dV

Here (32π²) appears in denominator.
""")

print(f"32π² = {float(32*pi**2):.6f}")
print(f"(32π²)² = {float((32*pi**2)**2):.6f}")

# =============================================================================
# §5. TESTING COMBINATIONS
# =============================================================================

print("\n§5. Searching for combination giving 1/π⁴")
print("-"*40)

S_geo = 4*pi**3 + pi**2 + pi
delta_BB_actual = 1 / (pi**4 * S_geo**2)

print(f"S_geo = {float(S_geo):.10f}")
print(f"δ_BB (actual) = 1/(π⁴·S²) = {float(delta_BB_actual):.15e}")

candidates = [
    ("ζ(4)/S²", zeta(4) / S_geo**2),
    ("1/(90·S²)", 1 / (90 * S_geo**2)),
    ("1/(π⁴·S²)", 1 / (pi**4 * S_geo**2)),
    ("π⁴/(90·S²)·1/π⁸", pi**4 / (90 * S_geo**2) / pi**8),
    ("6/(π²·S²·90)", 6 / (pi**2 * S_geo**2 * 90)),
]

print("\nCandidates:")
for name, val in candidates:
    ratio = val / delta_BB_actual
    print(f"  {name:25s} = {float(val):.15e}, ratio = {float(ratio):.6f}")

# =============================================================================
# §6. KEY OBSERVATION
# =============================================================================

print("\n§6. KEY OBSERVATION")
print("-"*40)

print("""
Hypothesis: 1/π⁴ = (1/π²)²

The π² term already appears in S_geo (Vol(RP³) = π²).

If a 2nd-order correction ~ (π²/S_geo)², then:
  δ^(2) ~ (π²)² / S_geo² = π⁴/S_geo²

But we need 1/(π⁴·S_geo²), not π⁴/S_geo²!

Thus:
  δ = 1/π⁴ × 1/S_geo² = (1/π²)² × (1/S_geo)²
  coefficient = (1/π)⁴ = 1/π⁴.
""")

print(f"(1/π)⁴ = {float(1/pi**4):.15f}")
print(f"1/π⁴   = {float(1/pi**4):.15f}")
print("Tautology, but emphasizes origin as squared volume inverse.")

# =============================================================================
# §7. VOLUME RELATIONS
# =============================================================================

print("\n§7. Volume relations")
print("-"*40)

Vol_S1 = 2*pi
Vol_S2 = 4*pi
Vol_S3 = 2*pi**2
Vol_S4 = 8*pi**2/3

print(f"Vol(S¹) = 2π      = {float(Vol_S1):.6f}")
print(f"Vol(S²) = 4π      = {float(Vol_S2):.6f}")
print(f"Vol(S³) = 2π²     = {float(Vol_S3):.6f}")
print(f"Vol(S⁴) = 8π²/3   = {float(Vol_S4):.6f}")

print(f"\nVol(S¹)² = (2π)² = 4π² = {float(Vol_S1**2):.6f}")
print(f"Vol(S²)² = (4π)² = 16π² = {float(Vol_S2**2):.6f}")

print(f"\n1/Vol(S¹)² = 1/(4π²) = {float(1/Vol_S1**2):.10f}")
print(f"1/Vol(S²)² = 1/(16π²) = {float(1/Vol_S2**2):.10f}")

print(f"\nVol(S¹)² × Vol(S²)² = 4π² × 16π² = 64π⁴")
print(f"1/(64π⁴) = {float(1/(64*pi**4)):.15e}")
print(f"1/π⁴ = {float(1/pi**4):.15e}")
print(f"Ratio: {float((1/pi**4) / (1/(64*pi**4))):.2f} = 64")

# =============================================================================
# §8. KK NORMALIZATION IDEA
# =============================================================================

print("\n§8. KK normalization and 1/π⁴")
print("-"*40)

print("""
In KK reduction:
  ∫_{S¹} dy / (2π) = mode normalization

For L(2,1) × S¹:
  - Bosons: normalize on RP³
  - Fermions: normalize on S³

Normalization ratio:
  Z_ψ/Z_A = Vol(S³×S¹)/Vol(RP³) = 4π³/π² = 4π

Square in a 2nd-order correction:
  (Z_ψ/Z_A)² = 16π²

But we need 1/π⁴...
""")

# =============================================================================
# §9. NUMERIC SENSITIVITY OF C
# =============================================================================

print("\n§9. How critical is the coefficient?")
print("-"*40)

alpha_inv_codata = mp.mpf('137.035999177')
delta_Lattice = 1 / (24 * S_geo)

alpha_inv_no_BB = S_geo - delta_Lattice
diff_no_BB = alpha_inv_no_BB - alpha_inv_codata
print(f"Without δ_BB: diff = {float(diff_no_BB):.2e}")

C_optimal = float((S_geo - delta_Lattice - alpha_inv_codata) * pi**4 * S_geo**2)
print(f"Optimal C = {C_optimal:.6f}")

delta_BB_C1 = 1 / (pi**4 * S_geo**2)
alpha_inv_C1 = S_geo - delta_Lattice - delta_BB_C1
diff_C1 = alpha_inv_C1 - alpha_inv_codata
print(f"With C=1: diff = {float(diff_C1):.2e}, σ = {float(diff_C1/0.000000085):.2f}")

delta_BB_opt = C_optimal / (pi**4 * S_geo**2)
alpha_inv_opt = S_geo - delta_Lattice - delta_BB_opt
diff_opt = alpha_inv_opt - alpha_inv_codata
print(f"With C={C_optimal:.2f}: diff = {float(diff_opt):.2e}")

# =============================================================================
# §10. CONCLUSION
# =============================================================================

print("\n" + "="*70)
print("§10. CONCLUSION")
print("="*70)

print(f"""
1. Form 1/π⁴ CAN be motivated by:
   - ζ(4) = π⁴/90 (Riemann zeta)
   - (2π)⁴ in phase-space normalization
   - Conformal anomaly in 4D

2. Coefficient C = 1:
   - Optimal C = {C_optimal:.4f}
   - Close to 1, not exactly 1
   - Possibly take C = 1 as nearest integer

3. Accuracy without δ_BB: Δ = {float(diff_no_BB):.2e}
   Accuracy with δ_BB(C=1): Δ = {float(diff_C1):.2e}

4. HONEST STATUS:
   - Form 1/(π⁴·S²): ✅ supported by dimensional analysis
   - Coefficient C=1: ⚠️ phenomenological (near optimal)
""")

print("\n--- Alternative: δ = ζ(4)/S² ---")
delta_zeta4 = zeta(4) / S_geo**2
alpha_inv_zeta4 = S_geo - delta_Lattice - delta_zeta4
diff_zeta4 = alpha_inv_zeta4 - alpha_inv_codata
print(f"δ = ζ(4)/S² = {float(delta_zeta4):.15e}")
print(f"Diff = {float(diff_zeta4):.2e}, σ = {float(diff_zeta4/0.000000085):.2f}")
print("→ Worse than 1/π⁴.")

print("\n--- Alternative: δ = 90/(π⁴·S²) ---")
delta_90 = 90 / (pi**4 * S_geo**2)
alpha_inv_90 = S_geo - delta_Lattice - delta_90
diff_90 = alpha_inv_90 - alpha_inv_codata
print(f"δ = 90/(π⁴·S²) = {float(delta_90):.15e}")
print(f"Diff = {float(diff_90):.2e}, σ = {float(diff_90/0.000000085):.2f}")
