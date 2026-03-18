import { motion } from 'framer-motion';

interface StickProps {
  id: number;
  isHovered: boolean;
  onHoverStart: () => void;
  onHoverEnd: () => void;
  onClick: () => void;
  isAiTaking?: boolean;
}

export const Stick = ({ isHovered, onHoverStart, onHoverEnd, onClick, isAiTaking }: StickProps) => {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.5, y: -50 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0, y: 50 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
      className={`stick ${isHovered ? 'hover-active' : ''} ${isAiTaking ? 'stick-ai-taking' : ''}`}
      onMouseEnter={onHoverStart}
      onMouseLeave={onHoverEnd}
      onClick={onClick}
    />
  );
};
