#!/usr/bin/env python3
import cmath
import json
import math
from fractions import Fraction
from pathlib import Path


def circle_logdet_ratio(rho, beta):
    numerator = math.cosh(2.0 * math.pi * rho) - math.cos(
        2.0 * math.pi * beta
    )
    denominator = math.cosh(2.0 * math.pi * rho) - 1.0
    return math.log(numerator / denominator)


def paired_logdet(energy, mass):
    return cmath.log(mass + 1j * energy) + cmath.log(
        mass - 1j * energy
    )


def paired_mass_derivative(energy, mass):
    return 1.0 / (mass + 1j * energy) + 1.0 / (
        mass - 1j * energy
    )


def asymmetric_three_spectrum():
    return (
        [1.5] * 2
        + [2.5] * 6
        + [3.5] * 12
        + [-1.5] * 1
        + [-2.5] * 5
        + [-3.5] * 11
    )


def product_control(beta, mass=1.0, momentum_cutoff=12):
    total = 0j
    derivative = 0j
    block_phase_max = 0.0
    for eigenvalue in asymmetric_three_spectrum():
        for momentum in range(-momentum_cutoff, momentum_cutoff + 1):
            circle_momentum = momentum + beta
            energy = math.sqrt(eigenvalue**2 + circle_momentum**2)
            block = paired_logdet(energy, mass)
            response = paired_mass_derivative(energy, mass)
            total += block
            derivative += response
            block_phase_max = max(block_phase_max, abs(block.imag))
    return {
        "beta": beta,
        "mass": mass,
        "momentum_cutoff": momentum_cutoff,
        "complex_logdet": [total.real, total.imag],
        "mass_derivative": [derivative.real, derivative.imag],
        "maximum_block_phase": block_phase_max,
    }


