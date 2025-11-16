"""
Sequence Game - AI Module
"""

from .heuristics import evaluate_state, calculate_sequence_potential
from .minimax import minimax, get_best_move, MinimaxAI

__all__ = ['evaluate_state', 'calculate_sequence_potential', 'minimax', 'get_best_move', 'MinimaxAI']
