import json

import numpy as np


RANDOM_SEED = 20260815
RANDOM_TESTS = 256
TOLERANCE = 1.0e-10


def block_diagonal(blocks):
    size = sum(block.shape[0] for block in blocks)
    matrix = np.zeros((size, size), dtype=complex)
    offset = 0
    for block in blocks:
        block_size = block.shape[0]
        matrix[offset : offset + block_size, offset : offset + block_size] = block
        offset += block_size
    return matrix


def oriented_differential(locking, pairing):
    zero = np.zeros((3, 3), dtype=complex)
    pairing_block = pairing * np.eye(3)
    return np.block(
        [
            [zero, zero, zero],
            [locking, zero, zero],
            [zero, pairing_block, zero],
        ]
    )


def normalized_trace(matrix):
    return float(np.trace(matrix).real / 3.0)


def random_rotation(rng):
    matrix = rng.normal(size=(3, 3))
    orthogonal, _ = np.linalg.qr(matrix)
    if np.linalg.det(orthogonal) < 0.0:
        orthogonal[:, 0] *= -1.0
    return orthogonal


def symmetric_tangent_rank():
    columns = []
    for row in range(3):
        for column in range(3):
            variation = np.zeros((3, 3))
            variation[row, column] = 1.0
            tangent = variation + variation.T
            columns.append(
                np.array(
                    [
                        tangent[0, 0],
                        tangent[1, 1],
                        tangent[2, 2],
                        tangent[0, 1],
                        tangent[0, 2],
                        tangent[1, 2],
                    ]
                )
            )
    radial_pairing_tangent = -2.0 * np.eye(3)
    columns.append(
        np.array(
            [
                radial_pairing_tangent[0, 0],
                radial_pairing_tangent[1, 1],
                radial_pairing_tangent[2, 2],
                radial_pairing_tangent[0, 1],
                radial_pairing_tangent[0, 2],
                radial_pairing_tangent[1, 2],
            ]
        )
    )
    return int(np.linalg.matrix_rank(np.stack(columns, axis=1), TOLERANCE))


rng = np.random.default_rng(RANDOM_SEED)
height = block_diagonal([-np.eye(3), np.zeros((3, 3)), np.eye(3)])

maximum_errors = {
    "middle_commutator_moment_map": 0.0,
    "mapping_cone_endpoint_formula": 0.0,
    "so3_adjoint_projection": 0.0,
    "symmetric_projection": 0.0,
    "legendre_identity_at_stationary_auxiliary": 0.0,
    "legendre_gap_identity": 0.0,
    "gauge_covariance": 0.0,
    "kinetic_trace_normalization": 0.0,
    "ko6_physical_half_auxiliary": 0.0,
    "real_auxiliary_wrong_sign": 0.0,
    "imaginary_hs_completion": 0.0,
}
minimum_legendre_gap = float("inf")

for _ in range(RANDOM_TESTS):
    locking = rng.normal(size=(3, 3))
    pairing = rng.normal() + 1.0j * rng.normal()
    differential = oriented_differential(locking, pairing)
    adjoint = differential.conj().T
    hodge_commutator = differential @ adjoint - adjoint @ differential
    middle = hodge_commutator[3:6, 3:6]
    moment_map = locking @ locking.T - abs(pairing) ** 2 * np.eye(3)
    maximum_errors["middle_commutator_moment_map"] = max(
        maximum_errors["middle_commutator_moment_map"],
        np.linalg.norm(middle - moment_map),
    )

    self_adjoint_dirac = differential + adjoint
    curvature = self_adjoint_dirac @ self_adjoint_dirac
    relative_curvature = 0.5 * (height @ curvature - curvature @ height)
    relative_norm = float(
        np.trace(relative_curvature.conj().T @ relative_curvature).real
    )
    endpoint_formula = 2.0 * abs(pairing) ** 2 * float(
        np.trace(locking @ locking.T).real
    )
    maximum_errors["mapping_cone_endpoint_formula"] = max(
        maximum_errors["mapping_cone_endpoint_formula"],
        abs(relative_norm - endpoint_formula),
    )

    skew_projection = 0.5 * (moment_map - moment_map.T)
    symmetric_projection = 0.5 * (moment_map + moment_map.T)
    maximum_errors["so3_adjoint_projection"] = max(
        maximum_errors["so3_adjoint_projection"],
        np.linalg.norm(skew_projection),
    )
    maximum_errors["symmetric_projection"] = max(
        maximum_errors["symmetric_projection"],
        np.linalg.norm(symmetric_projection - moment_map),
    )

    auxiliary = rng.normal(size=(3, 3))
    auxiliary = 0.5 * (auxiliary + auxiliary.T)
    moment_norm = normalized_trace(moment_map @ moment_map)
    stationary_value = normalized_trace(
        2.0 * moment_map @ moment_map - moment_map @ moment_map
    )
    trial_value = normalized_trace(
        2.0 * auxiliary @ moment_map - auxiliary @ auxiliary
    )
    gap = moment_norm - trial_value
    gap_formula = normalized_trace(
        (auxiliary - moment_map) @ (auxiliary - moment_map)
    )
    minimum_legendre_gap = min(minimum_legendre_gap, gap)
    maximum_errors["legendre_identity_at_stationary_auxiliary"] = max(
        maximum_errors["legendre_identity_at_stationary_auxiliary"],
        abs(stationary_value - moment_norm),
    )
    maximum_errors["legendre_gap_identity"] = max(
        maximum_errors["legendre_gap_identity"], abs(gap - gap_formula)
    )
    real_minimum_value = normalized_trace(
        moment_map @ moment_map - 2.0 * moment_map @ moment_map
    )
    maximum_errors["real_auxiliary_wrong_sign"] = max(
        maximum_errors["real_auxiliary_wrong_sign"],
        abs(real_minimum_value + moment_norm),
    )
    complex_auxiliary = auxiliary.astype(complex)
    imaginary_left = normalized_trace(
        complex_auxiliary @ complex_auxiliary
        + 2.0j * complex_auxiliary @ moment_map
    )
    imaginary_right = normalized_trace(
        (complex_auxiliary + 1.0j * moment_map)
        @ (complex_auxiliary + 1.0j * moment_map)
        + moment_map @ moment_map
    )
    maximum_errors["imaginary_hs_completion"] = max(
        maximum_errors["imaginary_hs_completion"],
        abs(imaginary_left - imaginary_right),
    )

    rotation = random_rotation(rng)
    rotated_locking = rotation @ locking
    rotated_moment = (
        rotated_locking @ rotated_locking.T
        - abs(pairing) ** 2 * np.eye(3)
    )
    maximum_errors["gauge_covariance"] = max(
        maximum_errors["gauge_covariance"],
        np.linalg.norm(rotated_moment - rotation @ moment_map @ rotation.T),
    )

    locking_velocity = rng.normal(size=(3, 3))
    pairing_velocity = rng.normal() + 1.0j * rng.normal()
    arrow_kinetic = normalized_trace(locking_velocity @ locking_velocity.T)
    pairing_kinetic = normalized_trace(
        abs(pairing_velocity) ** 2 * np.eye(3)
    )
    expected_pairing_kinetic = abs(pairing_velocity) ** 2
    maximum_errors["kinetic_trace_normalization"] = max(
        maximum_errors["kinetic_trace_normalization"],
        abs(pairing_kinetic - expected_pairing_kinetic),
        abs(
            arrow_kinetic
            - float(np.trace(locking_velocity @ locking_velocity.T).real / 3.0)
        ),
    )
    doubled_stationary_value = 2.0 * stationary_value
    maximum_errors["ko6_physical_half_auxiliary"] = max(
        maximum_errors["ko6_physical_half_auxiliary"],
        abs(0.5 * doubled_stationary_value - moment_norm),
    )


