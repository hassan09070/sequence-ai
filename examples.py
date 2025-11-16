"""
Example usage scenarios for the Sequence game implementation.
"""

from game import GameState, Board, Deck, Player
from ai import MinimaxAI, evaluate_state


def example_1_basic_game():
    """Example 1: Basic game setup and playing."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Game Setup")
    print("=" * 60)
    
    # Create a new game
    state = GameState(num_players=2)
    state.setup_game([
        {'name': 'Alice', 'is_ai': False},
        {'name': 'Bob', 'is_ai': False}
    ])
    
    print("\nGame initialized!")
    print(f"Current player: {state.get_current_player().name}")
    print(f"Sequences needed to win: {state.sequences_needed_to_win}")
    
    # Show first player's hand
    player1 = state.players[0]
    print(f"\n{player1.name}'s hand: {player1.hand}")
    
    # Get legal moves
    legal_moves = state.get_legal_moves(player1)
    print(f"\nNumber of legal moves: {len(legal_moves)}")
    
    if legal_moves:
        # Show first few moves
        print("\nFirst 5 legal moves:")
        for i, move in enumerate(legal_moves[:5], 1):
            print(f"  {i}. {move}")


def example_2_ai_vs_ai():
    """Example 2: AI vs AI game."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: AI vs AI Game")
    print("=" * 60)
    
    # Create game with AI players
    state = GameState(num_players=2)
    state.setup_game([
        {'name': 'AI Easy', 'is_ai': True},
        {'name': 'AI Hard', 'is_ai': True}
    ])
    
    # Create AI instances
    ai1 = MinimaxAI(player_id=1, difficulty='easy')
    ai2 = MinimaxAI(player_id=2, difficulty='hard')
    
    print("\nPlaying AI vs AI game (first 5 moves)...")
    
    # Play a few moves
    for turn in range(5):
        if state.is_terminal():
            break
        
        current_player = state.get_current_player()
        
        # Select appropriate AI
        ai = ai1 if current_player.player_id == 1 else ai2
        
        print(f"\nTurn {turn + 1}: {current_player.name}")
        
        # Get AI move
        move = ai.get_best_move(state)
        
        if move:
            print(f"  Plays: {move.card} at ({move.row}, {move.col})")
            stats = ai.get_stats()
            print(f"  Explored: {stats['nodes_explored']} nodes")
            
            # Apply move
            state.apply_move(move)
            state.next_turn()
        else:
            print("  No legal moves!")
            break
    
    # Show final board state
    print("\nBoard after 5 moves:")
    print(state.board)


def example_3_board_operations():
    """Example 3: Board operations and sequence detection."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Board Operations")
    print("=" * 60)
    
    board = Board()
    
    # Show board layout
    print("\nBoard card at (0, 1):", board.get_card_at(0, 1))
    print("Board card at (5, 5):", board.get_card_at(5, 5))
    
    # Find positions of a card
    positions = board.find_card_positions("5H")
    print(f"\nPositions of '5H' on board: {positions}")
    
    # Place some chips to create a sequence
    print("\nCreating a horizontal sequence for Player 1...")
    for col in range(5):
        board.place_chip(0, col + 1, player_id=1)
    
    print(board)
    
    # Check sequences
    sequences = board.check_sequence(player_id=1)
    print(f"\nPlayer 1 sequences: {sequences}")


def example_4_deck_operations():
    """Example 4: Deck operations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Deck Operations")
    print("=" * 60)
    
    deck = Deck()
    
    print(f"\nDeck size: {len(deck)} cards")
    print(f"Hand size for 2 players: {deck.get_hand_size(2)}")
    print(f"Hand size for 3 players: {deck.get_hand_size(3)}")
    
    # Shuffle and deal
    deck.shuffle()
    hand = deck.deal(7)
    
    print(f"\nDealt hand (7 cards): {hand}")
    print(f"Remaining cards: {deck.cards_remaining()}")
    
    # Check jack types
    test_cards = ["JH", "JD", "JS", "JC", "5H"]
    print("\nJack types:")
    for card in test_cards:
        two_eyed = deck.is_two_eyed_jack(card)
        one_eyed = deck.is_one_eyed_jack(card)
        print(f"  {card}: Two-eyed={two_eyed}, One-eyed={one_eyed}")


