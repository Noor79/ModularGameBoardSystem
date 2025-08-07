import abc
from typing import Dict, List, Any
from config import BoardConfig, PieceInfo, GameEvent, GameEventData

class GameLogic(abc.ABC):
    """Abstract base class for game logic implementations"""
    
    def __init__(self, board_config: BoardConfig):
        self.board_config = board_config
        self.pieces: Dict[str, PieceInfo] = {}
        self.board_state: Dict[str, Optional[PieceInfo]] = {}
        
        # Initialize empty board
        for position in board_config.position_mapping.keys():
            self.board_state[position] = None
    
    @abc.abstractmethod
    def get_game_name(self) -> str:
        """Return the name of this game"""
        pass
    
    @abc.abstractmethod
    def initialize_pieces(self) -> Dict[str, PieceInfo]:
        """Initialize pieces for this game. Return dict of uid -> PieceInfo"""
        pass
    
    @abc.abstractmethod
    def is_valid_move(self, piece: PieceInfo, from_pos: str, to_pos: str) -> bool:
        """Check if a move is valid according to game rules"""
        pass
    
    @abc.abstractmethod
    def get_possible_moves(self, piece: PieceInfo) -> List[str]:
        """Get all possible moves for a piece"""
        pass
    
    def handle_event(self, event: GameEventData) -> Dict[str, Any]:
        """
        Handle a game event and return response data
        Returns dict with keys: 'valid', 'message', 'highlights', etc.
        """
        if event.event_type == GameEvent.PIECE_PLACED:
            return self._handle_piece_placed(event)
        elif event.event_type == GameEvent.PIECE_LIFTED:
            return self._handle_piece_lifted(event)
        elif event.event_type == GameEvent.PIECE_MOVED:
            return self._handle_piece_moved(event)
        
        return {'valid': False, 'message': 'Unknown event type'}
    
    def _handle_piece_placed(self, event: GameEventData) -> Dict[str, Any]:
        """Handle piece placement"""
        piece = self.pieces.get(event.piece_uid)
        if not piece:
            # New piece - register it
            piece = PieceInfo(
                uid=event.piece_uid,
                piece_type="unknown",
                color="unknown",
                position=event.position
            )
            self.pieces[event.piece_uid] = piece
        
        # Update board state
        piece.position = event.position
        self.board_state[event.position] = piece
        
        # Get possible moves for highlighting
        possible_moves = self.get_possible_moves(piece)
        
        return {
            'valid': True,
            'message': f'{piece.color} {piece.piece_type} placed on {event.position}',
            'highlights': {
                'selected': [event.position],
                'possible_moves': possible_moves
            }
        }
    
    def _handle_piece_lifted(self, event: GameEventData) -> Dict[str, Any]:
        """Handle piece lift"""
        piece = self.pieces.get(event.piece_uid)
        if not piece:
            return {'valid': False, 'message': 'Unknown piece lifted'}
        
        # Clear board position
        if piece.position:
            self.board_state[piece.position] = None
        piece.position = None
        
        return {
            'valid': True,
            'message': f'{piece.color} {piece.piece_type} lifted from {event.position}',
            'highlights': {'clear': True}
        }
    
    def _handle_piece_moved(self, event: GameEventData) -> Dict[str, Any]:
        """Handle piece movement"""
        piece = self.pieces.get(event.piece_uid)
        if not piece:
            return {'valid': False, 'message': 'Unknown piece moved'}
        
        # Validate move
        if not self.is_valid_move(piece, event.from_position, event.position):
            return {
                'valid': False,
                'message': f'Invalid move: {event.from_position} to {event.position}',
                'highlights': {'invalid': [event.position]}
            }
        
        # Execute move
        if event.from_position:
            self.board_state[event.from_position] = None
        
        # Check for capture
        captured_piece = self.board_state.get(event.position)
        capture_message = ""
        if captured_piece:
            capture_message = f" (captured {captured_piece.color} {captured_piece.piece_type})"
            # Remove captured piece
            if captured_piece.uid in self.pieces:
                del self.pieces[captured_piece.uid]
        
        # Place piece
        piece.position = event.position
        self.board_state[event.position] = piece
        
        return {
            'valid': True,
            'message': f'{piece.color} {piece.piece_type} moved to {event.position}{capture_message}',
            'highlights': {'clear': True}
        }


