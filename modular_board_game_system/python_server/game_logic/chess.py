from typing import Dict, List, Optional
from config import PieceInfo
from game_logic.base import GameLogic

class ChessLogic(GameLogic):
    """Chess game logic implementation"""
    
    def get_game_name(self) -> str:
        return "Chess"
    
    def initialize_pieces(self) -> Dict[str, PieceInfo]:
        """Initialize chess pieces with known UIDs"""
        # This would be loaded from configuration in a real system
        piece_configs = [
            {"uid": "C5B7BD01", "type": "rook", "color": "White"},
            {"uid": "F3C7B501", "type": "king", "color": "White"},
            {"uid": "9B850802", "type": "knight", "color": "White"},
            {"uid": "7A74B701", "type": "pawn", "color": "White"},
            {"uid": "AB980802", "type": "rook", "color": "Black"},
            {"uid": "5BCA0E02", "type": "king", "color": "Black"},
            {"uid": "1BFD0802", "type": "knight", "color": "Black"},
            {"uid": "CE890E02", "type": "pawn", "color": "Black"},
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
        """Check if a chess move is valid"""
        if not piece.position or piece.position != from_pos:
            return False
        
        from_row, from_col = self.board_config.position_mapping[from_pos]
        to_row, to_col = self.board_config.position_mapping[to_pos]
        
        # Basic bounds check
        if not (0 <= to_row < self.board_config.size[0] and 0 <= to_col < self.board_config.size[1]):
            return False
        
        # Check if destination has friendly piece
        target_piece = self.board_state.get(to_pos)
        if target_piece and target_piece.color == piece.color:
            return False
        
        # Piece-specific movement rules
        if piece.piece_type == "pawn":
            return self._is_valid_pawn_move(piece, from_row, from_col, to_row, to_col, target_piece)
        elif piece.piece_type == "rook":
            return self._is_valid_rook_move(from_row, from_col, to_row, to_col)
        elif piece.piece_type == "knight":
            return self._is_valid_knight_move(from_row, from_col, to_row, to_col)
        elif piece.piece_type == "king":
            return self._is_valid_king_move(from_row, from_col, to_row, to_col)
        
        return False
    
    def _is_valid_pawn_move(self, piece: PieceInfo, from_row: int, from_col: int, 
                           to_row: int, to_col: int, target_piece: Optional[PieceInfo]) -> bool:
        """Validate pawn movement"""
        direction = -1 if piece.color == "White" else 1
        
        # Forward move
        if from_col == to_col and to_row == from_row + direction:
            return target_piece is None
        
        # Diagonal capture
        if abs(from_col - to_col) == 1 and to_row == from_row + direction:
            return target_piece is not None and target_piece.color != piece.color
        
        return False
    
    def _is_valid_rook_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate rook movement (simplified - no path checking)"""
        # Horizontal or vertical movement only
        if from_row == to_row or from_col == to_col:
            # In a real implementation, we'd check for pieces blocking the path
            return abs(from_row - to_row) + abs(from_col - to_col) <= 2  # Limited range for 4x4
        return False
    
    def _is_valid_knight_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate knight movement (simplified for 4x4)"""
        # Diagonal moves only in 4x4 chess
        return abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1
    
    def _is_valid_king_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Validate king movement"""
        return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1
    
    def get_possible_moves(self, piece: PieceInfo) -> List[str]:
        """Get all possible moves for a piece"""
        if not piece.position:
            return []
        
        possible_moves = []
        for position in self.board_config.position_mapping.keys():
            if self.is_valid_move(piece, piece.position, position):
                possible_moves.append(position)
        
        return possible_moves


