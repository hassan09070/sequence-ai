'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { GameAPI } from '@/lib/api';
import { DifficultyLevel } from '@/types';

export default function Home() {
  const router = useRouter();
  const [numPlayers, setNumPlayers] = useState(2);
  const [aiPlayers, setAiPlayers] = useState<Record<number, DifficultyLevel>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePlayerTypeChange = (playerId: number, isAI: boolean, difficulty: DifficultyLevel = 'medium') => {
    const newAiPlayers = { ...aiPlayers };
    if (isAI) {
      newAiPlayers[playerId] = difficulty;
    } else {
      delete newAiPlayers[playerId];
    }
    setAiPlayers(newAiPlayers);
  };

  const handleCreateGame = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await GameAPI.createGame({
        num_players: numPlayers,
        ai_config: Object.keys(aiPlayers).length > 0 ? aiPlayers : undefined,
      });

      router.push(`/game/${response.game_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create game');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-6xl font-bold text-gray-800 mb-4">🎮 Sequence</h1>
          <p className="text-xl text-gray-600">
            The classic strategy board game with AI opponents
          </p>
        </div>

        {/* Game Setup Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Create New Game</h2>

          {/* Number of Players */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Number of Players
            </label>
            <div className="flex gap-4">
              {[2, 3].map((num) => (
                <button
                  key={num}
                  onClick={() => setNumPlayers(num)}
                  className={`
                    flex-1 py-3 px-6 rounded-lg font-semibold transition-all
                    ${numPlayers === num
                      ? 'bg-blue-500 text-white shadow-lg scale-105'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }
                  `}
                >
                  {num} Players
                </button>
              ))}
            </div>
          </div>

          {/* Player Configuration */}
          <div className="space-y-4 mb-6">
            <label className="block text-sm font-semibold text-gray-700">
              Configure Players
            </label>
            
            {Array.from({ length: numPlayers }, (_, i) => i + 1).map((playerId) => (
              <div
                key={playerId}
                className="bg-gray-50 rounded-lg p-4 border-2 border-gray-200"
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="font-semibold text-gray-800">Player {playerId}</span>
                  <select
                    value={aiPlayers[playerId] ? 'ai' : 'human'}
                    onChange={(e) => {
                      const isAI = e.target.value === 'ai';
                      handlePlayerTypeChange(playerId, isAI);
                    }}
                    className="px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:outline-none"
                  >
                    <option value="human">Human</option>
                    <option value="ai">AI</option>
                  </select>
                </div>

                {aiPlayers[playerId] && (
                  <div>
                    <label className="block text-xs text-gray-600 mb-2">AI Difficulty</label>
                    <div className="grid grid-cols-4 gap-2">
                      {(['easy', 'medium', 'hard', 'expert'] as DifficultyLevel[]).map((diff) => (
                        <button
                          key={diff}
                          onClick={() => handlePlayerTypeChange(playerId, true, diff)}
                          className={`
                            py-2 px-3 rounded-lg text-sm font-semibold transition-all
                            ${aiPlayers[playerId] === diff
                              ? 'bg-purple-500 text-white'
                              : 'bg-white text-gray-700 hover:bg-purple-100'
                            }
                          `}
                        >
                          {diff.charAt(0).toUpperCase() + diff.slice(1)}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-4 bg-red-100 border-2 border-red-500 rounded-lg">
              <p className="text-red-700 text-center font-semibold">{error}</p>
            </div>
          )}

          {/* Create Game Button */}
          <button
            onClick={handleCreateGame}
            disabled={loading}
            className={`
              w-full py-4 rounded-lg font-bold text-lg transition-all
              ${loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
              }
            `}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                Creating Game...
              </span>
            ) : (
              'Start Game'
            )}
          </button>
        </div>

        {/* Features */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 shadow-lg text-center">
            <div className="text-3xl mb-2">🎯</div>
            <h3 className="font-bold text-gray-800">Strategic Gameplay</h3>
            <p className="text-sm text-gray-600">Form sequences to win</p>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-lg text-center">
            <div className="text-3xl mb-2">🤖</div>
            <h3 className="font-bold text-gray-800">Smart AI</h3>
            <p className="text-sm text-gray-600">4 difficulty levels</p>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-lg text-center">
            <div className="text-3xl mb-2">⚡</div>
            <h3 className="font-bold text-gray-800">Real-time</h3>
            <p className="text-sm text-gray-600">Instant updates</p>
          </div>
        </div>
      </div>
    </div>
  );
}
