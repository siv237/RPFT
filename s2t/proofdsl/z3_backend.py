"""Optional Z3 adapter.

The adapter deliberately returns solver evidence rather than an LCF theorem.
The MVP does not yet replay Z3 proof objects inside the trusted kernel.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec
from typing import Any, Iterable


class BackendUnavailable(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class SolverEvidence:
    status: str
    backend: str = "z3"
    trusted_theorem: bool = False


def available() -> bool:
    return find_spec("z3") is not None


def check(constraints: Iterable[Any]) -> SolverEvidence:
    if not available():
        raise BackendUnavailable(
            "install the optional z3-solver package to enable this backend"
        )
    import z3  # type: ignore[import-not-found]

    solver = z3.Solver()
    solver.add(*tuple(constraints))
    return SolverEvidence(status=str(solver.check()))