def main():
    spin = json.loads(
        Path("s2t_spin_generation_selector_results.json").read_text(
            encoding="utf-8"
        )
    )
    projected = json.loads(
        Path("s2t_projected_kk_determinant_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    tau = json.loads(
        Path("s2t_tau_uniqueness_normalization_results.json").read_text(
            encoding="utf-8"
        )
    )

    periodic = product_control(0.0)
    antiperiodic = product_control(0.5)
    relative_complex = [
        antiperiodic["complex_logdet"][index]
        - periodic["complex_logdet"][index]
        for index in range(2)
    ]
    relative_response = [
        antiperiodic["mass_derivative"][index]
        - periodic["mass_derivative"][index]
        for index in range(2)
    ]

    rho_one_half_shift = circle_logdet_ratio(1.0, 0.5)
    existing_half_shift = next(
        row["half_logdet_ratio"]
        for row in projected["shell_sweep"]
        if row["rho"] == 1.0
    )
    one_twelfth = float(Fraction(1, 12))
    eta_values = spin["spectral_cross_check"]["RP3_spin_eta_invariants"]

    results = {
        "status": "F2_phase_to_mass_gate_closes_negatively_for_the_minimal_vectorlike_Dirac_product_determinant",
        "date": "2026-08-06",
        "operator": {
            "carrier": "K=RP3 x S1",
            "product_square": "D_K^2=D_RP3^2 + D_S1^2",
            "product_energy": "E_jn=sqrt(lambda_j^2+(n+beta)^2/R1^2)",
            "vectorlike_block": "(m+iE_jn)(m-iE_jn)=m^2+E_jn^2>0",
            "complex_log_block": "log(m+iE)+log(m-iE)=log(m^2+E^2)",
            "mass_response_block": "1/(m+iE)+1/(m-iE)=2m/(m^2+E^2)",
        },
        "blockwise_phase_cancellation": {
            "purpose": (
                "Use a deliberately asymmetric signed three-dimensional spectrum. "
                "The four-dimensional Clifford pair still cancels the determinant "
                "phase for every product eigenvalue independently of that asymmetry."
            ),
            "three_dimensional_signed_mode_count": len(
                asymmetric_three_spectrum()
            ),
            "periodic_control": periodic,
            "antiperiodic_control": antiperiodic,
            "relative_antiperiodic_minus_periodic": relative_complex,
            "relative_mass_response": relative_response,
            "phase_cancels": abs(relative_complex[1]) < 1e-12,
            "mass_response_is_real": abs(relative_response[1]) < 1e-12,
        },
        "circle_functional_gate": {
            "rho": 1.0,
            "beta": 0.5,
            "relative_logdet_formula": (
                "log[(cosh(2 pi rho)-cos(2 pi beta))/(cosh(2 pi rho)-1)]"
            ),
            "computed_relative_logdet": rho_one_half_shift,
            "existing_projected_KK_value": existing_half_shift,
            "crosscheck_error": abs(
                rho_one_half_shift - existing_half_shift
            ),
            "absolute_zeta_minus_one": one_twelfth,
            "logdet_minus_one_twelfth": rho_one_half_shift - one_twelfth,
            "ratio_to_one_twelfth": rho_one_half_shift / one_twelfth,
            "finding": (
                "The Euclidean determinant ratio is a rho-dependent logarithmic "
                "function. It is not the Casimir sum |zeta_R(-1)|=1/12."
            ),
        },
        "eta_gate": {
            "project_RP3_eta_menu": eta_values,
            "claimed_minus_one_half_is_in_current_operator_menu": -0.5
            in eta_values,
            "vectorlike_4D_finding": (
                "Even if the three-dimensional factor has spectral asymmetry, the "
                "full charged-lepton Dirac determinant pairs plus/minus product "
                "energies and has no eta phase capable of shifting the real mass."
            ),
            "chiral_exception": (
                "A chiral determinant can carry a Dai-Freed phase, but then it is a "
                "determinant-line/topological term. A separate CP-odd or non-Gaussian "
                "coupling is required to feed it into a real scalar mass modulus."
            ),
        },
        "tau_formula_comparison": {
            "target_alpha_coefficient": tau["qed_integral_audit"][
                "target_coefficient_magnitude"
            ],
            "existing_real_QED_winding_coefficient_unit_normalization": tau[
                "qed_integral_audit"
            ]["raw_coefficient_sum_over_pi"],
            "existing_required_projection_weight": tau["qed_integral_audit"][
                "required_jacobian_magnitude"
            ],
            "eta_phase_supplies_missing_real_weight": False,
            "finding": (
                "The only existing real mass correction remains the QED winding "
                "self-energy. Adding an eta phase cannot replace its missing real "
                "projection normalization."
            ),
        },
        "no_go": {
            "statement": (
                "For a positive real Dirac mass and a vectorlike charged-lepton "
                "operator on RP3 x S1, spectral asymmetry can affect a separate "
                "determinant phase only before vectorlike pairing. The derivative "
                "of the real effective action with respect to the mass is determined "
                "by D^dagger D+m^2 and contains no additive eta term."
            ),
            "F2_passes": False,
            "reopening_conditions": [
                "derive a complex chiral Yukawa mass whose phase is not removable",
                "supply a CP-odd background or topological-sector sum that converts phase interference into a real potential",
                "derive the corresponding coupling and show that its real linear response equals alpha/3 without mass data",
            ],
        },
        "scientific_verdict": {
            "positive": (
                "The 4D topological interpretation remains coherent for determinant "
                "phases and global anomaly bookkeeping."
            ),
            "negative": (
                "In the minimal physical charged-lepton Dirac sector the eta phase "
                "cancels blockwise and the circle determinant is not zeta(-1). The "
                "decomposition 1/3=1/4+1/12 therefore does not generate a real mass shift."
            ),
            "program_effect": (
                "Criterion F.2 fails in the minimal Gaussian/vectorlike realization. "
                "The tau coefficient remains controlled by the previously audited "
                "real QED self-energy and its unresolved normalization."
            ),
        },
    }

    assert periodic["maximum_block_phase"] < 1e-12
    assert antiperiodic["maximum_block_phase"] < 1e-12
    assert abs(relative_complex[1]) < 1e-12
    assert abs(relative_response[1]) < 1e-12
    assert abs(rho_one_half_shift - existing_half_shift) < 1e-12
    assert abs(rho_one_half_shift - one_twelfth) > 1e-2
    assert -0.5 not in eta_values

    Path("s2t_eta_phase_mass_gate_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()