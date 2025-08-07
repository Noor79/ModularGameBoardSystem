from typing import Dict, List, Optional
from config import PieceInfo
from game_logic.base import GameLogic

class CheckersLogic(GameLogic):
    """Checkers game logic implementation"""
    
    def get_game_name(self) -> str:
        return "Checkers"
    
    def initialize_pieces(self) -> Dict[str, PieceInfo]:
        """Initialize checkers pieces"""
        # Example configuration for checkers
        piece_configs = [
            {"uid": "C5B7BD01", "type": "piece", "color": "Red"},
            {"uid": "F3C7B501", "type": "piece", "color": "Red"},
            {"uid": "9B850802", "type": "piece", "color": "Red"},
            {"uid": "7A74B701", "type": "piece", "color": "Red"},
            {"uid": "AB980802", "type": "piece", "color": "Black"},
            {"uid": "5BCA0E02", "type": "piece", "color": "Black"},
            {"uid": "1BFD0802", "type": "piece", "color": "Black"},
            {"uid": "CE890E02", "type": "piece", "color": "Black"},
        ]
        
        pieces = {}
        for config in piece_configs:
            piece = PieceInfo(
                uid=config["uid"],
                piece_type=config["type"],
                color=config["color"]
            )
            pieces[config["uid"]] = piece
            self.pieces[config["uid"]] = piece
        
        return pieces
    
    def is_valid_move(self, piece: PieceInfo, from_pos: str, to_pos: str) -> bool:
        """Check if a checkers move is valid"""
        if not piece.position or piece.position != from_pos:
            return False
        
        from_row, from_col = self.board_config.position_mapping[from_pos]
        to_row, to_col = self.board_config.position_mapping[to_pos]
        
        # Diagonal moves only
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        
        # Check direction (simplified)
        direction = -1 if piece.color == "Red" else 1
        if piece.piece_type == "piece" and (to_row - from_row) * direction <= 0:
            return False  # Regular pieces can only move forward
        
        # Check if destination is empty
        target_piece = self.board_state.get(to_pos)
        return target_piece is None or target_piece.color != piece.color
    
    def get_possible_moves(self, piece: PieceInfo) -> List[str]:
        """Get all possible moves for a checkers piece"""
        if not piece.position:
            return []
        
        possible_moves = []
        for position in self.board_config.position_mapping.keys():
            if self.is_valid_move(piece, piece.position, position):
                possible_moves.append(position)
        
        return possible_moves


