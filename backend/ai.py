import random

def get_possible_moves(heaps):
    moves = []
    for i, count in enumerate(heaps):
        for remove in range(1, count + 1):
            moves.append((i, remove))
    return moves

def make_move(heaps, move):
    new_heaps = list(heaps)
    new_heaps[move[0]] -= move[1]
    return new_heaps

def is_terminal(heaps):
    return sum(heaps) == 0

def minimax(heaps, depth, is_maximizing, alpha, beta):
    if is_terminal(heaps):
        # The preceding player took the last stick and won
        return -1 if is_maximizing else 1
    
    if depth == 0:
        # Perfect evaluation using Nim-sum
        nim_sum = 0
        for h in heaps:
            nim_sum ^= h
        eval_score = 1 if nim_sum > 0 else -1
        return eval_score if is_maximizing else -eval_score

    moves = get_possible_moves(heaps)
    
    if is_maximizing:
        max_eval = -float('inf')
        for move in moves:
            child = make_move(heaps, move)
            eval = minimax(child, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            child = make_move(heaps, move)
            eval = minimax(child, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(heaps, difficulty):
    moves = get_possible_moves(heaps)
    if not moves:
        return None

    if difficulty == 'easy':
        return random.choice(moves)
    
    if difficulty == 'medium':
        # 40% chance of playing randomly to simulate a mistake
        if random.random() < 0.4:
            return random.choice(moves)
        depth = 3
    else: # hard
        depth = 6 # Deep enough for most standard nim games.

    best_val = -float('inf')
    best_moves = []

    for move in moves:
        child = make_move(heaps, move)
        move_val = minimax(child, depth - 1, False, -float('inf'), float('inf'))
        if move_val > best_val:
            best_val = move_val
            best_moves = [move]
        elif move_val == best_val:
            best_moves.append(move)

    if best_moves:
        return random.choice(best_moves)
    return random.choice(moves)
