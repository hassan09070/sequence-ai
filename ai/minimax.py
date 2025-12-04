"""
Minimax Module for Sequence Game AI

Implements Minimax algorithm with Alpha-Beta pruning for optimal move selection.
"""

from typing import Optional, Tuple
import matplotlib.pyplot as plt
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.gamestate import GameState, Move
from .heuristics import evaluate_state


PERFORMANCE_HISTORY = [] 

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
        self.player_id = player_id
        self.difficulty = difficulty.lower()
        self.max_depth = self.DIFFICULTY_DEPTHS.get(self.difficulty, 2)
        self.nodes_explored = 0
        self.pruning_count = 0
    
    def get_best_move(self, state: GameState) -> Optional[Move]:
        """
        Get the best move for the current state using Minimax.
        """
        self.nodes_explored = 0
        self.pruning_count = 0
        start_time = time.time()

        legal_moves = state.get_legal_moves(state.players[self.player_id - 1])
        
        if not legal_moves:
            return None
        
        # If only one move
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
            
            alpha = max(alpha, best_value)
        

        duration = time.time() - start_time
        turn_number = len(PERFORMANCE_HISTORY) + 1
        PERFORMANCE_HISTORY.append({
            'turn': turn_number,
            'nodes': self.nodes_explored,
            'pruning': self.pruning_count,
            'time': duration
        })
        print(f"AI Turn {turn_number}: {self.nodes_explored} nodes in {duration:.2f}s, nodes pruned {self.pruning_count}")
        save_game_analysis() #plots graph
        return best_move
    
    def _prioritize_tactical_moves(self, state: GameState, moves: list[Move]) -> list[Move]:
        """
        Sorts tactical moves based on immediate threat/value using a lightweight heuristic.
        """
        scored_moves = []
        
        for move in moves:
            score = 0
            r, c = move.row, move.col
            is_removal = (move.move_type == "remove")
            is_two_eyed = state.deck.is_two_eyed_jack(move.card)

            # Removal Moves (One-Eyed Jacks)
            if is_removal:
                score += 50
                if 3 <= r <= 6 and 3 <= c <= 6: # removing from center 
                    score += 20
            
            else:
                if 3 <= r <= 6 and 3 <= c <= 6: # center
                    score += 10
                
                neighbors = 0
                directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
                
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < state.board.size and 0 <= nc < state.board.size:
                        chip = state.board.get_chip_at(nr, nc)
                        # Check if neighbor is same player or 3
                        if chip == move.player_id or chip == 3: 
                            neighbors += 1
                
                score += (neighbors * 15)

                if is_two_eyed:
                    score += 40

            scored_moves.append((score, move))
            
        #sort descending
        scored_moves.sort(key=lambda x: x[0], reverse=True)
    
        return [m for s, m in scored_moves]

    
    def get_tactical_moves(self, state: GameState, player_id: int) -> list[Move]:
        """
        Generates moves for the opponent based on board threats (Paranoid Strategy).
        Instead of peeking at their hand, we assume they can play anywhere that matters.
        """
        moves = []
        board = state.board
        opponent_id = state.get_opponent_id(player_id) # The AI 

        interesting_spots = set()

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        
        has_chips = False
        
        # We limit this to spots near existing chips to save time (Local Search)
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

        for row, col in interesting_spots:
            card_at_pos = board.get_card_at(row, col)
            moves.append(Move(player_id, card_at_pos, row, col, "place"))

        # Only remove chips that are actually blocking a sequence or part of a potential one
        for row in range(board.size):
            for col in range(board.size):
                chip = board.get_chip_at(row, col)
                if chip == opponent_id and not board._is_position_in_sequence(row, col):
                    moves.append(Move(player_id, 'JS', row, col, "remove"))

        if moves: moves = self._prioritize_tactical_moves(state,moves)
        
        if len(moves)>12: moves=moves[:12]
        return moves
    
    def _minimax(self, state: GameState, depth: int, alpha: float, beta: float,
                maximizing_player: bool) -> float:
        """
        Minimax algorithm with alpha-beta pruning.
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
                
                eval_score = self._minimax(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.pruning_count += 1
                    break  
            
            return max_eval
        
        else:
            # Minimizing player (opponent)
            tactical_moves = self.get_tactical_moves(state, current_player.player_id)

            if not tactical_moves:
                return evaluate_state(state, self.player_id)
            
            min_eval = float('inf')
            for move in tactical_moves:
                # Simulate move
                new_state = state.clone()
                sim_player = new_state.players[current_player.player_id - 1]
                sim_player.add_card(move.card)
                new_state.apply_move(move)
                new_state.next_turn()
                
                # Recursive minimax
                eval_score = self._minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)

                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.pruning_count += 1
                    break  
            
            return min_eval
    
    def get_stats(self) -> dict:
        """Get statistics about the last search."""
        return {
            'nodes_explored': self.nodes_explored,
            'pruning_count': self.pruning_count,
            'depth': self.max_depth,
            'difficulty': self.difficulty
        }

def get_best_move(state: GameState, player_id: int, difficulty: str = 'medium') -> Optional[Move]:
    """
    Convenience function to get the best move.
    """
    ai = MinimaxAI(player_id, difficulty)
    move = ai.get_best_move(state)
    
    if move:
        # Create a temporary copy to test the move
        test_state = state.clone()
        test_state.apply_move(move)
        
        if test_state.is_terminal():
            print("AI is making a winning move. Saving analysis plot...")
            save_game_analysis()

    return move

def save_game_analysis():
    """
    Generates a plot of the AI's performance during the game 
    and saves it to the ai/ folder.
    """
    if not PERFORMANCE_HISTORY:
        print("No AI stats to plot.")
        return

    turns = [data['turn'] for data in PERFORMANCE_HISTORY]
    nodes = [data['nodes'] for data in PERFORMANCE_HISTORY]
    times = [data['time'] for data in PERFORMANCE_HISTORY]
    pruned = [data['pruning'] for data in PERFORMANCE_HISTORY]

    # Create the plot
    plt.figure(figsize=(10, 8))
    
    # Subplot 1: Nodes vs Pruning
    plt.subplot(2, 1, 1)
    plt.plot(turns, nodes, 'b-o', linewidth=2, label='Nodes Explored')
    plt.plot(turns, pruned, 'g--x', linewidth=2, label='Branches Pruned') # Add Pruning line
    plt.title('Search Efficiency: Explored vs Pruned')
    plt.ylabel('Count')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Subplot 2: Time Taken
    plt.subplot(2, 1, 2)
    plt.plot(turns, times, 'r-o', linewidth=2, label='Time (seconds)')
    plt.title('Execution Time per Turn')
    plt.xlabel('Turn Number')
    plt.ylabel('Seconds')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.tight_layout()
    
    # Save file
    output_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(output_dir, 'live_game_analysis.png')
    plt.savefig(filename)
    plt.close()
    
    # print(f"Live: Analysis saved to: {filename}")
    
    # Clear history for next game
    # PERFORMANCE_HISTORY.clear()