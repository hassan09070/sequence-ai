'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { GameBoard } from '@/components/game/GameBoard';
import { PlayerHand } from '@/components/game/PlayerHand';
import { GameInfo } from '@/components/game/GameInfo';
import { GameAPI } from '@/lib/api';
import { GameState, DifficultyLevel } from '@/types';

interface GamePageProps {
  params: Promise<{
    gameId: string;
  }>;
}

export default function GamePage({ params }: GamePageProps) {
  const router = useRouter();
  const [gameId, setGameId] = useState<string>('');
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [selectedCard, setSelectedCard] = useState<string | null>(null);
  const [legalMoves, setLegalMoves] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [aiThinking, setAiThinking] = useState(false);

  // Unwrap params
  useEffect(() => {
    params.then(({ gameId: id }) => {
      setGameId(id);
    });
  }, [params]);

  // Fetch game state
  const fetchGameState = useCallback(async () => {
    if (!gameId) return;
    
    try {
      const state = await GameAPI.getGameState(gameId);
      setGameState(state);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch game state');
      console.error('Error fetching game state:', err);
    } finally {
      setLoading(false);
    }
  }, [gameId]);

  // Initial load
  useEffect(() => {
    if (gameId) {
      fetchGameState();
    }
  }, [gameId, fetchGameState]);

  // Fetch legal moves when card is selected
  useEffect(() => {
    if (!gameId || !gameState || !selectedCard) {
      setLegalMoves(new Set());
      return;
    }

    const fetchLegalMoves = async () => {
      try {
        const currentPlayer = gameState.players[gameState.current_player - 1];
        const response = await GameAPI.getLegalMoves(gameId, currentPlayer.player_id);
        
        // Filter moves for the selected card
        const movesForCard = response.moves
          .filter((move: any) => move.card === selectedCard)
          .map((move: any) => `${move.row},${move.col}`);
        
        setLegalMoves(new Set(movesForCard));
      } catch (err) {
        console.error('Error fetching legal moves:', err);
      }
    };

    fetchLegalMoves();
  }, [gameId, gameState, selectedCard]);

  // Handle AI move
  useEffect(() => {
    if (!gameState || !gameId || gameState.is_game_over || aiThinking) return;

    const currentPlayer = gameState.players[gameState.current_player - 1];
    if (currentPlayer?.is_ai) {
      setAiThinking(true);
      
      const makeAIMove = async () => {
        try {
          await new Promise(resolve => setTimeout(resolve, 1000)); // Delay for UX
          const response = await GameAPI.getAIMove(gameId, currentPlayer.player_id, 'medium');
          
          if (response.success && response.game_state) {
            setGameState(response.game_state);
          }
        } catch (err) {
          console.error('Error making AI move:', err);
        } finally {
          setAiThinking(false);
        }
      };

      makeAIMove();
    }
  }, [gameState, gameId, aiThinking]);

  // Handle cell click
  const handleCellClick = async (row: number, col: number) => {
    if (!gameId || !gameState || !selectedCard || gameState.is_game_over) return;

    const currentPlayer = gameState.players[gameState.current_player - 1];
    if (currentPlayer?.is_ai) return; // Don't allow manual moves for AI

    if (!legalMoves.has(`${row},${col}`)) {
      return; // Not a legal move
    }

    try {
      const response = await GameAPI.makeMove(gameId, selectedCard, row, col);
      
      if (response.success && response.game_state) {
        setGameState(response.game_state);
        setSelectedCard(null);
        setLegalMoves(new Set());
      } else {
        alert(response.message || 'Invalid move');
      }
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to make move');
    }
  };

  // Handle card selection
  const handleCardSelect = (card: string) => {
    if (gameState?.is_game_over) return;
    setSelectedCard(selectedCard === card ? null : card);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mx-auto mb-4"></div>
          <p className="text-xl font-semibold text-gray-700">Loading game...</p>
        </div>
      </div>
    );
  }

  if (error || !gameState) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-red-100">
        <div className="bg-white p-8 rounded-lg shadow-xl max-w-md">
          <h1 className="text-2xl font-bold text-red-600 mb-4">Error</h1>
          <p className="text-gray-700 mb-4">{error || 'Game not found'}</p>
          <button
            onClick={() => router.push('/')}
            className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const currentPlayer = gameState.players[gameState.current_player - 1];
  const isCurrentPlayerHuman = currentPlayer && !currentPlayer.is_ai;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-4xl font-bold text-gray-800">Sequence Game</h1>
          <button
            onClick={() => router.push('/')}
            className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition"
          >
            Exit Game
          </button>
        </div>

        {/* AI Thinking Indicator */}
        {aiThinking && (
          <div className="mb-4 p-4 bg-purple-100 border-2 border-purple-500 rounded-lg text-center">
            <p className="text-purple-800 font-semibold">
              🤖 AI is thinking...
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Game Board */}
          <div className="lg:col-span-3">
            <GameBoard
              board={gameState.board}
              legalMoves={legalMoves}
              onCellClick={handleCellClick}
            />

            {/* Current Player's Hand */}
            {isCurrentPlayerHuman && (
              <div className="mt-6">
                <PlayerHand
                  player={currentPlayer}
                  selectedCard={selectedCard}
                  onCardSelect={handleCardSelect}
                  disabled={gameState.is_game_over}
                />
              </div>
            )}
          </div>

          {/* Game Info Sidebar */}
          <div className="lg:col-span-1">
            <GameInfo
              players={gameState.players}
              currentPlayer={gameState.current_player}
              turnNumber={gameState.turn_number}
              isGameOver={gameState.is_game_over}
              winner={gameState.winner}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
