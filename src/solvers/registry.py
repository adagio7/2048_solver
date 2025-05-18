from solver import Solver

from typing import Dict

class SolverRegistry:
    """
    A registry for storing and retrieving solver classes.
    """
    _solvers: Dict[str, Solver] = {}

    @classmethod
    def register(cls, solver_class: Solver) -> None:
        """
        Register a solver class with a given name.
        """
        name = solver_class.name.lower()

        if name in cls._solvers:
            raise ValueError(f"Solver '{name}' is already registered.")

        cls._solvers[name] = solver_class

    @classmethod
    def get_solver(cls, name: str) -> Solver:
        """
        Retrieve a solver class by its name.
        """
        if name not in cls._solvers:
            raise ValueError(f"Solver '{name}' is not registered.")

        return cls._solvers[name]

    @classmethod
    def list_solvers(cls) -> Dict[str, Solver]:
        """
        List all registered solvers.
        """
        return cls._solvers