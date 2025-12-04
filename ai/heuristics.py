"""
Heuristics Module for Sequence Game AI
"""

from typing import List, Tuple, Set, Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.gamestate import GameState
from game.board import Board


class SequenceEvaluator:
    """
    Evaluates board positions for the AI player.
    """
    
    # UPDATED WEIGHTS
    WEIGHTS = {
        'complete_sequence': 10000,      # Win condition
        'four_in_row': 600,              
        'three_in_row': 150,             
        'two_in_row': 20,                
        'open_ended': 2.0,               
        'center_control': 15,            
        'corner_control': 5,
        'blocking_opponent': 900,       
        'card_playability': 5,           
        'wild_card_value': 50,
    }
    
    @staticmethod
    def evaluate_state(state: GameState, player_id: int) -> float:
        """Evaluate the game state from a player's perspective."""
        # Check terminal states
        if state.is_terminal():
            winner = state.get_winner()
            if winner == player_id:
                return float('inf')
            elif winner is not None:
                return float('-inf')
            return 0.0
        
        opponent_id = state.get_opponent_id(player_id)
        
        # Calculate component scores
        offensive_score = SequenceEvaluator._evaluate_offensive(state, player_id)
        defensive_score = SequenceEvaluator._evaluate_defensive(state, player_id, opponent_id)
        board_control_score = SequenceEvaluator._evaluate_board_control(state, player_id)
        card_utility_score = SequenceEvaluator._evaluate_card_utility(state, player_id)
        
        return offensive_score + defensive_score + board_control_score + card_utility_score
    
    @staticmethod
    def _evaluate_offensive(state: GameState, player_id: int) -> float:
        """Evaluate offensive potential (creating sequences)."""
        score = 0.0
        board = state.board
        
        complete_sequences = board.check_sequence(player_id)
        score += complete_sequences * SequenceEvaluator.WEIGHTS['complete_sequence']
        
        # Evaluate partial sequences
        score += SequenceEvaluator._evaluate_partial_sequences(board, player_id)
        return score

    @staticmethod
    def _evaluate_defensive(state: GameState, player_id: int, opponent_id: int) -> float:
        """Evaluate defensive position (blocking opponent)."""
        score = 0.0
        board = state.board
        
        threats = SequenceEvaluator._count_threats(board, opponent_id)
        score -= threats['four_in_row'] * SequenceEvaluator.WEIGHTS['blocking_opponent']
        score -= threats['three_in_row'] * (SequenceEvaluator.WEIGHTS['three_in_row'] * 1.5)
        
        return score

    @staticmethod
    def _evaluate_partial_sequences(board: Board, player_id: int) -> float:
        """
        Evaluate partial sequences (2, 3, 4 in a row).
        """
        score = 0.0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for row in range(board.size):
            for col in range(board.size):
                chip = board.get_chip_at(row, col)
                
                # Check if this chip belongs to us (or is wild)
                if chip == player_id or chip == 3:
                    for dr, dc in directions:
                        prev_r, prev_c = row - dr, col - dc
                        if 0 <= prev_r < board.size and 0 <= prev_c < board.size:
                            prev_chip = board.get_chip_at(prev_r, prev_c)
                            if prev_chip == player_id or prev_chip == 3:
                                continue

                        seq_score = SequenceEvaluator._analyze_line(board, row, col, dr, dc, player_id)
                        score += seq_score
        return score

    @staticmethod
    def _analyze_line(board: Board, r: int, c: int, dr: int, dc: int, player_id: int) -> float:
        """Helper to count length of sequence starting at r,c in direction dr,dc."""
        length = 0
        open_ends = 0
        
        # Check start openness (backward)
        prev_r, prev_c = r - dr, c - dc
        if 0 <= prev_r < board.size and 0 <= prev_c < board.size:
            if not board.is_position_occupied(prev_r, prev_c):
                open_ends += 1

        # Walk forward
        curr_r, curr_c = r, c
        while 0 <= curr_r < board.size and 0 <= curr_c < board.size:
            chip = board.get_chip_at(curr_r, curr_c)
            if chip == player_id or chip == 3:
                length += 1
                curr_r += dr
                curr_c += dc
            else:
                break
        
        # Check end openness (forward)
        if 0 <= curr_r < board.size and 0 <= curr_c < board.size:
            if not board.is_position_occupied(curr_r, curr_c):
                open_ends += 1
        
        # Calculate Score
        if length >= 5:
            return SequenceEvaluator.WEIGHTS['complete_sequence']
        elif length == 4:
            base = SequenceEvaluator.WEIGHTS['four_in_row']
            return base * (SequenceEvaluator.WEIGHTS['open_ended'] if open_ends > 0 else 1.0)
        elif length == 3:
            base = SequenceEvaluator.WEIGHTS['three_in_row']
            return base * (SequenceEvaluator.WEIGHTS['open_ended'] if open_ends > 0 else 1.0)
        elif length == 2:
            return SequenceEvaluator.WEIGHTS['two_in_row']
            
        return 0.0

    @staticmethod
    def _count_threats(board: Board, player_id: int) -> Dict[str, int]:
        """Counts how many 3s and 4s the player has."""
        counts = {'four_in_row': 0, 'three_in_row': 0}
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for row in range(board.size):
            for col in range(board.size):
                chip = board.get_chip_at(row, col)
                if chip == player_id or chip == 3:
                    for dr, dc in directions:
                        prev_r, prev_c = row - dr, col - dc
                        if 0 <= prev_r < board.size and 0 <= prev_c < board.size:
                            prev_chip = board.get_chip_at(prev_r, prev_c)
                            if prev_chip == player_id or prev_chip == 3:
                                continue

                        # Count length
                        length = 0
                        curr_r, curr_c = row, col
                        while 0 <= curr_r < board.size and 0 <= curr_c < board.size:
                            c_val = board.get_chip_at(curr_r, curr_c)
                            if c_val == player_id or c_val == 3:
                                length += 1
                                curr_r += dr
                                curr_c += dc
                            else:
                                break
                        
                        if length == 4: counts['four_in_row'] += 1
                        elif length == 3: counts['three_in_row'] += 1
        return counts

    @staticmethod
    def _evaluate_board_control(state: GameState, player_id: int) -> float:
        """Evaluate control of strategic positions (center)."""
        score = 0.0
        board = state.board
        
        # Center 4x4 area
        for r in range(3, 7):
            for c in range(3, 7):
                chip = board.get_chip_at(r, c)
                if chip == player_id:
                    score += SequenceEvaluator.WEIGHTS['center_control']
        return score

    @staticmethod
    def _evaluate_card_utility(state: GameState, player_id: int) -> float:
        """Evaluate value of cards in hand."""
        score = 0.0
        player = state.players[player_id - 1]
        
        if not player.hand or len(player.hand) < 2:
            return 0.0
            
        for card in player.hand:
            if state.deck.is_two_eyed_jack(card):
                score += SequenceEvaluator.WEIGHTS['wild_card_value']
            elif state.deck.is_one_eyed_jack(card):
                score += SequenceEvaluator.WEIGHTS['wild_card_value'] * 0.8
            else:
                score += SequenceEvaluator.WEIGHTS['card_playability']
        return score



def evaluate_state(state: GameState, player_id: int) -> float:
    return SequenceEvaluator.evaluate_state(state, player_id)

def calculate_sequence_potential(state: GameState, player_id: int) -> int:
    board = state.board
    threats = SequenceEvaluator._count_threats(board, player_id)
    return (threats['four_in_row'] * 10) + (threats['three_in_row'] * 3)
