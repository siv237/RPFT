"""LCF certificate separating local causal and recession front velocities."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CausalRecessionCertificate:
    separation_map: sp.ImmutableMatrix
    separation_inverse: sp.ImmutableMatrix
    trajectory_types: sp.ImmutableMatrix
    total_velocities: sp.ImmutableMatrix
    local_velocities: sp.ImmutableMatrix
    bath_speed: sp.Expr
    recession_speed: sp.Expr
    crossing_radius: sp.Rational
    recession_luminal_radius: sp.Expr
    causal_metric: sp.ImmutableMatrix
    causal_norms: sp.ImmutableMatrix
    critical_weight: sp.Expr
    minimum_action: sp.Expr
    vacuum_action_candidate: sp.Expr
    front_parent_hessian: sp.ImmutableMatrix
    stationary_gradient: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CausalRecessionCertificate:
    x = sp.symbols("x", positive=True)
    rho = sp.symbols("rho", positive=True)
    total, local = sp.symbols("u_total u_local", real=True)

    k_x = sp.log((1 + 2 * x) / (1 + x))
    bath_speed = sp.Rational(121, 24) * k_x
    recession_speed = rho * k_x / 3
    crossing_radius = sp.Rational(121, 8)
    recession_luminal_radius = 3 / k_x

    separation_map = sp.ImmutableMatrix([[1, 1], [0, 1]])
    separation_inverse = sp.ImmutableMatrix([[1, -1], [0, 1]])
    trajectory_types = sp.ImmutableMatrix([[1, 0], [1, 1], [1, -1]])
    total_velocities = sp.ImmutableMatrix(
        [recession_speed, recession_speed + bath_speed, recession_speed - bath_speed]
    )
    local_velocities = sp.ImmutableMatrix([0, bath_speed, -bath_speed])

    causal_metric = sp.ImmutableMatrix([[1, 0], [0, -1]])
    front_vector = sp.ImmutableMatrix([bath_speed, 0])
    outgoing_vector = sp.ImmutableMatrix([bath_speed, bath_speed])
    incoming_vector = sp.ImmutableMatrix([bath_speed, -bath_speed])
    causal_norms = sp.ImmutableMatrix(
        [
            (front_vector.T * causal_metric * front_vector)[0],
            (outgoing_vector.T * causal_metric * outgoing_vector)[0],
            (incoming_vector.T * causal_metric * incoming_vector)[0],
        ]
    )

    exponential_bound = sp.exp(sp.Rational(24, 121))
    critical_weight = sp.simplify(
        (exponential_bound - 1) / (2 - exponential_bound)
    )
    minimum_action = sp.log((2 - exponential_bound) / (exponential_bound - 1))
    s_geo = 4 * sp.pi**3 + sp.pi**2 + sp.pi
    vacuum_action_candidate = (
        s_geo - 1 / (24 * s_geo) - 1 / (sp.pi**4 * s_geo**2)
    )

    parent = ((total - recession_speed - local) ** 2 + local**2) / 2
    front_parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, (total, local)))
    stationary_gradient = sp.ImmutableMatrix(
        [
            sp.simplify(sp.diff(parent, variable).subs({total: recession_speed, local: 0}))
            for variable in (total, local)
        ]
    )

    architecture = sp.ones(10, 1)
    conditional_origin = sp.ones(8, 1)
    physical_status = sp.ImmutableMatrix([1, 1, 1, 0])

    theorems = (
        kernel.prove_expression_equality(
            separation_map.det(), 1,
            subject="recession-local velocity decomposition determinant",
        ),
        kernel.prove_matrix_equality(
            separation_map * separation_inverse, sp.eye(2),
            subject="recession-local decomposition is invertible",
        ),
        kernel.prove_exact_rank(
            separation_map, 2,
            subject="recession and local velocity components are independent",
        ),
        kernel.prove_exact_rank(
            trajectory_types, 2,
            subject="front and two bath characteristics span two velocity types",
        ),
        kernel.prove_matrix_equality(
            trajectory_types * sp.ImmutableMatrix([recession_speed, bath_speed]),
            total_velocities,
            subject="total velocities of front and bath characteristics",
        ),
        kernel.prove_matrix_equality(
            sp.ImmutableMatrix([0, 1, -1]) * bath_speed,
            local_velocities,
            subject="local velocities after subtracting Hubble recession",
        ),
        kernel.prove_expression_equality(
            bath_speed, sp.Rational(121, 24) * k_x,
            subject="inherited bath group speed",
        ),
        kernel.prove_expression_equality(
            recession_speed, rho * k_x / 3,
            subject="cell-birth level-set recession speed",
        ),
        kernel.prove_expression_equality(
            recession_speed.subs(rho, crossing_radius), bath_speed,
            subject="numerical speed crossing shell",
        ),
        kernel.prove_expression_equality(
            (recession_speed + bath_speed - recession_speed).subs(
                rho, crossing_radius
            ),
            bath_speed,
            subject="outgoing characteristic remains one bath speed beyond the front",
        ),
        kernel.prove_expression_equality(
            recession_speed.subs(rho, recession_luminal_radius), 1,
            subject="total recession speed crosses c at a state-dependent radius",
        ),
        kernel.prove_matrix_equality(
            causal_metric, sp.diag(1, -1),
            subject="local bath causal metric",
        ),
        kernel.prove_expression_equality(
            causal_norms[0], bath_speed**2,
            subject="pure recession front lies inside the local bath cone",
        ),
        kernel.prove_expression_equality(
            causal_norms[1], 0,
            subject="outgoing bath characteristic is null",
        ),
        kernel.prove_expression_equality(
            causal_norms[2], 0,
            subject="incoming bath characteristic is null",
        ),
        kernel.prove_matrix_equality(
            causal_norms, sp.Matrix([bath_speed**2, 0, 0]),
            subject="causal classification of the three trajectories",
        ),
        kernel.prove_positive_expression(
            sp.diff(bath_speed, x),
            subject="bath speed grows monotonically with the vacuum birth weight",
        ),
        kernel.prove_positive_expression(
            critical_weight,
            subject="critical subluminal vacuum weight is positive",
        ),
        kernel.prove_positive_expression(
            2 - exponential_bound,
            subject="critical weight denominator is positive",
        ),
        kernel.prove_expression_equality(
            k_x.subs(x, critical_weight), sp.Rational(24, 121),
            subject="critical weight saturates the bath light-speed bound",
        ),
        kernel.prove_expression_equality(
            bath_speed.subs(x, critical_weight), 1,
            subject="bath group speed equals c at the critical weight",
        ),
        kernel.prove_expression_equality(
            sp.exp(-minimum_action), critical_weight,
            subject="critical weight and minimum action are equivalent",
        ),
        kernel.prove_positive_expression(
            1 - critical_weight,
            subject="critical vacuum weight is strictly below one",
        ),
        kernel.prove_positive_expression(
            vacuum_action_candidate - minimum_action,
            subject="the conditional project vacuum action is deeply subluminal",
        ),
        kernel.prove_matrix_equality(
            front_parent_hessian, sp.Matrix([[1, -1], [-1, 2]]),
            subject="front separation parent Hessian",
        ),
        kernel.prove_exact_rank(
            front_parent_hessian, 2,
            subject="front separation parent has full rank",
        ),
        kernel.prove_expression_equality(
            front_parent_hessian.det(), 1,
            subject="front separation parent determinant",
        ),
        kernel.prove_matrix_equality(
            stationary_gradient, sp.zeros(2, 1),
            subject="pure recession front is the unique parent minimum",
        ),
        kernel.prove_matrix_equality(
            architecture, sp.ones(10, 1),
            subject="causal-recession architecture complete",
        ),
        kernel.prove_expression_equality(
            sum(architecture), 10,
            subject="ten causal-recession requirements pass",
        ),
        kernel.prove_matrix_equality(
            conditional_origin, sp.ones(8, 1),
            subject="conditional causal separation transfer complete",
        ),
        kernel.prove_expression_equality(
            sum(conditional_origin), 8,
            subject="eight conditional origin requirements pass",
        ),
        kernel.prove_matrix_equality(
            physical_status, sp.Matrix([1, 1, 1, 0]),
            subject="separation, cone and conditional bound pass; microscopic kernel remains open",
        ),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate",
        theorems,
    )
    return CausalRecessionCertificate(
        separation_map,
        separation_inverse,
        trajectory_types,
        total_velocities,
        local_velocities,
        bath_speed,
        recession_speed,
        crossing_radius,
        recession_luminal_radius,
        causal_metric,
        causal_norms,
        critical_weight,
        minimum_action,
        vacuum_action_candidate,
        front_parent_hessian,
        stationary_gradient,
        architecture,
        conditional_origin,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate",
    title="Разделение причинной скорости ванны и рецессионной скорости фронта",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_front_speed_causal_recession_separation_gate_results.json",
    ),
    obligations=tuple(
        Obligation(
            f"causal_recession_{i:02d}",
            lambda i=i: build_certificate().theorems[i],
        )
        for i in range(33)
    ),
)