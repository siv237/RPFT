import mpmath as mp

mp.mp.dps = 80

# Multiplicities (Ikeda 1979) for even/odd projection
# Scalars (Delta_0): lambda_n = n(n+2), mult_S3 = (n+1)^2
# Vectors coexact (Delta_1): lambda_n = (n+1)^2, mult_S3 = 2 n (n+2)
# Dirac: eigenvalues ±(n+3/2), mult_S3 = 2 (n+1)(n+2)
# On L(2,1): even n survive for bosons; odd n survive for spinor.

def mult_scalar_L(n):
    return 0.5 * (1 + (-1) ** n) * (n + 1) ** 2

def mult_scalar_even_S3(n):
    return 0.5 * (n + 1) ** 2

def mult_vector_L(n):
    return 0.5 * (1 + (-1) ** n) * 2 * n * (n + 2)

def mult_vector_even_S3(n):
    return 0.5 * 2 * n * (n + 2)

def mult_dirac_L(n):
    # note: odd n suppressed, so factor (1+(-1)^{n+1})
    return 0.5 * (1 + (-1) ** (n + 1)) * 2 * (n + 1) * (n + 2)

def mult_dirac_even_S3(n):
    # reference even sector
    return 0.5 * 2 * (n + 1) * (n + 2)

def lam_scalar(n):
    return n * (n + 2)

def lam_vector(n):
    return (n + 1) ** 2

def lam_dirac(n):
    return (n + 1.5) ** 2  # use square of eigenvalue for determinant

def delta_zeta(s, N, mult_L, mult_ref, lam_fn):
    s = mp.mpf(s)
    total = mp.mpf("0")
    for n in range(1, N + 1):
        dL = mult_L(n)
        dR = mult_ref(n)
        if dL:
            total += dL * lam_fn(n) ** (-s)
        if dR:
            total -= dR * lam_fn(n) ** (-s)
    return total

def delta_zeta_deriv0(N, mult_L, mult_ref, lam_fn):
    f = lambda ss: delta_zeta(ss, N, mult_L, mult_ref, lam_fn)
    return mp.diff(f, 0)

# Reference circle scalar value
ref_circle = -mp.log(mp.sqrt(2 * mp.pi))

Ns = [10, 20, 40, 80]
print("ref circle =", ref_circle)

for label, mL, mR, lam in [
    ("scalar", mult_scalar_L, mult_scalar_even_S3, lam_scalar),
    ("vector", mult_vector_L, mult_vector_even_S3, lam_vector),
    ("dirac", mult_dirac_L, mult_dirac_even_S3, lam_dirac),
]:
    print(f"\n=== {label} Δζ'(0;N) with even-S3 subtraction ===")
    for N in Ns:
        dz0 = delta_zeta_deriv0(N, mL, mR, lam)
        kappa = (-dz0) / ref_circle
        print(f"N={N:3d} dz0={dz0} kappa≈{kappa}")
