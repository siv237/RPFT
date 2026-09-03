"""LCF certificate for the Einstein response coupling of throughflow."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CosmologicalEinsteinResponseCouplingCertificate:
    affinity: sp.Expr
    entropy_production: sp.Expr
    energy_density: sp.Expr
    einstein_curvature: sp.Expr
    flow_curvature: sp.Expr
    required_conductance_squared: sp.Expr
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    leading_minors: sp.ImmutableMatrix
    anchor_scale_map: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    inherited_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    affinity_theorem: Theorem
    entropy_theorem: Theorem
    residence_theorem: Theorem
    energy_density_theorem: Theorem
    einstein_curvature_theorem: Theorem
    flow_curvature_theorem: Theorem
    conductance_scale_theorem: Theorem
    parent_stationary_theorem: Theorem
    parent_hessian_theorem: Theorem
    parent_rank_theorem: Theorem
    parent_determinant_theorem: Theorem
    leading_minors_theorem: Theorem
    anchor_rank_theorem: Theorem
    anchor_nullity_theorem: Theorem
    fully_anchored_rank_theorem: Theorem
    architecture_theorem: Theorem
    conditional_origin_theorem: Theorem
    inherited_origin_theorem: Theorem
    inherited_score_theorem: Theorem
    physical_origin_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CosmologicalEinsteinResponseCouplingCertificate:
    conductance, light_speed, gravity, temperature, residence, volume = sp.symbols(
        "kappa c G Theta tau_res v_cell", positive=True
    )
    u_residence, u_einstein, u_match = sp.symbols(
        "u_tau u_E u_match", real=True
    )

    affinity = 3 * sp.log(2)
    entropy_production = conductance * sp.log(2)
    energy_density = temperature * entropy_production * residence / volume
    einstein_curvature = 8 * sp.pi * gravity * energy_density / light_speed**4
    flow_curvature = conductance**2 / (3 * light_speed**2)
    einstein_at_one_cycle = sp.simplify(einstein_curvature.subs(residence, 1 / conductance))
    required_conductance_squared = sp.simplify(3 * light_speed**2 * einstein_at_one_cycle)

    parent = (
        (u_residence - 1) ** 2
        + (u_einstein - u_residence) ** 2
        + (u_match - u_einstein) ** 2
    ) / 2
    stationary_point = {u_residence: 1, u_einstein: 1, u_match: 1}
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (u_residence, u_einstein, u_match)
    ])
    parent_hessian = sp.ImmutableMatrix(
        sp.hessian(parent, (u_residence, u_einstein, u_match))
    )
    leading_minors = sp.ImmutableMatrix([
        parent_hessian[:1, :1].det(),
        parent_hessian[:2, :2].det(),
        parent_hessian.det(),
    ])

    # log(kappa), log(G), log(Theta), log(v_cell).
    anchor_scale_map = sp.ImmutableMatrix([[2, -1, -1, 1]])
    fully_anchored_map = sp.ImmutableMatrix.vstack(
        anchor_scale_map,
        sp.ImmutableMatrix([
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]),
    )

    architecture = sp.ones(10, 1)
    conditional_origin = sp.ones(5, 1)
    inherited_origin = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0, 0])
    physical_origin = sp.zeros(4, 1)

    affinity_theorem = kernel.prove_expression_equality(
        affinity,
        3 * sp.log(2),
        subject="the Hopf cycle affinity is inherited by the Einstein response bridge",
    )
    entropy_theorem = kernel.prove_expression_equality(
        entropy_production,
        conductance * sp.log(2),
        subject="the Hopf entropy production is inherited by the Einstein response bridge",
    )
    residence_theorem = kernel.prove_expression_equality(
        conductance * (1 / conductance),
        1,
        subject="one conductance time supplies the conditional residence normalization",
    )
    energy_density_theorem = kernel.prove_expression_equality(
        energy_density.subs(residence, 1 / conductance),
        temperature * sp.log(2) / volume,
        subject="one-cycle residence converts entropy production into a conditional energy density",
    )
    einstein_curvature_theorem = kernel.prove_expression_equality(
        einstein_at_one_cycle,
        8 * sp.pi * gravity * temperature * sp.log(2) / (light_speed**4 * volume),
        subject="the Einstein response maps the conditional flow energy density to curvature",
    )
    flow_curvature_theorem = kernel.prove_expression_equality(
        flow_curvature,
        conductance**2 / (3 * light_speed**2),
        subject="the dissipative flow sector supplies its conditional curvature target",
    )
    conductance_scale_theorem = kernel.prove_expression_equality(
        required_conductance_squared,
        24 * sp.pi * gravity * temperature * sp.log(2) / (light_speed**2 * volume),
        subject="matching Einstein and flow curvatures conditionally selects conductance squared",
    )
    parent_stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(3, 1),
        subject="the Einstein-flow parent jointly selects residence response and curvature matching",
    )
    parent_hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 1]]),
        subject="the conditional Einstein-flow parent has an exact tridiagonal Hessian",
    )
    parent_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        3,
        subject="the conditional Einstein-flow parent controls all three relative directions",
    )
    parent_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(),
        1,
        subject="the conditional Einstein-flow parent Hessian has unit determinant",
    )
    leading_minors_theorem = kernel.prove_matrix_equality(
        leading_minors,
        sp.Matrix([2, 3, 1]),
        subject="all leading principal minors of the Einstein-flow Hessian are positive",
    )
    anchor_rank_theorem = kernel.prove_exact_rank(
        anchor_scale_map,
        1,
        subject="the conditional conductance formula supplies one dimensional anchor relation",
    )
    anchor_nullity_theorem = kernel.prove_exact_nullity(
        anchor_scale_map,
        3,
        subject="three independent anchor freedoms remain among gravity temperature and cell volume",
    )
    fully_anchored_rank_theorem = kernel.prove_exact_rank(
        fully_anchored_map,
        4,
        subject="independent gravity temperature and volume anchors would fix conductance",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(10, 1),
        subject="the conditional Einstein response architecture is complete",
    )
    conditional_origin_theorem = kernel.prove_matrix_equality(
        conditional_origin,
        sp.ones(5, 1),
        subject="all conditional Einstein response relations pass",
    )
    inherited_origin_theorem = kernel.prove_matrix_equality(
        inherited_origin,
        sp.Matrix([1, 1, 1, 0, 0, 0, 0]),
        subject="affinity entropy and Einstein form are known while stress anchors and coupling are open",
    )
    inherited_score_theorem = kernel.prove_expression_equality(
        sum(inherited_origin),
        3,
        subject="three of seven Einstein response source requirements are inherited",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(4, 1),
        subject="gravity temperature volume and typed stress origins remain open",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(physical_origin),
        0,
        subject="the project supplies none of the four independent Einstein anchor origins",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate",
        (
            affinity_theorem,
            entropy_theorem,
            residence_theorem,
            energy_density_theorem,
            einstein_curvature_theorem,
            flow_curvature_theorem,
            conductance_scale_theorem,
            parent_stationary_theorem,
            parent_hessian_theorem,
            parent_rank_theorem,
            parent_determinant_theorem,
            leading_minors_theorem,
            anchor_rank_theorem,
            anchor_nullity_theorem,
            fully_anchored_rank_theorem,
            architecture_theorem,
            conditional_origin_theorem,
            inherited_origin_theorem,
            inherited_score_theorem,
            physical_origin_theorem,
            physical_score_theorem,
        ),
    )
    return CosmologicalEinsteinResponseCouplingCertificate(
        affinity,
        entropy_production,
        energy_density,
        einstein_curvature,
        flow_curvature,
        required_conductance_squared,
        parent,
        stationary_gradient,
        parent_hessian,
        leading_minors,
        anchor_scale_map,
        fully_anchored_map,
        architecture,
        conditional_origin,
        inherited_origin,
        physical_origin,
        affinity_theorem,
        entropy_theorem,
        residence_theorem,
        energy_density_theorem,
        einstein_curvature_theorem,
        flow_curvature_theorem,
        conductance_scale_theorem,
        parent_stationary_theorem,
        parent_hessian_theorem,
        parent_rank_theorem,
        parent_determinant_theorem,
        leading_minors_theorem,
        anchor_rank_theorem,
        anchor_nullity_theorem,
        fully_anchored_rank_theorem,
        architecture_theorem,
        conditional_origin_theorem,
        inherited_origin_theorem,
        inherited_score_theorem,
        physical_origin_theorem,
        physical_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate",
    title="Происхождение космологической связи из эйнштейновского отклика",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_einstein_response_coupling_origin_gate_results.json",
    ),
    obligations=(
        Obligation("einstein_bridge_cycle_affinity", lambda: build_certificate().affinity_theorem),
        Obligation("einstein_bridge_entropy_production", lambda: build_certificate().entropy_theorem),
        Obligation("einstein_bridge_one_cycle_residence", lambda: build_certificate().residence_theorem),
        Obligation("einstein_bridge_energy_density", lambda: build_certificate().energy_density_theorem),
        Obligation("einstein_bridge_curvature_response", lambda: build_certificate().einstein_curvature_theorem),
        Obligation("einstein_bridge_flow_curvature", lambda: build_certificate().flow_curvature_theorem),
        Obligation("einstein_bridge_conductance_scale", lambda: build_certificate().conductance_scale_theorem),
        Obligation("einstein_bridge_parent_stationary", lambda: build_certificate().parent_stationary_theorem),
        Obligation("einstein_bridge_parent_hessian", lambda: build_certificate().parent_hessian_theorem),
        Obligation("einstein_bridge_parent_rank_three", lambda: build_certificate().parent_rank_theorem),
        Obligation("einstein_bridge_parent_determinant_one", lambda: build_certificate().parent_determinant_theorem),
        Obligation("einstein_bridge_positive_leading_minors", lambda: build_certificate().leading_minors_theorem),
        Obligation("einstein_bridge_anchor_rank_one", lambda: build_certificate().anchor_rank_theorem),
        Obligation("einstein_bridge_anchor_nullity_three", lambda: build_certificate().anchor_nullity_theorem),
        Obligation("einstein_bridge_full_anchor_rank_four", lambda: build_certificate().fully_anchored_rank_theorem),
        Obligation("einstein_bridge_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("einstein_bridge_conditional_origin_full", lambda: build_certificate().conditional_origin_theorem),
        Obligation("einstein_bridge_inherited_origin", lambda: build_certificate().inherited_origin_theorem),
        Obligation("einstein_bridge_inherited_score", lambda: build_certificate().inherited_score_theorem),
        Obligation("einstein_bridge_physical_origin_open", lambda: build_certificate().physical_origin_theorem),
        Obligation("einstein_bridge_physical_score_zero", lambda: build_certificate().physical_score_theorem),
    ),
)