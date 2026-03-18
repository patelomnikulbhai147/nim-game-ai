import { motion, AnimatePresence } from 'framer-motion';

interface WinnerModalProps {
  winner: string | null;
  onRestart: () => void;
}

export const WinnerModal = ({ winner, onRestart }: WinnerModalProps) => {
  return (
    <AnimatePresence>
      {winner && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="modal-overlay"
        >
          <motion.div 
            initial={{ scale: 0.8, y: 50 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.8, y: 50 }}
            transition={{ type: "spring", damping: 20, stiffness: 300 }}
            className="modal-content glass-panel"
          >
            <h2 className={`modal-title ${winner === 'human' ? '' : 'lost'}`}>
              {winner === 'human' ? 'You Win!' : 'AI Wins!'}
            </h2>
            <p className="subtitle" style={{ marginBottom: '2rem' }}>
              {winner === 'human' ? 'Flawless victory over the machines!' : 'Better luck next time.'}
            </p>
            <button onClick={onRestart} className="btn-primary">
              Play Again
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
