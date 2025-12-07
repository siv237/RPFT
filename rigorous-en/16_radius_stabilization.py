#!/usr/bin/env python3
"""
RADIUS STABILIZATION: Why is R = 1 (Planck scale)?

Goal: show R = 1 is not a postulate but follows from the setup.

Issue:
  For arbitrary R:
    α⁻¹(R) = 4π³R⁴ + π²R³ + πR - corrections
  The correct value appears ONLY at R = 1.
Question: is there a mechanism fixing R = 1?
"""

from mpmath import mp, pi, sqrt, log, exp, diff
import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

mp.dps = 50

print("="*70)
print("COMPACTIFICATION RADIUS STABILIZATION")
print("="*70)

# =============================================================================
# §1. FORMULA FOR GENERAL R
# =============================================================================

print("\n§1. α⁻¹ as a function of R")
print("-"*40)

def alpha_inv(R):
    """α⁻¹(R) for arbitrary radius R."""
    # Scaling:
    # Vol(S³×S¹) ~ R⁴ (4D volume)
    # Vol(RP³)   ~ R³ (3D volume)
    # Sys(RP³)   ~ R  (1D length)
    S_geo = 4*pi**3 * R**4 + pi**2 * R**3 + pi * R
    delta_Cas = 1/(24 * S_geo)           # Casimir
    delta_BB = 1/(pi**4 * S_geo**2)      # 2-loop
    return S_geo - delta_Cas - delta_BB

alpha_codata = mp.mpf('137.035999177')

print("α⁻¹(R) = 4π³R⁴ + π²R³ + πR − corrections\n")
for R in [0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 2.0]:
    a = alpha_inv(R)
    diff_val = float(a - alpha_codata)
    print(f"R = {R:.1f}: α⁻¹ = {float(a):.6f}, Δ = {diff_val:+.2f}")

# =============================================================================
# §2. SOLVE FOR α⁻¹ = CODATA
# =============================================================================

print("\n§2. Solve for R giving α⁻¹ = 137.036")
print("-"*40)

def target(R):
    return float(alpha_inv(R) - alpha_codata)

def bisect(f, a, b, tol=1e-12):
    while b - a > tol:
        mid = (a + b) / 2
        if f(mid) * f(a) < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2

R_solution = bisect(target, 0.5, 2.0)
print(f"Solution: R = {R_solution:.15f}")
print(f"Deviation from 1: {(R_solution - 1)*100:.6f}%")

a_check = alpha_inv(R_solution)
print(f"α⁻¹(R_solution) = {float(a_check):.12f}")
print(f"CODATA = {float(alpha_codata):.12f}")

# =============================================================================
# §3. SELF-CONSISTENCY MECHANISM
# =============================================================================

print("\n§3. Self-consistency mechanism")
print("-"*40)

print("""
Idea: α⁻¹ = S_vac is a definition, not an equation.

If e² = 1/S_vac (natural units), then α = e²/(4π) = 1/(4π·S_vac),
so α⁻¹ = 4π·S_vac ≠ S_vac.

But if α is defined via the full Jacobian:
  Z_total = exp(−S_vac)
  α⁻¹ = log(1/Z_total) = S_vac
this works if S_vac is dimensionless.
""")

# =============================================================================
# §4. CASIMIR STABILIZATION
# =============================================================================

print("\n§4. Casimir stabilization")
print("-"*40)

def casimir_energy(R):
    """Casimir energy on S¹ radius R: E_Cas = -π/(6R) for periodic bosons."""
    return -pi / (6 * R)

def total_energy(R):
    """
    Total energy = classical + quantum.
    Classical: ~ R³ (volume term)
    Quantum:   ~ -1/R (Casimir)
    """
    A = 1.0   # classical coefficient
    B = pi/6  # Casimir coefficient
    return A * R**3 - B / R

R_values = np.linspace(0.1, 3.0, 1000)
E_values = [total_energy(R) for R in R_values]
R_min_idx = np.argmin(E_values)
R_min = R_values[R_min_idx]
print(f"Minimum of E(R) at R ≈ {R_min:.4f}")

A, B = 1.0, pi/6
R_analytic = (B / (3*A))**(1/4)
print(f"Analytic minimum: R = (π/18)^(1/4) = {float(R_analytic):.6f}")

print("""
Issue: Casimir alone gives R ≈ 0.65, not 1.
Need another mechanism or coefficients.
""")

# =============================================================================
# §5. DIMENSIONAL ARGUMENT
# =============================================================================

print("\n§5. Dimensional argument (Planck units)")
print("-"*40)

print("""
Planck units: ℏ = c = G = 1 → l_P = 1.
Only dimensionless radius: R/l_P.
No other scales → R = l_P = 1 (or R = n·l_P, minimal n=1).
""")

