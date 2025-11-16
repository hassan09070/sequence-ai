"""
Player Module for Sequence Game

Represents a player with hand management and chip tracking.
"""

from typing import List, Optional
import copy


class Player:
    """
    Represents a player in the Sequence game.
    
    Attributes:
        player_id: Unique identifier (1 or 2)
        name: Player name
        hand: List of cards in player's hand
        chip_type: Chip identifier (same as player_id)
        is_ai: Whether this player is controlled by AI
    """
    
    def __init__(self, player_id: int, name: Optional[str] = None, is_ai: bool = False):
        """
        Initialize a player.
        
        Args:
            player_id: Unique player identifier (1 or 2)
            name: Player name (defaults to "Player {id}")
            is_ai: Whether this player is AI-controlled
        """
        if player_id not in [1, 2]:
            raise ValueError("Player ID must be 1 or 2")
        
        self.player_id = player_id
        self.name = name if name else f"Player {player_id}"
        self.hand = []
        self.chip_type = player_id  # Chip type matches player ID
        self.is_ai = is_ai
        self.sequences_completed = 0
    
    def add_card(self, card: str):
        """
        Add a card to the player's hand.
        
        Args:
            card: Card string (e.g., "5H", "KD")
        """
        self.hand.append(card)
    
    def add_cards(self, cards: List[str]):
        """
        Add multiple cards to the player's hand.
        
        Args:
            cards: List of card strings
        """
        self.hand.extend(cards)
    
    def remove_card(self, card: str) -> bool:
        """
        Remove a card from the player's hand.
        
        Args:
            card: Card string to remove
            
        Returns:
            True if card was removed, False if not in hand
        """
        if card in self.hand:
            self.hand.remove(card)
            return True
        return False
    
    def has_card(self, card: str) -> bool:
        """
        Check if player has a specific card in hand.
        
        Args:
            card: Card string to check
            
        Returns:
            True if card is in hand
        """
        return card in self.hand
    
    def get_hand(self) -> List[str]:
        """Get a copy of the player's current hand."""
        return self.hand.copy()
    
    def hand_size(self) -> int:
        """Get the number of cards in the player's hand."""
        return len(self.hand)
    
    def is_hand_empty(self) -> bool:
        """Check if the player's hand is empty."""
        return len(self.hand) == 0
    
    def clear_hand(self):
        """Remove all cards from the player's hand."""
        self.hand = []
    
    def sort_hand(self):
        """Sort the player's hand alphabetically."""
        self.hand.sort()
    
    def clone(self) -> 'Player':
        """Create a deep copy of the player."""
        new_player = Player(self.player_id, self.name, self.is_ai)
        new_player.hand = copy.deepcopy(self.hand)
        new_player.sequences_completed = self.sequences_completed
        return new_player
    
    def to_dict(self, hide_hand: bool = False) -> dict:
        """
        Serialize player to dictionary for JSON export.
        
        Args:
            hide_hand: If True, hide the hand details (for opponent view)
            
        Returns:
            Dictionary representation of player
        """
        return {
            'player_id': self.player_id,
            'name': self.name,
            'chip_type': self.chip_type,
            'is_ai': self.is_ai,
            'hand_size': len(self.hand),
            'hand': self.hand if not hide_hand else ['***'] * len(self.hand),
            'sequences_completed': self.sequences_completed
        }
    
    def __str__(self) -> str:
        """String representation of the player."""
        return f"{self.name} (P{self.player_id}) - Hand: {len(self.hand)} cards"
    
    def __repr__(self) -> str:
        """Detailed representation of the player."""
        return f"Player(id={self.player_id}, name='{self.name}', hand={self.hand}, is_ai={self.is_ai})"