def example_5_heuristic_evaluation():
    """Example 5: Heuristic evaluation."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Heuristic Evaluation")
    print("=" * 60)
    
    # Create a game state with some moves played
    state = GameState(num_players=2)
    state.setup_game([
        {'name': 'Player 1', 'is_ai': False},
        {'name': 'Player 2', 'is_ai': False}
    ])
    
    # Place some chips manually
    state.board.place_chip(3, 3, player_id=1)
    state.board.place_chip(3, 4, player_id=1)
    state.board.place_chip(3, 5, player_id=1)
    state.board.place_chip(4, 3, player_id=2)
    state.board.place_chip(4, 4, player_id=2)
    
    print("\nBoard state:")
    print(state.board)
    
    # Evaluate for both players
    score_p1 = evaluate_state(state, player_id=1)
    score_p2 = evaluate_state(state, player_id=2)
    
    print(f"\nEvaluation scores:")
    print(f"  Player 1: {score_p1:.2f}")
    print(f"  Player 2: {score_p2:.2f}")
    print(f"\nPlayer 1 is {'winning' if score_p1 > score_p2 else 'losing'}")


def example_6_game_state_json():
    """Example 6: Game state serialization."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Game State JSON Serialization")
    print("=" * 60)
    
    state = GameState(num_players=2)
    state.setup_game([
        {'name': 'Alice', 'is_ai': False},
        {'name': 'Bob', 'is_ai': True}
    ])
    
    # Make a few moves
    legal_moves = state.get_legal_moves()
    if legal_moves:
        state.apply_move(legal_moves[0])
        state.next_turn()
    
    # Serialize to JSON
    json_output = state.to_json(hide_opponent_hands=False)
    
    print("\nGame state as JSON:")
    print(json_output[:500] + "...")  # Show first 500 chars
    
    # Save to file
    with open('example_game_state.json', 'w') as f:
        f.write(json_output)
    
    print("\nFull game state saved to: example_game_state.json")


def example_7_complete_game():
    """Example 7: Complete game simulation."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Complete Game Simulation")
    print("=" * 60)
    
    state = GameState(num_players=2)
    state.setup_game([
        {'name': 'AI 1 (Medium)', 'is_ai': True},
        {'name': 'AI 2 (Easy)', 'is_ai': True}
    ])
    
    ai1 = MinimaxAI(player_id=1, difficulty='medium')
    ai2 = MinimaxAI(player_id=2, difficulty='easy')
    
    print("\nSimulating complete game...")
    turn = 0
    max_turns = 50  # Safety limit
    
    while not state.is_terminal() and turn < max_turns:
        current_player = state.get_current_player()
        ai = ai1 if current_player.player_id == 1 else ai2
        
        move = ai.get_best_move(state)
        
        if move:
            state.apply_move(move)
            state.next_turn()
            turn += 1
        else:
            print("No legal moves available!")
            break
    
    print(f"\nGame finished after {turn} turns")
    
    if state.is_terminal():
        winner = state.players[state.winner - 1]
        print(f"Winner: {winner.name}")
        
        # Show sequence counts
        for player in state.players:
            sequences = state.board.check_sequence(player.player_id)
            print(f"  {player.name}: {sequences} sequences")
    else:
        print("Game reached turn limit")
    
    print("\nFinal board:")
    print(state.board)


def run_all_examples():
    """Run all examples."""
    examples = [
        example_1_basic_game,
        example_2_ai_vs_ai,
        example_3_board_operations,
        example_4_deck_operations,
        example_5_heuristic_evaluation,
        example_6_game_state_json,
        example_7_complete_game,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
        
        input("\n\nPress Enter to continue to next example...")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SEQUENCE GAME - EXAMPLES")
    print("=" * 60)
    print("\nThis script demonstrates various features of the Sequence game.")
    print("\nAvailable examples:")
    print("  1. Basic game setup")
    print("  2. AI vs AI game")
    print("  3. Board operations")
    print("  4. Deck operations")
    print("  5. Heuristic evaluation")
    print("  6. Game state JSON serialization")
    print("  7. Complete game simulation")
    
    choice = input("\nRun all examples? (y/n): ").strip().lower()
    
    if choice == 'y':
        run_all_examples()
    else:
        print("\nRun individual examples by calling the functions:")
        print("  python -c 'from examples import example_1_basic_game; example_1_basic_game()'")
