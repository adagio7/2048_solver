from .solver import Solver

from typing import Dict, List

class SolverRegistry:
    """
    A registry for storing and retrieving solver classes.
    """
    _solvers: Dict[str, Solver] = {}

    @classmethod
    def register(cls, solver_class: Solver) -> Solver:
        """
        Register a solver class with a given name.
        """
        name = solver_class.name.lower()

        if name in cls._solvers:
            raise ValueError(f"Solver '{name}' is already registered.")

        cls._solvers[name] = solver_class
        return solver_class

    @classmethod
    def get_solver(cls, name: str) -> Solver:
        """
        Retrieve a solver class by its name.
        """
        if name not in cls._solvers:
            raise ValueError(f"Solver '{name}' is not registered.")

        return cls._solvers[name]

    @classmethod
    def list_solvers(cls) -> List[str]:
        """
        List all registered solvers.
        """
        return list(cls._solvers.keys())