from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from typing import Dict, List

from game import NimGameState, MoveRequest
from ai import get_best_move, is_terminal, make_move

app = FastAPI(title="Nim Game VS AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage
sessions: Dict[str, NimGameState] = {}

class NewGameRequest(BaseModel):
    difficulty: str = 'medium'
    initial_heaps: List[int] = [3, 4, 5]

@app.post("/new_game")
def create_new_game(req: NewGameRequest):
    session_id = str(uuid.uuid4())
    state = NimGameState(
        heaps=req.initial_heaps,
        player_to_move="human",
        difficulty=req.difficulty,
        terminal=False,
        winner=None
    )
    sessions[session_id] = state
    return {"session_id": session_id, "state": state}

@app.get("/state/{session_id}")
def get_state(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

@app.post("/human_move/{session_id}")
def human_move(session_id: str, move: MoveRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = sessions[session_id]
    
    if state.terminal:
        raise HTTPException(status_code=400, detail="Game already over")
    
    if state.player_to_move != "human":
        raise HTTPException(status_code=400, detail="Not human's turn")
        
    heap_idx = move.heap_index
    if heap_idx < 0 or heap_idx >= len(state.heaps):
        raise HTTPException(status_code=400, detail="Invalid heap")
        
    if move.remove_count < 1 or move.remove_count > state.heaps[heap_idx]:
        raise HTTPException(status_code=400, detail="Invalid remove count")
        
    # Apply move
    state.heaps = make_move(state.heaps, (heap_idx, move.remove_count))
    
    if is_terminal(state.heaps):
        state.terminal = True
        state.winner = "human"
    else:
        state.player_to_move = "ai"
        
    return {"status": "success", "state": state}

@app.post("/ai_move/{session_id}")
def ai_move(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    state = sessions[session_id]
    
    if state.terminal:
        raise HTTPException(status_code=400, detail="Game already over")
        
    if state.player_to_move != "ai":
        raise HTTPException(status_code=400, detail="Not AI's turn")
        
    best_move = get_best_move(state.heaps, state.difficulty)
    if best_move is None:
        raise HTTPException(status_code=500, detail="No valid moves for AI")
        
    state.heaps = make_move(state.heaps, best_move)
    
    if is_terminal(state.heaps):
        state.terminal = True
        state.winner = "ai"
    else:
        state.player_to_move = "human"
        
    return {
        "move": {"heap_index": best_move[0], "remove_count": best_move[1]},
        "state": state
    }
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
