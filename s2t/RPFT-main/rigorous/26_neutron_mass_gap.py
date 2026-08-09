#!/usr/bin/env python3
"""26. NEUTRON MASS GAP CHECK

Reproducible numerical verification of the neutron gap hypothesis:

  m_n = m_p + m_e * Δ_n

Two variants:
  (A) Δ_n = ln(4π)
  (B) Δ_n = ln(4π) - 2/(3*S_vac^2)

Also checks the beta Q-value:
  Qβ = m_n - m_p - m_e = m_e*(Δ_n - 1)

All numbers use CODATA/PDG constants directly (no fitting).
"""

from __future__ import annotations

import math


def s_vac_from_geometry() -> float:
    """Compute S_vac from the project's standard geometric formula."""
    pi = math.pi
    s_geo = 4 * pi**3 + pi**2 + pi
    delta_cas = 1 / (24 * s_geo)
    delta_bb = 1 / (pi**4 * s_geo**2)
    return s_geo - delta_cas - delta_bb


def main() -> None:
    pi = math.pi

    # --- Experimental constants (CODATA/PDG) ---
    # Masses in MeV
    m_e = 0.51099895000
    m_p = 938.27208816
    m_n = 939.56542052

    # Derived experimental gap factors
    delta_exp = (m_n - m_p) / m_e
    q_beta_exp = m_n - m_p - m_e

    # --- Theory building blocks ---
    s_vac = s_vac_from_geometry()

    ln_4pi = math.log(4 * pi)
    spin_corr = 2 / (3 * s_vac**2)

    # If we postulate a correction of the form:
    #   Δ = ln(4π) - c / S_vac^2
    # then c is fixed by experiment as:
    #   c_fit = (ln(4π) - Δ_exp) * S_vac^2
    c_fit = (ln_4pi - delta_exp) * (s_vac**2)

    # Two hypotheses for Delta_n
    delta_A = ln_4pi
    delta_B = ln_4pi - spin_corr

    # Alternative hypothesis from /Проработка/mendeleev.md (RPFT-v18.0):
    # Δ_np = sqrt(2π) + 10/(3 S_vac)
    delta_C = math.sqrt(2 * pi) + (10 / (3 * s_vac))

    # Predicted masses and Q-values
    def pred(delta: float) -> tuple[float, float]:
        mn_pred = m_p + m_e * delta
        q_beta = mn_pred - m_p - m_e
        return mn_pred, q_beta

    mn_A, q_A = pred(delta_A)
    mn_B, q_B = pred(delta_B)
    mn_C, q_C = pred(delta_C)

    # --- Output ---
    print("=" * 72)
    print("NEUTRON GAP CHECK (UGSM/RPFT)")
    print("=" * 72)

    print("\n[INPUTS]")
    print(f"m_e (MeV): {m_e:.11f}")
    print(f"m_p (MeV): {m_p:.8f}")
    print(f"m_n (MeV): {m_n:.8f}")

    print("\n[GEOMETRY]")
    print(f"S_vac (from geometry): {s_vac:.12f}")
    print(f"ln(4π):               {ln_4pi:.12f}")
    print(f"2/(3*S_vac^2):        {spin_corr:.12f}")
    print(f"c_fit in Δ=ln(4π)-c/S^2: {c_fit:.12f}")

    print("\n[EXPERIMENT]")
    print(f"Δ_exp = (m_n-m_p)/m_e: {delta_exp:.12f}")
    print(f"Qβ_exp = m_n-m_p-m_e:  {q_beta_exp:.12f} MeV")

    print("\n[HYPOTHESIS A]  Δ = ln(4π)")
    print(f"Δ_A:                  {delta_A:.12f}")
    print(f"m_n(pred):            {mn_A:.8f} MeV")
    print(f"m_n error:            {mn_A - m_n:+.6e} MeV")
    print(f"Qβ(pred):             {q_A:.12f} MeV")
    print(f"Qβ error:             {q_A - q_beta_exp:+.6e} MeV")

    print("\n[HYPOTHESIS B]  Δ = ln(4π) - 2/(3*S_vac^2)")
    print(f"Δ_B:                  {delta_B:.12f}")
    print(f"m_n(pred):            {mn_B:.8f} MeV")
    print(f"m_n error:            {mn_B - m_n:+.6e} MeV")
    print(f"Qβ(pred):             {q_B:.12f} MeV")
    print(f"Qβ error:             {q_B - q_beta_exp:+.6e} MeV")

    print("\n[HYPOTHESIS C]  Δ = sqrt(2π) + 10/(3*S_vac)")
    print(f"Δ_C:                  {delta_C:.12f}")
    print(f"m_n(pred):            {mn_C:.8f} MeV")
    print(f"m_n error:            {mn_C - m_n:+.6e} MeV")
    print(f"Qβ(pred):             {q_C:.12f} MeV")
    print(f"Qβ error:             {q_C - q_beta_exp:+.6e} MeV")

    print("\n[NOTES]")
    print("- Hypothesis A tests whether the neutron gap is purely ln(Zψ/ZA)=ln(4π).")
    print("- Hypothesis B adds a small correction ~ O(S_vac^-2) motivated by spin/chirality.")
    print("- Hypothesis C is an alternative parameterization used elsewhere in the repo.")

    print("\n[COEFFICIENT TEST]  Δ = ln(4π) - c/S_vac^2")
    print("We compare simple rational candidates for c (no fitting):")

    candidates = [
        ("1/2", 1 / 2),
        ("2/3", 2 / 3),
        ("3/4", 3 / 4),
        ("1", 1.0),
        ("5/6", 5 / 6),
    ]

    print(f"{'c':<6} {'Δ(c)':>14} {'m_n err (eV)':>14} {'Qβ err (eV)':>14}")
    for name, c_val in candidates:
        delta_cand = ln_4pi - (c_val / (s_vac**2))
        mn_pred, q_pred = pred(delta_cand)
        mn_err_eV = (mn_pred - m_n) * 1e6
        q_err_eV = (q_pred - q_beta_exp) * 1e6
        print(f"{name:<6} {delta_cand:>14.12f} {mn_err_eV:>14.4f} {q_err_eV:>14.4f}")


if __name__ == "__main__":
    main()
