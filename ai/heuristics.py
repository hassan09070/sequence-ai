"""
Heuristics Module for Sequence Game AI

Provides evaluation functions for assessing game states.
"""

from typing import List, Tuple, Set
import sys

# Import game modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.gamestate import GameState
from game.board import Board


class SequenceEvaluator:
    """
    Evaluates board positions for the AI player.
    
    Considers multiple factors:
    - Offensive: Potential sequences and near-complete sequences
    - Defensive: Blocking opponent sequences
    - Board control: Strategic position control
    - Card utility: Value of cards in hand
    """
    
    # Evaluation weights
    WEIGHTS = {
        'complete_sequence': 10000,      # Completed sequence (win condition)
        'four_in_row': 500,               # 4 connected chips (one away from sequence)
        'three_in_row': 100,              # 3 connected chips
        'two_in_row': 20,                 # 2 connected chips
        'open_ended': 1.5,                # Multiplier for open-ended sequences
        'center_control': 5,              # Controlling center positions
        'corner_control': 3,              # Controlling near corners
        'blocking_opponent': 150,         # Blocking opponent's 4-in-row
        'card_playability': 2,            # Having playable cards
        'wild_card_value': 50,            # Value of two-eyed jacks
    }
    
    # Center positions (strategically valuable)
    CENTER_POSITIONS = [
        (4, 4), (4, 5), (5, 4), (5, 5),
        (3, 4), (3, 5), (4, 3), (4, 6),
        (5, 3), (5, 6), (6, 4), (6, 5)
    ]
    
    @staticmethod
    def evaluate_state(state: GameState, player_id: int) -> float:
        """
        Evaluate the game state from a player's perspective.
        
        Args:
            state: Current game state
            player_id: Player ID to evaluate for (1 or 2)
            
        Returns:
            Evaluation score (higher is better for player)
        """
        # Check terminal states
        if state.is_terminal():
            winner = state.get_winner()
            if winner == player_id:
                return float('inf')  # Win
            else:
                return float('-inf')  # Loss
        
        opponent_id = state.get_opponent_id(player_id)
        
        # Calculate component scores
        offensive_score = SequenceEvaluator._evaluate_offensive(state, player_id)
        defensive_score = SequenceEvaluator._evaluate_defensive(state, player_id, opponent_id)
        board_control_score = SequenceEvaluator._evaluate_board_control(state, player_id)
        card_utility_score = SequenceEvaluator._evaluate_card_utility(state, player_id)
        
        # Combine scores
        total_score = (
            offensive_score +
            defensive_score +
            board_control_score +
            card_utility_score
        )
        
        return total_score
    
    @staticmethod
    def _evaluate_offensive(state: GameState, player_id: int) -> float:
        """Evaluate offensive potential (creating sequences)."""
        score = 0.0
        board = state.board
        
        # Check for completed sequences
        complete_sequences = board.check_sequence(player_id)
        score += complete_sequences * SequenceEvaluator.WEIGHTS['complete_sequence']
        
        # Evaluate partial sequences (2, 3, 4 in a row)
        score += SequenceEvaluator._evaluate_partial_sequences(board, player_id)
        
        return score
    
    @staticmethod
    def _evaluate_defensive(state: GameState, player_id: int, opponent_id: int) -> float:
        """Evaluate defensive strength (blocking opponent)."""
        score = 0.0
        board = state.board
        
        # Check opponent's threats
        opponent_threats = SequenceEvaluator._count_threats(board, opponent_id)
        
        # High penalty for opponent 4-in-row (must block!)
        score -= opponent_threats['four_in_row'] * SequenceEvaluator.WEIGHTS['four_in_row']
        
        # Moderate penalty for opponent 3-in-row
        score -= opponent_threats['three_in_row'] * SequenceEvaluator.WEIGHTS['three_in_row'] * 0.5
        
        return score
    
    @staticmethod
    def _evaluate_board_control(state: GameState, player_id: int) -> float:
        """Evaluate control of strategic board positions."""
        score = 0.0
        board = state.board
        
        # Count chips in center positions
        center_chips = 0
        for row, col in SequenceEvaluator.CENTER_POSITIONS:
            if board.get_chip_at(row, col) == player_id:
                center_chips += 1
        
        score += center_chips * SequenceEvaluator.WEIGHTS['center_control']
        
        return score
    
    @staticmethod
    def _evaluate_card_utility(state: GameState, player_id: int) -> float:
        """Evaluate the utility of cards in hand."""
        score = 0.0
        player = state.players[player_id - 1]
        
        # Count playable cards
        legal_moves = state.get_legal_moves(player)
        playable_cards = len(set(move.card for move in legal_moves))
        score += playable_cards * SequenceEvaluator.WEIGHTS['card_playability']
        
        # Bonus for wild cards (two-eyed jacks)
        wild_cards = sum(1 for card in player.hand if state.deck.is_two_eyed_jack(card))
        score += wild_cards * SequenceEvaluator.WEIGHTS['wild_card_value']
        
        return score
    
    @staticmethod
    def _evaluate_partial_sequences(board: Board, player_id: int) -> float:
        """Evaluate partial sequences (2, 3, 4 in a row)."""
        score = 0.0
        
        # Check all directions
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal (top-left to bottom-right)
            (1, -1),  # Diagonal (top-right to bottom-left)
        ]
        
        for row in range(board.size):
            for col in range(board.size):
                if board.get_chip_at(row, col) == player_id or board.get_chip_at(row, col) == 3:
                    for dr, dc in directions:
                        sequence_info = SequenceEvaluator._analyze_sequence_from_position(
                            board, row, col, dr, dc, player_id
                        )
                        score += sequence_info['score']
        
        return score / 2  # Divide by 2 to avoid double counting
    
    @staticmethod
    def _analyze_sequence_from_position(board: Board, start_row: int, start_col: int,
                                       dr: int, dc: int, player_id: int) -> dict:
        """
        Analyze a potential sequence starting from a position in a direction.
        
        Returns:
            Dictionary with 'count', 'open_ends', and 'score'
        """
        count = 0
        positions = []
        
        # Count consecutive chips in direction
        row, col = start_row, start_col
        for _ in range(5):
            if not (0 <= row < board.size and 0 <= col < board.size):
                break
            
            chip = board.get_chip_at(row, col)
            if chip == player_id or chip == 3:  # Player's chip or wild
                count += 1
                positions.append((row, col))
            else:
                break
            
            row += dr
            col += dc
        
        # Calculate score based on count
        score = 0.0
        if count >= 4:
            score = SequenceEvaluator.WEIGHTS['four_in_row']
        elif count == 3:
            score = SequenceEvaluator.WEIGHTS['three_in_row']
        elif count == 2:
            score = SequenceEvaluator.WEIGHTS['two_in_row']
        
        # Bonus for open ends (can extend the sequence)
        open_ends = SequenceEvaluator._count_open_ends(
            board, start_row, start_col, dr, dc, count
        )
        if open_ends > 0:
            score *= (1 + open_ends * 0.2)  # 20% bonus per open end
        
        return {
            'count': count,
            'open_ends': open_ends,
            'score': score
        }
    
    @staticmethod
    def _count_open_ends(board: Board, start_row: int, start_col: int,
                        dr: int, dc: int, count: int) -> int:
        """Count how many ends of a sequence are open (can be extended)."""
        open_ends = 0
        
        # Check before start
        before_row = start_row - dr
        before_col = start_col - dc
        if (0 <= before_row < board.size and 0 <= before_col < board.size):
            if board.get_chip_at(before_row, before_col) == 0:
                open_ends += 1
        
        # Check after end
        after_row = start_row + dr * count
        after_col = start_col + dc * count
        if (0 <= after_row < board.size and 0 <= after_col < board.size):
            if board.get_chip_at(after_row, after_col) == 0:
                open_ends += 1
        
        return open_ends
    
    @staticmethod
    def _count_threats(board: Board, player_id: int) -> dict:
        """Count opponent threat levels (potential sequences)."""
        threats = {
            'four_in_row': 0,
            'three_in_row': 0,
            'two_in_row': 0
        }
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for row in range(board.size):
            for col in range(board.size):
                if board.get_chip_at(row, col) == player_id or board.get_chip_at(row, col) == 3:
                    for dr, dc in directions:
                        count = SequenceEvaluator._count_consecutive(
                            board, row, col, dr, dc, player_id
                        )
                        
                        if count >= 4:
                            threats['four_in_row'] += 1
                        elif count == 3:
                            threats['three_in_row'] += 1
                        elif count == 2:
                            threats['two_in_row'] += 1
        
        return threats
    
    @staticmethod
    def _count_consecutive(board: Board, start_row: int, start_col: int,
                          dr: int, dc: int, player_id: int) -> int:
        """Count consecutive chips in a direction."""
        count = 0
        row, col = start_row, start_col
        
        for _ in range(5):
            if not (0 <= row < board.size and 0 <= col < board.size):
                break
            
            chip = board.get_chip_at(row, col)
            if chip == player_id or chip == 3:
                count += 1
            else:
                break
            
            row += dr
            col += dc
        
        return count


def evaluate_state(state: GameState, player_id: int) -> float:
    """
    Convenience function to evaluate a game state.
    
    Args:
        state: Game state to evaluate
        player_id: Player ID to evaluate for
        
    Returns:
        Evaluation score
    """
    return SequenceEvaluator.evaluate_state(state, player_id)


def calculate_sequence_potential(state: GameState, player_id: int) -> int:
    """
    Calculate the potential for creating sequences.
    
    Args:
        state: Game state
        player_id: Player ID
        
    Returns:
        Potential score (number of near-sequences)
    """
    board = state.board
    potential = 0
    
    # Count 3-in-row and 4-in-row patterns
    threats = SequenceEvaluator._count_threats(board, player_id)
    potential += threats['four_in_row'] * 10
    potential += threats['three_in_row'] * 3
    
    return potential
