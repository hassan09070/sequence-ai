// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_V1_PREFIX = '/api/v1';

export const API = {
  BASE_URL: API_BASE_URL,
  GAME: {
    CREATE: `${API_BASE_URL}${API_V1_PREFIX}/game/create`,
    GET_STATE: (gameId: string) => `${API_BASE_URL}${API_V1_PREFIX}/game/${gameId}`,
    MAKE_MOVE: (gameId: string) => `${API_BASE_URL}${API_V1_PREFIX}/game/${gameId}/move`,
    AI_MOVE: (gameId: string) => `${API_BASE_URL}${API_V1_PREFIX}/game/${gameId}/ai-move`,
    LEGAL_MOVES: (gameId: string, playerId: number) => 
      `${API_BASE_URL}${API_V1_PREFIX}/game/${gameId}/legal-moves?player_id=${playerId}`,
    DELETE: (gameId: string) => `${API_BASE_URL}${API_V1_PREFIX}/game/${gameId}`,
    LIST: `${API_BASE_URL}${API_V1_PREFIX}/game/`,
  },
};
