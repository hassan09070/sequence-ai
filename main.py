"""
Main Game Runner for Sequence Board Game

Provides interfaces for playing Sequence with human and AI players.
"""

import sys
import os
from typing import Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import GameState, Board, Deck, Player
from ai import MinimaxAI


class SequenceGame:
    """Main game controller for Sequence."""
    
    def __init__(self):
        """Initialize the game controller."""
        self.state: Optional[GameState] = None
        self.ai_players = {}  # player_id -> MinimaxAI
    
    def start_new_game(self, num_players: int = 2, ai_config: Optional[dict] = None):
        """
        Start a new game.
        
        Args:
            num_players: Number of players (2 or 3)
            ai_config: Dictionary mapping player_id to AI difficulty
                      e.g., {2: 'medium'} makes player 2 an AI on medium difficulty
        """
        self.state = GameState(num_players)
        
        # Configure players
        player_configs = []
        for i in range(1, num_players + 1):
            is_ai = ai_config and i in ai_config
            config = {
                'name': f'AI Player {i}' if is_ai else f'Human Player {i}',
                'is_ai': is_ai
            }
            player_configs.append(config)
            
            # Create AI instance if needed
            if is_ai:
                difficulty = ai_config[i]
                self.ai_players[i] = MinimaxAI(i, difficulty)
        
        self.state.setup_game(player_configs)
        print("🎮 Sequence Game Started!")
        print(f"Players: {num_players}")
        print(f"Sequences needed to win: {self.state.sequences_needed_to_win}")
        print("=" * 50)
    
    def play_turn(self) -> bool:
        """
        Play one turn (current player makes a move).
        
        Returns:
            True if game continues, False if game is over
        """
        if self.state.is_terminal():
            return False
        
        current_player = self.state.get_current_player()
        print(f"\n{'=' * 50}")
        print(f"Turn: {current_player.name}")
        print(f"{'=' * 50}")
        
        # AI player
        if current_player.is_ai:
            ai = self.ai_players[current_player.player_id]
            print(f"AI is thinking (difficulty: {ai.difficulty})...")
            
            move = ai.get_best_move(self.state)
            
            if move:
                stats = ai.get_stats()
                print(f"AI explored {stats['nodes_explored']} nodes, "
                      f"pruned {stats['pruning_count']} branches")
                print(f"AI plays: {move.card} at position ({move.row}, {move.col})")
                
                self.state.apply_move(move)
                self.state.next_turn()
            else:
                print("AI has no legal moves!")
                return False
        
        # Human player
        else:
            self._display_game_state()
            move = self._get_human_move(current_player)
            
            if move:
                success = self.state.apply_move(move)
                if success:
                    self.state.next_turn()
                    print(f"✓ Move successful: {move.card} at ({move.row}, {move.col})")
                else:
                    print("✗ Invalid move! Try again.")
                    return self.play_turn()  # Retry
            else:
                print("No legal moves available!")
                return False
        
        # Check if game is over
        if self.state.is_terminal():
            self._display_game_state()
            winner = self.state.players[self.state.winner - 1]
            print(f"\n{'🏆' * 20}")
            print(f"   GAME OVER - {winner.name} WINS!")
            print(f"{'🏆' * 20}\n")
            return False
        
        return True
    
    def _display_game_state(self):
        """Display the current game state."""
        print("\n" + str(self.state))
    
    def _get_human_move(self, player: Player):
        """
        Get a move from a human player via console input.
        
        Args:
            player: Current player
            
        Returns:
            Move object or None
        """
        from game.gamestate import Move
        
        print(f"\nYour hand: {player.hand}")
        
        legal_moves = self.state.get_legal_moves(player)
        if not legal_moves:
            return None
        
        # Group moves by card
        moves_by_card = {}
        for move in legal_moves:
            if move.card not in moves_by_card:
                moves_by_card[move.card] = []
            moves_by_card[move.card].append(move)
        
        # Display available cards
        print("\nAvailable cards to play:")
        for i, card in enumerate(sorted(moves_by_card.keys()), 1):
            move_count = len(moves_by_card[card])
            print(f"  {i}. {card} ({move_count} positions available)")
        
        # Get card choice
        while True:
            try:
                card_idx = int(input("\nSelect card number (or 0 to see full board): ")) - 1
                if card_idx == -1:
                    self._display_game_state()
                    continue
                
                card = sorted(moves_by_card.keys())[card_idx]
                break
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")
        
        # Get position choice
        available_moves = moves_by_card[card]
        
        if len(available_moves) == 1:
            # Only one position available
            return available_moves[0]
        
        print(f"\nAvailable positions for {card}:")
        for i, move in enumerate(available_moves, 1):
            print(f"  {i}. Row {move.row}, Col {move.col} ({move.move_type})")
        
        while True:
            try:
                pos_idx = int(input("\nSelect position number: ")) - 1
                return available_moves[pos_idx]
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")
    
    def play_game(self):
        """Play a complete game (loop until game over)."""
        while self.play_turn():
            pass
    
    def save_game_state(self, filename: str):
        """Save the current game state to a JSON file."""
        if self.state:
            with open(filename, 'w') as f:
                f.write(self.state.to_json())
            print(f"Game saved to {filename}")
    
    def get_game_state_json(self) -> str:
        """Get the current game state as JSON string."""
        if self.state:
            return self.state.to_json()
        return "{}"


def main():
    """Main entry point for the game."""
    print("=" * 60)
    print("            WELCOME TO SEQUENCE BOARD GAME")
    print("=" * 60)
    
    # Game setup
    print("\nGame Setup:")
    print("1. Human vs Human")
    print("2. Human vs AI")
    print("3. AI vs AI (Demo)")
    
    while True:
        try:
            choice = int(input("\nSelect game mode (1-3): "))
            if choice in [1, 2, 3]:
                break
        except ValueError:
            pass
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    game = SequenceGame()
    
    if choice == 1:
        # Human vs Human
        game.start_new_game(num_players=2, ai_config=None)
    
    elif choice == 2:
        # Human vs AI
        print("\nSelect AI difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Expert")
        
        while True:
            try:
                diff_choice = int(input("\nDifficulty (1-4): "))
                if diff_choice in [1, 2, 3, 4]:
                    break
            except ValueError:
                pass
            print("Invalid choice.")
        
        difficulty_map = {1: 'easy', 2: 'medium', 3: 'hard', 4: 'expert'}
        difficulty = difficulty_map[diff_choice]
        
        game.start_new_game(num_players=2, ai_config={2: difficulty})
    
    else:
        # AI vs AI Demo
        print("\nAI vs AI Demo")
        print("Player 1: AI (Medium)")
        print("Player 2: AI (Medium)")
        
        game.start_new_game(num_players=2, ai_config={1: 'medium', 2: 'medium'})
    
    # Play the game
    game.play_game()
    
    # Save option
    save = input("\nSave game state? (y/n): ").strip().lower()
    if save == 'y':
        filename = input("Enter filename (default: game_state.json): ").strip()
        if not filename:
            filename = "game_state.json"
        game.save_game_state(filename)


if __name__ == "__main__":
    main()
