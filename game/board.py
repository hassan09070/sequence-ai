"""
Board Module for Sequence Game

Manages the 10x10 game board with card mappings and chip placements.
"""

from typing import List, Tuple, Optional, Dict
import copy


class Board:
    """
    Represents the Sequence game board.
    
    The board is a 10x10 grid where:
    - Each cell maps to a playing card
    - Corner cells (0,0), (0,9), (9,0), (9,9) are wild/free spaces
    - Players place chips to form sequences
    """
    
    # Standard Sequence board layout (10x10)
    BOARD_LAYOUT = [
        ["XX", "6D", "7D", "8D", "9D", "10D", "QD", "KD", "AD", "XX"],
        ["5D", "3H", "2H", "2S", "3S", "4S", "5S", "6S", "7S", "AC"],
        ["4D", "4H", "KD", "AD", "AC", "KC", "QC", "10C", "8S", "KC"],
        ["3D", "5H", "QD", "QH", "10H", "9H", "8H", "9C", "9S", "QC"],
        ["2D", "6H", "10D", "KH", "3H", "2H", "7H", "8C", "10S", "10C"],
        ["AS", "7H", "9D", "AH", "4H", "5H", "6H", "7C", "QS", "9C"],
        ["KS", "8H", "8D", "2C", "3C", "4C", "5C", "6C", "KS", "8C"],
        ["QS", "9H", "7D", "6D", "5D", "4D", "3D", "2D", "AS", "7C"],
        ["10S", "10H", "QH", "KH", "AH", "2C", "3C", "4C", "5C", "6C"],
        ["XX", "9S", "8S", "7S", "6S", "5S", "4S", "3S", "2S", "XX"]
    ]
    
    # Wild corner positions
    WILD_POSITIONS = [(0, 0), (0, 9), (9, 0), (9, 9)]
    
    def __init__(self):
        """Initialize the board with card layout and empty chip grid."""
        self.size = 10
        self.card_grid = copy.deepcopy(self.BOARD_LAYOUT)
        # Chip grid: 0 = empty, 1 = player 1, 2 = player 2
        self.chip_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        # Track positions that are part of completed sequences (cannot be removed)
        self.sequence_positions: Dict[int, List[List[Tuple[int, int]]]] = {1: [], 2: []}
        
        # Mark wild corners as occupied for both players (special value 3)
        for row, col in self.WILD_POSITIONS:
            self.chip_grid[row][col] = 3
    
    def get_card_at(self, row: int, col: int) -> str:
        """Get the card at the specified position."""
        if not self._is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self.card_grid[row][col]
    
    def get_chip_at(self, row: int, col: int) -> int:
        """Get the chip at the specified position (0=empty, 1=P1, 2=P2, 3=wild)."""
        if not self._is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self.chip_grid[row][col]
    
    def find_card_positions(self, card: str) -> List[Tuple[int, int]]:
        """
        Find all positions on the board where a specific card appears.
        
        Args:
            card: Card string (e.g., "5H", "KD")
            
        Returns:
            List of (row, col) tuples
        """
        positions = []
        for row in range(self.size):
            for col in range(self.size):
                if self.card_grid[row][col] == card:
                    positions.append((row, col))
        return positions
    
    def place_chip(self, row: int, col: int, player_id: int) -> bool:
        """
        Place a chip at the specified position.
        
        Args:
            row: Row index (0-9)
            col: Column index (0-9)
            player_id: Player identifier (1 or 2)
            
        Returns:
            True if placement was successful, False otherwise
        """
        if not self._is_valid_position(row, col):
            return False
        
        # Cannot place on already occupied positions (except wild, which can't be placed on anyway)
        if self.chip_grid[row][col] != 0:
            return False
        
        self.chip_grid[row][col] = player_id
        return True
    
    def remove_chip(self, row: int, col: int) -> bool:
        """
        Remove a chip from the specified position (for one-eyed jack).
        
        Args:
            row: Row index (0-9)
            col: Column index (0-9)
            
        Returns:
            True if removal was successful, False otherwise
        """
        if not self._is_valid_position(row, col):
            return False
        
        # Cannot remove from wild corners or empty positions
        if (row, col) in self.WILD_POSITIONS or self.chip_grid[row][col] == 0:
            return False
        
        # Cannot remove from a completed sequence
        if self._is_position_in_sequence(row, col):
            return False
        
        self.chip_grid[row][col] = 0
        return True
    
    def is_position_occupied(self, row: int, col: int) -> bool:
        """Check if a position is occupied by any chip."""
        if not self._is_valid_position(row, col):
            return False
        return self.chip_grid[row][col] != 0
    
    def _is_position_in_sequence(self, row: int, col: int) -> bool:
        """Check if a position is part of any completed sequence."""
        for player_id in [1, 2]:
            for sequence in self.sequence_positions.get(player_id, []):
                if (row, col) in sequence:
                    return True
        return False
    
    def check_sequence(self, player_id: int) -> int:
        """
        Check for sequences (5 connected chips) for a player.
        
        Args:
            player_id: Player identifier (1 or 2)
            
        Returns:
            Number of sequences found
        """
        sequences = 0
        visited = set()
        found_sequences = []
        
        # Check horizontal sequences
        sequences += self._check_horizontal_sequences(player_id, visited, found_sequences)
        
        # Check vertical sequences
        sequences += self._check_vertical_sequences(player_id, visited, found_sequences)
        
        # Check diagonal sequences (top-left to bottom-right)
        sequences += self._check_diagonal_sequences(player_id, visited, direction="tlbr", found_sequences=found_sequences)
        
        # Check diagonal sequences (top-right to bottom-left)
        sequences += self._check_diagonal_sequences(player_id, visited, direction="trbl", found_sequences=found_sequences)
        
        # Store the sequences
        self.sequence_positions[player_id] = found_sequences
        
        return sequences
    
    def get_sequence_positions(self, player_id: int) -> List[List[Tuple[int, int]]]:
        """Get all sequence positions for a player."""
        return self.sequence_positions.get(player_id, [])
    
    def _check_horizontal_sequences(self, player_id: int, visited: set, found_sequences: List = None) -> int:
        """Check for horizontal sequences."""
        if found_sequences is None:
            found_sequences = []
        sequences = 0
        for row in range(self.size):
            for col in range(self.size - 4):
                sequence = []
                for i in range(5):
                    chip = self.chip_grid[row][col + i]
                    if chip == player_id or chip == 3:  # Wild corners count for both
                        sequence.append((row, col + i))
                    else:
                        break
                
                if len(sequence) == 5:
                    seq_tuple = tuple(sorted(sequence))
                    if seq_tuple not in visited:
                        visited.add(seq_tuple)
                        found_sequences.append(list(sequence))
                        sequences += 1
        return sequences
    
    def _check_vertical_sequences(self, player_id: int, visited: set, found_sequences: List = None) -> int:
        """Check for vertical sequences."""
        if found_sequences is None:
            found_sequences = []
        sequences = 0
        for col in range(self.size):
            for row in range(self.size - 4):
                sequence = []
                for i in range(5):
                    chip = self.chip_grid[row + i][col]
                    if chip == player_id or chip == 3:  # Wild corners count for both
                        sequence.append((row + i, col))
                    else:
                        break
                
                if len(sequence) == 5:
                    seq_tuple = tuple(sorted(sequence))
                    if seq_tuple not in visited:
                        visited.add(seq_tuple)
                        found_sequences.append(list(sequence))
                        sequences += 1
        return sequences
    
    def _check_diagonal_sequences(self, player_id: int, visited: set, direction: str, found_sequences: List = None) -> int:
        """Check for diagonal sequences."""
        if found_sequences is None:
            found_sequences = []
        sequences = 0
        
        if direction == "tlbr":  # Top-left to bottom-right
            for row in range(self.size - 4):
                for col in range(self.size - 4):
                    sequence = []
                    for i in range(5):
                        chip = self.chip_grid[row + i][col + i]
                        if chip == player_id or chip == 3:
                            sequence.append((row + i, col + i))
                        else:
                            break
                    
                    if len(sequence) == 5:
                        seq_tuple = tuple(sorted(sequence))
                        if seq_tuple not in visited:
                            visited.add(seq_tuple)
                            found_sequences.append(list(sequence))
                            sequences += 1
        
        elif direction == "trbl":  # Top-right to bottom-left
            for row in range(self.size - 4):
                for col in range(4, self.size):
                    sequence = []
                    for i in range(5):
                        chip = self.chip_grid[row + i][col - i]
                        if chip == player_id or chip == 3:
                            sequence.append((row + i, col - i))
                        else:
                            break
                    
                    if len(sequence) == 5:
                        seq_tuple = tuple(sorted(sequence))
                        if seq_tuple not in visited:
                            visited.add(seq_tuple)
                            found_sequences.append(list(sequence))
                            sequences += 1
        
        return sequences
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is within board bounds."""
        return 0 <= row < self.size and 0 <= col < self.size
    
    def clone(self) -> 'Board':
        """Create a deep copy of the board."""
        new_board = Board()
        new_board.chip_grid = copy.deepcopy(self.chip_grid)
        new_board.sequence_positions = copy.deepcopy(self.sequence_positions)
        return new_board
    
    def to_dict(self) -> dict:
        """Serialize board to dictionary for JSON export."""
        return {
            'size': self.size,
            'card_grid': self.card_grid,
            'chip_grid': self.chip_grid,
            'sequence_positions': self.sequence_positions
        }
    
    def __str__(self) -> str:
        """String representation of the board showing chips."""
        lines = []
        lines.append("   " + " ".join(f"{i:2}" for i in range(self.size)))
        lines.append("  +" + "---" * self.size + "+")
        
        for row in range(self.size):
            row_str = f"{row:2}|"
            for col in range(self.size):
                chip = self.chip_grid[row][col]
                if chip == 0:
                    row_str += " . "
                elif chip == 1:
                    row_str += " 1 "
                elif chip == 2:
                    row_str += " 2 "
                elif chip == 3:
                    row_str += " * "
            row_str += "|"
            lines.append(row_str)
        
        lines.append("  +" + "---" * self.size + "+")
        return "\n".join(lines)
