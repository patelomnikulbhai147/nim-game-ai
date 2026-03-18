export interface GameState {
  heaps: number[];
  player_to_move: string;
  difficulty: string;
  terminal: boolean;
  winner: string | null;
}
