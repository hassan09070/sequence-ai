"""
Pydantic models for API request/response validation
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):
    """Request to create a new game - Human vs AI only"""
    num_players: int = Field(2, ge=2, le=2, description="Number of players (always 2 for Human vs AI)")
    ai_config: Optional[Dict[int, str]] = Field(None, description="AI configuration {player_id: difficulty}")


class CreateGameResponse(BaseModel):
    """Response after creating a game"""
    game_id: str
    num_players: int
    current_player: int
    message: str


class MoveRequest(BaseModel):
    """Request to make a move"""
    card: str = Field(..., description="Card to play (e.g., '5H', 'JD')")
    row: int = Field(..., ge=0, le=9, description="Board row (0-9)")
    col: int = Field(..., ge=0, le=9, description="Board column (0-9)")


class MoveResponse(BaseModel):
    """Response after making a move"""
    success: bool
    message: str
    game_state: Optional[Dict[str, Any]] = None
    is_game_over: bool = False
    winner: Optional[int] = None


class AIRequest(BaseModel):
    """Request for AI to make a move"""
    player_id: int = Field(..., ge=1, le=2, description="Player ID for AI (always 2 for Human vs AI)")
    difficulty: str = Field("medium", description="AI difficulty: easy, medium, hard, expert")


class AIResponse(BaseModel):
    """Response with AI move"""
    success: bool
    message: str
    move: Optional[Dict[str, Any]] = None
    stats: Optional[Dict[str, Any]] = None  # Changed from Dict[str, int] to allow mixed types
    game_state: Optional[Dict[str, Any]] = None
    is_game_over: bool = False
    winner: Optional[int] = None


class GameStateResponse(BaseModel):
    """Full game state response"""
    game_id: str
    num_players: int
    current_player: int
    turn_number: int
    is_game_over: bool
    winner: Optional[int]
    board: List[List[Dict[str, Any]]]
    players: List[Dict[str, Any]]
    sequences: Dict[str, List[List[List[int]]]]  # player_id -> list of sequences (each sequence is list of [row, col] pairs)
    sequences_needed_to_win: int


class LegalMovesResponse(BaseModel):
    """Legal moves for a player"""
    player_id: int
    moves: List[Dict[str, Any]]
    count: int


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
