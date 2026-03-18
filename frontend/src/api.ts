import axios from 'axios';
import type { GameState } from './types';

const API_BASE = "https://nim-game-backend.onrender.com";

export const api = {
  newGame: async (difficulty: string) => {
    const res = await axios.post(`${API_URL}/new_game`, { difficulty });
    return res.data as { session_id: string; state: GameState };
  },
  getState: async (sessionId: string) => {
    const res = await axios.get(`${API_URL}/state/${sessionId}`);
    return res.data as GameState;
  },
  humanMove: async (sessionId: string, heapIndex: number, removeCount: number) => {
    const res = await axios.post(`${API_URL}/human_move/${sessionId}`, { heap_index: heapIndex, remove_count: removeCount });
    return res.data.state as GameState;
  },
  aiMove: async (sessionId: string) => {
    const res = await axios.post(`${API_URL}/ai_move/${sessionId}`);
    return res.data.state as GameState;
  }
};
