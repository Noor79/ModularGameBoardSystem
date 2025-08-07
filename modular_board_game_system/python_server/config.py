import dataclasses
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum

@dataclasses.dataclass
class BoardConfig:
    """Configuration for board layout and hardware mapping"""
    size: Tuple[int, int]  # (rows, cols)
    position_mapping: Dict[str, Tuple[int, int]]  # position -> (row, col)
    square_size: int = 150
    
    @classmethod
    def create_4x4_config(cls):
        """Create standard 4x4 board configuration"""
        positions = {}
        for row in range(4):
            for col in range(4):
                pos_name = f"{chr(97 + col)}{4 - row}"  # a1, b1, etc.
                positions[pos_name] = (row, col)
        
        return cls(
            size=(4, 4),
            position_mapping=positions,
            square_size=150
        )
    
    @classmethod
    def create_8x8_config(cls):
        """Create standard 8x8 board configuration"""
        positions = {}
        for row in range(8):
            for col in range(8):
                pos_name = f"{chr(97 + col)}{8 - row}"  # a1, b1, etc.
                positions[pos_name] = (row, col)
        
        return cls(
            size=(8, 8),
            position_mapping=positions,
            square_size=80
        )

@dataclasses.dataclass
class PieceInfo:
    """Information about a game piece"""
    uid: str
    piece_type: str
    color: str
    position: Optional[str] = None
    
class GameEvent(Enum):
    """Types of game events"""
    PIECE_PLACED = "PLACE"
    PIECE_LIFTED = "LIFT"
    PIECE_MOVED = "MOVE"

@dataclasses.dataclass
class GameEventData:
    """Data for a game event"""
    event_type: GameEvent
    piece_uid: str
    position: str
    from_position: Optional[str] = None


