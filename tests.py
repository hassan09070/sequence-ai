"""
Unit tests for the Sequence game implementation.

Run with: python -m pytest tests.py
Or: python tests.py
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import Board, Deck, Player, GameState
from ai import MinimaxAI, evaluate_state


class TestBoard:
    """Test cases for the Board class."""
    
    def test_board_initialization(self):
        """Test board is initialized correctly."""
        board = Board()
        assert board.size == 10
        assert len(board.chip_grid) == 10
        assert len(board.chip_grid[0]) == 10
        
        # Check wild corners
        assert board.get_chip_at(0, 0) == 3
        assert board.get_chip_at(0, 9) == 3
        assert board.get_chip_at(9, 0) == 3
        assert board.get_chip_at(9, 9) == 3
    
    def test_card_layout(self):
        """Test board has correct card layout."""
        board = Board()
        assert board.get_card_at(0, 0) == "XX"  # Wild corner
        assert board.get_card_at(0, 1) == "6D"
        assert board.get_card_at(1, 0) == "5D"
    
    def test_place_chip(self):
        """Test placing chips on the board."""
        board = Board()
        
        # Place valid chip
        assert board.place_chip(1, 1, player_id=1) == True
        assert board.get_chip_at(1, 1) == 1
        
        # Cannot place on occupied position
        assert board.place_chip(1, 1, player_id=2) == False
        
        # Cannot place on wild corner
        assert board.place_chip(0, 0, player_id=1) == False
    
    def test_remove_chip(self):
        """Test removing chips from the board."""
        board = Board()
        
        # Place and remove chip
        board.place_chip(3, 3, player_id=1)
        assert board.remove_chip(3, 3) == True
        assert board.get_chip_at(3, 3) == 0
        
        # Cannot remove from empty position
        assert board.remove_chip(3, 3) == False
        
        # Cannot remove from wild corner
        assert board.remove_chip(0, 0) == False
    
    def test_find_card_positions(self):
        """Test finding card positions."""
        board = Board()
        
        positions = board.find_card_positions("5H")
        assert len(positions) > 0
        
        # Verify all positions have the card
        for row, col in positions:
            assert board.get_card_at(row, col) == "5H"
    
    def test_sequence_detection_horizontal(self):
        """Test horizontal sequence detection."""
        board = Board()
        
        # Create horizontal sequence
        for col in range(5):
            board.place_chip(3, col, player_id=1)
        
        sequences = board.check_sequence(player_id=1)
        assert sequences >= 1
    
    def test_sequence_detection_vertical(self):
        """Test vertical sequence detection."""
        board = Board()
        
        # Create vertical sequence
        for row in range(5):
            board.place_chip(row, 3, player_id=1)
        
        sequences = board.check_sequence(player_id=1)
        assert sequences >= 1
    
    def test_sequence_detection_diagonal(self):
        """Test diagonal sequence detection."""
        board = Board()
        
        # Create diagonal sequence (top-left to bottom-right)
        for i in range(5):
            board.place_chip(i, i, player_id=1)
        
        sequences = board.check_sequence(player_id=1)
        assert sequences >= 1
    
    def test_board_clone(self):
        """Test board cloning."""
        board = Board()
        board.place_chip(3, 3, player_id=1)
        
        cloned = board.clone()
        assert cloned.get_chip_at(3, 3) == 1
        
        # Modify clone
        cloned.place_chip(4, 4, player_id=2)
        
        # Original unchanged
        assert board.get_chip_at(4, 4) == 0


class TestDeck:
    """Test cases for the Deck class."""
    
    def test_deck_initialization(self):
        """Test deck is initialized with correct number of cards."""
        deck = Deck()
        assert len(deck) == 104  # 2 full decks
    
    def test_shuffle(self):
        """Test deck shuffling."""
        deck1 = Deck()
        deck2 = Deck()
        
        # Before shuffle, should be identical
        assert deck1.cards == deck2.cards
        
        # After shuffle, likely different
        deck1.shuffle()
        # Can't guarantee different, but should work
    
    def test_deal_cards(self):
        """Test dealing cards."""
        deck = Deck()
        initial_count = len(deck)
        
        hand = deck.deal(7)
        assert len(hand) == 7
        assert len(deck) == initial_count - 7
    
    def test_discard_and_reshuffle(self):
        """Test discarding and reshuffling."""
        deck = Deck()
        
        # Deal some cards
        hand = deck.deal(10)
        
        # Discard them
        for card in hand:
            deck.discard(card)
        
        assert len(deck.discarded) == 10
        
        # Reshuffle
        deck.reshuffle_discards()
        assert len(deck.discarded) == 0
        assert len(deck.cards) > 0
    
    def test_jack_identification(self):
        """Test identifying jack types."""
        deck = Deck()
        
        assert deck.is_two_eyed_jack("JH") == True
        assert deck.is_two_eyed_jack("JD") == True
        assert deck.is_two_eyed_jack("JS") == False
        
        assert deck.is_one_eyed_jack("JS") == True
        assert deck.is_one_eyed_jack("JC") == True
        assert deck.is_one_eyed_jack("JH") == False
        
        assert deck.is_jack("JH") == True
        assert deck.is_jack("5H") == False
    
    def test_hand_sizes(self):
        """Test hand size calculation."""
        deck = Deck()
        
        assert deck.get_hand_size(2) == 7
        assert deck.get_hand_size(3) == 6


class TestPlayer:
    """Test cases for the Player class."""
    
    def test_player_initialization(self):
        """Test player initialization."""
        player = Player(player_id=1, name="Alice")
        
        assert player.player_id == 1
        assert player.name == "Alice"
        assert player.chip_type == 1
        assert len(player.hand) == 0
    
    def test_add_remove_cards(self):
        """Test adding and removing cards."""
        player = Player(player_id=1)
        
        player.add_card("5H")
        assert player.has_card("5H")
        assert player.hand_size() == 1
        
        player.add_cards(["KD", "3S"])
        assert player.hand_size() == 3
        
        player.remove_card("5H")
        assert not player.has_card("5H")
        assert player.hand_size() == 2
    
    def test_player_clone(self):
        """Test player cloning."""
        player = Player(player_id=1, name="Alice")
        player.add_cards(["5H", "KD", "3S"])
        
        cloned = player.clone()
        assert cloned.player_id == player.player_id
        assert cloned.hand == player.hand
        assert cloned is not player  # Different objects


class TestGameState:
    """Test cases for the GameState class."""
    
    def test_game_initialization(self):
        """Test game state initialization."""
        state = GameState(num_players=2)
        state.setup_game()
        
        assert len(state.players) == 2
        assert state.current_player_idx == 0
        assert state.sequences_needed_to_win == 2
        assert not state.game_over
    
    def test_deal_initial_hands(self):
        """Test dealing initial hands."""
        state = GameState(num_players=2)
        state.setup_game()
        
        for player in state.players:
            assert player.hand_size() == 7
    
    def test_get_legal_moves(self):
        """Test getting legal moves."""
        state = GameState(num_players=2)
        state.setup_game()
        
        moves = state.get_legal_moves()
        assert len(moves) > 0
        
        # All moves should have valid cards
        current_player = state.get_current_player()
        for move in moves:
            assert move.card in current_player.hand
    
    def test_apply_move(self):
        """Test applying a move."""
        state = GameState(num_players=2)
        state.setup_game()
        
        initial_hand_size = state.get_current_player().hand_size()
        legal_moves = state.get_legal_moves()
        
        if legal_moves:
            move = legal_moves[0]
            success = state.apply_move(move)
            
            assert success
            # Hand size should be same (draw after playing)
            assert state.players[move.player_id - 1].hand_size() == initial_hand_size
    
    def test_turn_progression(self):
        """Test turn progression."""
        state = GameState(num_players=2)
        state.setup_game()
        
        assert state.current_player_idx == 0
        
        state.next_turn()
        assert state.current_player_idx == 1
        
        state.next_turn()
        assert state.current_player_idx == 0  # Wrap around
    
    def test_game_state_clone(self):
        """Test game state cloning."""
        state = GameState(num_players=2)
        state.setup_game()
        
        cloned = state.clone()
        
        # Make move in original
        moves = state.get_legal_moves()
        if moves:
            state.apply_move(moves[0])
        
        # Clone should be unchanged
        assert len(cloned.move_history) < len(state.move_history)


class TestAI:
    """Test cases for the AI implementation."""
    
    def test_ai_initialization(self):
        """Test AI initialization."""
        ai = MinimaxAI(player_id=1, difficulty='medium')
        
        assert ai.player_id == 1
        assert ai.difficulty == 'medium'
        assert ai.max_depth == 2
    
    def test_ai_get_move(self):
        """Test AI getting a move."""
        state = GameState(num_players=2)
        state.setup_game([
            {'name': 'Human', 'is_ai': False},
            {'name': 'AI', 'is_ai': True}
        ])
        
        # Skip to AI turn
        state.next_turn()
        
        ai = MinimaxAI(player_id=2, difficulty='easy')
        move = ai.get_best_move(state)
        
        assert move is not None
        assert move.player_id == 2
    
    def test_different_difficulties(self):
        """Test different AI difficulty levels."""
        difficulties = ['easy', 'medium', 'hard', 'expert']
        expected_depths = [1, 2, 3, 4]
        
        for diff, depth in zip(difficulties, expected_depths):
            ai = MinimaxAI(player_id=1, difficulty=diff)
            assert ai.max_depth == depth
    
    def test_heuristic_evaluation(self):
        """Test heuristic evaluation."""
        state = GameState(num_players=2)
        state.setup_game()
        
        # Evaluate initial state
        score = evaluate_state(state, player_id=1)
        
        # Score should be a number
        assert isinstance(score, (int, float))


def run_tests():
    """Run all tests manually (without pytest)."""
    test_classes = [TestBoard, TestDeck, TestPlayer, TestGameState, TestAI]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        print(f"\n{'=' * 60}")
        print(f"Running {test_class.__name__}")
        print(f"{'=' * 60}")
        
        test_instance = test_class()
        
        # Get all test methods
        test_methods = [m for m in dir(test_instance) if m.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"✓ {method_name}")
                passed_tests += 1
            except AssertionError as e:
                print(f"✗ {method_name}: {e}")
                failed_tests.append(f"{test_class.__name__}.{method_name}")
            except Exception as e:
                print(f"✗ {method_name}: ERROR - {e}")
                failed_tests.append(f"{test_class.__name__}.{method_name}")
    
    print(f"\n{'=' * 60}")
    print("Test Summary")
    print(f"{'=' * 60}")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    
    if failed_tests:
        print("\nFailed tests:")
        for test in failed_tests:
            print(f"  - {test}")
    
    return len(failed_tests) == 0


if __name__ == "__main__":
    print("Running Sequence Game Tests...\n")
    success = run_tests()
    
    if success:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
