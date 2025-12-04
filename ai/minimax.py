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
    
    def get_tactical_moves(self, state: GameState, player_id: int) -> list[Move]:
        """
        Generates moves for the opponent based on board threats (Paranoid Strategy).
        Instead of peeking at their hand, we assume they can play anywhere that matters.
        """
        moves = []
        board = state.board
        opponent_id = state.get_opponent_id(player_id) # The AI (us)

        interesting_spots = set()

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        
        has_chips = False
        # 1. Check all empty spots for PLACEMENT (Offense & Defense)
        # We limit this to spots near existing chips to save time (Local Search)
        # or spots that are critical.
        for row in range(board.size):
            for col in range(board.size):
                if board.is_position_occupied(row, col):
                    has_chips = True
                    for dr, dc in directions:
                        new_r, new_c = row+dr, col + dc
                        if 0<=new_r<board.size and 0<=new_c<board.size:
                            if not board.is_position_occupied(new_r, new_c):
                                interesting_spots.add((new_r, new_c))


        # If board is empty (first move), just look at center and corners
        if not has_chips:
            interesting_spots.update([(4,4), (4,5), (5,4), (5,5), (0,0), (0,9), (9,0), (9,9)])

        # 2. Generate Place Moves for Hot Spots Only
        for row, col in interesting_spots:
            card_at_pos = board.get_card_at(row, col)
            moves.append(Move(player_id, card_at_pos, row, col, "place"))
        
        # 3. Add Removal Moves (Limit these too!)
        # Only remove chips that are actually blocking a sequence or part of a potential one
        for row in range(board.size):
            for col in range(board.size):
                chip = board.get_chip_at(row, col)
                if chip == opponent_id and not board._is_position_in_sequence(row, col):
                    moves.append(Move(player_id, 'JS', row, col, "remove"))

        return moves
    
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
    
        
        if maximizing_player:
            # Maximizing player (AI)
            
            legal_moves = state.get_legal_moves(current_player)

            if not legal_moves:
               return evaluate_state(state, self.player_id)
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
            tactical_moves = self.get_tactical_moves(state, current_player.player_id)

            # if len(tactical_moves)>15:
            #    tactical_moves = tactical_moves[:15]

            if not tactical_moves:
                return evaluate_state(state, self.player_id)
            min_eval = float('inf')
            for move in tactical_moves:
                # Simulate move
                new_state = state.clone()
                sim_player = new_state.players[current_player.player_id - 1]
                sim_player.add_card(move.card)
                
                # Now apply the move (it will work because we added the card)
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
