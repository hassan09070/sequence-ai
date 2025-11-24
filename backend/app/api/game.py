"""
Game API Routes
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from ..models import (
    CreateGameRequest,
    CreateGameResponse,
    MoveRequest,
    MoveResponse,
    AIRequest,
    AIResponse,
    GameStateResponse,
    LegalMovesResponse,
    ErrorResponse
)
from ..services import game_manager

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/create", response_model=CreateGameResponse, status_code=status.HTTP_201_CREATED)
async def create_game(request: CreateGameRequest):
    """
    Create a new game instance
    
    - **num_players**: Number of players (2 or 3)
    - **ai_config**: Optional AI configuration {player_id: difficulty}
    """
    try:
        game_id, state = game_manager.create_game(
            num_players=request.num_players,
            ai_config=request.ai_config
        )
        
        return CreateGameResponse(
            game_id=game_id,
            num_players=state.num_players,
            current_player=state.current_player_idx + 1,  # Convert 0-based to 1-based
            message=f"Game created successfully with {state.num_players} players"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """
    Get the current state of a game
    
    - **game_id**: Unique game identifier
    """
    state = game_manager.get_game(game_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game {game_id} not found"
        )
    
    game_data = game_manager.game_state_to_dict(state)
    
    return GameStateResponse(
        game_id=game_id,
        num_players=game_data['num_players'],
        current_player=game_data['current_player'],
        turn_number=game_data['turn_number'],
        is_game_over=game_data['is_game_over'],
        winner=game_data['winner'],
        board=game_data['board'],
        players=game_data['players'],
        sequences=game_data['sequences'],
        sequences_needed_to_win=game_data['sequences_needed_to_win']
    )


@router.post("/{game_id}/move", response_model=MoveResponse)
async def make_move(game_id: str, move: MoveRequest):
    """
    Make a move in the game
    
    - **game_id**: Unique game identifier
    - **card**: Card to play (e.g., '5H', 'JD')
    - **row**: Board row (0-9)
    - **col**: Board column (0-9)
    """
    state = game_manager.get_game(game_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game {game_id} not found"
        )
    
    if state.is_terminal():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is already over"
        )
    
    try:
        # Make the move
        success = state.make_move(card=move.card, row=move.row, col=move.col)
        
        if not success:
            return MoveResponse(
                success=False,
                message="Invalid move",
                is_game_over=False
            )
        
        # Check if game is over
        is_game_over = state.is_terminal()
        winner = state.get_winner() if is_game_over else None
        
        game_data = game_manager.game_state_to_dict(state)
        
        return MoveResponse(
            success=True,
            message="Move successful",
            game_state=game_data,
            is_game_over=is_game_over,
            winner=winner
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{game_id}/ai-move", response_model=AIResponse)
async def get_ai_move(game_id: str, request: AIRequest):
    """
    Get and execute AI move
    
    - **game_id**: Unique game identifier
    - **player_id**: Player ID for AI
    - **difficulty**: AI difficulty (easy, medium, hard, expert)
    """
    state = game_manager.get_game(game_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game {game_id} not found"
        )
    
    if state.is_terminal():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is already over"
        )
    
    try:
        # Get or create AI
        ai = game_manager.get_ai(game_id, request.player_id)
        if not ai:
            ai = game_manager.create_ai(game_id, request.player_id, request.difficulty)
        
        # Get best move
        best_move = ai.get_best_move(state)
        
        if not best_move:
            return AIResponse(
                success=False,
                message="No legal moves available",
                is_game_over=state.is_terminal()
            )
        
        # Apply the move
        state.apply_move(best_move)
        state.next_turn()
        
        # Get stats
        stats = ai.get_stats()
        
        # Check if game is over
        is_game_over = state.is_terminal()
        winner = state.get_winner() if is_game_over else None
        
        game_data = game_manager.game_state_to_dict(state)
        
        return AIResponse(
            success=True,
            message="AI move executed",
            move={
                'card': best_move.card,
                'row': best_move.row,
                'col': best_move.col,
                'is_removal': best_move.move_type == 'remove'
            },
            stats=stats,
            game_state=game_data,
            is_game_over=is_game_over,
            winner=winner
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{game_id}/legal-moves", response_model=LegalMovesResponse)
async def get_legal_moves(game_id: str, player_id: int):
    """
    Get all legal moves for a player
    
    - **game_id**: Unique game identifier
    - **player_id**: Player ID (1-based)
    """
    state = game_manager.get_game(game_id)
    
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game {game_id} not found"
        )
    
    try:
        player = state.players[player_id - 1]
        legal_moves = state.get_legal_moves(player)
        
        moves_data = [
            {
                'card': move.card,
                'row': move.row,
                'col': move.col,
                'is_removal': move.move_type == 'remove'
            }
            for move in legal_moves
        ]
        
        return LegalMovesResponse(
            player_id=player_id,
            moves=moves_data,
            count=len(moves_data)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: str):
    """
    Delete a game
    
    - **game_id**: Unique game identifier
    """
    success = game_manager.delete_game(game_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game {game_id} not found"
        )
    
    return None


@router.get("/", response_model=List[str])
async def list_games():
    """
    Get list of all active game IDs
    """
    return game_manager.list_games()
