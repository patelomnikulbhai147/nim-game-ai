from pydantic import BaseModel
from typing import List, Optional

class NimGameState(BaseModel):
    heaps: List[int]
    player_to_move: str
    difficulty: str
    terminal: bool
    winner: Optional[str] = None

class MoveRequest(BaseModel):
    heap_index: int
    remove_count: int
