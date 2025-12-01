import { API } from './config';
import type {
  CreateGameRequest,
  CreateGameResponse,
  GameState,
  MoveResponse,
  AIResponse,
  DifficultyLevel,
} from '@/types';

export class GameAPI {
  private static async request<T>(
    url: string,
    options?: RequestInit
  ): Promise<T> {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        throw new Error('Cannot connect to game server. Please ensure the backend is running on http://localhost:8000');
      }
      throw error;
    }
  }

  static async createGame(request: CreateGameRequest): Promise<CreateGameResponse> {
    return this.request<CreateGameResponse>(API.GAME.CREATE, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  static async getGameState(gameId: string): Promise<GameState> {
    return this.request<GameState>(API.GAME.GET_STATE(gameId));
  }

  static async makeMove(
    gameId: string,
    card: string,
    row: number,
    col: number
  ): Promise<MoveResponse> {
    return this.request<MoveResponse>(API.GAME.MAKE_MOVE(gameId), {
      method: 'POST',
      body: JSON.stringify({ card, row, col }),
    });
  }

  static async getAIMove(
    gameId: string,
    playerId: number,
    difficulty: DifficultyLevel = 'medium'
  ): Promise<AIResponse> {
    return this.request<AIResponse>(API.GAME.AI_MOVE(gameId), {
      method: 'POST',
      body: JSON.stringify({ player_id: playerId, difficulty }),
    });
  }

  static async getLegalMoves(gameId: string, playerId: number): Promise<any> {
    return this.request(API.GAME.LEGAL_MOVES(gameId, playerId));
  }

  static async deleteGame(gameId: string): Promise<void> {
    await this.request(API.GAME.DELETE(gameId), {
      method: 'DELETE',
    });
  }

  static async listGames(): Promise<string[]> {
    return this.request<string[]>(API.GAME.LIST);
  }
}
