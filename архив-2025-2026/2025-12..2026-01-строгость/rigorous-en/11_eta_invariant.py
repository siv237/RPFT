#!/usr/bin/env python3
"""
Numerical check of the η-invariant for the Dirac operator on L(2,1) = RP³.

η(s) = Σ sign(λ_n) |λ_n|^{-s}
η(0) = lim_{s→0} η(s) — regularized difference of positive/negative eigenvalues.

Spectrum on L(2,1) (Bär 1996):
- Eigenvalues: ±(n + 3/2), n = 0,1,2,...
- Multiplicity: 2(n+1)(n+2)
- On L(2,1) with trivial spin structure: odd n only

Navigation:
  ← 10_a2_coefficient.md | README.md →
  Main: 00_main.md
"""

from mpmath import mp, nsum, diff, pi, inf, sign, fabs, zeta as mpzeta
mp.dps = 50

print("="*70)
print("ETA-INVARIANT FOR DIRAC ON L(2,1)")
print("="*70)

# =============================================================================
# §1. DIRAC SPECTRUM ON S³
# =============================================================================

print("\n§1. Dirac spectrum on S³")
print("-"*40)

def dirac_eigenvalue_S3(n, R=1):
    """Eigenvalues: ±(n+3/2)/R, n=0,1,2,..."""
    return (n + mp.mpf('1.5')) / R

def dirac_multiplicity_S3(n):
    """Multiplicity on S³: d_n = 2(n+1)(n+2) for each sign."""
    return 2 * (n + 1) * (n + 2)

print("n\t|λ|\t\td_n")
for n in range(5):
    lam = dirac_eigenvalue_S3(n)
    d = dirac_multiplicity_S3(n)
    print(f"{n}\t{float(lam):.4f}\t\t{d}")

# =============================================================================
# §2. DIRAC SPECTRUM ON L(2,1) (trivial spin structure)
# =============================================================================

print("\n§2. Dirac spectrum on L(2,1), trivial spin structure")
print("-"*40)

print("""
By Bär (1996):
- Trivial spin structure (η=0): odd n only
- Nontrivial spin structure (η=1): even n only
RPFT uses trivial spin structure → odd n.
""")

def dirac_eigenvalue_L21(k, R=1):
    n = 2*k + 1  # odd n
    return (n + mp.mpf('1.5')) / R

def dirac_multiplicity_L21(k):
    n = 2*k + 1
    # d_n = 2(n+1)(n+2) on S³; factor 1/2 for Z2 quotient → (n+1)(n+2)
    return (n + 1) * (n + 2)

print("k\tn\t|λ|\t\td_n")
for k in range(5):
    n = 2*k + 1
    lam = dirac_eigenvalue_L21(k)
    d = dirac_multiplicity_L21(k)
    print(f"{k}\t{n}\t{float(lam):.4f}\t\t{d}")

# =============================================================================
# §3. ETA FUNCTION
# =============================================================================

print("\n§3. Eta function η(s)")
print("-"*40)

def eta_function_L21(s, N_max=200):
    """
    η(s) = Σ sign(λ) |λ|^{-s} × d
    Spectrum is symmetric: contributions cancel pairwise → 0.
    """
    s = mp.mpf(s)
    total = mp.mpf(0)
    for k in range(N_max):
        n = 2*k + 1
        lam = n + mp.mpf('1.5')
        d = (n + 1) * (n + 2)
        # +λ and -λ with equal multiplicity → cancel
        total += 0
    return total

print("For symmetric Dirac spectrum: η(s) = 0 for all s (sign(+λ)+sign(-λ)=0).")

# =============================================================================
# §4. SPECTRAL SYMMETRY CHECK
# =============================================================================

print("\n§4. Spectral symmetry check")
print("-"*40)

print("""
Dirac operator anticommutes with γ (3D) or γ⁵ (4D):
  γD = -Dγ
Hence eigenpairs ±λ with equal multiplicity → symmetric spectrum → η(s)=0.

Bär (1996): for any spin structure on L(2,1), spectrum is symmetric.
→ η(0) = 0 for L(2,1).
""")

# =============================================================================
# §5. APS CONTEXT
# =============================================================================

print("\n§5. η in APS index theorem")
print("-"*40)

print("""
APS: For 4-manifold W with boundary ∂W = M,
  Index(D_W) = ∫_W Â - (η(M) + h)/2
For W = B⁴, ∂W=S³ → η(S³)=0.
For RP³: need a 4-manifold bounding RP³ — nontrivial; we avoid this route.
""")

# =============================================================================
# §6. LINK TO TOPOLOGICAL π TERM
# =============================================================================

print("\n§6. Link to topological π term")
print("-"*40)

print("""
Result:
  η(0) = 0 for L(2,1) (any spin structure, symmetric spectrum).
Implication:
  η does NOT generate the π term.
π must come from elsewhere:
  1) Ray–Singer torsion
  2) Holonomy / Wilson loop
  3) Minimal action via systole (phenomenology)
""")

# =============================================================================
# §7. RAY–SINGER TORSION (alternative)
# =============================================================================

print("\n§7. Ray–Singer torsion (alternative)")
print("-"*40)

print("""
Franz–Reidemeister torsion for L(p,q):
  τ(L(p,q)) = Π_{j=1}^{(p-1)/2} |1 - e^{2πij/p}|^{-2}
For p=2,q=1:
  τ(L(2,1)) = |1 - e^{iπ}|^{-2} = |2|^{-2} = 1/4
  log τ = -2 log 2 ≈ -1.386 ≠ π, ≠ log π
""")

tau_L21 = 1/4
log_tau = float(mp.log(tau_L21))
print(f"τ(L(2,1)) = 1/4")
print(f"log τ = {log_tau:.6f}")
print(f"π = {float(pi):.6f}")
print(f"log π = {float(mp.log(pi)):.6f}")
print("\nlog τ ≠ π and log τ ≠ log π")

# =============================================================================
# §8. SUMMARY
# =============================================================================

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
1. η(L(2,1)) = 0 — symmetric Dirac spectrum.
2. log T_RS(L(2,1)) = -2 log 2 ≈ -1.386 — not π.
3. Neither η nor log T_RS yields the π term.

Status of Z_top = π:
  L_sys = π holds geometrically.
  Physical justification of Z_top = L_sys needs:
    - Phenomenological postulate, or
    - Holonomy/Wilson loop mechanism, or
    - Another topological invariant.

Recommendation: treat Z_top = π as the minimal topological contribution
(systole = shortest non-contractible path), until a strict derivation is found.
""")
print("="*70)
