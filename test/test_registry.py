import pytest

from src.solvers.registry import SolverRegistry
from src.solvers.human import HumanSolver
from src.solvers.random import RandomSolver
from src.solvers.minmax import MinMaxSolver

class TestSolverRegistry:
    def test_register_and_get_solver(self):
        # Given
        class DummySolver:
            name = "dummy_solver"

        # When
        SolverRegistry.register(DummySolver)

        # Then
        assert SolverRegistry.get_solver("dummy_solver") == DummySolver

    def test_get_solver_non_existent_solver(self):
        # When / Then
        with pytest.raises(KeyError):
            SolverRegistry.get_solver("non_existent_solver")

    def test_list_solvers(self):
        # Given
        class AnotherDummySolver:
            name = "another_dummy_solver"

        SolverRegistry.register(AnotherDummySolver)

        # When
        solvers = SolverRegistry.list_solvers()

        # Then
        assert "dummy_solver" in solvers
        assert "another_dummy_solver" in solvers

    def test_register_human(self):
        # Then
        assert SolverRegistry.get_solver(HumanSolver.name)

    def test_register_random(self):
        # Then
        assert SolverRegistry.get_solver(RandomSolver.name)

    def test_register_minmax(self):
        # Then
        assert SolverRegistry.get_solver(MinMaxSolver.name)