"""
GameState Module for Sequence Game

Manages the complete game state including board, players, and game logic.
"""

from typing import List, Tuple, Optional, Dict
import copy
import json

from .board import Board
from .deck import Deck
from .player import Player


class Move:
    """Represents a single move in the game."""
    
    def __init__(self, player_id: int, card: str, row: int, col: int, 
                 move_type: str = "place"):
        """
        Initialize a move.
        
        Args:
            player_id: ID of player making the move
            card: Card being played
            row: Row position on board
            col: Column position on board
            move_type: Type of move ("place" or "remove")
        """
        self.player_id = player_id
        self.card = card
        self.row = row
        self.col = col
        self.move_type = move_type  # "place" or "remove"
    
    def to_dict(self) -> dict:
        """Convert move to dictionary."""
        return {
            'player_id': self.player_id,
            'card': self.card,
            'position': [self.row, self.col],
            'move_type': self.move_type
        }
    
    def __repr__(self) -> str:
        return f"Move(P{self.player_id}, {self.card}, ({self.row},{self.col}), {self.move_type})"


class GameState:
    """
    Manages the complete game state for Sequence.
    
    Handles all game logic including:
    - Board and chip management
    - Player turns and moves
    - Win condition detection
    - Legal move generation
    """
    
    def __init__(self, num_players: int = 2):
        """
        Initialize a new game state.
        
        Args:
            num_players: Number of players (default: 2)
        """
        if num_players not in [2, 3]:
            raise ValueError("Sequence supports 2-3 players")
        
        self.board = Board()
        self.deck = Deck()
        self.num_players = num_players
        self.players: List[Player] = []
        self.current_player_idx = 0
        self.move_history: List[Move] = []
        self.sequences_needed_to_win = 2 if num_players == 2 else 1
        self.winner: Optional[int] = None
        self.game_over = False
    
    def setup_game(self, player_configs: Optional[List[Dict]] = None):
        """
        Set up a new game with players and initial hands.
        
        Args:
            player_configs: List of player configurations
                           [{'name': 'Alice', 'is_ai': False}, ...]
        """
        # Create players
        if player_configs:
            for i, config in enumerate(player_configs[:self.num_players], start=1):
                player = Player(
                    player_id=i,
                    name=config.get('name', f'Player {i}'),
                    is_ai=config.get('is_ai', False)
                )
                self.players.append(player)
        else:
            # Default: create human players
            for i in range(1, self.num_players + 1):
                self.players.append(Player(player_id=i))
        
        # Shuffle and deal cards
        self.deck.shuffle()
        self.deal_initial_hands()
    
    def deal_initial_hands(self):
        """Deal initial cards to all players."""
        hand_size = self.deck.get_hand_size(self.num_players)
        
        for player in self.players:
            cards = self.deck.deal(hand_size)
            player.add_cards(cards)
    
    def get_current_player(self) -> Player:
        """Get the player whose turn it is."""
        return self.players[self.current_player_idx]
    
    def get_opponent_id(self, player_id: int) -> int:
        """Get opponent player ID (for 2-player game)."""
        return 2 if player_id == 1 else 1
    
    def next_turn(self):
        """Advance to the next player's turn."""
        self.current_player_idx = (self.current_player_idx + 1) % self.num_players
    
    def get_legal_moves(self, player: Optional[Player] = None) -> List[Move]:
        """
        Get all legal moves for a player.
        
        Args:
            player: Player to get moves for (default: current player)
            
        Returns:
            List of legal Move objects
        """
        if player is None:
            player = self.get_current_player()
        
        legal_moves = []
        
        for card in player.hand:
            # Handle two-eyed jacks (wild - can place anywhere)
            if self.deck.is_two_eyed_jack(card):
                for row in range(self.board.size):
                    for col in range(self.board.size):
                        if not self.board.is_position_occupied(row, col):
                            legal_moves.append(Move(player.player_id, card, row, col, "place"))
            
            # Handle one-eyed jacks (remove opponent chip)
            elif self.deck.is_one_eyed_jack(card):
                opponent_id = self.get_opponent_id(player.player_id)
                for row in range(self.board.size):
                    for col in range(self.board.size):
                        chip = self.board.get_chip_at(row, col)
                        # Only include removal if chip belongs to opponent AND is not in a completed sequence
                        if chip == opponent_id and not self.board._is_position_in_sequence(row, col):
                            legal_moves.append(Move(player.player_id, card, row, col, "remove"))
            
            # Handle regular cards
            else:
                positions = self.board.find_card_positions(card)
                for row, col in positions:
                    if not self.board.is_position_occupied(row, col):
                        legal_moves.append(Move(player.player_id, card, row, col, "place"))
        
        return legal_moves
    
    def apply_move(self, move: Move) -> bool:
        """
        Apply a move to the game state.
        
        Args:
            move: Move object to apply
            
        Returns:
            True if move was successful
        """
        player = self.players[move.player_id - 1]
        
        # Validate player has the card
        if not player.has_card(move.card):
            return False
        
        # Apply the move based on type
        if move.move_type == "place":
            success = self.board.place_chip(move.row, move.col, move.player_id)
        elif move.move_type == "remove":
            success = self.board.remove_chip(move.row, move.col)
        else:
            return False
        
        if not success:
            return False
        
        # Remove card from hand and draw new one
        player.remove_card(move.card)
        self.deck.discard(move.card)
        
        # Draw a new card if deck has cards
        if self.deck.cards_remaining() > 0:
            new_card = self.deck.deal(1)[0]
            player.add_card(new_card)
        elif self.deck.discarded:
            # Reshuffle discards if deck is empty
            self.deck.reshuffle_discards()
            if self.deck.cards_remaining() > 0:
                new_card = self.deck.deal(1)[0]
                player.add_card(new_card)
        
        # Record move
        self.move_history.append(move)
        
        # Check for win condition
        self._check_win_condition(move.player_id)
        
        return True
    
    def make_move(self, card: str, row: int, col: int) -> bool:
        """
        Convenience method to make a move for the current player.
        
        Args:
            card: Card to play
            row: Row position
            col: Column position
            
        Returns:
            True if move was successful
        """
        player = self.get_current_player()
        
        # Determine move type
        move_type = "remove" if self.deck.is_one_eyed_jack(card) else "place"
        
        move = Move(player.player_id, card, row, col, move_type)
        success = self.apply_move(move)
        
        if success:
            self.next_turn()
        
        return success
    
    def _check_win_condition(self, player_id: int):
        """Check if a player has won the game."""
        sequences = self.board.check_sequence(player_id)
        
        if sequences >= self.sequences_needed_to_win:
            self.winner = player_id
            self.game_over = True
            self.players[player_id - 1].sequences_completed = sequences
    
    def is_terminal(self) -> bool:
        """Check if the game has ended."""
        return self.game_over
    
    def get_winner(self) -> Optional[int]:
        """Get the winner's player ID (None if no winner)."""
        return self.winner
    
    def clone(self) -> 'GameState':
        """Create a deep copy of the game state."""
        new_state = GameState(self.num_players)
        new_state.board = self.board.clone()
        new_state.deck = self.deck.clone()
        new_state.players = [p.clone() for p in self.players]
        new_state.current_player_idx = self.current_player_idx
        new_state.move_history = copy.deepcopy(self.move_history)
        new_state.sequences_needed_to_win = self.sequences_needed_to_win
        new_state.winner = self.winner
        new_state.game_over = self.game_over
        return new_state
    
    def to_json(self, hide_opponent_hands: bool = False) -> str:
        """
        Serialize game state to JSON.
        
        Args:
            hide_opponent_hands: Whether to hide opponent hands
            
        Returns:
            JSON string representation
        """
        current_player_id = self.get_current_player().player_id
        
        state_dict = {
            'board': self.board.to_dict(),
            'players': [
                p.to_dict(hide_hand=(hide_opponent_hands and p.player_id != current_player_id))
                for p in self.players
            ],
            'current_player': current_player_id,
            'deck_remaining': self.deck.cards_remaining(),
            'sequences_needed': self.sequences_needed_to_win,
            'game_over': self.game_over,
            'winner': self.winner,
            'move_count': len(self.move_history)
        }
        
        return json.dumps(state_dict, indent=2)
    
    def __str__(self) -> str:
        """String representation of the game state."""
        lines = []
        lines.append(f"\n{'=' * 50}")
        lines.append(f"SEQUENCE GAME - Turn {len(self.move_history) + 1}")
        lines.append(f"{'=' * 50}\n")
        
        # Show current player
        current = self.get_current_player()
        lines.append(f"Current Player: {current.name} (P{current.player_id})")
        lines.append(f"Cards in hand: {current.hand}\n")
        
        # Show board
        lines.append(str(self.board))
        lines.append("")
        
        # Show player info
        for player in self.players:
            sequences = self.board.check_sequence(player.player_id)
            lines.append(f"{player.name}: {player.hand_size()} cards, "
                        f"{sequences}/{self.sequences_needed_to_win} sequences")
        
        if self.game_over:
            winner = self.players[self.winner - 1]
            lines.append(f"\n🏆 GAME OVER - {winner.name} WINS! 🏆")
        
        return "\n".join(lines)
