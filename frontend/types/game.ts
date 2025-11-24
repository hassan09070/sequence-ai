// Game types
export interface Cell {
  card: string;
  chip: number | null;
  is_wild: boolean;
}

export interface Player {
  player_id: number;
  name: string;
  hand: string[];
  is_ai: boolean;
  chips_remaining: number;
}

export interface GameState {
  game_id: string;
  num_players: number;
  current_player: number;
  turn_number: number;
  is_game_over: boolean;
  winner: number | null;
  board: Cell[][];
  players: Player[];
  sequences: Record<number, [number, number][][]>;  // player_id -> array of sequences, each sequence is array of [row, col] pairs
}

export interface Move {
  card: string;
  row: number;
  col: number;
  is_removal?: boolean;
}

export interface CreateGameRequest {
  num_players: number;
  ai_config?: Record<number, string>;
}

export interface CreateGameResponse {
  game_id: string;
  num_players: number;
  current_player: number;
  message: string;
}

export interface MoveResponse {
  success: boolean;
  message: string;
  game_state?: any;
  is_game_over: boolean;
  winner: number | null;
}

export interface AIResponse {
  success: boolean;
  message: string;
  move?: Move;
  stats?: {
    nodes_explored: number;
    pruning_count: number;
  };
  game_state?: any;
  is_game_over: boolean;
  winner: number | null;
}

export type DifficultyLevel = 'easy' | 'medium' | 'hard' | 'expert';

export interface WebSocketMessage {
  type: 'connected' | 'move' | 'state_update' | 'player_joined' | 'player_disconnected';
  game_id?: string;
  message?: string;
  data?: any;
  connections?: number;
}
