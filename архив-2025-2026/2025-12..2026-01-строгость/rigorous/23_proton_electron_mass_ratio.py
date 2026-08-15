import math

def calculate_proton_electron_ratio():
    # 1. Define Constants from Geometric Theory
    pi = math.pi
    
    # S_geo components
    term_4pi3 = 4 * pi**3
    term_pi2 = pi**2
    term_pi = pi
    S_geo = term_4pi3 + term_pi2 + term_pi
    
    # Alpha calculation (from 12_alpha_derivation.md)
    # alpha^-1 = S_geo - 1/(24*S_geo) - 1/(pi^4 * S_geo^2)  (assuming C=1)
    # Note: README says C=1 gives -0.04 sigma. We stick to the standard formula.
    # The README formula: alpha^-1 = S_geo - 1/(24*S_geo) - 1/(pi^4 * S_geo^2)
    
    delta_cas = 1 / (24 * S_geo)
    delta_bb = 1 / (math.pi**4 * S_geo**2)
    
    S_vac = S_geo - delta_cas - delta_bb
    alpha_inv = S_vac
    
    # 2. Calculate mu (proton-to-electron mass ratio)
    # Formula: mu = 6*pi^5 + 3*pi/(2*S_vac) + (3 + 1/pi)/(S_vac^2)
    
    # Term 1: Hadronic Core (Geometric Volume of SU(3) sector)
    # 3 quarks * Vol(S^3) * Vol(S^5) = 3 * (2*pi^2) * (pi^3) = 6*pi^5
    core_term = 6 * pi**5
    
    # Term 2: Electromagnetic Equiparrition
    # 3 quarks * 1/2 * pi * alpha
    em_term = (3 * pi) / (2 * S_vac)
    
    # Term 3: Hyperfine / Higher Order
    # Scaling with alpha^2
    hf_term = (3 + 1/pi) / (S_vac**2)
    
    mu_theoretical = core_term + em_term + hf_term
    
    # 3. Comparison with CODATA 2022
    # Value: 1836.152 673 426 (32)
    mu_codata = 1836.152673426
    uncertainty = 0.000000032
    
    diff = mu_theoretical - mu_codata
    rel_error = diff / mu_codata
    sigma = diff / uncertainty
    
    return {
        "S_vac": S_vac,
        "core_term": core_term,
        "em_term": em_term,
        "hf_term": hf_term,
        "mu_theoretical": mu_theoretical,
        "mu_codata": mu_codata,
        "uncertainty": uncertainty,
        "difference": diff,
        "sigma": sigma,
        "relative_error_ppb": rel_error * 1e9
    }

if __name__ == "__main__":
    results = calculate_proton_electron_ratio()
    print("=== Proton-Electron Mass Ratio Derivation ===")
    print(f"S_vac (Inverse Alpha): {results['S_vac']:.12f}")
    print("-" * 40)
    print(f"Term 1 (Hadronic Core 6π⁵):   {results['core_term']:.12f}")
    print(f"Term 2 (EM Correction):       {results['em_term']:.12f}")
    print(f"Term 3 (Hyperfine/HO):        {results['hf_term']:.12f}")
    print("-" * 40)
    print(f"μ (Theoretical):              {results['mu_theoretical']:.12f}")
    print(f"μ (CODATA 2022):              {results['mu_codata']:.12f}")
    print("-" * 40)
    print(f"Difference:                   {results['difference']:.2e}")
    print(f"Sigma:                        {results['sigma']:.2f} σ")
    print(f"Relative Error:               {results['relative_error_ppb']:.4f} ppb")
    
    if abs(results['sigma']) < 2.0:
        print("STATUS: ✅ SUCCESS (Agreement within 2σ)")
    else:
        print("STATUS: ⚠️ WARNING (Deviation > 2σ)")
