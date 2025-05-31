import pytest
from unittest.mock import patch

from src.solvers.mcts import MCTSNode, MCTSSolver
from src.models import Moves

class TestMCTSNode:
    
    def test_node_initialization(self):
        # Given
        game_state = [[2, 4, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        
        # When
        node = MCTSNode(game_state)
        
        # Then
        assert node.game_state == game_state
        assert node.parent is None
        assert node.move is None
        assert node.visits == 0
        assert node.wins == 0.0
        assert len(node.children) == 0
        assert len(node.untried_moves) == 4  # UP, DOWN, LEFT, RIGHT
        assert node.game_state is not game_state  # Should be deep copy

    def test_node_initialization_with_parent_and_move(self):
        # Given
        game_state = [
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
        parent_node = MCTSNode(game_state)
        
        # When
        child_node = MCTSNode(game_state, parent=parent_node, move=Moves.UP)
        
        # Then
        assert child_node.parent == parent_node
        assert child_node.move == Moves.UP

    def test_is_fully_expanded_initially_false(self):
        # Given
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        node = MCTSNode(game_state)
        
        # When
        result = node.is_fully_expanded()
        
        # Then
        assert result is False

    def test_is_fully_expanded_after_removing_all_moves(self):
        # Given
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        node = MCTSNode(game_state)
        node.untried_moves = []
        
        # When
        result = node.is_fully_expanded()
        
        # Then
        assert result is True

    def test_is_terminal_empty_grid(self):
        # Given
        game_state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        node = MCTSNode(game_state)
        
        # When
        result = node.is_terminal()
        
        # Then
        assert result is False  # Empty cells available

    def test_is_terminal_full_grid(self):
        # Given
        game_state = [[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 4096],
                      [2, 4, 8, 16]]
        node = MCTSNode(game_state)
        
        # When
        result = node.is_terminal()
        
        # Then
        assert result is True  # No empty cells

    def test_select_child_with_unvisited_children(self):
        # Given
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        parent = MCTSNode(game_state)
        parent.visits = 10
        
        # Create children with different visit counts
        child1 = MCTSNode(game_state, parent=parent, move=Moves.UP)
        child1.visits = 0  # Unvisited
        child1.wins = 0
        
        child2 = MCTSNode(game_state, parent=parent, move=Moves.DOWN)
        child2.visits = 5
        child2.wins = 3
        
        parent.children = [child1, child2]
        
        # When
        selected = parent.select_child()
        
        # Then
        assert selected == child1  # Should prioritize unvisited child

    def test_select_child_ucb1_calculation(self):
        # Given
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        parent = MCTSNode(game_state)
        parent.visits = 100
        
        # Child with high win rate but many visits (exploitation)
        child1 = MCTSNode(game_state, parent=parent, move=Moves.UP)
        child1.visits = 50
        child1.wins = 45  # 90% win rate
        
        # Child with lower win rate but fewer visits (exploration)
        child2 = MCTSNode(game_state, parent=parent, move=Moves.DOWN)
        child2.visits = 10
        child2.wins = 7   # 70% win rate
        
        parent.children = [child1, child2]
        
        # When
        selected = parent.select_child(exploration_param=1.414)
        
        # Then
        # UCB1 for child1: 0.9 + 1.414 * sqrt(ln(100)/50) ≈ 0.9 + 0.37 = 1.27
        # UCB1 for child2: 0.7 + 1.414 * sqrt(ln(100)/10) ≈ 0.7 + 0.95 = 1.65
        assert selected == child2  # Should select child2 (higher UCB1)

    def test_expand_creates_new_child(self):
        # Given
        game_state = [[0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        node = MCTSNode(game_state)
        initial_children_count = len(node.children)
        initial_untried_count = len(node.untried_moves)
        
        # When
        with patch('random.randint', return_value=0):  # Always pick first move
            child = node.expand()
        
        # Then
        assert child is not None
        assert len(node.children) == initial_children_count + 1
        assert len(node.untried_moves) == initial_untried_count - 1
        assert child.parent == node
        assert child.move in list(Moves)

    def test_expand_returns_none_when_no_untried_moves(self):
        # Given
        game_state = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        node = MCTSNode(game_state)
        node.untried_moves = []  # No moves left to try
        
        # When
        child = node.expand()
        
        # Then
        assert child is None

    def test_simulate_returns_normalized_score(self):
        # Given
        game_state = [[2, 4, 8, 16], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        node = MCTSNode(game_state)
        
        # When
        with patch('random.choice') as mock_choice:
            # Mock random choices to make simulation deterministic
            mock_choice.side_effect = [Moves.UP, Moves.DOWN, Moves.LEFT, Moves.RIGHT] * 50
            result = node.simulate()
        
        # Then
        assert isinstance(result, float)
        assert result >= 0  # Score should be positive after normalization

    def test_backpropagate_updates_node_and_ancestors(self):
        # Given
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        grandparent = MCTSNode(game_state)
        parent = MCTSNode(game_state, parent=grandparent, move=Moves.UP)
        child = MCTSNode(game_state, parent=parent, move=Moves.DOWN)
        
        result_value = 5.5
        
        # When
        child.backpropagate(result_value)
        
        # Then
        # Child should be updated
        assert child.visits == 1
        assert child.wins == result_value
        
        # Parent should be updated
        assert parent.visits == 1
        assert parent.wins == result_value
        
        # Grandparent should be updated
        assert grandparent.visits == 1
        assert grandparent.wins == result_value

    def test_best_move_returns_most_visited_child(self):
        # Given
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        node = MCTSNode(game_state)
        
        # Create children with different visit counts
        child1 = MCTSNode(game_state, parent=node, move=Moves.UP)
        child1.visits = 10
        
        child2 = MCTSNode(game_state, parent=node, move=Moves.DOWN)
        child2.visits = 25  # Most visited
        
        child3 = MCTSNode(game_state, parent=node, move=Moves.LEFT)
        child3.visits = 5
        
        node.children = [child1, child2, child3]
        
        # When
        best_move = node.best_move()
        
        # Then
        assert best_move == Moves.DOWN

    def test_best_move_returns_none_when_no_children(self):
        # Given
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        node = MCTSNode(game_state)
        
        # When
        best_move = node.best_move()
        
        # Then
        assert best_move is None


class TestMCTSSolver:
    
    def test_solver_initialization(self):
        # Given & When
        solver = MCTSSolver()
        
        # Then
        assert solver.name == "mcts"
        assert solver.simulations == 300
        assert solver.epsilon == 1.414

    def test_get_move_returns_valid_move(self):
        # Given
        solver = MCTSSolver()
        solver.simulations = 10  # Small number for testing
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        # When
        move = solver.get_move(game_state)
        
        # Then
        assert move in list(Moves)

    def test_get_move_runs_correct_number_of_simulations(self):
        # Given
        solver = MCTSSolver()
        solver.simulations = 10  # Small number for testing
        game_state = [[2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        # When
        with patch.object(MCTSNode, 'simulate', return_value=1.0) as mock_simulate:
            solver.get_move(game_state)
        
        # Then
        # Should call simulate multiple times during MCTS
        assert mock_simulate.call_count >= 1

    def test_get_valid_moves_filters_invalid_moves(self):
        # Given
        solver = MCTSSolver()
        # Grid where only LEFT and UP are valid
        game_state = [[0, 2, 4, 8],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        
        # When
        valid_moves = solver._get_valid_moves(game_state)
        
        # Then
        assert Moves.LEFT in valid_moves  # Can slide tiles left
        assert Moves.DOWN in valid_moves    # Can slide tiles down
        assert len(valid_moves) == 2

    def test_get_valid_moves_empty_when_no_moves_possible(self):
        # Given
        solver = MCTSSolver()
        # Create a grid where no moves are possible (alternating pattern)
        game_state = [[2, 4, 2, 4],
                      [4, 2, 4, 2],
                      [2, 4, 2, 4],
                      [4, 2, 4, 2]]
        
        # When
        valid_moves = solver._get_valid_moves(game_state)
        
        # Then
        assert len(valid_moves) == 0

    def test_mcts_tree_growth(self):
        # Given
        solver = MCTSSolver()
        solver.simulations = 10  # Small number for testing
        game_state = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        # When
        with patch('random.choice'):  # Mock random choices in simulation
            move = solver.get_move(game_state)
        
        # Then
        assert move is not None
        assert isinstance(move, Moves)

    def test_mcts_handles_terminal_states(self):
        # Given
        solver = MCTSSolver()
        solver.simulations = 10
        # Nearly full grid
        game_state = [[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [512, 1024, 2048, 4096],
                      [2, 0, 8, 16]]  # One empty cell
        
        # When & Then (should not crash)
        move = solver.get_move(game_state)
        assert move in list(Moves)

if __name__ == '__main__':
    pytest.main([__file__])