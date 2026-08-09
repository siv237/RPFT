#!/usr/bin/env python3
"""
ANALYSIS OF THE C=1 COEFFICIENT IN 1/(π⁴·S²)

Goal: understand why C ≈ 1 (optimal C = 0.9936).
Method: explore 2-loop structure and geometric invariants.

Navigation:
  ← 13_casimir_explicit.py | README.md →
  Main: 00_main.md
"""

from mpmath import mp, pi, zeta as mpzeta, log, exp, sqrt
mp.dps = 80

print("="*70)
print("ANALYSIS OF COEFFICIENT C=1")
print("="*70)

# =============================================================================
# §1. INPUTS
# =============================================================================

print("\n§1. Inputs")
print("-"*40)

S_geo = 4*pi**3 + pi**2 + pi
alpha_codata = mp.mpf('137.035999177')
sigma = mp.mpf('0.000000085')

delta_24 = 1 / (24 * S_geo)
alpha_no_2loop = S_geo - delta_24
diff_no_2loop = alpha_no_2loop - alpha_codata

print(f"S_geo = {float(S_geo):.12f}")
print(f"α⁻¹ (no 2-loop) = {float(alpha_no_2loop):.12f}")
print(f"Diff = {float(diff_no_2loop):.2e}")
print(f"In σ = {float(diff_no_2loop/sigma):.1f}σ")

# Optimal C
C_opt = float((S_geo - delta_24 - alpha_codata) * pi**4 * S_geo**2)
print(f"\nOptimal C = {C_opt:.10f}")
print(f"Deviation from 1: {(C_opt - 1)*100:.4f}%")

# =============================================================================
# §2. HYPOTHESIS: C FROM NORMALIZATION
# =============================================================================

print("\n§2. Hypothesis: C from determinant normalization")
print("-"*40)

print("""
In 2-loop:
  Γ^(2) = (1/2!) × (Γ^(1))² × (top. factor)

Boson:  +1/2 × (...)²
Fermion: -1/2 × (...)² (Grassmann sign)

Sum → 0, not 1. Need another mechanism.
""")

c_boson = mp.mpf('0.5')    # 1/2!
c_fermion = mp.mpf('-0.5') # -1/2!
print(f"Boson: {float(c_boson)}, Fermion: {float(c_fermion)}, Sum = {float(c_boson + c_fermion)}")
print("→ simple sum cancels, so not the source.")

# =============================================================================
# §3. HYPOTHESIS: C = Vol(RP³)²/π⁴
# =============================================================================

print("\n§3. Hypothesis: C = Vol(RP³)²/π⁴")
print("-"*40)

Vol_RP3 = pi**2
Vol_RP3_squared = Vol_RP3**2

print(f"Vol(RP³) = π² = {float(Vol_RP3):.10f}")
print(f"Vol(RP³)² = π⁴ = {float(Vol_RP3_squared):.10f}")
print(f"Ratio Vol²/π⁴ = {float(Vol_RP3_squared / pi**4):.10f}")
print("Observation: π⁴ = (π²)² = Vol(RP³)² → 1/π⁴ = 1/Vol²; if invariant=1 → C=1.")

# =============================================================================
# §4. HYPOTHESIS: C VIA ζ(4)
# =============================================================================

print("\n§4. Hypothesis: C via ζ(4)")
print("-"*40)

zeta_4 = mpzeta(4)
print(f"ζ(4) = π⁴/90 = {float(zeta_4):.15f}")
print(f"π⁴/90 = {float(pi**4/90):.15f}")

C_from_zeta = 90 * zeta_4 / pi**4
print(f"90×ζ(4)/π⁴ = {float(C_from_zeta):.10f}")

delta_zeta4 = zeta_4 / S_geo**2
alpha_zeta4 = S_geo - delta_24 - delta_zeta4
diff_zeta4 = (alpha_zeta4 - alpha_codata) / sigma
print(f"\nWith δ = ζ(4)/S²: deviation = {float(diff_zeta4):.1f}σ (worse).")

# =============================================================================
# §5. SCAN NEAR C≈1
# =============================================================================

print("\n§5. Scan around C≈1")
print("-"*40)

