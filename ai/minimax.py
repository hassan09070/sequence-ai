"""
Minimax Module for Sequence Game AI

Implements Minimax algorithm with Alpha-Beta pruning for optimal move selection.
"""

from typing import Optional, Tuple
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.gamestate import GameState, Move
from .heuristics import evaluate_state


class MinimaxAI:
    """
    AI player using Minimax with Alpha-Beta pruning.
    
    Difficulty levels:
    - Easy: depth 1 (looks 1 move ahead)
    - Medium: depth 2 (looks 2 moves ahead)
    - Hard: depth 3-4 (looks 3-4 moves ahead)
    """
    
    DIFFICULTY_DEPTHS = {
        'easy': 1,
        'medium': 2,
        'hard': 3,
        'expert': 4
    }
    
    def __init__(self, player_id: int, difficulty: str = 'medium'):
        """
        Initialize the AI.
        
        Args:
            player_id: AI's player ID (1 or 2)
            difficulty: Difficulty level ('easy', 'medium', 'hard', 'expert')
        """
        self.player_id = player_id
        self.difficulty = difficulty.lower()
        self.max_depth = self.DIFFICULTY_DEPTHS.get(self.difficulty, 2)
        self.nodes_explored = 0
        self.pruning_count = 0
    
    def get_best_move(self, state: GameState) -> Optional[Move]:
        """
        Get the best move for the current state using Minimax.
        
        Args:
            state: Current game state
            
        Returns:
            Best move to make (or None if no legal moves)
        """
        self.nodes_explored = 0
        self.pruning_count = 0
        
        legal_moves = state.get_legal_moves(state.players[self.player_id - 1])
        
        if not legal_moves:
            return None
        
        # If only one move, return it
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Try each legal move
        for move in legal_moves:
            # Simulate the move
            new_state = state.clone()
            new_state.apply_move(move)
            new_state.next_turn()
            
            # Evaluate using minimax
            move_value = self._minimax(
                new_state,
                depth=self.max_depth - 1,
                alpha=alpha,
                beta=beta,
                maximizing_player=False  # Opponent's turn next
            )
            
            # Update best move
            if move_value > best_value:
                best_value = move_value
                best_move = move
            
            # Update alpha
            alpha = max(alpha, best_value)
        
        return best_move
    
    def _minimax(self, state: GameState, depth: int, alpha: float, beta: float,
                maximizing_player: bool) -> float:
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            state: Current game state
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: True if maximizing, False if minimizing
            
        Returns:
            Evaluation score for this state
        """
        self.nodes_explored += 1
        
        # Terminal conditions
        if state.is_terminal():
            winner = state.get_winner()
            if winner == self.player_id:
                return float('inf')
            else:
                return float('-inf')
        
        # Depth limit reached - evaluate state
        if depth == 0:
            return evaluate_state(state, self.player_id)
        
        current_player = state.get_current_player()
        legal_moves = state.get_legal_moves(current_player)
        
        # No legal moves - unlikely but handle it
        if not legal_moves:
            return evaluate_state(state, self.player_id)
        
        if maximizing_player:
            # Maximizing player (AI)
            max_eval = float('-inf')
            
            for move in legal_moves:
                # Simulate move
                new_state = state.clone()
                new_state.apply_move(move)
                new_state.next_turn()
                
                # Recursive minimax
                eval_score = self._minimax(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                
                # Alpha-beta pruning
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.pruning_count += 1
                    break  # Beta cut-off
            
            return max_eval
        
        else:
            # Minimizing player (opponent)
            min_eval = float('inf')
            
            for move in legal_moves:
                # Simulate move
                new_state = state.clone()
                new_state.apply_move(move)
                new_state.next_turn()
                
                # Recursive minimax
                eval_score = self._minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                
                # Alpha-beta pruning
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.pruning_count += 1
                    break  # Alpha cut-off
            
            return min_eval
    
    def get_stats(self) -> dict:
        """Get statistics about the last search."""
        return {
            'nodes_explored': self.nodes_explored,
            'pruning_count': self.pruning_count,
            'depth': self.max_depth,
            'difficulty': self.difficulty
        }


def minimax(state: GameState, depth: int, maximizing_player: bool,
           alpha: float, beta: float, player_id: int) -> float:
    """
    Standalone minimax function.
    
    Args:
        state: Game state to evaluate
        depth: Search depth
        maximizing_player: True if maximizing, False if minimizing
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        player_id: Player ID to optimize for
        
    Returns:
        Evaluation score
    """
    # Terminal state
    if state.is_terminal():
        winner = state.get_winner()
        if winner == player_id:
            return float('inf')
        else:
            return float('-inf')
    
    # Depth limit
    if depth == 0:
        return evaluate_state(state, player_id)
    
    legal_moves = state.get_legal_moves()
    
    if not legal_moves:
        return evaluate_state(state, player_id)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            new_state = state.clone()
            new_state.apply_move(move)
            new_state.next_turn()
            
            eval_score = minimax(new_state, depth - 1, False, alpha, beta, player_id)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            
            if beta <= alpha:
                break
        
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            new_state = state.clone()
            new_state.apply_move(move)
            new_state.next_turn()
            
            eval_score = minimax(new_state, depth - 1, True, alpha, beta, player_id)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            
            if beta <= alpha:
                break
        
        return min_eval


def get_best_move(state: GameState, player_id: int, difficulty: str = 'medium') -> Optional[Move]:
    """
    Convenience function to get the best move.
    
    Args:
        state: Current game state
        player_id: Player ID
        difficulty: AI difficulty level
        
    Returns:
        Best move to make
    """
    ai = MinimaxAI(player_id, difficulty)
    return ai.get_best_move(state)
