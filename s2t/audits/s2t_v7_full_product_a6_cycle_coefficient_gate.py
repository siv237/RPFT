#!/usr/bin/env python3
"""Audit full weak intertwiners in the candidate sixth-order cycles."""

import hashlib
import json
from itertools import combinations, permutations
from pathlib import Path

import sympy as sp


def put_map(matrix, offsets, dims, target, source, block):
    """Insert a real block and its transpose into a self-adjoint matrix."""
    i, j = offsets[target], offsets[source]
    matrix[i : i + dims[target], j : j + dims[source]] = block
    matrix[j : j + dims[source], i : i + dims[target]] = block.T


def colored_cycle_matrix(branch, x, y):
    names = ["QL", "uR", "dR", "XL", "eR", "LL", "YR"]
    dims = {"QL": 6, "uR": 3, "dR": 3, "XL": 1, "eR": 1, "LL": 2, "YR": 2}
    offsets = {}
    total = 0
    for name in names:
        offsets[name] = total
        total += dims[name]
    matrix = sp.zeros(total)
    higgs = sp.Matrix([0, 1])
    higgs_tilde = sp.Matrix([1, 0])
    color = sp.Matrix([1, 0, 0])
    put_map(matrix, offsets, dims, "uR", "QL", sp.kronecker_product(sp.eye(3), higgs_tilde.T))
    put_map(matrix, offsets, dims, "dR", "QL", sp.kronecker_product(sp.eye(3), higgs.T))
    put_map(matrix, offsets, dims, "eR", "LL", higgs.T)
    put_map(matrix, offsets, dims, "eR", "XL", sp.ones(1, 1))
    put_map(matrix, offsets, dims, "YR", "LL", sp.eye(2))
    put_map(matrix, offsets, dims, "QL", "YR", sp.kronecker_product(y * color, sp.eye(2)))
    put_map(matrix, offsets, dims, branch, "XL", x * color)
    return matrix


def weak_cycle_matrix(x, y, aligned=True):
    names = ["LL", "XR", "XL", "eR", "YL", "YR"]
    dims = {"LL": 2, "XR": 1, "XL": 1, "eR": 1, "YL": 2, "YR": 2}
    offsets = {}
    total = 0
    for name in names:
        offsets[name] = total
        total += dims[name]
    matrix = sp.zeros(total)
    e1 = sp.Matrix([1, 0])
    e2 = sp.Matrix([0, 1])
    put_map(matrix, offsets, dims, "XR", "XL", sp.ones(1, 1))
    put_map(matrix, offsets, dims, "eR", "XL", sp.ones(1, 1))
    put_map(matrix, offsets, dims, "YR", "YL", sp.eye(2))
    put_map(matrix, offsets, dims, "YR", "LL", sp.eye(2))
    put_map(matrix, offsets, dims, "XR", "LL", (x * e1).T)
    put_map(matrix, offsets, dims, "eR", "YL", (y * (e1 if aligned else e2)).T)
    return matrix


def hessian_at_origin(polynomial, variables):
    hessian = sp.hessian(polynomial, variables).subs({v: 0 for v in variables})
    eigenvalues = []
    for value, multiplicity in hessian.eigenvals().items():
        eigenvalues.extend([str(sp.simplify(value))] * multiplicity)
    return hessian, sorted(eigenvalues)


def simple_six_cycles():
    left = ["QL", "LL", "XL", "YL"]
    right = ["uR", "dR", "eR", "XR", "YR"]
    edges = {
        ("QL", "uR"), ("QL", "dR"), ("QL", "YR"),
        ("LL", "eR"), ("LL", "XR"), ("LL", "YR"),
        ("XL", "uR"), ("XL", "dR"), ("XL", "eR"),
        ("XL", "XR"), ("XL", "YR"),
        ("YL", "eR"), ("YL", "XR"), ("YL", "YR"),
    }
    background = {
        ("QL", "uR"), ("QL", "dR"), ("LL", "eR"),
        ("LL", "YR"), ("XL", "XR"), ("XL", "eR"), ("YL", "YR"),
    }
    cycles = set()
    for ls in combinations(left, 3):
        for rs in combinations(right, 3):
            for lp in permutations(ls):
                for rp in permutations(rs):
                    cycle_edges = []
                    for index in range(3):
                        first = (lp[index], rp[index])
                        second = (lp[(index + 1) % 3], rp[index])
                        if first not in edges or second not in edges:
                            break
                        cycle_edges.extend([first, second])
                    else:
                        cycles.add(frozenset(cycle_edges))
    quadratic = []
    for cycle in cycles:
        zero_edges = sorted(cycle - background)
        if len(zero_edges) == 2:
            quadratic.append({
                "edges": ["-".join(edge) for edge in sorted(cycle)],
                "zero_edges": ["-".join(edge) for edge in zero_edges],
            })
    return len(cycles), sorted(quadratic, key=lambda item: item["zero_edges"])


