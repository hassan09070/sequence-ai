"""
Game Service - Manages game instances and state
"""
import sys
import os
import uuid
from typing import Dict, Optional, List
import json

# Add parent directory to path to import game modules
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
project_dir = os.path.dirname(backend_dir)
sys.path.insert(0, project_dir)

from game import GameState, Player
from ai import MinimaxAI


class GameManager:
    """Manages multiple game instances"""
    
    def __init__(self):
        """Initialize the game manager"""
        self.games: Dict[str, GameState] = {}
        self.ai_players: Dict[str, Dict[int, MinimaxAI]] = {}  # game_id -> {player_id -> AI}
    
    def create_game(self, num_players: int = 2, ai_config: Optional[Dict[int, str]] = None) -> tuple[str, GameState]:
        """
        Create a new game instance
        
        Args:
            num_players: Number of players (2 or 3)
            ai_config: Dictionary mapping player_id to AI difficulty
            
        Returns:
            Tuple of (game_id, GameState)
        """
        game_id = str(uuid.uuid4())
        state = GameState(num_players)
        
        # Configure players
        player_configs = []
        for i in range(1, num_players + 1):
            is_ai = ai_config and i in ai_config
            config = {
                'name': f'AI Player {i}' if is_ai else f'Player {i}',
                'is_ai': is_ai
            }
            player_configs.append(config)
        
        state.setup_game(player_configs)
        
        # Create AI instances if needed
        if ai_config:
            self.ai_players[game_id] = {}
            for player_id, difficulty in ai_config.items():
                self.ai_players[game_id][player_id] = MinimaxAI(player_id, difficulty)
        
        self.games[game_id] = state
        return game_id, state
    
    def get_game(self, game_id: str) -> Optional[GameState]:
        """Get a game by ID"""
        return self.games.get(game_id)
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a game"""
        if game_id in self.games:
            del self.games[game_id]
            if game_id in self.ai_players:
                del self.ai_players[game_id]
            return True
        return False
    
    def get_ai(self, game_id: str, player_id: int) -> Optional[MinimaxAI]:
        """Get AI player for a game"""
        if game_id in self.ai_players:
            return self.ai_players[game_id].get(player_id)
        return None
    
    def create_ai(self, game_id: str, player_id: int, difficulty: str = "medium") -> MinimaxAI:
        """Create an AI player for a game"""
        if game_id not in self.ai_players:
            self.ai_players[game_id] = {}
        
        ai = MinimaxAI(player_id, difficulty)
        self.ai_players[game_id][player_id] = ai
        return ai
    
    def game_state_to_dict(self, state: GameState) -> dict:
        """
        Convert GameState to dictionary for JSON serialization
        
        Args:
            state: GameState instance
            
        Returns:
            Dictionary representation
        """
        # Get board state
        board_data = []
        for row in range(10):
            row_data = []
            for col in range(10):
                chip_value = state.board.get_chip_at(row, col)
                cell = {
                    'card': state.board.get_card_at(row, col),
                    'chip': chip_value if chip_value != 0 else None,
                    'is_wild': (row, col) in state.board.WILD_POSITIONS
                }
                row_data.append(cell)
            board_data.append(row_data)
        
        # Get player data
        players_data = []
        for player in state.players:
            players_data.append({
                'player_id': player.player_id,
                'name': player.name,
                'hand': player.hand,
                'is_ai': player.is_ai,
                'chips_remaining': 50  # Placeholder - chips are unlimited in the game
            })
        
        # Get sequences count and positions for each player
        sequences_data = {}
        for player in state.players:
            sequences_count = state.board.check_sequence(player.player_id)
            sequence_positions = state.board.get_sequence_positions(player.player_id)
            sequences_data[str(player.player_id)] = sequence_positions
        
        return {
            'num_players': state.num_players,
            'current_player': state.current_player_idx + 1,  # Convert 0-based to 1-based
            'turn_number': len(state.move_history),
            'is_game_over': state.is_terminal(),
            'winner': state.get_winner() if state.is_terminal() else None,
            'board': board_data,
            'players': players_data,
            'sequences': sequences_data,
            'sequences_needed_to_win': state.sequences_needed_to_win
        }
    
    def list_games(self) -> List[str]:
        """Get list of all active game IDs"""
        return list(self.games.keys())


# Global game manager instance
game_manager = GameManager()
