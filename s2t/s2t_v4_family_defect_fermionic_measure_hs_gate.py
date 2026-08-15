#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np


TOLERANCE = 1.0e-9
RANDOM_SEED = 20260815
RANDOM_TESTS = 128


def block_diagonal(blocks):
    size = sum(block.shape[0] for block in blocks)
    result = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        block_size = block.shape[0]
        result[offset : offset + block_size, offset : offset + block_size] = block
        offset += block_size
    return result


def particle_dirac(locking, pairing):
    zero = np.zeros((3, 3), dtype=complex)
    pairing_block = pairing * np.eye(3)
    return np.block(
        [
            [zero, locking.conj().T, zero],
            [locking, zero, pairing_block.conj().T],
            [zero, pairing_block, zero],
        ]
    )


def full_dirac(locking, pairing):
    particle = particle_dirac(locking, pairing)
    return block_diagonal([particle, particle.conj()])


def regulated_log_pfaffian(dirac, momentum):
    positive = momentum**2 * np.eye(dirac.shape[0]) + dirac @ dirac
    sign, log_determinant = np.linalg.slogdet(positive)
    assert sign.real > 0
    return 0.5 * float(log_determinant.real)


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    identity9 = np.eye(9)
    zero9 = np.zeros((9, 9))
    reality = np.block([[zero9, identity9], [identity9, zero9]])
    grading_particle = block_diagonal([np.eye(3), -np.eye(3), np.eye(3)])
    grading = block_diagonal([grading_particle, -grading_particle])

    locking = rng.normal(size=(3, 3))
    pairing = rng.normal() + 1.0j * rng.normal()
    dirac = full_dirac(locking, pairing)
    bilinear = reality @ dirac
    plus = np.where(np.diag(grading).real > 0)[0]
    chiral_bilinear = bilinear[np.ix_(plus, plus)]

    maximum_errors = {
        "finite_bilinear_symmetry": float(np.linalg.norm(bilinear - bilinear.T)),
        "chiral_grassmann_antisymmetric_part": float(
            np.linalg.norm(chiral_bilinear - chiral_bilinear.T)
        ),
        "radial_spectrum": 0.0,
        "radial_pfaffian_formula": 0.0,
        "even_moment_formula": 0.0,
    }

    for _ in range(RANDOM_TESTS):
        rho = float(rng.uniform(0.05, 1.8))
        radius = float(rng.uniform(0.05, 1.8))
        momentum = float(rng.uniform(0.2, 2.0))
        radial_dirac = full_dirac(rho * np.eye(3), radius)
        spectral_radius = np.sqrt(rho**2 + radius**2)
        expected_spectrum = np.array(
            [-spectral_radius] * 6 + [0.0] * 6 + [spectral_radius] * 6
        )
        maximum_errors["radial_spectrum"] = max(
            maximum_errors["radial_spectrum"],
            float(
                np.linalg.norm(
                    np.sort(np.linalg.eigvalsh(radial_dirac)) - expected_spectrum
                )
            ),
        )
        formula = 3.0 * np.log(momentum**2) + 6.0 * np.log(
            momentum**2 + rho**2 + radius**2
        )
        maximum_errors["radial_pfaffian_formula"] = max(
            maximum_errors["radial_pfaffian_formula"],
            abs(regulated_log_pfaffian(radial_dirac, momentum) - formula),
        )
        for power in range(1, 5):
            moment = float(
                np.trace(np.linalg.matrix_power(radial_dirac, 2 * power)).real
            )
            expected = 12.0 * (rho**2 + radius**2) ** power
            maximum_errors["even_moment_formula"] = max(
                maximum_errors["even_moment_formula"], abs(moment - expected)
            )

    equal_sum_points = [(1.0, 0.0), (2.0 ** -0.5, 2.0 ** -0.5)]
    momentum = 0.73
    pfaffians = [
        regulated_log_pfaffian(full_dirac(rho * np.eye(3), radius), momentum)
        for rho, radius in equal_sum_points
    ]
    target_values = [
        (rho**2 - radius**2) ** 2 for rho, radius in equal_sum_points
    ]

    result = {
        "date": "2026-08-15",
        "gate": "version4_family_defect_fermionic_measure_hs_gate",
        "finite_KO6": {
            "bilinear": "J_linear D_F is symmetric",
            "chiral_bilinear_rank": int(np.linalg.matrix_rank(chiral_bilinear)),
            "grassmann_antisymmetric_rank": int(
                np.linalg.matrix_rank(0.5 * (chiral_bilinear - chiral_bilinear.T))
            ),
        },
        "spacetime_completed_radial_measure": {
            "spectrum": "0^6 and +/-sqrt(rho^2+r^2), each sign multiplicity 6",
            "log_pfaffian": "3 log p^2 + 6 log(p^2+rho^2+r^2)",
            "even_moments": "Tr D_F^(2n)=12(rho^2+r^2)^n",
            "loop_quartic_ratio": [1, 2, 1],
            "required_ratio": [1, -2, 1],
        },
        "equal_sum_counterexample": {
            "points": equal_sum_points,
            "pfaffian_values": pfaffians,
            "moment_map_square_values": target_values,
        },
        "project_archaeology": {
            "derived_four_fermion_Sym3_channel": False,
            "HS_requires_prior_quartic_kernel": True,
            "project_torsion_is_cohomological_Z2_not_Cartan_torsion": True,
        },
        "maximum_errors": maximum_errors,
        "verdict": {
            "standalone_finite_KO6_pfaffian": "zero_by_symmetry",
            "completed_Gaussian_measure": "depends_only_on_rho2_plus_r2",
            "imaginary_HS_origin": "not_derived",
            "Version_IV_family_defect_parent_route": "closed",
            "reopening": "Version V requires a derived four-fermion channel, modified calculus, Cartan torsion, or a new finite carrier",
        },
    }

    assert result["finite_KO6"]["grassmann_antisymmetric_rank"] == 0
    assert max(maximum_errors.values()) < TOLERANCE
    assert abs(pfaffians[0] - pfaffians[1]) < TOLERANCE
    assert abs(target_values[0] - target_values[1]) > 0.9

    Path("s2t_v4_family_defect_fermionic_measure_hs_gate_results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()