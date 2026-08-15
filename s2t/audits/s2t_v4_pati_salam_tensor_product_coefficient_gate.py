#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np


OUTPUT = Path("s2t_v4_pati_salam_tensor_product_coefficient_gate_results.json")


def odd_completion(rectangular):
    rows, columns = rectangular.shape
    zero_rows = np.zeros((rows, rows), dtype=complex)
    zero_columns = np.zeros((columns, columns), dtype=complex)
    operator = np.block(
        [[zero_rows, rectangular], [rectangular.conj().T, zero_columns]]
    )
    grading = np.diag([1.0] * rows + [-1.0] * columns)
    return operator, grading


def quartic_action(operator):
    return 0.5 * float(np.trace(np.linalg.matrix_power(operator, 4)).real)


def main():
    rng = np.random.default_rng(20260814)
    majorana_seed = rng.normal(size=(2, 3)) + 1j * rng.normal(size=(2, 3))
    scalar_seed = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))

    majorana_operator, majorana_grading = odd_completion(majorana_seed)
    scalar_operator, _ = odd_completion(scalar_seed)
    identity_majorana = np.eye(majorana_operator.shape[0])
    identity_scalar = np.eye(scalar_operator.shape[0])

    product_operator = np.kron(majorana_operator, identity_scalar)
    product_operator += np.kron(majorana_grading, scalar_operator)

    product_quartic = quartic_action(product_operator)
    separate_majorana = scalar_operator.shape[0] * quartic_action(majorana_operator)
    separate_scalar = majorana_operator.shape[0] * quartic_action(scalar_operator)
    mixed_quartic = product_quartic - separate_majorana - separate_scalar

    majorana_norm_squared = float(np.vdot(majorana_seed, majorana_seed).real)
    scalar_norm_squared = float(np.vdot(scalar_seed, scalar_seed).real)
    elementary_tensor_norm = majorana_norm_squared * scalar_norm_squared
    product_coefficient = mixed_quartic / elementary_tensor_norm

    doubled_product = np.block(
        [
            [product_operator, np.zeros_like(product_operator)],
            [np.zeros_like(product_operator), product_operator.conj()],
        ]
    )
    doubled_majorana = np.block(
        [
            [majorana_operator, np.zeros_like(majorana_operator)],
            [np.zeros_like(majorana_operator), majorana_operator.conj()],
        ]
    )
    doubled_scalar = np.block(
        [
            [scalar_operator, np.zeros_like(scalar_operator)],
            [np.zeros_like(scalar_operator), scalar_operator.conj()],
        ]
    )
    physical_half_mixed = 0.5 * quartic_action(doubled_product)
    physical_half_mixed -= 0.5 * scalar_operator.shape[0] * quartic_action(
        doubled_majorana
    )
    physical_half_mixed -= 0.5 * majorana_operator.shape[0] * quartic_action(
        doubled_scalar
    )
    physical_half_coefficient = physical_half_mixed / elementary_tensor_norm

    tensor_block = np.kron(majorana_seed, scalar_seed)
    oriented_tensor, _ = odd_completion(tensor_block)
    oriented_norm_coefficient = float(
        np.vdot(oriented_tensor, oriented_tensor).real / elementary_tensor_norm
    )

    multiplicity_ledger = []
    for copies in range(1, 4):
        coefficient = copies * product_coefficient
        multiplicity_ledger.append(
            {
                "copies": copies,
                "coefficient": coefficient,
                "strict_threshold_pass": coefficient > 4.0 + 1.0e-9,
                "copy_commutant_complex_dimension": copies * copies,
                "irreducible_identical_copy_system": copies == 1,
            }
        )

    output = {
        "gate": "version4_pati_salam_tensor_product_coefficient",
        "canonical_product": {
            "Dirac": "D1 tensor I + Gamma1 tensor D2",
            "square": "D1^2 tensor I + I tensor D2^2",
            "mixed_term_in_half_Tr_D4": "Tr(D1^2) Tr(D2^2)",
            "Tr_D1_squared_over_seed_norm": 2.0,
            "Tr_D2_squared_over_seed_norm": 2.0,
            "coefficient_c": product_coefficient,
            "expected_exact_coefficient": 4.0,
            "error": abs(product_coefficient - 4.0),
        },
        "KO6_physical_half_trace": {
            "coefficient_c": physical_half_coefficient,
            "error_from_four": abs(physical_half_coefficient - 4.0),
            "doubling_changes_coefficient": False,
        },
        "single_oriented_curvature_block": {
            "Hilbert_Schmidt_coefficient": oriented_norm_coefficient,
            "expected": 2.0,
        },
        "strict_stability_threshold": {
            "required": "c>4",
            "canonical_c": product_coefficient,
            "verdict": "threshold saturation with four phi zero modes",
        },
        "identical_copy_multiplicity": multiplicity_ledger,
        "verdict": (
            "The canonical graded product spectral action fixes c=4 exactly, and KO6 "
            "doubling followed by the physical half-trace leaves it unchanged. This "
            "saturates but does not pass the strict phi-stability threshold. Two "
            "identical copies would give c=8, but their M2(C) copy commutant violates "
            "the already established one-copy irreducibility condition."
        ),
        "next_gate": (
            "test whether a non-identical irreducible auxiliary factor or a derived "
            "higher spectral moment lifts the four zero modes without introducing a "
            "new continuous coefficient; otherwise close the tensor-product rescue"
        ),
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()