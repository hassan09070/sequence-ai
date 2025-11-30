'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { GameAPI } from '@/lib/api';
import { DifficultyLevel } from '@/types';

export default function Home() {
  const router = useRouter();
  const [aiDifficulty, setAiDifficulty] = useState<DifficultyLevel>('medium');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreateGame = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await GameAPI.createGame({
        num_players: 2,
        ai_config: { 2: aiDifficulty },
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
            Human vs AI - The classic strategy board game
          </p>
        </div>

        {/* Game Setup Card */}
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Start New Game</h2>

          {/* Game Mode Info */}
          <div className="mb-6 p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
            <div className="flex items-center gap-3">
              <span className="text-2xl">👤</span>
              <div>
                <p className="font-semibold text-gray-800">You (Player 1)</p>
                <p className="text-sm text-gray-600">Human - You play first</p>
              </div>
            </div>
            <div className="my-3 border-t border-blue-200"></div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">🤖</span>
              <div>
                <p className="font-semibold text-gray-800">AI (Player 2)</p>
                <p className="text-sm text-gray-600">Computer opponent</p>
              </div>
            </div>
          </div>

          {/* AI Difficulty Selection */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Select AI Difficulty
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {(['easy', 'medium', 'hard', 'expert'] as DifficultyLevel[]).map((diff) => (
                <button
                  key={diff}
                  onClick={() => setAiDifficulty(diff)}
                  className={`
                    py-3 px-4 rounded-lg text-sm font-semibold transition-all
                    ${aiDifficulty === diff
                      ? 'bg-purple-500 text-white shadow-lg scale-105'
                      : 'bg-gray-100 text-gray-700 hover:bg-purple-100'
                    }
                  `}
                >
                  {diff === 'easy' && '😊 '}
                  {diff === 'medium' && '🎯 '}
                  {diff === 'hard' && '💪 '}
                  {diff === 'expert' && '🧠 '}
                  {diff.charAt(0).toUpperCase() + diff.slice(1)}
                </button>
              ))}
            </div>
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
                Starting Game...
              </span>
            ) : (
              'Play vs AI'
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
            <div className="text-3xl mb-2">👤</div>
            <h3 className="font-bold text-gray-800">Single Player</h3>
            <p className="text-sm text-gray-600">Human vs AI mode</p>
          </div>
        </div>
      </div>
    </div>
  );
}
