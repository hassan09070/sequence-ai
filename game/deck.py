"""
Deck Module for Sequence Game

Manages the card deck (2 standard 52-card decks) and dealing logic.
"""

import random
from typing import List, Tuple
import copy


class Deck:
    """
    Represents the Sequence game deck.
    
    The deck consists of 2 full standard 52-card decks (104 cards total).
    Jacks have special meanings in Sequence:
    - Two-eyed Jacks (JH, JD): Wild - can place chip anywhere
    - One-eyed Jacks (JS, JC): Remove opponent's chip
    """
    
    # Standard card ranks and suits
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['H', 'D', 'C', 'S']  # Hearts, Diamonds, Clubs, Spades
    
    # Jack categorization
    TWO_EYED_JACKS = ['JH', 'JD']  # Can place anywhere
    ONE_EYED_JACKS = ['JS', 'JC']  # Can remove opponent chip
    
    def __init__(self):
        """Initialize a Sequence deck (2 standard decks)."""
        self.cards = self._create_deck()
        self.discarded = []
    
    def _create_deck(self) -> List[str]:
        """
        Create a Sequence deck (2 full standard decks).
        
        Returns:
            List of card strings (e.g., ["2H", "3D", ...])
        """
        single_deck = [f"{rank}{suit}" for suit in self.SUITS for rank in self.RANKS]
        # Sequence uses 2 full decks
        return single_deck + single_deck
    
    def shuffle(self):
        """Shuffle the deck randomly."""
        random.shuffle(self.cards)
    
    def deal(self, count: int = 1) -> List[str]:
        """
        Deal cards from the deck.
        
        Args:
            count: Number of cards to deal
            
        Returns:
            List of dealt cards
            
        Raises:
            ValueError: If not enough cards in deck
        """
        if count > len(self.cards):
            raise ValueError(f"Not enough cards in deck. Requested: {count}, Available: {len(self.cards)}")
        
        dealt_cards = []
        for _ in range(count):
            if self.cards:
                dealt_cards.append(self.cards.pop())
        
        return dealt_cards
    
    def discard(self, card: str):
        """
        Add a card to the discard pile.
        
        Args:
            card: Card string to discard
        """
        self.discarded.append(card)
    
    def reshuffle_discards(self):
        """Reshuffle discarded cards back into the deck."""
        self.cards.extend(self.discarded)
        self.discarded = []
        self.shuffle()
    
    def cards_remaining(self) -> int:
        """Get the number of cards remaining in the deck."""
        return len(self.cards)
    
    def is_two_eyed_jack(self, card: str) -> bool:
        """
        Check if a card is a two-eyed jack (wild card).
        
        Args:
            card: Card string
            
        Returns:
            True if card is JH or JD
        """
        return card in self.TWO_EYED_JACKS
    
    def is_one_eyed_jack(self, card: str) -> bool:
        """
        Check if a card is a one-eyed jack (remove chip).
        
        Args:
            card: Card string
            
        Returns:
            True if card is JS or JC
        """
        return card in self.ONE_EYED_JACKS
    
    def is_jack(self, card: str) -> bool:
        """
        Check if a card is any jack.
        
        Args:
            card: Card string
            
        Returns:
            True if card is any jack
        """
        return card.startswith('J')
    
    @staticmethod
    def get_hand_size(num_players: int) -> int:
        """
        Get the standard hand size for Sequence based on player count.
        
        Args:
            num_players: Number of players (2-3 typically)
            
        Returns:
            Number of cards per hand
        """
        hand_sizes = {
            2: 7,  # 2 players: 7 cards each
            3: 6,  # 3 players: 6 cards each
            4: 6,  # 4 players (2 teams): 6 cards each
        }
        return hand_sizes.get(num_players, 7)
    
    def clone(self) -> 'Deck':
        """Create a deep copy of the deck."""
        new_deck = Deck()
        new_deck.cards = copy.deepcopy(self.cards)
        new_deck.discarded = copy.deepcopy(self.discarded)
        return new_deck
    
    def to_dict(self) -> dict:
        """Serialize deck to dictionary for JSON export."""
        return {
            'cards': self.cards,
            'discarded': self.discarded,
            'remaining': len(self.cards)
        }
    
    def __len__(self) -> int:
        """Return the number of cards remaining in the deck."""
        return len(self.cards)
    
    def __str__(self) -> str:
        """String representation of the deck."""
        return f"Deck(cards={len(self.cards)}, discarded={len(self.discarded)})"
