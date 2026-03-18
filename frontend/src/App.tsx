import { useState, useEffect } from 'react';
import { api } from './api';
import type { GameState } from './types';
import { Board } from './components/Board';
import { Controls } from './components/Controls';
import { WinnerModal } from './components/WinnerModal';
import './App.css'; // Optional if anything was here, else it uses index.css globally

function App() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [difficulty, setDifficulty] = useState('medium');
  const [isAiThinking, setIsAiThinking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startNewGame = async () => {
    try {
      const res = await api.newGame(difficulty);
      setSessionId(res.session_id);
      setGameState(res.state);
      setIsAiThinking(false);
      setError(null);
    } catch (err) {
      setError("Failed to start new game.");
    }
  };

  useEffect(() => {
    startNewGame();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleRemove = async (heapIndex: number, count: number) => {
    if (!sessionId || !gameState || gameState.terminal || gameState.player_to_move !== 'human' || isAiThinking) return;

    try {
      // Optimistic update
      const newState = { ...gameState };
      newState.heaps = [...newState.heaps];
      newState.heaps[heapIndex] -= count;
      setGameState(newState);

      const backendState = await api.humanMove(sessionId, heapIndex, count);
      setGameState(backendState);

      if (!backendState.terminal && backendState.player_to_move === 'ai') {
        triggerAiMove(sessionId);
      }
    } catch (err) {
      setError("Invalid move.");
    }
  };

  const triggerAiMove = async (sid: string) => {
    setIsAiThinking(true);
    // Add artificial delay for "thinking" effect to make animations nicer
    setTimeout(async () => {
      try {
        const backendState = await api.aiMove(sid);
        setGameState(backendState);
      } catch (err) {
        setError("AI failed to move.");
      } finally {
        setIsAiThinking(false);
      }
    }, 800);
  };

  if (!gameState) return <div className="app-container"><div className="loader" /></div>;

  return (
    <div className="app-container">
      <div className="header">
        <h1 className="title">Neon Nim</h1>
        <p className="subtitle">Outsmart the AI in the ancient game of Nim.</p>
        {error && <p style={{color: 'var(--secondary)', marginTop: '0.5rem'}}>{error}</p>}
      </div>

      <div className="game-layout">
        <Controls 
          difficulty={difficulty}
          onDifficultyChange={setDifficulty}
          onNewGame={startNewGame}
          disabled={isAiThinking}
        />

        <div className={`turn-indicator ${gameState.player_to_move === 'human' ? 'turn-human' : 'turn-ai'}`}>
          {gameState.terminal ? 'Game Over' : (
            gameState.player_to_move === 'human' ? "Your Turn" : (
              <span>AI is thinking<span className="loader"></span></span>
            )
          )}
        </div>

        <Board 
          heaps={gameState.heaps} 
          onRemove={handleRemove} 
          disabled={isAiThinking || gameState.terminal}
          isAiTurn={gameState.player_to_move === 'ai'}
        />
      </div>

      <WinnerModal winner={gameState.winner} onRestart={startNewGame} />
    </div>
  );
}

export default App;
