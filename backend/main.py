from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# =======================
# SIMPLE GAME LOGIC
# =======================

class NimState:
    def __init__(self, heaps, player_to_move):
        self.heaps = heaps
        self.player_to_move = player_to_move  # 1 = human, -1 = AI

def is_terminal(heaps):
    return all(h == 0 for h in heaps)

def apply_move(heaps, move):
    heap, remove = move
    new_heaps = heaps.copy()
    new_heaps[heap] -= remove
    return new_heaps

def choose_ai_move(heaps):
    # Simple AI: remove 1 from first non-empty heap
    for i, h in enumerate(heaps):
        if h > 0:
            return (i, 1)
    return (0, 0)

# =======================
# GLOBAL STATE
# =======================

game_state: Optional[NimState] = None

class Move(BaseModel):
    heap: int
    remove: int

# =======================
# LIFESPAN (INIT GAME)
# =======================

@asynccontextmanager
async def lifespan(app: FastAPI):
    global game_state
    game_state = NimState([5, 3, 7], 1)
    yield

app = FastAPI(lifespan=lifespan)

# =======================
# CORS (IMPORTANT)
# =======================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================
# ROUTES
# =======================

@app.get("/")
def home():
    return {"message": "Nim Game API running 🚀"}

# 👉 GET STATE
@app.get("/state")
def get_state():
    if game_state is None:
        raise HTTPException(404, "No game")

    return {
        "heaps": game_state.heaps,
        "player_to_move": "human" if game_state.player_to_move == 1 else "ai",
        "terminal": is_terminal(game_state.heaps)
    }

# 👉 NEW GAME
@app.post("/new_game")
def new_game():
    global game_state
    game_state = NimState([5, 3, 7], 1)
    return {"message": "New game started", "heaps": game_state.heaps}

# 👉 HUMAN MOVE
@app.post("/human_move")
def human_move(move: Move):
    global game_state

    if game_state is None or game_state.player_to_move != 1:
        raise HTTPException(400, "Not human turn")

    if move.heap < 0 or move.heap >= len(game_state.heaps):
        raise HTTPException(400, "Invalid heap")

    if move.remove < 1 or move.remove > game_state.heaps[move.heap]:
        raise HTTPException(400, "Invalid remove count")

    new_heaps = apply_move(game_state.heaps, (move.heap, move.remove))
    game_state = NimState(new_heaps, -1)

    return {
        "new_heaps": new_heaps,
        "ai_turn_next": True
    }

# 👉 AI MOVE
@app.get("/ai_move")
def ai_move():
    global game_state

    if game_state is None or game_state.player_to_move != -1:
        raise HTTPException(400, "Not AI turn")

    move = choose_ai_move(game_state.heaps)
    new_heaps = apply_move(game_state.heaps, move)
    game_state = NimState(new_heaps, 1)

    winner = "AI" if is_terminal(new_heaps) else None

    return {
        "move": {"heap": move[0], "remove": move[1]},
        "new_heaps": new_heaps,
        "winner": winner
    }

# =======================
# RUN LOCAL (OPTIONAL)
# =======================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)