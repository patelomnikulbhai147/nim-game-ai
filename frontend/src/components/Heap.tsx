import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { Stick } from './Stick';

interface HeapProps {
  count: number;
  heapIndex: number;
  onRemove: (heapIndex: number, count: number) => void;
  disabled: boolean;
  isAiTurn: boolean;
}

export const Heap = ({ count, heapIndex, onRemove, disabled, isAiTurn }: HeapProps) => {
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);

  const handleStickClick = (index: number) => {
    if (disabled || isAiTurn) return;
    const removeCount = count - index;
    onRemove(heapIndex, removeCount);
    setHoverIndex(null);
  };

  const sticks = Array.from({ length: count }, (_, i) => i);

  return (
    <div className="heap-row">
      <div className="heap-label">Heap {heapIndex + 1}</div>
      <div className="stick-container">
        <AnimatePresence mode="popLayout">
          {sticks.map((id) => {
            const isHovered = hoverIndex !== null && id >= hoverIndex && !disabled && !isAiTurn;
            return (
              <Stick
                key={id}
                id={id}
                isHovered={isHovered}
                onHoverStart={() => setHoverIndex(id)}
                onHoverEnd={() => setHoverIndex(null)}
                onClick={() => handleStickClick(id)}
              />
            );
          })}
        </AnimatePresence>
      </div>
    </div>
  );
};