print("C\t\tα⁻¹\t\t\tΔσ")
print("-"*50)
for C_test in [0.99, 0.993, 0.9936, 0.994, 0.995, 1.0, 1.005, 1.01]:
    delta_2loop = C_test / (pi**4 * S_geo**2)
    alpha_test = S_geo - delta_24 - delta_2loop
    diff_sigma = float((alpha_test - alpha_codata) / sigma)
    print(f"{C_test:.4f}\t\t{float(alpha_test):.12f}\t{diff_sigma:+.2f}σ")

# =============================================================================
# §6. SIMPLE REPRESENTATIONS
# =============================================================================

print("\n§6. Simple representations")
print("-"*40)

print(f"C_opt = {C_opt:.15f}")
candidates = [
    ("1", 1),
    ("1 - 1/π²", float(1 - 1/pi**2)),
    ("1 - 1/(2π²)", float(1 - 1/(2*pi**2))),
    ("π²/(π²+1)", float(pi**2/(pi**2+1))),
    ("1 - 1/S_geo", float(1 - 1/S_geo)),
    ("1 - 1/24", float(1 - 1/24)),
    ("cos(1/π)", float(mp.cos(1/pi))),
    ("1 - 1/137", float(1 - 1/137)),
    ("(24-1)/24", float(23/24)),
    ("exp(-1/S_geo)", float(exp(-1/S_geo))),
    ("1 - 1/(π²·24)", float(1 - 1/(pi**2 * 24))),
]
for name, val in candidates:
    diff_pct = (val - C_opt) / C_opt * 100
    print(f"  {name:20s} = {val:.10f}  (diff: {diff_pct:+.4f}%)")

# =============================================================================
# §7. BEST MATCH & C=1
# =============================================================================

print("\n§7. Best match & C=1")
print("-"*40)
best_name, best_val = min(candidates, key=lambda x: abs(x[1] - C_opt))
print(f"Closest: {best_name} = {best_val:.10f}")
print(f"C_opt = {C_opt:.10f}")
print(f"Diff: {(best_val - C_opt)*100:.6f}%")

delta_C1 = 1 / (pi**4 * S_geo**2)
alpha_C1 = S_geo - delta_24 - delta_C1
diff_C1 = (alpha_C1 - alpha_codata) / sigma
print(f"\nWith C=1: deviation = {float(diff_C1):.2f}σ → within experimental error.")

# =============================================================================
# §8. RADIATIVE CORRECTIONS HYPOTHESIS
# =============================================================================

print("\n§8. Radiative corrections hypothesis")
print("-"*40)

alpha_qed = 1/S_geo
delta_rad = alpha_qed / pi
C_corrected = 1 - delta_rad
print(f"α/π = {float(delta_rad):.10f}")
print(f"C = 1 - α/π = {float(C_corrected):.10f}")
print(f"Diff vs C_opt: {float((C_corrected - C_opt)*100):.4f}%")

delta_rad2 = alpha_qed / (2*pi)
print(f"C = 1 - α/(2π) = {float(1 - delta_rad2):.10f}")
print(f"C = 1 - 1/(π·S) = {float(1 - 1/(pi*S_geo)):.10f}")

# =============================================================================
# §9. SUMMARY
# =============================================================================

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"""
1. Optimal C = {C_opt:.10f} (deviation from 1: {(C_opt - 1)*100:.4f}%)
2. With C=1: deviation = {float(diff_C1):.2f}σ → OK experimentally.
3. Interpretations:
   - C = 1 as natural dimensionless choice
   - C ≈ 1 − α/π as possible radiative tweak
   - C = Vol(RP³)²/π⁴ = 1 as geometric identity
4. Status:
   - C=1 works to 0.64%
   - Strict derivation would need full 2-loop on L(2,1)×S¹
""")

# =============================================================================
# §10. FINAL CHECK
# =============================================================================

print("\n§10. Final formula")
print("-"*40)

alpha_final = S_geo - 1/(24*S_geo) - 1/(pi**4 * S_geo**2)
print("α⁻¹ = S_geo - 1/(24·S) - 1/(π⁴·S²)")
print(f"    = {float(S_geo):.12f}")
print(f"    - {float(1/(24*S_geo)):.15e}")
print(f"    - {float(1/(pi**4*S_geo**2)):.15e}")
print(f"    = {float(alpha_final):.15f}")
print(f"\nCODATA = {float(alpha_codata):.15f}")
print(f"Deviation = {float((alpha_final - alpha_codata)/sigma):.2f}σ")

print("="*70)