def main():
    x, y = sp.symbols("x y", real=True)
    higgs = sp.Matrix([0, 1])
    higgs_tilde = sp.Matrix([1, 0])
    up_overlap = (higgs_tilde.T * higgs)[0]
    down_overlap = (higgs.T * higgs)[0]

    up_polynomial = sp.expand(sp.trace(colored_cycle_matrix("uR", x, y) ** 6))
    down_polynomial = sp.expand(sp.trace(colored_cycle_matrix("dR", x, y) ** 6))
    weak_parallel = sp.expand(sp.trace(weak_cycle_matrix(x, y, aligned=True) ** 6))
    weak_orthogonal = sp.expand(sp.trace(weak_cycle_matrix(x, y, aligned=False) ** 6))

    up_mixed = up_polynomial.coeff(x, 1).coeff(y, 1)
    down_mixed = down_polynomial.coeff(x, 1).coeff(y, 1)
    weak_mixed = weak_parallel.coeff(x, 1).coeff(y, 1)
    weak_orthogonal_mixed = weak_orthogonal.coeff(x, 1).coeff(y, 1)

    up_hessian, up_eigenvalues = hessian_at_origin(up_polynomial, (x, y))
    down_hessian, down_eigenvalues = hessian_at_origin(down_polynomial, (x, y))
    weak_hessian, weak_eigenvalues = hessian_at_origin(weak_parallel, (x, y))
    cycle_count, quadratic_cycles = simple_six_cycles()

    gaussian_factor = -sp.Rational(1, 6)
    assert up_overlap == 0
    assert down_overlap == 1
    assert up_mixed == 0
    assert down_mixed == 12
    assert weak_mixed == 12
    assert weak_orthogonal_mixed == 0
    assert cycle_count == 14
    assert len(quadratic_cycles) == 3
    assert gaussian_factor * down_mixed == -2
    assert gaussian_factor * weak_mixed == -2
    result = {
        "gate": "version7_full_product_a6_cycle_coefficient_gate",
        "explicit_weak_intertwiners": {
            "H": [0, 1],
            "H_tilde": [1, 0],
            "H_tilde_dagger_H": str(up_overlap),
            "H_dagger_H": str(down_overlap),
        },
        "cycle_enumeration": {
            "simple_six_cycles_in_full_strict_graph": cycle_count,
            "cycles_quadratic_in_zero_fields_about_singlet_vacuum": len(quadratic_cycles),
            "quadratic_cycles": quadratic_cycles,
        },
        "restricted_exact_trace_polynomials": {
            "up_colored_pair": str(up_polynomial),
            "down_colored_pair": str(down_polynomial),
            "weak_pair_aligned": str(weak_parallel),
            "weak_pair_orthogonal_control": str(weak_orthogonal),
        },
        "mixed_coefficients_in_Tr_Phi6": {
            "original_up_cycle": str(up_mixed),
            "down_aligned_cycle": str(down_mixed),
            "weak_doublet_cycle_aligned_components": str(weak_mixed),
            "weak_doublet_cycle_orthogonal_control": str(weak_orthogonal_mixed),
        },
        "origin_hessians_of_Tr_Phi6": {
            "up_pair": {"matrix": str(up_hessian.tolist()), "eigenvalues": up_eigenvalues},
            "down_pair": {"matrix": str(down_hessian.tolist()), "eigenvalues": down_eigenvalues},
            "weak_pair": {"matrix": str(weak_hessian.tolist()), "eigenvalues": weak_eigenvalues},
        },
        "gaussian_a6_reduction": {
            "coefficient_of_Tr_Phi6": str(gaussian_factor),
            "original_up_cycle_bilinear": str(gaussian_factor * up_mixed),
            "down_cycle_bilinear": str(gaussian_factor * down_mixed),
            "weak_cycle_bilinear": str(gaussian_factor * weak_mixed),
            "conditional_central_holonomy_selected_by_surviving_cycle": "W_C=I",
        },
        "verdict": {
            "original_uR_virtual_cycle_survives_full_weak_trace": False,
            "reason": "H_tilde^dagger H=0",
            "down_type_cycle_survives": True,
            "weak_doublet_competitor_survives": True,
            "original_virtual_determinant_model_has_nonzero_kappa": False,
            "full_product_a6_pass_for_original_cycle": False,
            "status": "original_cycle_no_go_down_and_weak_competition_open",
            "next_gate": "version7_weak_aligned_cycle_competition_gate",
        },
    }

    out = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v7_full_product_a6_cycle_coefficient_gate_results.json"
    )
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()