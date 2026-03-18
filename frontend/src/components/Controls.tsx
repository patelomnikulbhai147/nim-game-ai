interface ControlsProps {
  difficulty: string;
  onDifficultyChange: (d: string) => void;
  onNewGame: () => void;
  disabled: boolean;
}

export const Controls = ({ difficulty, onDifficultyChange, onNewGame, disabled }: ControlsProps) => {
  return (
    <div className="controls-bar glass-panel">
      <select 
        value={difficulty} 
        onChange={(e) => onDifficultyChange(e.target.value)}
        disabled={disabled}
        className="select-styled"
      >
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </select>
      <button 
        onClick={onNewGame} 
        disabled={disabled}
        className={`btn-primary ${disabled ? 'btn-disabled' : ''}`}
      >
        New Game
      </button>
    </div>
  );
};
