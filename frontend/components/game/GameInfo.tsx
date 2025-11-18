'use client';

import { Player } from '@/types';

interface GameInfoProps {
  players: Player[];
  currentPlayer: number;
  turnNumber: number;
  isGameOver: boolean;
  winner: number | null;
}

const getPlayerColor = (playerId: number): string => {
  switch (playerId) {
    case 1: return 'bg-blue-500';
    case 2: return 'bg-green-500';
    case 3: return 'bg-yellow-500';
    default: return 'bg-gray-500';
  }
};

export function GameInfo({ players, currentPlayer, turnNumber, isGameOver, winner }: GameInfoProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Game Info</h2>
      
      {/* Turn info */}
      <div className="mb-4">
        <p className="text-sm text-gray-600">Turn: {turnNumber}</p>
        {!isGameOver && (
          <p className="text-lg font-semibold text-gray-800">
            Current: <span className="text-blue-600">{players[currentPlayer - 1]?.name}</span>
          </p>
        )}
      </div>

      {/* Game over message */}
      {isGameOver && winner && (
        <div className="mb-4 p-4 bg-yellow-100 border-2 border-yellow-500 rounded-lg">
          <p className="text-xl font-bold text-center text-yellow-800">
            🏆 {players[winner - 1]?.name} Wins! 🏆
          </p>
        </div>
      )}

      {/* Players list */}
      <div className="space-y-2">
        <h3 className="font-semibold text-gray-700 mb-2">Players:</h3>
        {players.map((player) => (
          <div
            key={player.player_id}
            className={`
              p-3 rounded-lg border-2
              ${currentPlayer === player.player_id && !isGameOver ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}
            `}
          >
            <div className="flex items-center gap-2">
              <div className={`w-4 h-4 rounded-full ${getPlayerColor(player.player_id)}`} />
              <div className="flex-1">
                <p className="font-semibold text-gray-800">
                  {player.name}
                  {player.is_ai && <span className="ml-2 text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">AI</span>}
                </p>
                <p className="text-xs text-gray-600">
                  {player.chips_remaining} chips | {player.hand.length} cards
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
