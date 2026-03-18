import { Heap } from './Heap';

interface BoardProps {
  heaps: number[];
  onRemove: (heapIndex: number, count: number) => void;
  disabled: boolean;
  isAiTurn: boolean;
}

export const Board = ({ heaps, onRemove, disabled, isAiTurn }: BoardProps) => {
  return (
    <div className="board-container glass-panel">
      {heaps.map((count, idx) => (
        <Heap
          key={idx}
          heapIndex={idx}
          count={count}
          onRemove={onRemove}
          disabled={disabled}
          isAiTurn={isAiTurn}
        />
      ))}
    </div>
  );
};