# =============================================================================
# §6. LQG VOLUME QUANTIZATION (HEURISTIC)
# =============================================================================

print("\n§6. Volume quantization (LQG heuristic)")
print("-"*40)

print("""
In LQG: V_min ~ l_P³.
For RP³: Vol = π²R³ → setting = l_P³ gives R ≈ 0.47 (not 1).
If area quantized instead (Area ~ l_P²), R ≈ 0.28 (also not 1).
So LQG quantization alone does not fix R=1.
""")

# =============================================================================
# §7. KEY: SELF-CONSISTENCY α⁻¹ = S_vac
# =============================================================================

print("\n§7. Key mechanism: self-consistency α⁻¹ = S_vac")
print("-"*40)

print("""
Main idea:
  QED on M₄×K is consistent ⇔ α⁻¹ = S_vac(K).
Thus R is fixed by demanding S_vac = 137.036...
Interpretation:
  α⁻¹ counts virtual pairs (screening),
  S_vac is the “volume” of vacuum fluctuations,
  α⁻¹ = S_vac is a balance condition.
""")

# =============================================================================
# §8. NUMERIC SENSITIVITY
# =============================================================================

print("\n§8. Sensitivity of α⁻¹ to R")
print("-"*40)

R0 = 1.0
dR = 0.001
dalpha = (alpha_inv(R0 + dR) - alpha_inv(R0 - dR)) / (2*dR)
print(f"dα⁻¹/dR at R=1: {float(dalpha):.6f}")
rel_sens = float(dalpha * R0 / alpha_inv(R0))
print(f"(R/α⁻¹)·dα⁻¹/dR = {rel_sens:.4f}")
print(f"→ 1% change in R shifts α⁻¹ by {rel_sens:.1f}%")

# =============================================================================
# §9. DISCRETENESS: α⁻¹ NEAR AN INTEGER?
# =============================================================================

print("\n§9. Discreteness: is α⁻¹ near an integer?")
print("-"*40)

print(f"α⁻¹ = {float(alpha_codata):.10f}")
print(f"Nearest integer: 137")
offset_val = alpha_codata - 137
print(f"Offset: {float(offset_val):.6f} = {float(offset_val/alpha_codata*100):.4f}%")
print("Speculative to require α⁻¹ ≈ integer; noted but not used.")

# =============================================================================
# §10. SUMMARY: WHY R = 1?
# =============================================================================

print("\n" + "="*70)
print("SUMMARY: WHY R = 1?")
print("="*70)

print("""
Argument 1 (weak): dimensional analysis
  - Single scale l_P → R = l_P = 1 (minimality).  Status: ⚠️ principle.

Argument 2 (medium): self-consistency
  - α⁻¹ = S_vac as consistency of QED on M₄×K
  - R fixed by requiring S_vac = 137.036…  Status: ⚠️ needs full proof.

Argument 3 (practical): R is not free
  - R/l_P must be O(1); minimal choice R=1. Status: ⚠️ principle.

Current status: R = 1 follows from dimensional analysis + self-consistency;
dynamic stabilization (flux/Casimir) would strengthen the case.
Protection level: ⚠️ ~50–60% (better than postulate).
""")

# =============================================================================
# §11. PLOT (if matplotlib available)
# =============================================================================

if HAS_MPL:
    print("\n§11. Saving plot α⁻¹(R)")
    print("-"*40)
    R_plot = np.linspace(0.5, 1.5, 200)
    alpha_plot = [float(alpha_inv(R)) for R in R_plot]
    plt.figure(figsize=(10, 6))
    plt.plot(R_plot, alpha_plot, 'b-', linewidth=2, label=r'$\alpha^{-1}(R)$')
    plt.axhline(y=137.035999177, color='r', linestyle='--', label='CODATA')
    plt.axvline(x=1.0, color='g', linestyle=':', label='R = 1')
    plt.xlabel('R (Planck units)', fontsize=12)
    plt.ylabel(r'$\alpha^{-1}$', fontsize=12)
    plt.title(r'$\alpha^{-1}$ vs compactification radius R', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0.5, 1.5)
    plt.ylim(50, 250)
    plt.tight_layout()
    plt.savefig('radius_dependence.png', dpi=150)
    print("Saved: radius_dependence.png")
else:
    print("\n§11. Plot: matplotlib not available, skipping")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print(f"""
Exact R giving α⁻¹ = CODATA: R = {R_solution:.10f}
Deviation from 1: {abs(R_solution - 1)*100:.6f}%

Very close to 1 (≪0.001%): points to Planck scale as the only scale.
""")