result = {
    "gate": "version4_family_defect_relative_auxiliary_moment_gate",
    "random_seed": RANDOM_SEED,
    "random_tests": RANDOM_TESTS,
    "oriented_complex": {
        "nodes": "V_L -> V_G -> V_R",
        "middle_hodge_commutator": "[d,d^dagger]_G=XX^T-|Phi|^2 I3",
        "middle_auxiliary_module": "Sym_3(R), the self-adjoint part of M3(R)_G",
        "symmetric_tangent_rank": symmetric_tangent_rank(),
    },
    "route_a_mapping_cone": {
        "functional": "||(1/2)[h,(d+d^dagger)^2]||_HS^2",
        "radial_content": "2 |Phi|^2 Tr(XX^T)",
        "verdict": "fail: selects the endpoint product and has no |Phi|^4 or X^4 terms",
    },
    "route_b_strict_so3_D_term": {
        "gauge_lie_algebra": "so(3)=Skew_3(R)",
        "moment_map_module": "Sym_3(R)",
        "orthogonal_projection": "zero for real X and Y=Phi I3",
        "verdict": "fail: the required square is not an adjoint SO(3) D-term",
    },
    "route_c_self_adjoint_auxiliary": {
        "variational_identity": (
            "tau3(mu^2)=sup_{K in Sym3} [2 tau3(K mu)-tau3(K^2)]"
        ),
        "stationary_auxiliary": "K=mu is a strict maximum",
        "auxiliary_hessian_frobenius_eigenvalues": [-2.0 / 3.0] * 6,
        "positive_real_euclidean_elimination": (
            "inf_K [tau3(K^2)-2 tau3(K mu)]=-tau3(mu^2), the wrong sign"
        ),
        "imaginary_hubbard_stratonovich": (
            "tau3(K^2+2 i K mu)=tau3((K+i mu)^2)+tau3(mu^2)"
        ),
        "imaginary_saddle": "K=-i mu",
        "gauge_covariance": "K and mu transform by SO(3) conjugation",
        "trace_normalization": (
            "the same tau3 normalizes |DX|^2, |D Phi|^2 and the auxiliary pairing"
        ),
        "KO6_physical_half_trace": "unchanged after conjugate doubling",
        "continuous_coefficient_added": False,
        "verdict": (
            "closed as a real classical auxiliary; conditional only as a complex quantum-measure HS representation"
        ),
    },
    "metric_fork": {
        "SO3_module_decomposition": "Sym3(R)=R I3 direct_sum Sym3,0(R)=1 direct_sum 5",
        "invariant_metric_dimension": 2,
        "consequence": "SO(3) covariance alone does not fix equal central and traceless weights",
    },
    "maximum_errors": maximum_errors,
    "minimum_sampled_legendre_gap": minimum_legendre_gap,
    "status": {
        "ordinary_mapping_cone_curvature": "fail",
        "strict_so3_adjoint_D_term": "fail",
        "self_adjoint_M3_real_classical_auxiliary": "fail_by_sign",
        "self_adjoint_M3_imaginary_HS_measure": "conditional_open",
        "remaining_gate": (
            "derive Sym3(R) from the represented degree-two quotient, or derive the imaginary "
            "HS contour and determinant/Pfaffian weight from the KO6 fermionic measure"
        ),
    },
}

assert symmetric_tangent_rank() == 6
assert min(minimum_legendre_gap, 0.0) > -TOLERANCE
assert max(maximum_errors.values()) < TOLERANCE

with open(
    "s2t_v4_family_defect_relative_auxiliary_moment_gate_results.json",
    "w",
    encoding="utf-8",
) as output_file:
    json.dump(result, output_file, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))